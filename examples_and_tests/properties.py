# HSV фильтры для цветов маркеров (подобран на основе colordistinguisher_helper.py)
import numpy as np

pink_hsv_min = np.array((140, 40, 150), np.uint8)
pink_hsv_max = np.array((255, 255, 255), np.uint8)

green_hsv_min = np.array((50, 60, 150), np.uint8)
green_hsv_max = np.array((80, 255, 255), np.uint8)

yellow_hsv_min = np.array((0, 20, 150), np.uint8)
yellow_hsv_max = np.array((40, 255, 255), np.uint8)

universal_hsv_min = np.array((0, 20, 150), np.uint8)
universal_hsv_max = np.array((255, 255, 255), np.uint8)