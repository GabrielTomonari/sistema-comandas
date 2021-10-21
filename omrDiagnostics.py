# Import modules
import cv2
import numpy as np
from numpy.core.fromnumeric import std
from numpy.lib.function_base import average
import utils
from pyzbar import pyzbar
import beepy
import tkinter.messagebox as tkmsgbox

count = 0
products = 25
choices = 10
timer = 0
lastDetected = False
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
cap = cv2.VideoCapture(0)
imgHeight = 1920
imgWidth = 1080

while(1):
    ret, frame = cap.read()
    if frame is not None:
        img = frame
    else: img = cv2.imread("comanda2.jpg")
    img = cv2.resize(img, (imgHeight, imgWidth))
    #img = utils.increase_brightness(img,40)
    #img = utils.increase_contrast(img)
    imgRotated = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
    # CREATE A BLANK IMAGE FOR TESTING DEBUGING IF REQUIRED
    imgBlank = np.zeros((imgWidth, imgHeight, 3), np.uint8)
    # CONVERT IMAGE TO GRAY SCALE
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (79, 79), 3)  # ADD GAUSSIAN BLUR
    high_thresh, thresh_im = cv2.threshold(imgBlur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    lowThresh = 0.5*high_thresh
    imgThreshold = cv2.Canny(imgBlur, lowThresh, high_thresh)  # APPLY CANNY BLUR
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgThreshold, kernel, iterations=2)  # APPLY DILATION
    imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # APPLY EROSION

    # FIND ALL COUNTOURS
    imgContours = img.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
    imgBigContour = img.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
    contours, hierarchy = cv2.findContours(
        imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # FIND ALL CONTOURS
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0),
                    10)  # DRAW ALL DETECTED CONTOURS

    # FIND THE BIGGEST COUNTOUR
    biggest, maxArea = utils.biggestContour(
        contours)  # FIND THE BIGGEST CONTOUR
    if biggest.size != 0:
            if lastDetected == True and maxArea > 400000:
                timer+=1
                #print("Detectando bordas"+timer*"-")
            else:
                timer=0
            biggest = utils.reorder(biggest)
            # DRAW THE BIGGEST CONTOUR
            cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20)
            imgBigContour = utils.drawRectangle(imgBigContour, biggest, 2)
            pts1 = np.float32(biggest)  # PREPARE POINTS FOR WARP
            # PREPARE POINTS FOR WARP
            pts2 = np.float32([[0, 0], [imgHeight, 0], [0, imgWidth], [imgHeight, imgWidth]])
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            imgWarpColored = cv2.warpPerspective(img, matrix, (imgHeight, imgWidth))
            imgWarpColoredRotated = cv2.rotate(imgWarpColored,cv2.ROTATE_90_CLOCKWISE)

            # REMOVE 20 PIXELS FORM EACH SIDE
            imgWarpColored = imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
            imgWarpColored = cv2.resize(imgWarpColored, (imgHeight, imgWidth))
            boxesCountoursList = [[210,30],[210,590],[1670,590],[1670,30]]
            ctr = np.array(boxesCountoursList).reshape((-1,1,2)).astype(np.int32)
            cv2.drawContours(imgWarpColored,[ctr],-1,(0,255,0),2)

            boxesArea = imgWarpColored.copy()
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
                
            #
            #print("-----------------------")
            myChoices=[]
            myGeneralAverge = average(myPixelVal)
            myGeneralDeviation = std(myPixelVal)
            myGeneralAnswerThreshold = myGeneralDeviation*2
            myGeneralUpperLimit = myGeneralAverge+myGeneralAnswerThreshold
            #print("General Average:"+str(myGeneralAverge))
            #print("General Deviation:"+str(myGeneralDeviation))

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
            

            imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
            imgAdaptiveThre = cv2.adaptiveThreshold(imgWarpGray,255, 1, 1, 11, 2)
            imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
            imgAdaptiveThre = cv2.medianBlur(imgAdaptiveThre, 3)

            #cv2.imshow("Tresh", boxesAreaTreshRotated)
            # Image Array for Display
            lastDetected = True
            imageArray = ([img, imgGray, imgThreshold, imgContours],
                        [imgBigContour, imgWarpColored, imgWarpGray, imgAdaptiveThre],[boxesArea,boxesAreaTresh,imgBlur,imgBlank])

            imgWarpColoredRotated = utils.show_choices(imgWarpColoredRotated,myChoices)
            cv2.imshow("Scan", imgWarpColoredRotated)

    else:
            lastDetected = False
            timer=0
            imageArray = ([img, imgGray, imgThreshold, imgContours],
                       [imgBlank, imgBlank, imgBlank, imgBlank])

        # LABELS FOR DISPLAY
    # lables = [["Original", "Gray", "Threshold", "Contours", "Biggest Contour",
    #             "Warp Prespective", "Warp Gray", "Adaptive Threshold"]]

    stackedImage = utils.stackImages(imageArray, 1)
    imgBigContour = cv2.rotate(imgBigContour,cv2.ROTATE_90_COUNTERCLOCKWISE)

    cv2.imshow("Result", imgRotated)
    if (timer>=7):
        print('\a')
        #print (np.matrix(myChoices))
        cv2.destroyAllWindows()
        imgWarpColoredRotated = utils.show_choices(imgWarpColoredRotated,myChoices)
        cv2.imshow("Scan", imgWarpColoredRotated)
        #beepy.beep(sound="ping")
        qtd = utils.count_total(myChoices)
        utils.totalPrice(qtd,productsList,priceList)
        break


    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.waitKey(0)

