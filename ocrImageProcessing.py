import cv2
import utils
import numpy as np
import re
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

img = cv2.imread("test.jpg")
img = cv2.resize(img,(400,800))
img = img[90:img.shape[0]-100, 0:img.shape[1]]
imgGray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
imgGray = cv2.medianBlur(imgGray,5)
imgThresh = cv2.threshold(imgGray,37,255,cv2.THRESH_TOZERO)[1]


raw_text = pytesseract.image_to_string(imgThresh)

prices = re.findall("\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?", raw_text)
for price in prices:
    print(price)


cv2.imshow("Resultado",imgThresh)
cv2.waitKey(200000)
cv2.destroyAllWindows