import os
import subprocess
from pathlib import Path

def run_colmap(image_dir, output_dir):
    # 创建COLMAP项目目录
    project_path = os.path.join(output_dir, "colmap_project")
    os.makedirs(project_path, exist_ok=True)
    
    # 创建COLMAP数据库
    db_path = os.path.join(project_path, "database.db")
    sparse_dir = os.path.join(project_path, "sparse")
    dense_dir = os.path.join(project_path, "dense")
    
    # 使用完整路径指定COLMAP可执行文件
    colmap_path = r"C:\Program Files\colmap\colmap.bat"

    # 特征提取 - 使用 colmap_path
    subprocess.run([
        colmap_path, "feature_extractor",  # 这里使用变量而不是字符串
        "--database_path", db_path,
        "--image_path", image_dir,
        "--ImageReader.single_camera", "1",
        "--ImageReader.camera_model", "PINHOLE"  # 添加这行强制使用针孔模型
    ])
    
    # 特征匹配 - 使用 colmap_path
    subprocess.run([
        colmap_path, "exhaustive_matcher",  # 这里使用变量而不是字符串
        "--database_path", db_path
    ])
    
    # 稀疏重建 - 使用 colmap_path
    os.makedirs(sparse_dir, exist_ok=True)
    subprocess.run([
        colmap_path, "mapper",  # 这里使用变量而不是字符串
        "--database_path", db_path,
        "--image_path", image_dir,
        "--output_path", sparse_dir
    ])
    
    # 转换为文本格式 - 使用 colmap_path
    sparse_text_dir = os.path.join(output_dir, "sparse_text")
    os.makedirs(sparse_text_dir, exist_ok=True)
    subprocess.run([
        colmap_path, "model_converter",  # 这里使用变量而不是字符串
        "--input_path", os.path.join(sparse_dir, "0"),
        "--output_path", sparse_text_dir,
        "--output_type", "TXT"
    ])
    
    print(f"COLMAP processing complete. Results in {sparse_text_dir}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_dir", type=str, default="data/train")
    parser.add_argument("--output_dir", type=str, default="data/custom_object")
    
    args = parser.parse_args()
    run_colmap(args.image_dir, args.output_dir)