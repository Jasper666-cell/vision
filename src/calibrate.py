"""仅对官方编号 left 棋盘图标定，不使用电脑摄像头照片。"""
from pathlib import Path
import json
import cv2
import numpy as np

# 这组官方棋盘图为 9 列、6 行内角点；请打开原图自己数一次。
pattern = (9, 6)
numbers = list(range(1, 10)) + list(range(11, 15))
files = [Path(f"data/calibration/left{n:02d}.jpg") for n in numbers]
missing = [path.name for path in files if not path.exists()]
if missing:
    raise SystemExit("请先下载完整棋盘图片，缺少：" + ", ".join(missing))
out = Path("results/corners")
out.mkdir(parents=True, exist_ok=True)

# 与角点检测结果相同：一行内先遍历 x，然后换到下一行 y。
object_grid = np.zeros((pattern[0] * pattern[1], 3), dtype=np.float32)
object_grid[:, :2] = np.mgrid[0:pattern[0], 0:pattern[1]].T.reshape(-1, 2)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
object_points, image_points, successful, failed = [], [], [], []
image_size = None
flags = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE

for path in files:
    image = cv2.imread(str(path))
    if image is None:
        failed.append(path.name)
        print("读取失败：", path.name)
        continue
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    size = (gray.shape[1], gray.shape[0])
    if image_size is None:
        image_size = size
    if size != image_size:
        raise SystemExit("图片分辨率不一致：" + path.name)
    found, corners = cv2.findChessboardCorners(gray, pattern, flags)
    if not found:
        failed.append(path.name)
        print("角点检测失败，跳过：", path.name)
        continue
    refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
    object_points.append(object_grid.copy())
    image_points.append(refined)
    successful.append(path.name)
    marked = image.copy()
    cv2.drawChessboardCorners(marked, pattern, refined, True)
    if not cv2.imwrite(str(out / (path.stem + "_corners.png")), marked):
        raise RuntimeError("角点图保存失败：" + path.name)
    print("角点检测成功：", path.name)

print(f"成功检测 {len(successful)} / {len(files)} 张")
if len(successful) < 3:
    raise SystemExit("成功图片不足三张，请核对原图及内角点尺寸后再标定。")

rms, matrix, distortion, rvecs, tvecs = cv2.calibrateCamera(
    object_points, image_points, image_size, None, None
)
np.savez("results/camera_params.npz", camera_matrix=matrix,
         dist_coeffs=distortion, image_size=np.array(image_size), rms=np.array(rms))

chosen = successful[0]
original = cv2.imread("data/calibration/" + chosen)
corrected = cv2.undistort(original, matrix, distortion, None, matrix)
comparison = np.hstack((original, corrected))
for name, image in [("undistorted.png", corrected), ("undistort_compare.png", comparison)]:
    if not cv2.imwrite("results/" + name, image):
        raise RuntimeError("去畸变图保存失败：" + name)

report = {
    "pattern_columns_rows": list(pattern), "image_size_width_height": list(image_size),
    "success_count": len(successful), "total_count": len(files),
    "successful_files": successful, "failed_files": failed,
    "camera_matrix": matrix.tolist(), "dist_coeffs": distortion.ravel().tolist(),
    "rms_pixels": float(rms), "undistorted_source": chosen,
    "object_point_spacing": 1, "object_point_unit": "棋盘单位",
}
Path("results/calibration_info.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("内参矩阵：\n", matrix)
print("畸变系数：", distortion.ravel())
print("RMS 重投影误差（像素）：", rms)
print("图片尺寸（宽，高）：", image_size)
print("去畸变对比：左侧原图，右侧去畸变。参数属于样本对应的相机。")
