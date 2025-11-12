import xml.etree.ElementTree as ET
from pathlib import Path
import argparse
from PIL import Image

def detect_ns(root):
    if root.tag.startswith("{"):
        return {"ns": root.tag.split("}")[0].strip("{")}
    return {"ns": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15"}

def bbox_from_points(points_str, img_w, img_h, margin=20):
    coords = [list(map(int, p.split(','))) for p in points_str.split() if ',' in p]
    if not coords:
        return None
    xs = [c[0] for c in coords]; ys = [c[1] for c in coords]
    x_min = max(0, min(xs) - margin); y_min = max(0, min(ys) - margin)
    x_max = min(img_w, max(xs) + margin); y_max = min(img_h, max(ys) + margin)
    return (x_min, y_min, x_max, y_max)

def extract_lines(xml_file: Path, image_dir: Path, out_dir: Path):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = detect_ns(root)

    image_name = xml_file.stem + ".JPG"
    img_path = image_dir / image_name
    if not img_path.exists():
        image_name = xml_file.stem + ".jpg"
        img_path = image_dir / image_name
    if not img_path.exists():
        image_name = xml_file.stem + ".png"
        img_path = image_dir / image_name
    if not img_path.exists():
        image_name = xml_file.stem + ".tif"
        img_path = image_dir / image_name

    img = Image.open(img_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for text_line in root.findall('.//ns:TextLine', ns):
        line_id = text_line.get('id', f'line_{count}')

        baseline = text_line.find('.//ns:Baseline', ns)
        bbox = None
        if baseline is not None and baseline.get('points'):
            bbox = bbox_from_points(baseline.get('points'), img.width, img.height, margin=20)

        if bbox is None:
            coords = text_line.find('.//ns:Coords', ns)
            if coords is not None and coords.get('points'):
                bbox = bbox_from_points(coords.get('points'), img.width, img.height, margin=5)

        if bbox is None:
            continue

        crop = img.crop(bbox)
        crop.save(out_dir / f"{xml_file.stem}_{line_id}.png")
        count += 1

    print(f"✅ {xml_file.name}: 裁切 {count} 行")
    return count

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-x","--xml_dir", required=True)
    parser.add_argument("-i","--image_dir", required=True)
    parser.add_argument("-o","--output", required=True)
    a = parser.parse_args()

    xml_dir = Path(a.xml_dir)
    image_dir = Path(a.image_dir)
    out_dir = Path(a.output)

    for xml_file in xml_dir.glob("*.xml"):
        extract_lines(xml_file, image_dir, out_dir)

if __name__ == "__main__":
    main()
