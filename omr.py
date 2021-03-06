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
        meals = scanFront(cap)
        qt = scanBack(cap)
    else: 
        errorMessage()
    cap.release()
    cv2.destroyAllWindows()
    return meals, qt

def errorMessage():
    tkmsgbox.showinfo("Erro", "Erro: Câmera não detectada")

## Scans an ticket and corrects its perspective
def scanImage(cap):
    lastDetected = False
    timer=0
    while(1):
        #print("Escaneando imagem")
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

def scanBack(cap):
    products = 25
    choices = 10
    img = scanImage(cap)
    boxesArea = img.copy()
    boxesArea = boxesArea[30:590, 210:1670]
    boxesArea = cv2.resize(boxesArea,(imgHeight,imgWidth))

    # APPLY ADAPTIVE THRESHOLD
    boxesAreaGray = cv2.cvtColor(boxesArea, cv2.COLOR_BGR2GRAY)
    boxesAreaTresh = cv2.threshold(boxesAreaGray,70, 255, cv2.THRESH_BINARY_INV)[1]
    boxesAreaTreshRotated = cv2.rotate(boxesAreaTresh,cv2.ROTATE_90_CLOCKWISE)
    boxes=utils.splitBoxes(boxesAreaTreshRotated)
    
    # COUNT NON ZERO PIXELS
    myPixelVal = np.zeros((products,choices))
    countC=0
    countR=0

    for box in boxes:
        totalPixels = cv2.countNonZero(box)
        myPixelVal[countR][countC] = totalPixels
        countC+=1
        if (countC==choices):
            countR+=1
            countC=0
    #print(myPixelVal)
        
    myChoices=[]
    myGeneralAverge = average(myPixelVal)
    myGeneralDeviation = std(myPixelVal)
    myGeneralAnswerThreshold = myGeneralDeviation*2
    myGeneralUpperLimit = myGeneralAverge+myGeneralAnswerThreshold

    for x in range(0,products):
        arr = myPixelVal[x]
        myAverage = average(arr)
        myDeviation = std(arr)
        myAnswerThreshold = myDeviation * 3
        lowerLimit = myAverage - myAnswerThreshold
        upperLimit = myAverage + myAnswerThreshold
        answers = []
        for y in arr:
            if (y>=upperLimit or y>=myGeneralUpperLimit):
                answers.append(1)
            else:
                answers.append(0)
        myChoices.append(answers)

    #qtd = utils.count_total(myChoices)
    #utils.totalPrice(qtd,productsList,priceList)
    qt=[]
    for row in myChoices:
        row_qt = sum(row)
        qt.append(row_qt)
    
    return qt

def scanFront(cap):
    reader = easyocr.Reader(['en'])
    img = scanImage(cap)
    img = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
    img = cv2.resize(img,(400,800))
    img = img[90:img.shape[0]-100, 0:img.shape[1]]
    imgGray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    result = reader.readtext(imgGray,detail=0)
    raw_text=""
    for line in result:
        raw_text = raw_text+" "+line

    prices = re.findall("\d+[,.]\d+", raw_text)
    meals=[]
    for price in prices:
        meals.append(price)
    cv2.destroyAllWindows()
    return meals
        

