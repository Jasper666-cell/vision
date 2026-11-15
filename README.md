# vision

第二次任务：摄像头拍照、NumPy/OpenCV 图像处理与棋盘图相机标定。

目前已准备项目目录和环境；拍照、图像处理、标定代码及对应结果仍待完成。完整勾选清单在项目上一层的《第二次任务_待办清单.md》。

## 环境

- 操作系统：Windows 11，64 位。
- 环境工具：uv；使用项目内 `.venv`。
- Python：3.14.10。
- 依赖：NumPy、opencv-python；版本及验证结果见 [环境配置说明](环境配置说明.md)，精确版本记录于 `requirements.txt`。

在项目目录打开 PowerShell，重建环境：

```powershell
uv --no-cache venv --python 3.14 .venv
uv --no-cache pip install --python .venv\Scripts\python.exe -r requirements.txt
```

后续脚本写好后，用以下形式运行，将路径换为实际脚本：

```powershell
.\.venv\Scripts\python.exe .\src\实际脚本名.py
```

这里的“实际脚本名.py”是占位示例，当前尚无该脚本。无需运行虚拟环境激活脚本，也能直接使用项目解释器。

## 1. 拍照

待完成：代码、运行命令、`data/photo.jpg` 及照片展示。

## 2. 数组与通道操作

待完成：图像形状与数据类型、像素与区域坐标、裁剪图、原图/局部改色/仅 B/仅 G/仅 R/灰度对比，以及通道顺序简答。

## 3. 滤波

待完成：约 5% 椒盐噪声、固定随机种子、3×3 与 9×9 中值滤波、同一区域放大对比，以及基于自己结果的简答。

## 4. 相机标定

待完成：官方 `left*.jpg` 样本、棋盘内角点尺寸、成功检测数量、至少三张角点图、内参矩阵、畸变系数、RMS 重投影误差（像素）、图片分辨率、`results/camera_params.npz`、去畸变对比，以及 `fx/fy/cx/cy` 简答。

样本图片的标定参数属于该数据集对应的相机。
