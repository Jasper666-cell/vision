"""先运行 process.py，再运行本文件。"""
from pathlib import Path
import json
import cv2
import numpy as np

gray = cv2.imread("results/gray.png", cv2.IMREAD_GRAYSCALE)
if gray is None:
    raise SystemExit("请先在 vision 目录运行 src/process.py，生成 gray.png。")

seed = 42
ratio = 0.05
rng = np.random.default_rng(seed)
noisy = gray.copy()
count = round(gray.size * ratio)
# replace=False 保证抽到的像素位置不重复，总计约 5%。
indices = rng.choice(gray.size, size=count, replace=False)
half = count // 2
noisy.flat[indices[:half]] = 0
noisy.flat[indices[half:]] = 255

median3 = cv2.medianBlur(noisy, 3)
median9 = cv2.medianBlur(noisy, 9)
images = [gray, noisy, median3, median9]
names = ["gray", "noisy", "median3", "median9"]

# 同一坐标区域取出后，用最近邻放大，便于看清噪点与边缘。
height, width = gray.shape
x1, y1 = width // 3, height // 3
x2, y2 = min(x1 + 80, width), min(y1 + 80, height)
patches = [cv2.resize(image[y1:y2, x1:x2], None, fx=4, fy=4,
                      interpolation=cv2.INTER_NEAREST) for image in images]

for name, image in zip(names[1:], images[1:]):
    if not cv2.imwrite("results/" + name + ".png", image):
        raise RuntimeError("保存失败：" + name)

# 四张图形状相同，拼图可直接上下、左右拼接。
comparison = np.vstack((np.hstack(images[:2]), np.hstack(images[2:])))
zoom = np.vstack((np.hstack(patches[:2]), np.hstack(patches[2:])))
for name, image in [("filter_compare.png", comparison), ("filter_zoom.png", zoom)]:
    if not cv2.imwrite("results/" + name, image):
        raise RuntimeError("保存失败：" + name)

info = {
    "seed": seed, "selected_noise_ratio": count / gray.size,
    "selected_pixels": count, "pepper_pixels": half,
    "salt_pixels": count - half,
    "changed_pixels": int(np.count_nonzero(noisy != gray)),
    "kernels": [3, 9], "zoom_xyxy": [x1, y1, x2, y2],
    "zoom_scale": 4,
    "layout": "左上：原灰度；右上：含噪；左下：3x3；右下：9x9",
}
Path("results/filter_info.json").write_text(
    json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("随机种子 =", seed, "选中像素比例 =", count / gray.size)
print(f"放大区域：x=[{x1}, {x2})，y=[{y1}, {y2})")
print("拼图位置：左上原灰度，右上含噪，左下3x3，右下9x9。")
print("完成：请打开 filter_compare.png 和 filter_zoom.png 观察。")
