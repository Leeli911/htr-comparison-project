#!/usr/bin/env python3
"""
图像放大预处理 - 使用双三次插值
"""

import argparse
from pathlib import Path
from PIL import Image
import sys

def upscale_image(input_path: Path, output_path: Path, scale: float = 2.0):
    """
    使用双三次插值放大图像
    
    Args:
        input_path: 输入图像路径
        output_path: 输出图像路径
        scale: 放大倍数
    """
    try:
        img = Image.open(input_path)
        original_size = img.size
        
        # 计算新尺寸
        new_width = int(original_size[0] * scale)
        new_height = int(original_size[1] * scale)
        new_size = (new_width, new_height)
        
        # 使用双三次插值放大
        upscaled = img.resize(new_size, Image.BICUBIC)
        
        # 保存，保持高质量
        upscaled.save(output_path, quality=95)
        
        return original_size, new_size
        
    except Exception as e:
        raise Exception(f"处理失败 {input_path.name}: {e}")

def main():
    parser = argparse.ArgumentParser(description="使用双三次插值放大图像")
    parser.add_argument('-i', '--input', required=True, help='输入目录')
    parser.add_argument('-o', '--output', required=True, help='输出目录')
    parser.add_argument('-s', '--scale', type=float, default=2.0, 
                        help='放大倍数 (默认: 2.0)')
    
    args = parser.parse_args()
    
    input_dir = Path(args.input)
    output_dir = Path(args.output)
    
    if not input_dir.exists():
        print(f"❌ 输入目录不存在: {input_dir}")
        sys.exit(1)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 查找所有图片
    image_files = list(input_dir.glob('*.JPG')) + list(input_dir.glob('*.jpg'))
    
    if not image_files:
        print(f"❌ 在 {input_dir} 没有找到图片文件")
        sys.exit(1)
    
    print(f"找到 {len(image_files)} 张图片")
    print(f"放大倍数: {args.scale}x")
    print(f"使用方法: 双三次插值 (Bicubic)")
    print()
    
    success_count = 0
    for img_path in sorted(image_files):
        try:
            output_path = output_dir / img_path.name
            original_size, new_size = upscale_image(img_path, output_path, args.scale)
            
            print(f"✅ {img_path.name:20s} {original_size[0]:4d}x{original_size[1]:4d} → {new_size[0]:4d}x{new_size[1]:4d}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ {img_path.name}: {e}")
    
    print()
    print(f"✅ 完成！成功处理 {success_count}/{len(image_files)} 张图片")
    print(f"�� 输出目录: {output_dir}")

if __name__ == '__main__':
    main()
