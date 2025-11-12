#!/usr/bin/env python3

import sys
from pathlib import Path
import argparse

LAYPA_CODE_DIR = Path("/mimer/NOBACKUP/groups/naiss2025-22-39/lili_project/loghi/laypa")
sys.path.insert(0, str(LAYPA_CODE_DIR))

def run_laypa(input_dir: Path, output_dir: Path, config_path: Path, weights_path: Path):
    from inference import main as laypa_main

    # 确保传给 Detectron2 的是绝对路径，避免相对路径解析问题
    weights_abs = str(Path(weights_path).resolve())

    class Args:
        def __init__(self):
            # 必要参数
            self.config = str(config_path)
            self.input = [str(input_dir)]
            self.output = str(output_dir)

            # ✅ 关键修正：Detectron2 实际读取 cfg.TEST.WEIGHTS
            self.opts = ["TEST.WEIGHTS", weights_abs]

            # 其余按 inference.py 需要的参数对齐
            self.whitelist = None
            self.save_confidence_heatmap = False
            self.num_workers = 2

    args = Args()

    print("\n[LAYPA] Running Layout Analysis")
    print("Input:", args.input)
    print("Output:", args.output)
    print("Config:", args.config)
    print("Weights (abs):", args.opts[1], "\n")

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    laypa_main(args)

    print("✅ Done.")

def main():
    parser = argparse.ArgumentParser(description="Run Laypa layout analysis")
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("-c", "--config", required=True)
    parser.add_argument("-w", "--weights", required=True)
    a = parser.parse_args()
    run_laypa(Path(a.input), Path(a.output), Path(a.config), Path(a.weights))

if __name__ == "__main__":
    main()
