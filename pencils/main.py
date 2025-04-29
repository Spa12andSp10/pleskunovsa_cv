import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.morphology import binary_closing
from skimage.transform import resize
from pathlib import Path

image_path = Path(__file__).parent / 'img'
total = 0
files = sum(1 for item in image_path.iterdir() if item.is_file())
for i in range(1, files + 1):
    image = plt.imread(image_path / f"img ({i}).jpg")
    gray = image.mean(axis=2)
    resize_image = resize(gray, (1500, 1500))
    resize_image = resize_image[20:1480, 20:1480]
    binary = resize_image < 130
    binary = binary_closing(binary, np.ones((35, 35)))
    labeled = label(binary)
    regions = regionprops(labeled)
    cnt = 0
    for region in regions:
        if region.eccentricity > 0.99:
            cnt += 1
            total += 1
    print(f"Pencils: {cnt}, image: {i}")
print(f"All pencils {total}")
