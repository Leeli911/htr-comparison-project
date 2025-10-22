#!/bin/bash

echo "🔬 开始 Beam Search 参数对比实验"
echo "预计总时间: 50-60 分钟"
echo ""

# 创建输出目录
mkdir -p logs

for beams in 1 2 4 8; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "▶️  测试 num_beams = $beams"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    start_time=$(date +%s)
    
    # 运行识别
    htrflow pipeline \
        configs/htrflow/pipeline_beam${beams}.yaml \
        data/samples/test.jpg \
        2>&1 | tee logs/beam${beams}.log
    
    end_time=$(date +%s)
    elapsed=$((end_time - start_time))
    
    echo ""
    echo "✅ num_beams=$beams 完成，用时: ${elapsed}秒"
    echo ""
    
    # 分析结果
    if [ -f "outputs/htrflow/beam${beams}/samples/test.json" ]; then
        echo "📊 分析结果:"
        python scripts/analyze_json.py outputs/htrflow/beam${beams}/samples/test.json
    fi
    
    echo ""
done

echo "🎉 所有实验完成！"
echo ""
echo "查看结果:"
echo "  ls -lh outputs/htrflow/beam*/"
