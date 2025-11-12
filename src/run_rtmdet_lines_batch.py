from pathlib import Path
import cv2
from mmdet.apis import init_detector, inference_detector

CONFIG = "rtmdet_lines/config.py"
WEIGHTS = "rtmdet_lines/model.pth"

def main():
    input_dir = Path("data/raw/24_with_gt")
    out_dir = Path("results/rtmdet_lines")
    out_dir.mkdir(parents=True, exist_ok=True)

    print("✅ Loading RTMDet model...")
    model = init_detector(CONFIG, WEIGHTS, device="cuda:0")

    for img_path in sorted(input_dir.glob("*.JPG")):
        print(f"→ Detecting lines in {img_path.name}")
        result = inference_detector(model, str(img_path))

        # RTMDet 返回的 result[0] 为行框
        bboxes = result.pred_instances.bboxes.cpu().numpy() if hasattr(result, "pred_instances") else result[0]

        img = cv2.imread(str(img_path))
        for i, (x1, y1, x2, y2) in enumerate(bboxes):
            crop = img[int(y1):int(y2), int(x1):int(x2)]
            if crop.size > 0:
                cv2.imwrite(str(out_dir / f"{img_path.stem}_line_{i:03d}.png"), crop)

    print("\n✅ 完成！输出在 results/rtmdet_lines/")
