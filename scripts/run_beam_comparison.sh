#!/bin/bash

echo "🔬 开始 Beam Search 参数对比实验"
echo ""

for beams in 1 2 4 8; do
    echo "▶ 测试 num_beams = $beams"
    
    # 记录开始时间
    start_time=$(date +%s)
    
    # 运行识别
    htrflow pipeline configs/htrflow/pipeline_beam${beams}.yaml data/samples/test.jpg
    
    # 记录结束时间
    end_time=$(date +%s)
    elapsed=$((end_time - start_time))
    
    echo "  ✓ 完成，用时: ${elapsed}秒"
    echo ""
done

echo "🎉 实验完成！"
echo ""
echo "查看结果："
echo "  ls -lh outputs/htrflow/beam*/"
