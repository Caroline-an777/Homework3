import os
import subprocess
import numpy as np
import json
from math import cos, sin, pi

def generate_circular_trajectory(num_frames=300, radius=3.0, height=1.0):
    """生成圆形相机轨迹"""
    cameras = []
    for i in range(num_frames):
        angle = 2 * pi * i / num_frames
        x = radius * cos(angle)
        z = radius * sin(angle)
        
        # 相机位置
        position = [x, height, z]
        
        # 相机朝向 (看向原点)
        target = [0, height/2, 0]
        
        # 上方向
        up = [0, 1, 0]
        
        cameras.append({
            "position": position,
            "target": target,
            "up": up
        })
    
    return cameras

def render_video(model_path, output_dir, resolution=(1280, 720)):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. 生成轨迹文件
    trajectory = generate_circular_trajectory()
    traj_path = os.path.join(output_dir, "trajectory.json")
    with open(traj_path, "w") as f:
        json.dump(trajectory, f)
    
    # 2. 渲染视频
    cmd = [
        "python", "render.py",
        "-m", model_path,
        "--trajectory", traj_path,
        "--skip_train",
        "--resolution", f"{resolution[0]}x{resolution[1]}",
        "-o", os.path.join(output_dir, "render.mp4")
    ]
    
    print("Rendering video...")
    subprocess.run(cmd)
    print(f"Video saved to {os.path.join(output_dir, 'render.mp4')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, default="outputs/trained_model")
    parser.add_argument("--output_dir", type=str, default="outputs/renderings")
    
    args = parser.parse_args()
    render_video(args.model_path, args.output_dir)