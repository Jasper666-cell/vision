from pathlib import Path
import cv2
Path("date").mkdir(exist_ok=True)
camera = cv2.VideoCapture(0)
try:
    if not camera.isOpened():
        raise SystemExit("摄像头打开失败,请尝试把编号0改成1.")
    print("请打开摄像头画面窗口,按s保存照片,按q退出.")
    while True:
        success, frame = camera.read()
        if not success:
            print("读取画面失败，程序退出。")
            break
        cv2.imshow("Camera", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("s"):
            saved = cv2.imwrite("data/photo.jpg", frame)
            if saved:
                print("照片已保存到 data/photo.jpg")
            else:
                print("保存失败，请检查文件夹是否可以写入。")
        elif key == ord("q"):
            break
finally:
    camera.release()
    cv2.destroyAllWindows()