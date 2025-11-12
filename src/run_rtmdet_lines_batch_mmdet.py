#!/usr/bin/env python3
from pathlib import Path
import os
import cv2
import numpy as np

# 重要：先导入 mmdet，避免其他包提前改注册表
from mmdet.apis import init_detector, inference_detector

# 绝对路径更稳
ROOT = Path("/mimer/NOBACKUP/groups/naiss2025-22-39/lili_project/htr-comparison-project")
CFG  = ROOT / "rtmdet_lines" / "config.py"
CKPT = ROOT / "rtmdet_lines" / "model.pth"
INPUT_DIR = ROOT / "data" / "raw" / "24_with_gt"
OUT_DIR   = ROOT / "results" / "rtmdet_lines"

def to_numpy_boxes(pred):
    """兼容 MMDet3.x 的返回格式"""
    # DetDataSample
    if hasattr(pred, "pred_instances"):
        b = pred.pred_instances.bboxes
        s = pred.pred_instances.scores if hasattr(pred.pred_instances, "scores") else None
        b = b.detach().cpu().numpy()
        if s is not None:
            s = s.detach().cpu().numpy()
        return b, s
    # 旧 tuple/list
    if isinstance(pred, (list, tuple)) and len(pred) > 0:
        arr = pred[0]
        if hasattr(arr, "cpu"):
            arr = arr.cpu().numpy()
        return arr, None
    # 最后兜底
    return np.zeros((0,4), dtype=np.float32), None

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("✅ Loading RTMDet:", CFG, "|", CKPT)
    model = init_detector(str(CFG), str(CKPT), device="cuda:0")

    imgs = sorted(list(INPUT_DIR.glob("*.JPG")) + list(INPUT_DIR.glob("*.jpg")) + list(INPUT_DIR.glob("*.png")))
    if not imgs:
        raise SystemExit(f"未找到图片: {INPUT_DIR}")

    for p in imgs:
        print(f"→ {p.name}")
        pred = inference_detector(model, str(p))
        boxes, scores = to_numpy_boxes(pred)

        img = cv2.imread(str(p))
        if img is None:
            print(f"跳过，无法读取图像: {p}")
            continue

        # 置信度阈值（若有 scores）
        if scores is not None:
            keep = scores >= 0.35
            boxes = boxes[keep]

        for i, (x1, y1, x2, y2) in enumerate(boxes.astype(int)):
            x1 = max(0, x1); y1 = max(0, y1)
            x2 = min(img.shape[1], x2); y2 = min(img.shape[0], y2)
            if x2 <= x1 or y2 <= y1:
                continue
            crop = img[y1:y2, x1:x2]
            cv2.imwrite(str(OUT_DIR / f"{p.stem}_line_{i:03d}.png"), crop)

    print("\n✅ 完成！行裁切已保存到：", OUT_DIR)

if __name__ == "__main__":
    main()
