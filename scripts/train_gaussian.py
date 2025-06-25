import os
import subprocess
import argparse
from datetime import datetime

def train_gaussian_splatting(data_path, output_dir, iterations=30000):
    os.makedirs(output_dir, exist_ok=True)
    
    # 训练参数配置
    cmd = [
        "python", "gaussian-splatting/train.py",
        "-s", data_path,
        "-m", output_dir,
        "--iterations", str(iterations),
        "--eval",
        "--test_iterations", "5000,10000,15000,20000,25000,30000",
        "--save_iterations", "5000,10000,15000,20000,25000,30000",
        "--checkpoint_iterations", "5000,10000,15000,20000,25000,30000",
        "--quiet"
    ]
    
    print("Starting training...")
    print(" ".join(cmd))
    subprocess.run(cmd)
    
    # 启动TensorBoard
    tb_cmd = f"tensorboard --logdir {output_dir} --port 6006 &"
    print(f"Run TensorBoard with: {tb_cmd}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, default="data/custom_object")
    parser.add_argument("--output_dir", type=str, default="outputs/trained_model")
    parser.add_argument("--iterations", type=int, default=30000)
    
    args = parser.parse_args()
    train_gaussian_splatting(args.data_path, args.output_dir, args.iterations)