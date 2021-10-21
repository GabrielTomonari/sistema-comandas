# Import packages
import tkinter as tk

def open():
    # Window Geometry and Basic Settings
    windowHeight = 544
    windowWidth = 933
    window = tk.Tk()
    window.title("Realizar Vendas")
    window.geometry(str(windowWidth)+"x"+str(windowHeight))

    # Background Image
    bg = tk.PhotoImage(file="img/realizarVendasBG.png")
    label1 = tk.Label(window, image=bg)
    label1.place(x=-2, y=-1)

    window.mainloop()

#open()