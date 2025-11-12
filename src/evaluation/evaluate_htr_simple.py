#!/usr/bin/env python3
"""
评估 HTR 结果与 Ground Truth 的准确率
使用纯 Python 实现，不依赖外部库
"""

import sys
from pathlib import Path

def levenshtein_distance(s1, s2):
    """计算 Levenshtein 距离（编辑距离）"""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # 插入、删除、替换的成本
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def clean_text(text: str) -> str:
    """清理文本"""
    # 移除多余空格和换行
    text = ' '.join(text.split())
    # 统一标点符号
    text = text.replace('¬', '')  # 移除连字符
    return text

def calculate_cer(gt: str, pred: str) -> float:
    """计算字符错误率"""
    distance = levenshtein_distance(gt, pred)
    cer = distance / len(gt) if len(gt) > 0 else 0
    return cer * 100

def calculate_wer(gt: str, pred: str) -> float:
    """计算单词错误率"""
    gt_words = gt.split()
    pred_words = pred.split()
    distance = levenshtein_distance(gt_words, pred_words)
    wer = distance / len(gt_words) if len(gt_words) > 0 else 0
    return wer * 100

def main():
    gt_dir = Path("data/gt")
    htrflow_dir = Path("results/htrflow_baseline/text")
    
    if not gt_dir.exists() or not htrflow_dir.exists():
        print("❌ 目录不存在")
        print(f"GT dir: {gt_dir} - exists: {gt_dir.exists()}")
        print(f"HTRFlow dir: {htrflow_dir} - exists: {htrflow_dir.exists()}")
        sys.exit(1)
    
    print("=" * 70)
    print("HTRFlow vs Ground Truth 评估结果")
    print("=" * 70)
    print()
    
    results = []
    total_cer = 0
    total_wer = 0
    count = 0
    
    # 映射关系
    mapping = {
        'DSC_0127': 'lin127',
        'DSC_0128': 'lin128',
        'DSC_0129': 'lin129',
        'DSC_0130': 'lin130',
        'DSC_0131': 'lin131',
        'DSC_0132': 'lin132',
        'DSC_0133': 'lin133',
        'DSC_0134': 'lin134',
        'DSC_0135': 'lin135',
        'DSC_0136': 'lin136',
        'DSC_0137': 'lin137',
        'DSC_0138': 'lin138',
        'DSC_0139': 'lin139',
        'DSC_0140': 'lin140',
        'DSC_0141': 'lin141',
        'DSC_0142': 'lin142',
        'DSC_0143': 'lin143',
        'DSC_0144': 'lin144',
        'DSC_0145': 'lin145',
        'DSC_0146': 'lin146',
        'DSC_0148': 'lin148',
        'DSC_0150': 'lin150',
        'DSC_0152': 'lin152',
        'DSC_0153': 'lin153',
    }
    
    for img_name, gt_name in sorted(mapping.items()):
        gt_file = gt_dir / f"{gt_name}.txt"
        htrflow_file = htrflow_dir / f"{img_name}.txt"
        
        if not gt_file.exists():
            print(f"⚠️  GT 文件不存在: {gt_file}")
            continue
        
        if not htrflow_file.exists():
            print(f"⚠️  HTRFlow 文件不存在: {htrflow_file}")
            continue
        
        # 读取文本
        try:
            with open(gt_file, 'r', encoding='utf-8') as f:
                gt_text = clean_text(f.read())
            
            with open(htrflow_file, 'r', encoding='utf-8') as f:
                htrflow_text = clean_text(f.read())
            
            # 计算错误率
            cer = calculate_cer(gt_text, htrflow_text)
            wer = calculate_wer(gt_text, htrflow_text)
            
            total_cer += cer
            total_wer += wer
            count += 1
            
            print(f"{img_name}  CER: {cer:6.2f}%  WER: {wer:6.2f}%  "
                  f"GT: {len(gt_text):4d}字符  HTR: {len(htrflow_text):4d}字符")
            
            results.append({
                'file': img_name,
                'cer': cer,
                'wer': wer
            })
        except Exception as e:
            print(f"❌ 处理 {img_name} 时出错: {e}")
            continue
    
    if count > 0:
        avg_cer = total_cer / count
        avg_wer = total_wer / count
        
        print()
        print("=" * 70)
        print(f"平均 CER (字符错误率): {avg_cer:.2f}%")
        print(f"平均 WER (单词错误率): {avg_wer:.2f}%")
        print(f"成功评估: {count}/24 个文件")
        print("=" * 70)
        
        # 性能分析
        print()
        print("性能分析:")
        if avg_cer < 10:
            print("  ✅ 优秀！字符识别准确率超过 90%")
        elif avg_cer < 20:
            print("  ✅ 良好！对于历史文档来说这是很好的结果")
        elif avg_cer < 30:
            print("  ⚠️  中等。考虑使用更专业的模型")
        else:
            print("  ❌ 需要改进。可能需要专门训练的模型")
        
        # 保存结果
        output_file = Path("results/htrflow_baseline/evaluation_results.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"HTRFlow Evaluation Results\n")
            f.write(f"=" * 50 + "\n\n")
            f.write(f"Average CER: {avg_cer:.2f}%\n")
            f.write(f"Average WER: {avg_wer:.2f}%\n")
            f.write(f"Files evaluated: {count}/24\n\n")
            f.write(f"Individual Results:\n")
            f.write(f"-" * 50 + "\n")
            for r in results:
                f.write(f"{r['file']}: CER={r['cer']:.2f}%, WER={r['wer']:.2f}%\n")
        
        print(f"\n✅ 详细结果已保存到: {output_file}")
        
        # 保存 CSV 格式
        csv_file = Path("results/htrflow_baseline/evaluation_results.csv")
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write("file,cer,wer\n")
            for r in results:
                f.write(f"{r['file']},{r['cer']:.2f},{r['wer']:.2f}\n")
        
        print(f"✅ CSV 格式已保存到: {csv_file}")
    else:
        print("❌ 没有成功评估任何文件")

if __name__ == '__main__':
    main()
