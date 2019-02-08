from tkinter import *
import ttk
from tkinter import messagebox
from tkcalendar import Calendar,DateEntry
import pandas as pd
import os
import datetime
from time import strftime

curFolder = os.path.dirname(__file__)
database = os.path.join(curFolder,'worklog.csv')

def updateSelected():
    def acceptUpdate():
        for item in tree.selection():
            tree.item(item,text=titleVar.get(),values=(custVar.get(),dueVar.get(),rfiVar.get(),compVar.get(),
                                                       prodVar.get(),hrsVar.get(),noteVar.get()))
        updateMenu.destroy()

    for item in tree.selection():
        titleVar.set(tree.item(item,"text"))
        custVar.set(tree.item(item,"values")[0])
        dueVar.set(tree.item(item,"values")[1])
        rfiVar.set(tree.item(item,"values")[2])
        compVar.set(tree.item(item,"values")[3])
        prodVar.set(tree.item(item,"values")[4])
        hrsVar.set(tree.item(item,"values")[5])
        noteVar.set(tree.item(item,"values")[6])
    updateMenu = Toplevel(root,padx=5,pady=5,bg='#f2fbff')
    ttk.Label(updateMenu,text="Update Field",font=("Helvetica 12"),style='BG.TLabel').grid(row=0,column=0,pady=10)
    row = 1
    for entry in entryList:
        ttk.Label(updateMenu,text=entry[0]+':',font=("Helvetica 12"),style='BG.TLabel').grid(row=row,column=0,sticky=W,pady=2)
        ttk.Entry(updateMenu,textvariable=entry[1]).grid(row=row,column=1,sticky=E,pady=2)
        row += 1
    ttk.Button(updateMenu,text="Select Date",command=selectDueDate,style='blue.TButton').grid(row=3,column=2)
    ttk.Button(updateMenu,text="Select Date",command=selectCompDate,style='blue.TButton').grid(row=5,column=2)
    ttk.Button(updateMenu,text="Accept",command=acceptUpdate,style='green.TButton').grid(row=row,column=0)
    ttk.Button(updateMenu,text="Cancel",command=updateMenu.destroy,style='red.TButton').grid(row=row,column=1)

def clearFields():
    titleVar.set('')
    custVar.set('')
    dueVar.set('')
    rfiVar.set('')
    compVar.set('')
    prodVar.set('')
    hrsVar.set('')
    noteVar.set('')

def deleteSelected():
    tree.delete(tree.selection())

def viewSelected():
    pass

# dueVar
def selectDueDate():
    def getDueDate():
        dueVar.set(dueCal.selection_get())
        dueMenu.destroy()

    dueMenu = Toplevel(root)
    dueCal = Calendar(dueMenu,font="Ariel 14",selectmode='day',cursor='hand1')
    dueCal.grid(row=0,column=0)
    ttk.Button(dueMenu,text="OK",command=getDueDate,style='blue.TButton').grid(row=1,column=0)

# compVar
def selectCompDate():
    def getCompDate():
        compVar.set(compCal.selection_get())
        compMenu.destroy()
        
    compMenu = Toplevel(root)
    compCal = Calendar(compMenu,font="Ariel 14",selectmode='day',cursor='hand1')
    compCal.grid(row=0,column=0)
    ttk.Button(compMenu,text="OK",command=getCompDate,style='blue.TButton').grid(row=1,column=0)

def save():
    dataDict = {}
    titleList = []
    custList = []
    dueList = []
    rfiList = []
    compList = []
    prodList = []
    hrsList = []
    noteList = []
    for child in tree.get_children():
        titleList.append(tree.item(child,'text'))
        custList.append(tree.item(child,'values')[0])
        dueList.append(tree.item(child,'values')[1])
        rfiList.append(tree.item(child,'values')[2])
        compList.append(tree.item(child,'values')[3])
        prodList.append(tree.item(child,'values')[4])
        hrsList.append(tree.item(child,'values')[5])
        noteList.append(tree.item(child,'values')[6])
    dataDict['Title'] = titleList
    dataDict['Customer'] = custList
    dataDict['Due Date'] = dueList
    dataDict['RFI Number'] = rfiList
    dataDict['Completion Date'] = compList
    dataDict['No. Products'] = prodList
    dataDict['Hours Worked'] = hrsList
    dataDict['Notes'] = noteList
    df = pd.DataFrame.from_dict(dataDict)
    df = df[["Title","Customer","Due Date","RFI Number","Completion Date","No. Products","Hours Worked","Notes"]]
    df.to_csv(database,sep=',',encoding='utf-8')

