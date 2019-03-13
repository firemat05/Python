import tkinter as tk
import ttk
import sqlite3

items = ("Americano","Mocha","Green Tea","Raspberry","Cookie")
# type, price
itemsDict = {"Americano":[1,2.0],"Mocha":[1,3.5],"Green Tea":[2,1.25],"Raspberry":[4,3.25],
             "Cookie":[5,1.15]}
typeDict = {1:"Coffee",2:"Tea",3:"Cold Drink",4:"Smoothie",5:"Food Item"}
typeDictRev = {"Coffee":1,"Tea":2,"Cold Drink":3,"Smoothie":4,"Food Item":5}


def update():
    tree.delete(*tree.get_children())
    cursor.execute("select * from Product")
    for product in products:
        prodType = typeDict[product[3]]
        tree.insert("",tk.END,text=product[1],values=(product[2],prodType,product[0]))

def changeDropdown(event):
    typeOfItem = itemsDict[nameVar.get()][0]
    typeVar.set(typeDict[typeOfItem])
    priceVar.set(itemsDict[nameVar.get()][1])

#def query(sql,data):
#    with sq

def insertProductData():
    record = (nameVar.get(),priceVar.get(),typeDictRev[typeVar.get()])
    sql = "insert into Product (Name,Price,ProductTypeID) values (?,?,?)"
    cursor.execute(sql,record)
    db.commit()

root = tk.Tk()
root.title("SQLite GUI")

### tk variables ##
nameVar = tk.StringVar()
typeVar = tk.StringVar()
priceVar = tk.DoubleVar()

mainframe = ttk.Frame(root)
mainframe.grid(row=0,column=0)

ttk.Label(mainframe,text="SQLite GUI",font=("Ariel 14")).grid(row=0,column=0,pady=10,sticky='w')
ttk.Button(mainframe,text="Update",command=update).grid(row=1,column=0,pady=(0,5))

treeColumns = ("Price","Type","ID")
tree = ttk.Treeview(mainframe)
tree.grid(row=2,column=0,columnspan=4)
tree["columns"] = treeColumns
for treeColumn in treeColumns:
    tree.column(treeColumn,width=100)
    tree.heading(treeColumn,text=treeColumn)

ttk.Label(mainframe,text="New Entry:",font=("Ariel 12")).grid(row=3,column=0,pady=10,sticky='w')
ttk.Label(mainframe,text="Name:",font=("Ariel 10")).grid(row=4,column=0,sticky='w')
dropdown = ttk.Combobox(mainframe,textvariable=nameVar,values=items)
dropdown.grid(row=4,column=1)
dropdown.bind('<<ComboboxSelected>>',changeDropdown)

ttk.Label(mainframe,text="Type:",font=("Ariel 10")).grid(row=5,column=0,sticky='w')
ttk.Entry(mainframe,textvariable=typeVar).grid(row=5,column=1)
ttk.Label(mainframe,text="Price:",font=("Ariel 10")).grid(row=6,column=0,sticky='w')
ttk.Entry(mainframe,textvariable=priceVar).grid(row=6,column=1)
ttk.Button(mainframe,text="Submit",command=insertProductData).grid(row=7,column=0)

with sqlite3.connect(r'D:\Documents\sqlite\pythonsqlite2.db') as db:
    cursor = db.cursor()
    cursor.execute("select * from Product")
    products = cursor.fetchall()
    for product in products:
        prodType = typeDict[product[3]]
        tree.insert("",tk.END,text=product[1],values=(product[2],prodType,product[0]))

root.mainloop()
