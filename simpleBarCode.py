import cv2
import pyzbar
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FOCUS, 255)


while(True):
    success, frame = cap.read()

    cv2.imshow("image",frame)
    cv2.waitKey(1)

    for code in decode(frame):
        print(code.type)
        print(code.data.decode('utf-8'))
    
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break