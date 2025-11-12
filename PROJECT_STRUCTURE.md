# HTR Comparison Project - Directory Structure

## 项目目录结构
```
htr-comparison-project/
│
├── README.md                          # 项目主文档
├── PROJECT_STRUCTURE.md               # 本文件 - 目录说明
├── .gitignore                         # Git 忽略规则
├── requirements.txt                   # Python 依赖
│
├── data/                              # 📁 所有数据文件
│   ├── raw/                          # 原始数据（不修改）
│   │   ├── 24_with_gt/              # 24 张有 GT 的图片
│   │   │   ├── DSC_0127.JPG
│   │   │   └── ...
│   │   └── 28_more/                 # 额外 28 张图片
│   │       └── ...
│   │
│   ├── gt/                           # Ground Truth 文本
│   │   ├── lin127.txt
│   │   └── ...
│   │
│   ├── processed/                    # 预处理后的数据
│   │   ├── upscaled_2x/             # 2倍放大图片
│   │   └── upscaled_3x/             # 3倍放大图片（可选）
│   │
│   └── image_gt_mapping.txt          # 图片-GT 映射表
│
├── models/                            # 📦 所有模型文件（大文件，不上传 Git）
│   ├── laypa/                        # Laypa 模型（软链接）
│   ├── loghi/                        # Loghi-HTR 模型（软链接）
│   └── rtmdet_lines/                 # RTMDet 模型（待下载）
│
├── src/                               # 💻 源代码
│   ├── preprocessing/                # 预处理脚本
│   │   └── upscale_images.py        # 图像放大
│   │
│   ├── layout_analysis/              # 布局分析
│   │   ├── run_laypa.py             # Laypa 方案
│   │   └── run_rtmdet.py            # RTMDet 方案（待开发）
│   │
│   ├── htr_recognition/              # HTR 识别
│   │   ├── run_loghi.py             # Loghi 识别
│   │   └── run_htrflow.py           # HTRFlow 接口（待开发）
│   │
│   └── evaluation/                   # 评估脚本
│       ├── evaluate_htr_simple.py   # CER/WER 计算
│       └── compare_systems.py       # 系统对比（待开发）
│
├── scripts/                           # 🔧 运行脚本和管道
│   ├── run_loghi_simple.sh          # Loghi 完整管道
│   ├── inference_pipeline.sh        # 原始推理脚本
│   └── slurm/                       # SLURM 批处理脚本
│       └── batch_upscaled.sh        # 批量处理任务
│
├── results/                           # 📊 所有实验结果
│   ├── htrflow_baseline/            # HTRFlow 基准结果
│   │   ├── text/                    # 识别文本（28个文件）
│   │   ├── evaluation_results.txt   # 评估报告
│   │   └── evaluation_results.csv   # CSV 格式结果
│   │
│   ├── loghi_original/              # Loghi 原始图片结果（待生成）
│   ├── loghi_upscaled_2x/           # Loghi 放大图片结果（待生成）
│   └── comparison/                  # 对比分析（待生成）
│
├── experiments/                       # 🧪 实验记录
│   ├── exp001_htrflow_baseline/     # 实验 001
│   │   └── README.md                # 实验文档
│   ├── exp002_loghi_baseline/       # 实验 002（待进行）
│   └── exp003_rtmdet_loghi/         # 实验 003（待进行）
│
├── reports/                           # 📈 分析报告
│   ├── htrflow_baseline_summary.md  # HTRFlow 总结
│   └── progress_updates/            # 进度更新
│       ├── 2024-11-12_htrflow_complete.md
│       └── ...
│
├── docs/                              # 📚 文档
│   ├── ENVIRONMENT.md               # 环境配置说明
│   ├── ISSUES.md                    # 问题记录
│   └── SUPERVISOR_UPDATE.md         # 导师沟通记录
│
├── tests/                             # 🧪 测试文件
│   ├── single_original/             # 单图原始测试
│   ├── single_upscaled/             # 单图放大测试
│   └── batch/                       # 批量测试
│
├── logs/                              # 📋 运行日志
│   ├── slurm/                       # SLURM 任务日志
│   ├── test_simple.log              # 测试日志
│   └── ...
│
├── configs/                           # ⚙️ 配置文件
│   └── model_configs/               # 模型配置
│
└── screenshots/                       # 📸 截图和可视化
    └── ...
```

## 文件类型说明

### ✅ 需要上传到 Git 的文件
- 所有源代码（src/, scripts/）
- 配置文件（configs/）
- 文档（docs/, README.md）
- 实验记录（experiments/）
- 报告（reports/）
- 小型结果文件（evaluation_results.txt）

### ❌ 不上传到 Git 的文件（在 .gitignore 中）
- 大型数据文件（data/raw/, data/processed/）
- 模型文件（models/）
- 生成的结果（results/*/text/）
- 日志文件（logs/）
- 临时文件（tests/, __pycache__）
- 虚拟环境文件

### 📝 特殊处理
- Ground Truth 文本（data/gt/*.txt）：可以上传（小文件）
- 映射文件（data/image_gt_mapping.txt）：应该上传
- 评估结果（CSV/TXT）：应该上传
- HTRFlow 结果摘要：上传部分样本
