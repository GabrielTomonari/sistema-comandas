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

def updateProduct(id,name,price,window):
    value = price.replace(",",".")
    try:
        value = float(value)
        if not name or not value:
            tkmsgbox.showerror(title="Erro",message="Preencha o nome e o preço")
        else:
            conn = create_connection("database\products.sql")
            sql = 'UPDATE products SET name=?, price=? WHERE id=?'
            cur = conn.cursor()
            cur.execute(sql, (name,value,id,))
            tkmsgbox.showinfo(title="Produto editado",message="Produto editado")
            conn.commit()
            conn.close()
            closeWindow(window)
    except ValueError:
        tkmsgbox.showerror(title="Erro",message="Insira um número válido no preço")
        
def main(main_window, id, codes, name, price):
    editDialog = tk.Toplevel(main_window)
    editDialog.title("Editar Produto")
    editDialog.resizable(0, 0)
    editDialog.grab_set()


    # Widgets
    nameLabel = tk.Label(editDialog,text="Nome do produto")
    nameBox = tk.Entry(editDialog, width = 50)
    nameBox.insert(0,name)
    priceLabel = tk.Label(editDialog,text="Preço do produto")
    priceBox = tk.Entry(editDialog, width = 50)
    priceBox.insert(0,price)
    cancelButton = tk.Button(editDialog,text="Cancelar",command=editDialog.destroy)
    saveButton = tk.Button(editDialog,text="Salvar",command=lambda:updateProduct(id,nameBox.get(),priceBox.get(),editDialog))


    # Layout placing
    nameLabel.grid(row=0,column=0, padx=10, pady=10,sticky=tk.W)
    nameBox.grid(row=1,column=0,columnspan=2, padx= 10, pady=0)
    priceLabel.grid(row=2,column=0, padx=10, pady=10,sticky=tk.W)
    priceBox.grid(row=3,column=0,columnspan=2, padx= 10, pady=0)
    cancelButton.grid(row=4,column=0, padx= 10, pady=10)
    saveButton.grid(row=4,column=1, padx= 10, pady=10)

    editDialog.mainloop()


