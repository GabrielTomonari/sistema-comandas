import sqlite3
from sqlite3 import Error
import tkinter as tk
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import tkinter.messagebox as tkmsgbox
import editProductDialog
import addProductDialog

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def callback(sv,tree):
    if sv.get() == "":
        View(tree)
    else:
        search_records(sv.get(),tree)

def View(tree):
    tree.delete(*tree.get_children())
    conn = create_connection("database/products.sql")
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()

def search_records(search_entry, tree):
	lookup_record = search_entry
	
	# Clear the Treeview
	for record in tree.get_children():
		tree.delete(record)
	
	conn = create_connection("database/products.sql")
	c = conn.cursor()

	c.execute("SELECT rowid, * FROM products WHERE UPPER(name) LIKE ? OR codes LIKE ?", ("%"+lookup_record.upper()+"%","%"+lookup_record.upper()+"%"))
	records = c.fetchall()
	
	global count
	count = 0

	for record in records:
		if count % 2 == 0:
			tree.insert(parent='', index='end', iid=count, text='', values=(record[1],record[2],record[3],record[4]), tags=('evenrow',))
		else:
			tree.insert(parent='', index='end', iid=count, text='',values=(record[1],record[2],record[3],record[4]), tags=('oddrow',))
		
		count += 1

	conn.commit()
	conn.close()

def deleteProduct(tree):
    curItem = tree.focus()
    id = tree.item(curItem)['values'][0]
    conn = create_connection("database\products.sql")
    sql = 'DELETE FROM products WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    tkmsgbox.showinfo(title="Produto excluído",message="Produto excluído")
    conn.commit()
    conn.close()
    View(tree)

def showEditProductDialog(window,tree):
    try:
        curItem = tree.focus()
        values = tree.item(curItem)['values']
        editProductDialog.main(window,values[0],values[1],values[2],values[3])
    except:
        tkmsgbox.showwarning(title="Atenção",message="Selecione um produto para editá-lo")


def open(mainWindow):
    # Window Geometry and Basic Settings
    window = tk.Toplevel(mainWindow)
    window.grab_set()
    windowWidth = window.winfo_screenwidth()
    windowHeight = window.winfo_screenheight()
    window.state('zoomed')
    window.title("Gerenciar Produtos")
    window.geometry(str(windowWidth)+"x"+str(windowHeight))

    # Background Image
    img = Image.open("img/gerenciarProdutosBG.png")
    img = img.resize((windowWidth,windowHeight), Image.ANTIALIAS)   
    bg =  ImageTk.PhotoImage(img)
    bgLabel = tk.Label(window, image=bg)
    bgLabel.place(x=-2, y=-2)

    # Widgets
    sv = tk.StringVar()
    searchBox = tk.Entry(window,font=("Roboto",int(windowHeight*0.025)), textvariable=sv)
    tree= ttk.Treeview(window, column=("id","codes", "name", "price"), show='headings',selectmode=tk.BROWSE)
    sv.trace("w", lambda name, index, mode, sv=sv: callback(sv,tree))
    tree.heading("#1", text="ID")
    tree.column("#1", stretch=tk.NO,width=50, anchor="center")
    tree.heading("#2", text="Códigos")
    tree.heading("#3", text="Nome")
    tree.heading("#4", text="Preço")
    tree.column("#4", stretch=tk.NO,width=100, anchor="center")
    ## Edit button
    editIcon = tk.PhotoImage(file='img/buttons/edit.png')
    editIcon = editIcon.subsample(15,15)
    editButton = tk.Button(window,text="     Editar produto",image=editIcon, compound=tk.LEFT,command=lambda:showEditProductDialog(window,tree))
    ## New button
    newIcon = tk.PhotoImage(file='img/buttons/new.png')
    newIcon = newIcon.subsample(15,15)
    newButton = tk.Button(window,text="     Adicionar produto",image=newIcon, compound=tk.LEFT,command=lambda:addProductDialog.main(window,""))
    ## Delete button
    deleteIcon = tk.PhotoImage(file='img/buttons/delete.png')
    deleteIcon = deleteIcon.subsample(15,15)
    deleteButton = tk.Button(window,text="     Excluir produto",image=deleteIcon, compound=tk.LEFT,command=lambda:deleteProduct(tree))

    # Layout placing
    searchBox.place(anchor=tk.NW,relwidth=0.8,relheight=0.05,rely=0.08,relx=0.015)
    tree.place(anchor=tk.NW,relwidth=0.8,relheight=0.83,rely=0.15,relx=0.015)
    editButton.place(anchor=tk.NW,relwidth=0.15,relheight=0.05,rely=0.15,relx=0.83)
    newButton.place(anchor=tk.NW,relwidth=0.15,relheight=0.05,rely=0.225,relx=0.83)
    deleteButton.place(anchor=tk.NW,relwidth=0.15,relheight=0.05,rely=0.3,relx=0.83)

    View(tree)

    window.mainloop()


if __name__ == '__main__':
    open()

