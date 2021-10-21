import cv2
import tkinter as tk
import tkinter.messagebox as tkmsgbox

def scanImage():
    cap = cv2.VideoCapture(1)
    scanned=False
    while(scanned==False):
        ret, frame = cap.read()
        if frame is not None:
            img = frame
        else: 
            errorMessage()
            break

def errorMessage():
    tkmsgbox.showinfo("Erro", "Erro: Câmera não detectada")

scanImage()