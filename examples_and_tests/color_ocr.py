import cv2
import pytesseract
from PIL import Image

for i in range(1, 8):
    img = cv2.imread(f'crops/crop{i}.png')
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    cv2.imshow('img', img)
    cv2.waitKey(0)
    print(pytesseract.image_to_string(Image.fromarray(img), lang='eng'))
