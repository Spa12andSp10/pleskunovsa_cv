import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.morphology import (binary_closing, binary_dilation, binary_erosion, binary_opening)


image = np.load('wires6npy.txt')

labeled_start = label(image)


result = binary_erosion(image, np.ones(3).reshape(3, 1))

cnt, global_cnt = 0, 0
labeled = label(result)
for y in range(1, labeled.shape[0] - 1):
    if np.sum(labeled[y]) != 0:
        for x in range(1, labeled.shape[1] - 1):
            if labeled[y, x] == 0:
                cnt += 1
        if cnt != 0:
            print("Провод поделен на", cnt + 1, "частей")
            global_cnt += 1
        else:
            print("Провод поделен на", cnt, "частей")
            global_cnt += 1
        cnt = 0
if global_cnt != np.max(labeled_start):
    print(f"Есть {np.max(labeled_start) - global_cnt} провод, который полностью поврежден")
plt.imshow(result)
plt.show()