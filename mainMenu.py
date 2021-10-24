# Import packages
import tkinter as tk
import makeSale
import manageProducts


def main():

    # Window Geometry and Basic Settings
    windowHeight = 544
    windowWidth = 933
    window = tk.Tk()
    window.title("Sistema de Comandas - Chapéu de Sol")
    window.geometry(str(windowWidth)+"x"+str(windowHeight))

    # Background Image
    bg = tk.PhotoImage(file="img/mainMenuBG.png")
    label1 = tk.Label(window, image=bg)
    label1.place(x=-2, y=-1)

    # Buttons
    bt1 = tk.PhotoImage(file="img/buttons/realizarVendasBT.png")
    button1 = tk.Button(window, image = bt1,command=lambda : navigateNewWindow(window,makeSale))
    #button1.pack(side=tk.LEFT,padx=10)
    button1.place(relx=0.15, rely=0.5, anchor=tk.CENTER)

    bt2 = tk.PhotoImage(file="img/buttons/gerenciarProdutosBT.png")
    button2 = tk.Button(window, text = 'Click Me !', image = bt2,command=lambda : navigateNewWindow(window,manageProducts))
    #button2.pack(side=tk.LEFT,padx=10)
    button2.place(relx=0.38, rely=0.5, anchor=tk.CENTER)

    bt3 = tk.PhotoImage(file="img/buttons/elogiosEReclamacoesBT.png")
    button3 = tk.Button(window, text = 'Click Me !', image = bt3)
    #button3.pack(side=tk.LEFT,padx=10)
    button3.place(relx=0.61, rely=0.5, anchor=tk.CENTER)

    bt4 = tk.PhotoImage(file="img/buttons/fecharCaixaBT.png")
    button4 = tk.Button(window, text = 'Click Me !', image = bt4)
    #button4.pack(side=tk.LEFT,padx=10)
    button4.place(relx=0.84, rely=0.5, anchor=tk.CENTER)

    window.mainloop()

def navigateNewWindow(currentWindow,newWindowFile):
    newWindowFile.open(currentWindow)

main()
