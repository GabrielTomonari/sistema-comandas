import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmsgbox
import sqlite3
from sqlite3 import Error

def closeWindow(window):
        window.grab_release()
        window.destroy()

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def addProduct(code,name,price,window):
    value = price.replace(",",".")
    try:
        value = float(value)
        if not name or not value or not code:
            tkmsgbox.showerror(title="Erro",message="Preencha o código, o nome e o preço")
        else:
            conn = create_connection("database\products.sql")
            sql = '''INSERT INTO products (codes, name, price)
            VALUES(?,?,?)'''
            cur = conn.cursor()
            cur.execute(sql, (code,name,value))
            tkmsgbox.showinfo(title="Produto adicionado",message="Produto adicionado")
            conn.commit()
            conn.close()
            closeWindow(window)
    except ValueError:
        tkmsgbox.showerror(title="Erro",message="Insira um número válido no preço")
        
def main(main_window, code):
    addDialog = tk.Toplevel(main_window)
    addDialog.title("Adicionar Produto")
    addDialog.resizable(0, 0)
    addDialog.grab_set()


    # Widgets
    codeLabel = tk.Label(addDialog,text="Código do produto")
    codeBox = tk.Entry(addDialog, width = 50)
    codeBox.insert(0,code)
    nameLabel = tk.Label(addDialog,text="Nome do produto")
    nameBox = tk.Entry(addDialog, width = 50)
    priceLabel = tk.Label(addDialog,text="Preço do produto")
    priceBox = tk.Entry(addDialog, width = 50)
    cancelButton = tk.Button(addDialog,text="Cancelar",command=addDialog.destroy)
    saveButton = tk.Button(addDialog,text="Salvar",command=lambda:addProduct(codeBox.get(),nameBox.get(),priceBox.get(),addDialog))


    # Layout placing
    codeLabel.grid(row=0,column=0, padx=10, pady=10,sticky=tk.W)
    codeBox.grid(row=1,column=0,columnspan=2, padx= 10, pady=0)
    nameLabel.grid(row=2,column=0, padx=10, pady=10,sticky=tk.W)
    nameBox.grid(row=3,column=0,columnspan=2, padx= 10, pady=0)
    priceLabel.grid(row=4,column=0, padx=10, pady=10,sticky=tk.W)
    priceBox.grid(row=5,column=0,columnspan=2, padx= 10, pady=0)
    cancelButton.grid(row=6,column=0, padx= 10, pady=10)
    saveButton.grid(row=6,column=1, padx= 10, pady=10)

    addDialog.mainloop()


