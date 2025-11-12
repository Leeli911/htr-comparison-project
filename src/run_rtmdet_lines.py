#!/usr/bin/env python3
import argparse
from pathlib import Path
import cv2
import torch
from mmdet.apis import init_detector, inference_detector
from torchvision.ops import nms

def load_model():
    config = "rtmdet_lines/config.py"
    checkpoint = "rtmdet_lines/model.pth"
    model = init_detector(config, checkpoint, device="cuda")
    return model

def detect_lines(model, img_path, conf_thresh=0.4, iou_thresh=0.5):
    result = inference_detector(model, img_path)

    # result 是 list: [bboxes Nx5]
    bboxes = result[0]
    if bboxes is None or len(bboxes) == 0:
        return []

    # 拆分 box 和 score
    boxes = bboxes[:, :4]
    scores = bboxes[:, 4]

    keep = scores > conf_thresh
    boxes = boxes[keep]
    scores = scores[keep]

    if len(boxes) == 0:
        return []

    keep_idx = nms(boxes, scores, iou_thresh)
    return boxes[keep_idx].cpu().numpy()

def crop_lines(image_path, boxes, out_dir):
    img = cv2.imread(str(image_path))
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, (x1,y1,x2,y2) in enumerate(boxes):
        crop = img[int(y1):int(y2), int(x1):int(x2)]
        cv2.imwrite(str(out_dir / f"{image_path.stem}_line_{i:03d}.png"), crop)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    args = parser.parse_args()

    image = Path(args.input)
    model = load_model()
    boxes = detect_lines(model, image)
    crop_lines(image, boxes, image.parent / "rtmdet_lines")

    print(f"✅ {image.name}: 裁切 {len(boxes)} 行 → {image.parent/'rtmdet_lines'}")

if __name__ == "__main__":
    main()
