# HTRFlow vs Loghi 性能对比研究

**研究者**: Li Li  
**导师**: Anders Hast  
**机构**: Uppsala University  
**创建日期**: 2025-10-19

---

## 📊 项目状态

- ✅ Python 3.11.11 环境
- ✅ 虚拟环境 htrflow_env
- ✅ PyTorch 2.2.2 安装
- ✅ HTRFlow 安装
- ✅ 项目结构建立
- ⏸️ 等待第一次识别测试

---

## 🚀 快速开始
```bash
# 激活环境
source ~/htrflow_env/bin/activate

# 进入项目
cd ~/Documents/htr-comparison-project

# 验证安装
htrflow --help
```

---

## 📂 项目结构
```
htr-comparison-project/
├── configs/              # 配置文件
│   ├── htrflow/         # HTRFlow配置
│   └── loghi/           # Loghi配置
├── data/                 # 数据集
│   ├── raw/             # 原始图片
│   ├── samples/         # 测试样本
│   └── ground_truth/    # 标注文本
├── outputs/              # 实验结果
│   ├── htrflow/         # HTRFlow结果
│   ├── loghi/           # Loghi结果
│   ├── batch/           # 批量处理
│   └── figures/         # 图表
├── scripts/              # Python脚本
├── docs/                 # 项目文档
├── screenshots/          # 截图记录
├── notebooks/            # Jupyter分析
└── reports/              # 进度报告
```

---

## 📚 文档索引

- [项目计划](docs/project_plan.md)
- [实验日志](experiment_log.md)
- [进度追踪](progress_tracker.md)
- [会议记录](docs/meeting_notes.md)

---

## 🔗 相关链接

- HTRFlow: https://github.com/AI-Riksarkivet/htrflow
- Loghi: https://github.com/knaw-huc/loghi
- Swedish Lion Libre: https://huggingface.co/datasets/Riksarkivet/swedish-lion-libre
- Gender and Work: https://www.uu.se/en/research/gender-and-work

