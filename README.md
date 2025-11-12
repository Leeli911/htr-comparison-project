# HTR Comparison Project

Comparing Handwritten Text Recognition systems on 18th-century Swedish manuscripts.

## 🎯 Project Goal

Compare the performance of different HTR systems (HTRFlow, Loghi, PyLaia) on historical Swedish documents from the Gender and Work project.

# HTRFlow vs Loghi 性能对比研究

**研究者**: Li Li  
**导师**: Anders Hast  
**机构**: Uppsala University  
**创建日期**: 2025-10-19

---

## 📊 Current Status

### ✅ Completed
- [x] Alvis environment setup
- [x] Loghi + Laypa installation
- [x] 24 test images with ground truth prepared
- [x] Image preprocessing (bicubic upscaling)
- [x] HTRFlow baseline evaluation

### 🔄 In Progress
- [ ] RTMDet layout analysis integration
- [ ] Loghi complete pipeline testing
- [ ] Performance comparison

### ⏳ Planned
- [ ] Transfer learning experiments
- [ ] Final comparative analysis
- [ ] Project report

## 📈 Latest Results

### HTRFlow Baseline (Exp 001)
- **Average CER**: 21.25%
- **Average WER**: 46.05%
- **Success Rate**: 24/24 (100%)
- **Date**: 2024-11-12

Performance breakdown:
- Excellent (CER < 10%): 25%
- Good (CER 10-20%): 33%
- Needs improvement (CER > 25%): 38%

See [reports/htrflow_baseline_summary.md](reports/htrflow_baseline_summary.md) for details.

## 🗂️ Project Structure
```
htr-comparison-project/
├── src/                  # Source code
├── scripts/              # Pipeline scripts
├── data/                 # Input data (not in Git)
├── results/              # Output results
├── experiments/          # Experiment logs
├── reports/              # Analysis reports
└── docs/                 # Documentation
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for complete structure.

## 🚀 Quick Start

### Prerequisites
- Python 3.11
- Alvis cluster access
- Virtual environment: `/mimer/NOBACKUP/groups/naiss2025-22-39/lili_venv`

### Run Evaluation
```bash
# Activate environment
source /mimer/NOBACKUP/groups/naiss2025-22-39/lili_venv/bin/activate

# Evaluate HTR results
python3 src/evaluation/evaluate_htr_simple.py
```

### Run Loghi Pipeline
```bash
# Process images
bash scripts/run_loghi_simple.sh <input_directory>
```

## 📚 Documentation

- [Environment Setup](docs/ENVIRONMENT.md)
- [Known Issues](docs/ISSUES.md)
- [Project Structure](PROJECT_STRUCTURE.md)

---

## 🔗 相关链接

- HTRFlow: https://github.com/AI-Riksarkivet/htrflow
- Loghi: https://github.com/knaw-huc/loghi
- Swedish Lion Libre: https://huggingface.co/datasets/Riksarkivet/swedish-lion-libre
- Gender and Work: https://www.uu.se/en/research/gender-and-work

