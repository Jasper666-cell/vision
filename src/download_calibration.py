"""从 OpenCV 官方仓库下载编号为 left 的同组棋盘图片。"""
from pathlib import Path
import json
import urllib.request
import cv2
import numpy as np

folder = Path("data/calibration")
folder.mkdir(parents=True, exist_ok=True)
# 官方这组编号中没有 left10.jpg；left.jpg 是另一张图片，不在本组。
numbers = list(range(1, 10)) + list(range(11, 15))
base = "https://raw.githubusercontent.com/opencv/opencv/4.x/samples/data/"
failed = []
for number in numbers:
    name = f"left{number:02d}.jpg"
    path = folder / name
    if path.exists() and cv2.imread(str(path)) is not None:
        print("已存在，跳过：", name, flush=True)
        continue
    for attempt in range(2):
        try:
            request = urllib.request.Request(base + name, headers={"User-Agent": "vision-homework"})
            with urllib.request.urlopen(request, timeout=20) as response:
                content = response.read()
            image = cv2.imdecode(np.frombuffer(content, dtype=np.uint8), cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError("下载内容不是有效图片")
            path.write_bytes(content)
            print("已下载：", name, flush=True)
            break
        except Exception as error:
            print(f"{name} 第 {attempt + 1} 次失败：{error}", flush=True)
    else:
        failed.append(name)

Path("data/calibration/source.json").write_text(json.dumps({
    "source": base, "files": [f"left{n:02d}.jpg" for n in numbers],
    "failed": failed,
}, ensure_ascii=False, indent=2), encoding="utf-8")
if failed:
    raise SystemExit("部分图片下载失败：" + ", ".join(failed) + "；检查网络后重试或手动下载。")
print("完成：13 张编号 left 棋盘图已经准备好。")