def startup():
    if not os.path.exists(database):
        df = pd.DataFrame(columns=['Unnamed: 0',"Title","Customer","Due Date","RFI Number","Completion Date","No. Products","Hours Worked","Notes"])
        df.to_csv(database,sep=',',encoding='utf-8')
    df = pd.read_csv(database)
    for index, row in df.iterrows():
        tree.insert("",0,text=row[1],values=(row[2],row[3],row[4],row[5],row[6],row[7],row[8]))

def submitNew():
    tree.insert("",0,text=titleVar.get(),values=(custVar.get(),dueVar.get(),rfiVar.get(),compVar.get(),prodVar.get(),hrsVar.get(),noteVar.get()))

root = Tk()
root.title("Work Log")

# Styles
s = ttk.Style(root)
s.theme_use('clam')
s.configure('BG.TFrame',background='#f2fbff')
s.configure('BG.TLabel',background='#f2fbff')
s.configure('green.TButton',background='#e0ffe3')
s.configure('red.TButton',background='#ff7c7c')
s.configure('blue.TButton',background='#8eb2ed')

# Tk Variables
titleVar = StringVar()
custVar = StringVar()
dueVar = StringVar()
rfiVar = StringVar()
compVar = StringVar()
prodVar = IntVar()
hrsVar = IntVar()
noteVar = StringVar()

mainframe = ttk.Frame(root,style='BG.TFrame')
mainframe.grid(row=0,column=0)

ttk.Label(mainframe,text="Work Log",font=("Helvetica 14"),style='BG.TLabel').grid(row=0,column=0,columnspan=2,pady=10)

entryList = [["Title",titleVar],["Customer",custVar],["Due Date",dueVar],["RFI Number",rfiVar],["Completion Date",compVar],
             ["No. Products",prodVar],["Hours Worked",hrsVar],["Notes",noteVar]]
column = 0
for entry in entryList:
    ttk.Label(mainframe,text=entry[0]+':',style='BG.TLabel').grid(row=1,column=column)
    ttk.Entry(mainframe,textvariable=entry[1]).grid(row=2,column=column)
    column += 1

ttk.Button(mainframe,text="Submit New",command=submitNew,style='green.TButton').grid(row=3,column=0,pady=5,padx=2)
ttk.Button(mainframe,text="Select Date",command=selectDueDate,style='blue.TButton').grid(row=3,column=2,pady=5,padx=2)
ttk.Button(mainframe,text="Select Date",command=selectCompDate,style='blue.TButton').grid(row=3,column=4,pady=5,padx=2)
ttk.Button(mainframe,text="Clear Fields",command=clearFields,style='blue.TButton').grid(row=3,column=7,pady=5,padx=2)

treeHeaders = ("Customer","Due Date","RFI Number","Completion Date","No. Products","Hours Worked","Notes")
tree = ttk.Treeview(mainframe)
tree.grid(row=4,column=0,columnspan=8)
tree["columns"]=treeHeaders
for header in treeHeaders:
    tree.column(header,width=100)
    tree.heading(header,text=header)

ttk.Button(mainframe,text="Save",command=save,style='green.TButton').grid(row=5,column=0,pady=5,padx=2)
ttk.Button(mainframe,text="Update Selected",command=updateSelected,style='blue.TButton').grid(row=5,column=2,pady=5,padx=2)
ttk.Button(mainframe,text="Delete Selected",command=deleteSelected,style='red.TButton').grid(row=5,column=3,pady=5,padx=2)
ttk.Button(mainframe,text="View Selected",command=viewSelected,style='blue.TButton').grid(row=5,column=4,pady=5,padx=2)
ttk.Button(mainframe,text="Close",command=root.destroy,style='blue.TButton').grid(row=5,column=7,pady=5,padx=2)

startup()
root.mainloop()
