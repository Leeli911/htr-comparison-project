#!/bin/bash
# Loghi Inference Pipeline - Native (No Docker)
# Modified for HPC environment without Docker

set -e
set -o pipefail

# ========================================
# Configuration
# ========================================

# GPU device (0 for first GPU, -1 for CPU)
GPU=0

# Paths
LAYPA_DIR="/mimer/NOBACKUP/groups/naiss2025-22-39/lili_project/loghi/laypa"
LOGHI_HTR_DIR="/mimer/NOBACKUP/groups/naiss2025-22-39/lili_project/loghi/loghi-htr"
LOGHI_TOOLING_DIR="/mimer/NOBACKUP/groups/naiss2025-22-39/lili_project/loghi/loghi-tooling"

# Models
LAYPA_BASELINE_CONFIG="/mimer/NOBACKUP/groups/naiss2025-22-39/lili_project/loghi_models/laypa/general/baseline/config.yaml"
LAYPA_BASELINE_WEIGHTS="/mimer/NOBACKUP/groups/naiss2025-22-39/lili_project/loghi_models/laypa/general/baseline/model_best_mIoU.pth"
LOGHI_HTR_MODEL="/mimer/NOBACKUP/groups/naiss2025-22-39/lili_project/loghi_models/loghi-htr/generic-2023-02-15"

# Input/Output
if [ -z "$1" ]; then
    echo "Usage: $0 <input_directory>"
    exit 1
fi

IMAGES_PATH="$(readlink -f "$1")"
echo "Processing images in: $IMAGES_PATH"

# Create output directories
mkdir -p "$IMAGES_PATH/page"
mkdir -p "$IMAGES_PATH/lines"

# Temporary directory
TMPDIR="$IMAGES_PATH/tmp"
mkdir -p "$TMPDIR"
export IMAGES_PATH
export TMPDIR

# ========================================
# Step 1: Layout Analysis with Laypa
# ========================================
echo ""
echo "========================================="
echo "Step 1: Layout Analysis (Laypa)"
echo "========================================="

cd "$LAYPA_DIR"

# Set CUDA device
if [ "$GPU" -ge 0 ]; then
    export CUDA_VISIBLE_DEVICES=$GPU
    echo "Using GPU: $GPU"
else
    export CUDA_VISIBLE_DEVICES=""
    echo "Using CPU"
fi

python3 run.py \
    -c "$LAYPA_BASELINE_CONFIG" \
    -i "$IMAGES_PATH" \
    -o "$IMAGES_PATH" \
    --opts MODEL.WEIGHTS "$LAYPA_BASELINE_WEIGHTS"

echo "✅ Layout analysis completed"

# ========================================
# Step 2: Extract Line Images
# ========================================
echo ""
echo "========================================="
echo "Step 2: Extracting Text Lines"
echo "========================================="

# Check if loghi-tooling Java tools are available
MINION_EXTRACT="$LOGHI_TOOLING_DIR/minions/target/appassembler/bin/MinionExtractBaselines"

if [ -f "$MINION_EXTRACT" ]; then
    # Use Java-based extraction
    "$MINION_EXTRACT" \
        -input_path_image "$IMAGES_PATH" \
        -input_path_png "$IMAGES_PATH/page" \
        -output_path_page "$IMAGES_PATH/page"
    
    # Cut line images
    MINION_CUT="$LOGHI_TOOLING_DIR/minions/target/appassembler/bin/MinionCutFromImageBasedOnPageXMLNew"
    "$MINION_CUT" \
        -input_path "$IMAGES_PATH" \
        -outputbase "$IMAGES_PATH/lines" \
        -tmpdir "$TMPDIR"
else
    echo "Java tools not found, using Python fallback"
    # Create a simple Python script to extract lines
    python3 << 'PYTHON'
import os
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image

images_path = Path(os.environ['IMAGES_PATH'])
page_dir = images_path / 'page'
lines_dir = images_path / 'lines'
lines_dir.mkdir(exist_ok=True)

# 兼容常见 PAGE 命名空间
NS_CANDIDATES = [
    'http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15',
    'http://schema.primaresearch.org/PAGE/gts/pagecontent/2010-03-19',
    'http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15',
    'http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15',
]

def find_with_any_ns(elem, path):
    for ns in NS_CANDIDATES:
        res = elem.findall(path.format(ns=ns))
        if res:
            return res, ns
    return [], None

def first_with_any_ns(elem, path):
    for ns in NS_CANDIDATES:
        res = elem.find(path.format(ns=ns))
        if res is not None:
            return res, ns
    return None, None

def bbox_from_points(points, img_w, img_h, margin=20):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x_min = max(0, min(xs) - margin)
    y_min = max(0, min(ys) - margin)
    x_max = min(img_w, max(xs) + margin)
    y_max = min(img_h, max(ys) + margin)
    if x_max <= x_min or y_max <= y_min:
        return None
    return (x_min, y_min, x_max, y_max)

total_saved = 0

