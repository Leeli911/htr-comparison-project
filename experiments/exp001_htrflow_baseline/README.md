# Experiment 001: HTRFlow Baseline

## Date
2024-11-12

## Objective
建立 HTRFlow 性能基准线

## Dataset
- 24 张 18 世纪瑞典手写文档
- 来源：Gender and Work 项目

## Method
- 工具：HTRFlow 在线版
- 模型：Swedish - Spreads
- 处理：原始图片（3456x4608）

## Results

### 性能指标
```
平均 CER: 21.25%
平均 WER: 46.05%
成功处理: 24/24 (100%)

表现优秀 (CER < 10%): 6 个文档 (25%)
表现良好 (CER 10-20%): 8 个文档 (33%)
需要改进 (CER > 25%): 9 个文档 (38%)

最佳: DSC_0129 (CER: 4.84%)
最差: DSC_0131 (CER: 75.89%)
```

### 观察
1. HTRFlow 能够识别 18 世纪瑞典手写文档
2. 约 50% 文档识别质量很好
3. 约 38% 文档需要改进
4. 部分图片可能质量差或布局复杂

### 常见错误类型
- 古代字母形式识别错误
- 连笔字分割困难
- 褪色文字识别不准

## Conclusions
1. ✅ HTRFlow 可以作为性能基准
2. ✅ 证明这类文档可以被识别
3. ⚠️ 有改进空间，尤其是困难文档
4. 🎯 RTMDet + Loghi 目标：CER < 15%

## Next Steps
1. 测试 RTMDet 布局分析
2. 集成 RTMDet + Loghi 管道
3. 与 HTRFlow 对比性能
4. 考虑迁移学习改进困难文档
