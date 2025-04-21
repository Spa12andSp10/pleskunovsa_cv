import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.color import rgb2hsv
import numpy as np

def determine_the_shade(reg):
    cnt = 0
    shade = "Оттенок1"
    col = [0.19202898, 0.30476192, 0.41509435, 0.60897434, 0.8333333]
    for i in range(len(col)):
        cnt += 1
        if reg < col[i]:
            return shade
        else:
            shade = shade.replace(str(cnt), str(cnt + 1), 1)
    shade = shade.replace(str(cnt), str(cnt + 1), 1)
    return shade

image = plt.imread("balls_and_rects.png")
hsv_image = rgb2hsv(image)

gray = image.mean(axis=2)
binary = gray > 0
labeled = label(binary)
regions = regionprops(labeled)

cnt_ball, cnt_rect = 0, 0
colors_ball, colors_rect = [], []
res_rect, res_ball = {}, {}
for region in regions:
    if region.eccentricity == 0.0:
        yb, xb = region.centroid
        colors_ball.append(hsv_image[int(yb), int(xb), 0])
        cnt_ball += 1
    else:
        yr, xr = region.centroid
        colors_rect.append(hsv_image[int(yr), int(xr), 0])
        cnt_rect += 1
print(f"Общие число фигур равно {cnt_ball + cnt_rect}")


for i in colors_ball:
    color = determine_the_shade(i)
    if color not in res_ball:
        res_ball[color] = 0
    res_ball[color] += 1
print(f"Мячики по цветам {sorted(res_ball.items())}")

for i in colors_rect:
    color = determine_the_shade(i)
    if color not in res_rect:
        res_rect[color] = 0
    res_rect[color] += 1
print(f"Прямоугольники по цветам {sorted(res_rect.items())}")

plt.figure()
plt.subplot(121)
plt.plot(sorted(colors_ball), "o-")
plt.subplot(122)
plt.plot(sorted(colors_rect), "o-")
plt.show()