for xml_file in sorted(page_dir.glob('*.xml')):
    img_name_candidates = [xml_file.stem + ext for ext in ('.JPG', '.jpg', '.PNG', '.png', '.TIF', '.tif')]
    img_path = None
    for name in img_name_candidates:
        p = images_path / name
        if p.exists():
            img_path = p
            break
    if not img_path:
        print(f"  Warning: No image found for {xml_file.name}")
        continue

    img = Image.open(img_path)
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 找 TextLine（任何命名空间）
    lines, used_ns = find_with_any_ns(root, './/{{{ns}}}TextLine')
    if not lines:
        # 有些 XML 只有 TextRegion；这里可扩展：从 TextRegion 的 Coords 粗切
        regions, used_ns = find_with_any_ns(root, './/{{{ns}}}TextRegion')
        if not regions:
            print(f"  Warning: No TextLine or TextRegion in {xml_file.name}")
            continue
        # 粗切 TextRegion
        for idx, reg in enumerate(regions):
            coords_el = reg.find('.//{{{ns}}}Coords'.format(ns=used_ns))
            if coords_el is None:
                continue
            points_attr = coords_el.get('points', '')
            if not points_attr:
                continue
            pts = []
            for p in points_attr.split():
                try:
                    x, y = map(int, p.split(','))
                    pts.append((x, y))
                except:
                    pass
            if len(pts) < 3:
                continue
            box = bbox_from_points(pts, img.width, img.height, margin=10)
            if box:
                out = lines_dir / f"{xml_file.stem}_region_{idx:03d}.png"
                img.crop(box).save(out)
                total_saved += 1
        print(f"  Extracted {total_saved} rough region crops for {xml_file.name}")
        continue

    # 优先按 Baseline；若没有 Baseline，就退化为 TextLine.Coords
    saved_this_xml = 0
    for idx, line in enumerate(lines):
        line_id = line.get('id', f'line_{idx}')

        # Baseline
        baseline_el = line.find('.//{{{ns}}}Baseline'.format(ns=used_ns))
        if baseline_el is not None and baseline_el.get('points'):
            pts = []
            for p in baseline_el.get('points').split():
                try:
                    x, y = map(int, p.split(','))
                    pts.append((x, y))
                except:
                    pass
            if len(pts) >= 2:
                box = bbox_from_points(pts, img.width, img.height, margin=20)
                if box:
                    out = lines_dir / f"{xml_file.stem}_{line_id}.png"
                    img.crop(box).save(out)
                    saved_this_xml += 1
                    continue  # 这一行已成功

        # Fallback: Coords
        coords_el = line.find('.//{{{ns}}}Coords'.format(ns=used_ns))
        if coords_el is not None and coords_el.get('points'):
            pts = []
            for p in coords_el.get('points').split():
                try:
                    x, y = map(int, p.split(','))
                    pts.append((x, y))
                except:
                    pass
            if len(pts) >= 3:
                box = bbox_from_points(pts, img.width, img.height, margin=5)
                if box:
                    out = lines_dir / f"{xml_file.stem}_{line_id}.png"
                    img.crop(box).save(out)
                    saved_this_xml += 1

    total_saved += saved_this_xml
    print(f"  Extracted {saved_this_xml} line crops for {xml_file.name}")

print(f"✅ Line extraction completed. Total crops: {total_saved}")
PYTHON

fi

echo "✅ Line extraction completed"

# ========================================
# Step 3: HTR Recognition
# ========================================
echo ""
echo "========================================="
echo "Step 3: Text Recognition (Loghi-HTR)"
echo "========================================="

cd "$LOGHI_HTR_DIR"

# Create results file list
find "$IMAGES_PATH/lines" -name "*.png" > "$TMPDIR/line_images.txt"

if [ ! -s "$TMPDIR/line_images.txt" ]; then
    echo "❌ No line images found!"
    exit 1
fi

echo "Found $(wc -l < "$TMPDIR/line_images.txt") line images"

# Run HTR
python3 src/main.py \
    --model "$LOGHI_HTR_MODEL" \
    --batch_size 256 \
    --image_list "$TMPDIR/line_images.txt" \
    --results_file "$TMPDIR/results.txt" \
    --beam_width 1 \
    --use_mask false

if [ ! -f "$TMPDIR/results.txt" ]; then
    echo "❌ HTR failed to produce results"
    exit 1
fi

echo "✅ HTR recognition completed"

# ========================================
# Step 4: Merge Results into PageXML
# ========================================
echo ""
echo "========================================="
echo "Step 4: Merging Results into PageXML"
echo "========================================="

# Simple Python script to merge results
python3 << 'PYTHON'
import sys
import os
from pathlib import Path
import xml.etree.ElementTree as ET

images_path = Path(os.environ['IMAGES_PATH'])
tmpdir = Path(os.environ['TMPDIR'])
results_file = tmpdir / 'results.txt'
page_dir = images_path / 'page'

# Read HTR results
results = {}
with open(results_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) >= 2:
            img_path = parts[0]
            text = parts[1]
            # Extract line ID from filename
            filename = Path(img_path).stem
            results[filename] = text

print(f"Loaded {len(results)} HTR results")

# Update PageXML files
ns = {'ns': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15'}
ET.register_namespace('', ns['ns'])

for xml_file in page_dir.glob('*.xml'):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    modified = False
    for text_line in root.findall('.//ns:TextLine', ns):
        line_id = text_line.get('id', '')
        # Construct expected result key
        key = f"{xml_file.stem}_{line_id}"
        
        if key in results:
            # Find or create TextEquiv
            text_equiv = text_line.find('ns:TextEquiv', ns)
            if text_equiv is None:
                text_equiv = ET.SubElement(text_line, '{' + ns['ns'] + '}TextEquiv')
            
            # Find or create Unicode
            unicode_elem = text_equiv.find('ns:Unicode', ns)
            if unicode_elem is None:
                unicode_elem = ET.SubElement(text_equiv, '{' + ns['ns'] + '}Unicode')
            
            unicode_elem.text = results[key]
            modified = True
    
    if modified:
        tree.write(xml_file, encoding='utf-8', xml_declaration=True)
        print(f"✅ Updated {xml_file.name}")

print("✅ PageXML merging completed")
PYTHON

echo ""
echo "========================================="
echo "Pipeline Completed Successfully!"
echo "========================================="
echo "Output directory: $IMAGES_PATH/page"
echo "Results preview:"
ls -lh "$IMAGES_PATH/page"/*.xml | head -5

