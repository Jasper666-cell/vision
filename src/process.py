"""复制到 vision/src/ 后，在 vision 终端运行本文件。"""
from pathlib import Path
import json
import cv2
import numpy as np

Path("results").mkdir(exist_ok=True)
img = cv2.imread("data/photo.jpg")
if img is None:
    raise SystemExit("读不到照片：请在 vision 目录运行，并检查 data/photo.jpg。")

height, width, channels = img.shape
print("shape =", img.shape, "dtype =", img.dtype)
print("高 =", height, "宽 =", width, "通道数 =", channels)

# u 是横坐标，v 是纵坐标；数组访问时先写行，再写列。
u, v = width // 2, height // 2
print(f"像素 (u, v) = ({u}, {v})，BGR = {img[v, u]}")

# 切片包含起点，不包含终点；这里裁剪图像中央的一块区域。
x1, x2 = width // 4, width * 3 // 4
y1, y2 = height // 4, height * 3 // 4
crop = img[y1:y2, x1:x2].copy()
print(f"裁剪区域：x=[{x1}, {x2})，y=[{y1}, {y2})")

red = img.copy()
rx1, rx2 = width // 16, width // 4
ry1, ry2 = height // 16, height // 4
red[ry1:ry2, rx1:rx2] = (0, 0, 255)
print(f"红色区域：x=[{rx1}, {rx2})，y=[{ry1}, {ry2})")

# zeros_like 创建形状、数据类型相同，但所有元素都是 0 的数组。
only_b = np.zeros_like(img)
only_b[:, :, 0] = img[:, :, 0]
only_g = np.zeros_like(img)
only_g[:, :, 1] = img[:, :, 1]
only_r = np.zeros_like(img)
only_r[:, :, 2] = img[:, :, 2]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print("单通道保留彩色图的 shape =", only_b.shape)
print("灰度图的 shape =", gray.shape)

images = {
    "crop.png": crop, "red.png": red,
    "only_b.png": only_b, "only_g.png": only_g,
    "only_r.png": only_r, "gray.png": gray,
}
for name, image in images.items():
    if not cv2.imwrite("results/" + name, image):
        raise RuntimeError("保存失败：" + name)

info = {
    "shape": list(img.shape), "dtype": str(img.dtype),
    "pixel_uv": [u, v], "pixel_bgr": img[v, u].tolist(),
    "crop_xyxy": [x1, y1, x2, y2],
    "red_xyxy": [rx1, ry1, rx2, ry2],
    "gray_shape": list(gray.shape), "channel_order": "BGR",
}
Path("results/process_info.json").write_text(
    json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("完成：结果图片和坐标记录已写入 results，原照片未修改。")
