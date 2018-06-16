import re

import cv2
from PIL import Image
import pytesseract
from examples_and_tests.properties import *


def scan_for_selections(hsv_min, hsv_max, lang):
    img = cv2.imread('document.jpg')
    # преобразуем RGB картинку в HSV модель
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # применяем цветовой фильтр
    thresh = cv2.inRange(hsv, hsv_min, hsv_max)

    # thresh = cv2.dilate(thresh, np.ones((10, 10)), iterations=1)

    _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Пересохраняем вырезанные области
    for n, i in enumerate(contours):
        # Фильтруем по размеру
        if cv2.contourArea(i) > 2000:
            x, y, w, h = cv2.boundingRect(i)
            crop_img = img[y:y + h, x:x + w]
            #grayscaled = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
            #_, th = cv2.threshold(grayscaled, 125, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            string = pytesseract.image_to_string(Image.fromarray(crop_img), lang=lang)
            cleanString = re.sub('\W+', ' ', string)
            print(f"{cleanString} - {n}")
            cv2.imwrite(f'contours/crop{n}.png', crop_img)

print("PINK")
scan_for_selections(pink_hsv_min, pink_hsv_max, 'eng')
print("GREEN")
scan_for_selections(green_hsv_min, green_hsv_max, 'eng')
print("YELLOW")
scan_for_selections(yellow_hsv_min, yellow_hsv_max, 'eng')
print("ALL")
scan_for_selections(universal_hsv_min, universal_hsv_max, 'eng')
