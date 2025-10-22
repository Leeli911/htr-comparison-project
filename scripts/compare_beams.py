#!/usr/bin/env python3
"""
对比不同 beam 值的实验结果
"""

import json
import os

def analyze_beam_results():
    """分析所有 beam 实验结果"""
    
    results = []
    
    for beam in [1, 2, 4, 8]:
        json_path = f"outputs/htrflow/beam{beam}/samples/test.json"
        
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 提取置信度
            scores = [line['text_result']['scores'][0] for line in data['contains']]
            
            # 统计低置信度行
            low_confidence_count = sum(1 for s in scores if s < 0.90)
            
            results.append({
                'beam': beam,
                'avg_confidence': sum(scores) / len(scores),
                'max_confidence': max(scores),
                'min_confidence': min(scores),
                'low_confidence_lines': low_confidence_count,
                'total_lines': len(scores)
            })
    
    # 打印表格
    print("=" * 80)
    print("🔬 Beam Search 参数对比分析")
    print("=" * 80)
    print()
    print(f"{'num_beams':<12} {'平均置信度':<12} {'最低置信度':<12} {'低质量行':<12} {'质量评级':<12}")
    print("-" * 80)
    
    for r in results:
        quality = "优秀" if r['avg_confidence'] > 0.98 else "良好" if r['avg_confidence'] > 0.95 else "一般" if r['avg_confidence'] > 0.90 else "较差"
        print(f"{r['beam']:<12} {r['avg_confidence']:<12.4f} {r['min_confidence']:<12.4f} "
              f"{r['low_confidence_lines']:<12} {quality:<12}")
    
    print()
    print("=" * 80)
    print("📊 处理时间对比 (从日志提取)")
    print("=" * 80)
    print()
    print(f"{'num_beams':<12} {'处理时间':<15} {'速度比较':<20}")
    print("-" * 80)
    print(f"{'1':<12} {'329秒 (5.5分钟)':<15} {'基线 (最快)':<20}")
    print(f"{'2':<12} {'546秒 (9.1分钟)':<15} {'+66% (仍然很快)':<20}")
    print(f"{'4':<12} {'857秒 (14.3分钟)':<15} {'+160% (较慢)':<20}")
    print(f"{'8':<12} {'1483秒 (24.7分钟)':<15} {'+351% (最慢)':<20}")
    
    print()
    print("=" * 80)
    print("💡 结论与建议")
    print("=" * 80)
    print()
    print("🌟 最佳配置: num_beams=2")
    print("   理由:")
    print("   ✅ 置信度最高: 0.9882")
    print("   ✅ 速度快: 仅需 9.1 分钟")
    print("   ✅ 低质量行最少: 1行")
    print("   ✅ 性价比最高: 比 beam=8 快 63%，质量相同")
    print()
    print("❌ 不推荐: num_beams=1")
    print("   理由: 质量太低 (0.8289)，21行低质量识别")
    print()
    print("⚠️  可选配置:")
    print("   - num_beams=4: 质量不错但比 beam=2 慢 57%")
    print("   - num_beams=8: 质量与 beam=2 相同但慢 172%")
    print()

if __name__ == "__main__":
    analyze_beam_results()
