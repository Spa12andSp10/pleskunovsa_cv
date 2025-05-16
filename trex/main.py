import numpy as np
import time
import pyautogui
from skimage.measure import regionprops, label
import cv2
import mss
import os

wid = 40
cnt, t = 0, 0.3
location = None


while True:
    try:
        location = pyautogui.locateOnScreen("img.png", confidence=0.9)
        if location:
            break
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)


output_folder = "output_images"
os.makedirs(output_folder, exist_ok=True)

p1 = location[0] + location[2] + 13
p2 = location[1] + location[3] + 5
cactus_region = {'left': p1, 'top': p2, 'width': wid, 'height': 10}

pyautogui.PAUSE = 0.02


def handle_obstacle(binary_img):
    global cnt, p1, t, wid
    try:
        labeled_img = label(binary_img)
        regions = regionprops(labeled_img)

        obstacles = [reg for reg in regions if reg.area > 50]

        if len(obstacles) >= 1:
            pyautogui.keyUp('down')
            pyautogui.press('space')
            time.sleep(t)
            pyautogui.keyDown('down')
            cnt += 0.35
            if cnt > 1 and wid != 65 :
                p1 += 2
                wid += 1
                t = max(0.15 , t - 0.02)
                cnt = 0
    except Exception as  e :
        print(f"Ошибка в  обработке препятствия: {e}")


print("Запуск через 1 секунду...")
time.sleep(1)

try:
    with mss.mss() as sct:
        while True:
            screenshot = np.array(sct.grab(cactus_region))
            if screenshot.size == 0:
                print("Ошибка: скриншот пустой!")
                continue

            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            handle_obstacle(binary)

            cactus_region = {'left': p1, 'top': p2, 'width': wid, 'height': 10}

            cv2.imshow("Dino Bot", screenshot)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
except KeyboardInterrupt:
    print("Бот остановлен вручную")
finally:
    cv2.destroyAllWindows()