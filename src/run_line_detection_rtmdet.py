#!/usr/bin/env python3

import cv2
import torch
import numpy as np
from pathlib import Path
from PIL import Image
from torchvision.ops import nms

MODEL_DIR = Path("rtmdet_lines")  # 确保这里有 torchscript/model.ts

def load_model():
    model = torch.jit.load(str(MODEL_DIR / "torchscript" / "model.ts"),
                           map_location="cuda" if torch.cuda.is_available() else "cpu")
    model.eval()
    return model

def preprocess(image):
    img = np.asarray(image)[:, :, ::-1]
    img_resized = cv2.resize(img, (1024, 1024), interpolation=cv2.INTER_LINEAR)
    tensor = torch.from_numpy(img_resized).permute(2, 0, 1).float().unsqueeze(0)
    tensor = tensor / 255.0
    if torch.cuda.is_available():
        tensor = tensor.cuda()
    return img, tensor

def detect(model, tensor, conf=0.35, iou=0.5):
    with torch.no_grad():
        outputs = model(tensor)[0]
    boxes = outputs["boxes"]
    scores = outputs["scores"]

    keep = scores > conf
    boxes = boxes[keep]
    scores = scores[keep]

    if len(boxes) == 0:
        return []

    idx = nms(boxes, scores, iou)
    return boxes[idx].cpu().numpy()

def crop(img, boxes, outdir, name):
    outdir.mkdir(parents=True, exist_ok=True)
    h, w, _ = img.shape
    for i, (x1,y1,x2,y2) in enumerate(boxes):
        x1,y1 = max(0,int(x1)),max(0,int(y1))
        x2,y2 = min(w,int(x2)),min(h,int(y2))
        crop = img[y1:y2, x1:x2]
        if crop.size > 0:
            cv2.imwrite(str(outdir / f"{name}_line_{i:03d}.png"), crop)

def process_dir(img_dir, out_dir):
    model = load_model()
    files = sorted(list(Path(img_dir).glob("*.jpg")) +
                   list(Path(img_dir).glob("*.JPG")) +
                   list(Path(img_dir).glob("*.png")))

    for img_path in files:
        image = Image.open(img_path).convert("RGB")
        orig, tensor = preprocess(image)
        boxes = detect(model, tensor)

        crop(orig, boxes, Path(out_dir), img_path.stem)
        print(f"✅ {img_path.name}: {len(boxes)} 行")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("-i","--input", required=True)
    p.add_argument("-o","--output", required=True)
    a = p.parse_args()
    process_dir(a.input, a.output)
