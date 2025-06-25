import os
import subprocess
import json
import numpy as np
from PIL import Image
import torch
import torch.nn.functional as F

def calculate_psnr(img1, img2):
    """计算两幅图像的PSNR"""
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')
    return 20 * np.log10(255.0 / np.sqrt(mse))

def evaluate_model(model_path, test_dir):
    # 1. 在测试集上渲染图像
    output_dir = os.path.join(model_path, "test_renders")
    os.makedirs(output_dir, exist_ok=True)
    
    cmd = [
        "python", "render.py",
        "-m", model_path,
        "--skip_train",
        "-s", test_dir,
        "-o", output_dir
    ]
    subprocess.run(cmd)
    
    # 2. 计算指标
    test_images = sorted([f for f in os.listdir(test_dir) if f.endswith(('.jpg', '.png'))])
    psnrs = []
    
    for img_name in test_images:
        # 加载原始图像
        gt_path = os.path.join(test_dir, img_name)
        gt_img = np.array(Image.open(gt_path).astype(np.float32))
        
        # 加载渲染图像
        render_path = os.path.join(output_dir, os.path.splitext(img_name)[0] + ".png")
        render_img = np.array(Image.open(render_path).astype(np.float32))
        
        # 计算PSNR
        psnr = calculate_psnr(gt_img, render_img)
        psnrs.append(psnr)
        print(f"{img_name}: PSNR = {psnr:.2f}")
    
    # 保存结果
    results = {
        "mean_psnr": np.mean(psnrs),
        "min_psnr": np.min(psnrs),
        "max_psnr": np.max(psnrs),
        "per_image": {img: psnr for img, psnr in zip(test_images, psnrs)}
    }
    
    result_path = os.path.join(output_dir, "metrics.json")
    with open(result_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nAverage PSNR: {np.mean(psnrs):.2f}")
    print(f"Results saved to {result_path}")
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, default="outputs/trained_model")
    parser.add_argument("--test_dir", type=str, default="data/custom_object/test")
    
    args = parser.parse_args()
    evaluate_model(args.model_path, args.test_dir)