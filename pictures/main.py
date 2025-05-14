import cv2
from pathlib import Path
import numpy as np

video_path = Path(__file__).parent / "output.avi"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Ошибка: Не удалось открыть видео.")
    exit()

cnt = 0
total = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    total += 1
    cv2.imshow('Video', frame)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if np.array(image)[0][0] == 255 and np.array(image)[0][-1] != 255:
        cnt += 1
        cv2.imshow('Video', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
print(cnt)
print(total)
cap.release()
cv2.destroyAllWindows()