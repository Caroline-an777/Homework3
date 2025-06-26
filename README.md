# 3D Gaussian Splatting 物体重建与视图合成
## 项目概述
本项目基于3D Gaussian Splatting技术，实现物体的三维重建和新视图合成。通过多角度拍摄的物体图像，使用COLMAP进行相机位姿估计，训练3D高斯模型，并生成环绕物体的新视角视频。
### 核心功能
- 从多视角图像重建3D物体模型
- 生成高质量的新视图渲染
- 定量评估模型性能（PSNR、SSIM）
- 渲染物体环绕视频
## 环境配置
### 系统要求
- Ubuntu 20.04+
- NVIDIA GPU (推荐RTX 3090/4090)
- CUDA 11.7+
- Python 3.8+
### 安装依赖
```bash
# 克隆项目仓库
git clone https://github.com/yourname/3d-gaussian-splatting-project.git
cd 3d-gaussian-splatting-project

# 创建Python环境
conda create -n gsplat python=3.8
conda activate gsplat

# 安装PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117

# 安装项目依赖
pip install -r requirements.txt

# 安装COLMAP
sudo apt install colmap
```
也可以直接在autodl中直接选择官方镜像，镜像已部署colmap环境，操作起来更方便
## 数据集准备
- 拍摄物体视频（建议环绕物体360度拍摄）
- 从视频中抽取帧图像：
```bash
ffmpeg -i object.mp4 -vf fps=2 input/%04d.jpg
```
- 数据集目录结构：
```text
dataset/
└── green/
    ├── input/             # 原始图像
    │   ├── 0001.jpg
    │   ├── 0002.jpg
    │   └── ...
    └── sparse/            # COLMAP输出
        ├── cameras.txt
        ├── images.txt
        └── points3D.txt
└── toy/
    ├── input/             # 原始图像
    │   ├── 0001.jpg
    │   ├── 0002.jpg
    │   └── ...
    └── sparse/            # COLMAP输出
        ├── cameras.txt
        ├── images.txt
        └── points3D.txt
```
## 快速开始
- 相机位姿估计（COLMAP）
  ```bash
  python scripts/run_colmap.py dataset/green
  ```
- 训练3D高斯模型
  ```bash
  python train.py -s dataset/green 
  ```
- 渲染环绕视频
  ```bash
  python render_video.py \
  --model_path output/your_object_model \
  --iteration 30000 \
  --num_frames 120 \
  --radius 3.0 \
  --height 0.5
  ```
- 评估模型
  ```bash
  python evaluate.py -m output/train_model --iteration 30000
  ```
- 结果可视化
  ```bash
  tensorboard --logdir output/train_model/logs
  ```
- 渲染测试集图像
  ```bash
  python render.py -m output/train_model --iteration 30000
  ```
## 项目结构
```text
3d-gaussian-splatting-project/
├── data/                  # 示例数据集
├── output/                # 训练输出目录
├── scripts/               # 实用脚本
│   ├── run_colmap.py      # COLMAP自动化脚本
│   ├── video_to_frames.py # 视频抽帧脚本
│   └── ...
├── src/                   # 核心源代码
│   ├── colmap_utils.py    # COLMAP数据处理
│   ├── gaussian_model.py  # 3D高斯模型
│   ├── renderer.py        # 渲染器
│   └── ...
├── requirements.txt       # Python依赖
├── train.py               # 训练脚本
├── render_video.py        # 视频渲染脚本
├── evaluate.py            # 评估脚本
└── README.md              # 项目文档
```
## 模型性能对比
| 模型         | PSNR ↑  | SSIM ↑ | LPIPS ↓ | 训练时间  |
|--------------|---------|--------|---------|-----------|
| 皮卡丘手办     | 45.1 dB | 0.91   | 0.12    | 42 分钟   |
| 多肉盆栽      | 30.8 dB | 0.89   | 0.15    | 38 分钟   |
## 常见问题解决
- COLMAP重建失败
  ```bash
  # 尝试降低特征点阈值
  colmap feature_extractor ... --SiftExtraction.peak_threshold 0.004
  ```
- 训练显存不足
  ```bash
  # 减少批量大小
  python train.py ... --batch_size 1

  # 降低分辨率
  python train.py ... --resolution 0.5
  ```
- 点云渲染问题
  ```bash
  # 尝试不同迭代的模型
  python render_video.py ... --iteration 7000
  ```
