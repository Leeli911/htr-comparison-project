#!/usr/bin/env python3
"""
分析 HTRFlow JSON 输出的脚本
"""

import json
import sys
from pathlib import Path

def analyze_json(json_path):
    """分析 HTRFlow JSON 输出"""
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=" * 60)
    print(f"📄 文件分析: {data['file_name']}")
    print("=" * 60)
    
    # 基本信息
    print(f"\n📐 图片尺寸: {data['width']} x {data['height']}")
    print(f"📝 检测行数: {len(data['contains'])}")
    
    # 置信度统计
    scores = [line['text_result']['scores'][0] for line in data['contains']]
    avg_score = sum(scores) / len(scores)
    
    print(f"\n🎯 置信度统计:")
    print(f"   平均: {avg_score:.4f}")
    print(f"   最高: {max(scores):.4f}")
    print(f"   最低: {min(scores):.4f}")
    
    # 低置信度文本行
    print(f"\n⚠️  低置信度行 (<0.90):")
    for i, line in enumerate(data['contains']):
        score = line['text_result']['scores'][0]
        if score < 0.90:
            text = line['text_result']['texts'][0][:50]  # 前50字符
            print(f"   Line {i}: {score:.4f} - {text}...")
    
    # 处理步骤
    print(f"\n🔧 处理步骤:")
    for step in data['processing_steps']:
        print(f"   {step['description']}: {step['settings']['model_class']}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python analyze_json.py <json文件路径>")
        print("示例: python analyze_json.py outputs/htrflow/samples/test.json")
        sys.exit(1)
    
    analyze_json(sys.argv[1])
