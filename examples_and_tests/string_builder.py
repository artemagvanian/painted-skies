import cv2

from syndicate.kernel import Kernel

img = cv2.imread('document.jpg')

img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
vis = cv2.adaptiveThreshold(img_grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

processing_img = cv2.bitwise_not(vis)

opening = cv2.morphologyEx(processing_img, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))

kernel = Kernel.get_horizontal_kernel(5)

# Значение этого параметра зависит от расстояния между словами в тексте
N_ITERATIONS = 30

opening = cv2.dilate(opening, kernel, iterations=N_ITERATIONS)
opening = cv2.dilate(opening, cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5)), iterations=5)

_, contours, _ = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

n = 1
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if cv2.contourArea(cnt) > 2000:
        crop_img = img[y:y + h, x:x + w]
        cv2.imwrite(f'strings/crop{n}.png', crop_img)
        n += 1
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

cv2.imshow("Text detection result", cv2.resize(img, (0, 0), fx=0.25, fy=0.25))
cv2.waitKey(0)
