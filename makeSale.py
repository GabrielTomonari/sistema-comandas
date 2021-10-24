# Import packages
import tkinter as tk
from tkinter.constants import SINGLE
import omr
from PIL import Image
from PIL import ImageTk

meals = []
qt = []

def scan():
    global meals
    global qt
    meals, qt = omr.scanTicket()

def insertItems(listbox):
    global meals
    global qt
    for meal in meals:
        listbox.insert(tk.END, meal)
    for item in qt:
        listbox.insert(tk.END, item)
    meals=[]
    qt=[]

def removeItem(listbox):
    selectedIndex = listbox.curselection()
    if(selectedIndex):
        listbox.delete(selectedIndex[0])

def removeAllItems(listbox):
    size = listbox.size()
    if(size):
        listbox.delete(0,size)

def open(mainWindow):
    # Window Geometry and Basic Settings
    window = tk.Toplevel(mainWindow)
    window.grab_set()
    windowWidth = window.winfo_screenwidth()
    windowHeight = window.winfo_screenheight()
    
    #window.resizable(width=False, height=False)
    window.state('zoomed')
    window.title("Realizar Vendas")
    window.geometry(str(windowWidth)+"x"+str(windowHeight))
    window.grid_columnconfigure((1,3,5), weight=1)

    # Background Image
    img = Image.open("img/realizarVendasBG.png")
    img = img.resize((windowWidth,windowHeight), Image.ANTIALIAS)   
    bg =  ImageTk.PhotoImage(img)
    bgLabel = tk.Label(window, image=bg)
    bgLabel.place(x=-2, y=-2)

    # Widgets
    productsListLabel = tk.Label(window,text="Produtos na comanda",font=("Roboto Bold",int(windowHeight*0.02)))
    listbox = tk.Listbox(window,selectmode=SINGLE,font=("Roboto",int(windowHeight*0.02)))
    removeProduct = tk.Button(window, text="Excluir item selecionado",command=lambda:removeItem(listbox))
    removeAll = tk.Button(window, text="Excluir tudo",command=lambda:removeAllItems(listbox))

    # Layout placing
    productsListLabel.place(anchor=tk.NW,rely=0.1,relx=0.015)
    listbox.place(anchor=tk.NW,relwidth=0.8,relheight=0.75,rely=0.15,relx=0.015)
    removeProduct.place(anchor=tk.NW,rely=0.91,relx=0.015)
    removeAll.place(anchor=tk.NW,rely=0.91,relx=0.1)

    # Functions
    def addScannedItems(event=None):
        scan()
        insertItems(listbox)

    # Keybinds
    window.bind('<space>', addScannedItems)
    window.bind('<Delete>', lambda event:removeItem(listbox))

    

    window.mainloop()

if __name__ == '__main__':
    open()