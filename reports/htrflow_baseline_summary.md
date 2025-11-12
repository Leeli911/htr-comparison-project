# HTRFlow Baseline Performance Summary

## Overall Performance

| Metric | Value |
|--------|-------|
| Average CER | 21.25% |
| Average WER | 46.05% |
| Success Rate | 24/24 (100%) |

## Performance Distribution

| Category | Count | Percentage |
|----------|-------|------------|
| Excellent (CER < 10%) | 6 | 25% |
| Good (CER 10-20%) | 8 | 33% |
| Moderate (CER 20-30%) | 7 | 29% |
| Poor (CER > 30%) | 3 | 13% |

## Top 5 Best Results

1. DSC_0129: CER 4.84%, WER 21.05%
2. DSC_0146: CER 7.24%, WER 28.42%
3. DSC_0148: CER 7.53%, WER 30.73%
4. DSC_0150: CER 8.73%, WER 37.23%
5. DSC_0136: CER 8.75%, WER 32.09%

## Top 5 Worst Results

1. DSC_0131: CER 75.89%, WER 97.37%
2. DSC_0137: CER 58.75%, WER 77.51%
3. DSC_0142: CER 49.20%, WER 66.10%
4. DSC_0138: CER 37.38%, WER 60.90%
5. DSC_0128: CER 28.79%, WER 52.78%

## Recommendations

1. **For RTMDet + Loghi**: Target average CER < 15%
2. **Focus on improving**: 9 documents with CER > 25%
3. **Consider**: Image preprocessing for poor quality documents
4. **Future work**: Transfer learning with HTRFlow results
