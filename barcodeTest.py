# Import modules
import cv2
import numpy as np
from numpy.core.fromnumeric import std
from numpy.lib.function_base import average
import utils
import tkinter.messagebox as tkmsgbox
import time
import winsound
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
import re
import easyocr


imgHeight = 1920
imgWidth = 1080
productsList=[
    "Água 1,5 L",
    "Água com gás",
    "Água sem gás",
    "Água tônica",
    "Cerveja 600 mL Comum",
    "Cerveja 600 mL Premium",
    "Cerveja Lata",
    "Cerveja Long Neck",
    "H2OH",
    "Marmitex com churrasco",
    "Marmitex sem churrasco",
    "Picolé grupo 1",
    "Picolé grupo 2",
    "Picolé grupo 3",
    "Picolé grupo 4",
    "Red Bull",
    "Refrigerante 1 L",
    "Refrigerante 1,5 L",
    "Refrigerante 2 L",
    "Refrigerante 600 mL",
    "Refrigerante KS",
    "Refrigerante Lata",
    "Refrigerante NS",
    "Suco Copo",
    "Suco Jarra"
]
priceList=[
    6.0,
    4.0,
    3.0,
    5.0,
    13.0,
    16.0,
    5.0,
    7.0,
    5.0,
    18.0,
    19.0,
    7.0,
    4.0,
    9.0,
    3.0,
    12,
    8,
    10,
    12,
    6,
    4.5,
    5,
    5.5,
    5,
    16
]

def scanTicket():
    # Initialize video capture
    cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
    ret, frame = cap.read()
    if frame is not None:
        #products = scanBack(cap)
        #time.sleep(3) # Sleep for 3 seconds
        scanFront(cap)
    else: 
        errorMessage()
    cap.release()
    cv2.destroyAllWindows()

def errorMessage():
    tkmsgbox.showinfo("Erro", "Erro: Câmera não detectada")

## Scans an ticket and corrects its perspective
def scanImage(cap):
    lastDetected = False
    timer=0
    while(1):
        ret, frame = cap.read()
        img = frame
        img = cv2.resize(img, (imgHeight, imgWidth))
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (79, 79), 3)  # ADD GAUSSIAN BLUR
        high_thresh, thresh_im = cv2.threshold(imgBlur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        lowThresh = 0.5*high_thresh
        imgThreshold = cv2.Canny(imgBlur, lowThresh, high_thresh)  # APPLY CANNY BLUR
        contours, hierarchy = cv2.findContours(
            imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # FIND ALL CONTOURS
        biggest, maxArea = utils.biggestContour(
            contours)  # FIND THE BIGGEST CONTOUR
        if biggest.size != 0:
            if lastDetected == True and maxArea > 400000:
                timer+=1
            else:
                timer=0
                #lastDetected = False
            biggest = utils.reorder(biggest)
            pts1 = np.float32(biggest)  
            pts2 = np.float32([[0, 0], [imgHeight, 0], [0, imgWidth], [imgHeight, imgWidth]])
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            imgWarpColored = cv2.warpPerspective(img, matrix, (imgHeight, imgWidth))
            imgScanDisplay = img.copy()
            imgScanDisplay = utils.drawRectangle(imgScanDisplay, biggest, 10)
            imgScanDisplay = cv2.rotate(imgScanDisplay,cv2.ROTATE_90_CLOCKWISE)
            imgScanDisplay = cv2.resize(imgScanDisplay,(400,700))
            cv2.imshow("Scan",imgScanDisplay)
            cv2.waitKey(1)
            lastDetected = True
        else:
            imgScanDisplay = img.copy()
            imgScanDisplay = cv2.rotate(imgScanDisplay,cv2.ROTATE_90_CLOCKWISE)
            imgScanDisplay = cv2.resize(imgScanDisplay,(400,700))
            cv2.imshow("Scan",imgScanDisplay)
            cv2.waitKey(1)
        if (timer>=7):
            winsound.Beep(1900, 250)
            cv2.destroyAllWindows() 
            return imgWarpColored

def trackChaned(x):
    pass

def scanFront(cap):

    reader = easyocr.Reader(['en'])
    img = scanImage(cap)
    img = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
    img = cv2.resize(img,(400,800))
    img = img[90:img.shape[0]-100, 0:img.shape[1]] 
    result = reader.readtext(img) 
    for line in result:
        print(line)
    # img_cropped_gray = cv2.cvtColor(img_cropped_resized, cv2.COLOR_BGR2GRAY)
    # img_cropped_blur = cv2.medianBlur(img_cropped_gray,5)
    # img_cropped_threshold = cv2.threshold(img_cropped_blur, 37, 255, cv2.THRESH_BINARY)[1]
    # kernel = np.ones((1,1),np.uint8)
    # img_cropped_dilated = cv2.dilate(img_cropped_threshold, kernel, iterations = 1)

    #gray = cv2.cvtColor(img_cropped_resized, cv2.COLOR_RGB2GRAY)
    # gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # gray = cv2.bitwise_not(img_bin)
    # kernel = np.ones((2, 1), np.uint8)
    # img = cv2.erode(gray, kernel, iterations=1)
    # img = cv2.dilate(img, kernel, iterations=1)

    imgGray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    imgGray = cv2.medianBlur(imgGray,5)


    cv2.namedWindow('Color Track Bar')
    hh='Max'
    hl='Min'
    wnd = 'Colorbars'
    cv2.createTrackbar("Max", "Color Track Bar",3,255,trackChaned)
    cv2.createTrackbar("Min", "Color Track Bar",0,255,trackChaned)

    while(True):
        hul=cv2.getTrackbarPos("Max", "Color Track Bar")
        if hul%2 == 0:
            hul+=1 
        #img_cropped = cv2.threshold(img_cropped_blur, 37, 255, cv2.THRESH_BINARY)[1]
        #img = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
        #cv2.imwrite('test.jpg',img)
        # imgAdaptiveThre = cv2.adaptiveThreshold(gray,255, 1, 1, 15, 5)
        # imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
        # imgAdaptiveThre = cv2.medianBlur(imgAdaptiveThre, 11)
        imgThresh = cv2.threshold(img,63,255,cv2.THRESH_BINARY)[1]
        raw_text = pytesseract.image_to_string(imgThresh,config=r"--psm 6")
        cv2.imshow("resultado",imgThresh)
        cv2.waitKey(1)
        
        print(raw_text,'\n')
        prices = re.findall("\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?", raw_text)
        for price in prices:
            print(price)
        break
    cv2.destroyAllWindows()
scanTicket()

