import os
import cv2
import argparse
from pathlib import Path

def video_to_images(video_path, output_dir, frame_interval=5):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    count = 0
    saved_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        if count % frame_interval == 0:
            img_path = os.path.join(output_dir, f"frame_{saved_count:04d}.jpg")
            cv2.imwrite(img_path, frame)
            saved_count += 1
            print(f"Saved {img_path}")
        
        count += 1
    
    cap.release()
    print(f"Extracted {saved_count} images from video")

def split_dataset(image_dir, train_ratio=0.8):
    all_images = sorted([f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png'))])
    split_idx = int(len(all_images) * train_ratio)
    
    train_dir = os.path.join(image_dir, "..", "train")
    test_dir = os.path.join(image_dir, "..", "test")
    
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    
    # 移动训练集
    for img in all_images[:split_idx]:
        src = os.path.join(image_dir, img)
        dst = os.path.join(train_dir, img)
        os.rename(src, dst)
    
    # 移动测试集
    for img in all_images[split_idx:]:
        src = os.path.join(image_dir, img)
        dst = os.path.join(test_dir, img)
        os.rename(src, dst)
    
    print(f"Split dataset: {len(all_images[:split_idx])} train, {len(all_images[split_idx:])} test")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path", type=str, help="Path to input video")
    parser.add_argument("--output_dir", type=str, default="data/custom_object/images")
    parser.add_argument("--frame_interval", type=int, default=5)
    parser.add_argument("--split_ratio", type=float, default=0.8)
    
    args = parser.parse_args()
    
    if args.video_path:
        video_to_images(args.video_path, args.output_dir, args.frame_interval)
    
    split_dataset(args.output_dir, args.split_ratio)