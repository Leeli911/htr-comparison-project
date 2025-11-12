#!/bin/bash
# Loghi Inference Pipeline - Fixed for correct venv

set -e
set -o pipefail

# ========================================
# 加载项目配置
# ========================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config/env.sh"

# ========================================
# Configuration
# ========================================

# GPU device (0 for first GPU, -1 for CPU)
GPU=0

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
    -c "$LAYPA_MODEL_DIR/config.yaml" \
    -i "$IMAGES_PATH" \
    -o "$IMAGES_PATH/page" \
    --opts MODEL.WEIGHTS "$LAYPA_MODEL_DIR/model_best_mIoU.pth"

echo "✅ Layout analysis completed"

# ========================================
# Step 2: Extract Line Images
# ========================================
echo ""
echo "========================================="
echo "Step 2: Extracting Text Lines"
echo "========================================="

python3 << 'PYTHON'
import sys
import os
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image

images_path = Path(os.environ['IMAGES_PATH'])
page_dir = images_path / 'page'
lines_dir = images_path / 'lines'
lines_dir.mkdir(exist_ok=True)

ns = {'ns': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15'}

total_lines = 0
for xml_file in page_dir.glob('*.xml'):
    print(f"Processing {xml_file.name}")
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Find corresponding image
    img_name = xml_file.stem + '.JPG'
    img_path = images_path / img_name
    if not img_path.exists():
        img_name = xml_file.stem + '.jpg'
        img_path = images_path / img_name
    
    if not img_path.exists():
        print(f"  Warning: Image not found for {xml_file.name}")
        continue
    
    img = Image.open(img_path)
    
    # Extract text lines
    line_count = 0
    for idx, text_line in enumerate(root.findall('.//ns:TextLine', ns)):
        line_id = text_line.get('id', f'line_{idx}')
        
        # Get baseline coordinates
        baseline = text_line.find('.//ns:Baseline', ns)
        if baseline is None:
            continue
        
        points = baseline.get('points', '')
        if not points:
            continue
        
        # Parse points
        coords = [list(map(int, p.split(','))) for p in points.split()]
        if len(coords) < 2:
            continue
        
        # Simple bounding box extraction
        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]
        
        # Add margin
        margin = 20
        x_min = max(0, min(xs) - margin)
        x_max = min(img.width, max(xs) + margin)
        y_min = max(0, min(ys) - margin)
        y_max = min(img.height, max(ys) + margin)
        
        # Crop and save
        line_img = img.crop((x_min, y_min, x_max, y_max))
        output_path = lines_dir / f"{xml_file.stem}_{line_id}.png"
        line_img.save(output_path)
        line_count += 1
    
    print(f"  Extracted {line_count} lines")
    total_lines += line_count

print(f"✅ Line extraction completed: {total_lines} lines total")
PYTHON

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
    --model "$LOGHI_HTR_MODEL_DIR" \
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
            filename = Path(img_path).stem
            results[filename] = text

print(f"Loaded {len(results)} HTR results")

# Update PageXML files
ns = {'ns': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15'}
ET.register_namespace('', ns['ns'])

updated_count = 0
for xml_file in page_dir.glob('*.xml'):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    modified = False
    for text_line in root.findall('.//ns:TextLine', ns):
        line_id = text_line.get('id', '')
        key = f"{xml_file.stem}_{line_id}"
        
        if key in results:
            text_equiv = text_line.find('ns:TextEquiv', ns)
            if text_equiv is None:
                text_equiv = ET.SubElement(text_line, '{' + ns['ns'] + '}TextEquiv')
            
            unicode_elem = text_equiv.find('ns:Unicode', ns)
            if unicode_elem is None:
                unicode_elem = ET.SubElement(text_equiv, '{' + ns['ns'] + '}Unicode')
            
            unicode_elem.text = results[key]
            modified = True
    
    if modified:
        tree.write(xml_file, encoding='utf-8', xml_declaration=True)
        updated_count += 1

print(f"✅ Updated {updated_count} PageXML files")
PYTHON

echo ""
echo "========================================="
echo "Pipeline Completed Successfully!"
echo "========================================="
echo "Output directory: $IMAGES_PATH/page"
echo ""
echo "Results preview:"
ls -lh "$IMAGES_PATH/page"/*.xml 2>/dev/null | head -5

