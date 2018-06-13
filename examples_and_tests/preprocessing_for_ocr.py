import cv2
import pytesseract
from PIL import Image

IMAGE = 'contours/crop20442.png'

img = cv2.imread(IMAGE)
grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# th = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
_, th = cv2.threshold(grayscaled, 125, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imshow('Thresh', th)
string = pytesseract.image_to_string(Image.fromarray(th), lang='eng')
print(string)
cv2.waitKey(0)
