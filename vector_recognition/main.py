import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops

def count_holes(region):
    shape = region.image.shape
    new_image = np.zeros((shape[0] + 2, shape[1] + 2))
    new_image[1:-1, 1:-1] = region.image
    new_image = np.logical_not(new_image)
    labeled = label(new_image)
    return np.max(labeled) - 1

def extractor(region):
    area =  region.area / region.image.size
    cy, cx = region.centroid_local
    cy /= region.image.shape[0]
    cx /= region.image.shape[1]
    perimeter = region.perimeter
    perimeter /= region.image.size
    eccentricity = region.eccentricity
    vlines = np.sum(region.image, 0) == region.image.shape[0]
    vlines = np.sum(vlines) / region.image.shape[1]
    hlines = np.sum(region.image, 1) == region.image.shape[1]
    hlines = np.sum(hlines) / region.image.shape[0]
    holes = count_holes(region)
    r = region.image.shape[1] / region.image.shape[0]
    return np.array([area, cy, cx, perimeter, eccentricity, vlines, hlines, holes, cx < 0.45, abs(cx - cy), r])

def norm_l1(v1, v2):
    return ((v1 - v2) ** 2).sum() ** 0.5

def classificator(v, templates):
    result = "_"
    min_dist = 10 ** 16
    for key in templates:
        d = norm_l1(v, templates[key])
        if d < min_dist:
            result = key
            min_dist = d
    return result


image = plt.imread("alphabet-small.png")
gray = image.mean(axis = 2)
binary = gray < 1

labeled = label(binary)
regions = regionprops(labeled)

templates = {
    "A": extractor(regions[2]),
    "B": extractor(regions[3]),
    "8": extractor(regions[0]),
    "0": extractor(regions[1]),
    "1": extractor(regions[4]),
    "W": extractor(regions[5]),
    "X": extractor(regions[6]),
    "*": extractor(regions[7]),
    "-": extractor(regions[9]),
    "/": extractor(regions[8])
}

for region in regions:
    v = extractor(region)
    print(classificator(v, templates))

symbols = plt.imread("alphabet.png")[:,:,:-1]
gray = symbols.mean(axis = 2)
binary = gray > 0
labeled = label(binary)
regions = regionprops(labeled)
plt.figure()
v = extractor(regions[199])
plt.title(classificator(v, templates))
plt.imshow(regions[199].image)
plt.show()

