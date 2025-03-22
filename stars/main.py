import numpy as np
from skimage.measure import label
from skimage.morphology import binary_opening

image = np.load("stars.npy")

struct_cross = np.array([[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0],[0,1,0,1,0],[1,0,0,0,1]])
struct_plus = np.array([[0,0,1,0,0],[0,0,1,0,0],[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0]])
image_cross = binary_opening(image, struct_cross)
image_plus = binary_opening(image, struct_plus)
labeled_cross = label(image_cross)
labeled_plus = label(image_plus)

print(f"Количество звезд равно {np.max(labeled_cross) + np.max(labeled_plus)}")
