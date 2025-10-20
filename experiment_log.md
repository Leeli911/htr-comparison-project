# HTRFlow 实验日志

**项目**: HTRFlow vs Loghi 性能对比研究  
**研究者**: Li Li  
**开始日期**: 2025-10-19

---

## 实验 #000 - 项目立项

**日期**: 2025-10-19  
**目标**: 建立完整的项目环境和文档体系

### 环境配置

**系统信息**:
- macOS (Apple Silicon/Intel)
- Python 3.11.11
- PyTorch 2.2.2

**虚拟环境**:
- 名称: htrflow_env
- 位置: ~/htrflow_env/

**已安装包**:
```
torch==2.2.2
torchvision==0.17.2
torchaudio==2.2.2
htrflow (已安装)
```

### 项目结构
```
htr-comparison-project/
├── configs/htrflow/pipeline.yaml
├── data/{raw,samples,ground_truth}/
├── outputs/{htrflow,loghi,batch,figures}/
├── scripts/
├── docs/
├── screenshots/
├── notebooks/
├── reports/
├── README.md
├── requirements.txt
├── .gitignore
├── progress_tracker.md
└── experiment_log.md
```

### Git 仓库

- 初始化: ✅
- 首次提交: ✅
- 分支: master/main

### 结论

✅ 项目立项完成  
✅ 开发环境就绪  
✅ 准备进行第一次识别测试

### 下一步

1. 下载测试图片到 data/samples/
2. 运行 HTRFlow pipeline
3. 验证输出结果

---

[后续实验记录将在这里添加]

---

**最后更新**: 2025-10-19

## 实验 #001 - 第一次文本识别

**日期**: 2025-10-19  
**时间**: 20:12-20:29 (17分钟)  
**目标**: 验证 HTRFlow 能成功识别瑞典历史手写文档

### 实验设置
- **配置文件**: `configs/htrflow/pipeline.yaml`
- **测试图片**: `data/samples/test.jpg` (752KB)
- **图片来源**: 瑞典历史文档 (1613年)
- **处理设备**: CPU (macOS)

### Pipeline 步骤

1. **Segmentation (YOLO)**
   - 模型: `Riksarkivet/yolov9-lines-within-regions-1`
   - 模型大小: 122MB
   - 处理时间: ~3秒
   - 检测文本行: 33行

2. **TextRecognition (TrOCR)**
   - 模型: `Riksarkivet/trocr-base-handwritten-hist-swe-2`
   - 模型大小: 1.54GB
   - 处理时间: 约16分钟 (平均 30秒/行)
   - 批量大小: 1 (CPU限制)

3. **OrderLines**
   - 快速完成

4. **Export**
   - 输出格式: TXT
   - 输出位置: `outputs/htrflow/samples/test.txt`

### 实验结果

**性能数据**:
- 总处理时间: **1032秒** (约17分钟)
- 文本行数: 33行
- 平均速度: 30秒/行
- 识别文本长度: ~1800字符

**识别文本样本**:
```
Em wy Christinas medh Guds nåde, Sweriges, Göthes Wänder, Finnars
Karlers Lappgers i Norrlanden ähr Kryarnas och Eders i Lifland...
[完整内容见 outputs/htrflow/samples/test.txt]
```

**文档类型**: 1613年瑞典皇家文件（关于 Älvsborg 赎金）

### 观察与分析

**识别质量** (目测评估):
- ✅ 整体识别质量: 良好
- ✅ 瑞典语特殊字符 (å, ä, ö): 正确识别
- ✅ 17世纪拼写变体: 大部分正确
- ⚠️ 个别连写字母可能有误

**版面分析**:
- ✅ 成功检测所有33行文本
- ✅ 行序正确排列
- ✅ 无漏检

**CPU性能**:
- ⏱️ 单页处理约17分钟（CPU）
- 📝 预计 GPU 可提速 10-20倍
- ✅ 对于测试和研究足够

### 遇到的问题

#### 问题 #1: NumPy 版本冲突
- **现象**: `RuntimeError: Numpy is not available`
- **原因**: NumPy 2.2.6 与 PyTorch 2.2.2 不兼容
- **解决**: `pip install "numpy<2.0" --force-reinstall`
- **用时**: 5分钟

#### 问题 #2: 首次运行模型下载
- **现象**: 下载 1.54GB TrOCR 模型需要时间
- **用时**: ~65秒
- **备注**: 后续运行会使用缓存，无需重新下载

### 结论

✅ **HTRFlow 在 CPU 上成功运行**  
✅ **识别质量符合预期**  
✅ **适合瑞典历史文档识别**

### 下一步

- [ ] 测试 JSON 输出格式
- [ ] 对比不同 beam search 参数
- [ ] 准备更多测试图片
- [ ] 记录性能基准数据

### 截图

- 终端输出: `screenshots/20251019_first_run_terminal.png`
- 识别结果: `screenshots/20251019_first_run_output.png`

---
