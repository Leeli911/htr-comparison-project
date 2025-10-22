#!/bin/bash

echo "🔍 对比不同 beam 值的识别文本差异"
echo ""

for beam in 1 2 4 8; do
    echo "============================================"
    echo "num_beams = $beam"
    echo "============================================"
    
    # 提取前5行文本
    python << PYTHON
import json

with open('outputs/htrflow/beam${beam}/samples/test.json', 'r') as f:
    data = json.load(f)

print("前5行识别结果:")
for i in range(min(5, len(data['contains']))):
    line = data['contains'][i]
    text = line['text_result']['texts'][0]
    score = line['text_result']['scores'][0]
    print(f"Line {i}: [{score:.4f}] {text[:60]}...")

print()
PYTHON
done
