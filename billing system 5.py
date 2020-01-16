from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql

window=Tk()
window.geometry("1050x600")
window.title("billing")
#=================================field listner===================================
def quantityFIeldListner(a,b,c):
    global quantityVar
    global costVar
    global itemRate
    quantity=quantityVar.get()
    if quantity !="":
        try:
            quantity=float(quantity)
            cost=quantity*itemRate
            quantityVar.set("%.2f"%quantity)
            costVar.set("%.2f"%cost)
        except ValueError:
            quantity=quantity[:-1]
            quantityVar.set(quantity)
    else:
        quantity=0
        quantityVar.set("%.2f"%quantity)

def costFieldListner(a,b,c):
    global quantityVar
    global costVar
    global itemRate
    cost=costVar.get()
    if cost !="":
        try:
            cost=float(cost)
            quantity=cost/itemRate
            quantityVar.set("%.2f"%quantity)
            costVar.set("%.2f"%cost)
        except ValueError:
            cost=cost[:-1]
            costVar.set(cost)
    else:
        cost=0
        costVar.set(cost)
    
            
#============================global bariable for entrys=======================
#==========================login variables================================
usernameVar=StringVar()
passwordVar=StringVar()
#===============================main window variables=====================================
rateDict={}
options=[]
itemVariable=StringVar()
quantityVar=StringVar()
quantityVar.trace('w',quantityFIeldListner)
itemRate=2
rateVar=StringVar()
rateVar.set("%.2f"%itemRate)
costVar=StringVar()
costVar.trace('w',costFieldListner)

#===============================add item variables==========================
StoreOption=['Frozen','Fresh']
addItemNameVar=StringVar()
addItemRateVar=StringVar()
addItemTypeVar=StringVar()
storedTypeVar=StringVar()
storedTypeVar.set(StoreOption[0])
itemList=list()
totalCost=0
totalCostVar=StringVar()
totalCostVar.set("Total Cost ={}".format(totalCost))
updateItemId=""
#=======================function for generate bill==============
def generate_bill():
    global itemVariable
    global quantityVar
    global itemRate
    global costVar
    global itemList
    global totalCost
    global totalCostVar
    itemName=itemVariable.get()
    quantity=quantityVar.get()
    cost=costVar.get()
    conn=pymysql.connect(host="localhost",user="root",password="",database="billservice")
    cursor=conn.cursor()
    query="insert into bill(name,quantity,rate,cost)values('{}','{}','{}','{}')".format(itemName,quantity,itemRate,cost)
    cursor.execute(query)
    conn.commit()
    conn.close()
    listDict={"name":itemName,"rate":itemRate,"quantity":quantity,"cost":cost}
    itemList.append(listDict)
    totalCost+=float(cost)
    quantityVar.set("0")
    costVar.set("0")
    updateListView()
    totalCostVar.set("Total Cost ={}".format(totalCost))
#=====================update triview=================
def OnDoubleClick(event):
    global addItemNameVar
    global addItemRateVar
    global addItemTypeVar
    global storedTypeVar
    global updateItemId
    item=updateTV.selection()
    updateItemId=updateTV.item(item,"text")
    item_detail=updateTV.item(item,"values")
    item_index=StoreOption.index(item_detail[3])
    addItemTypeVar.set(item_detail[2])
    addItemRateVar.set(item_detail[1])
    addItemNameVar.set(item_detail[0])
    storedTypeVar.set(StoreOption[item_index])
def updateListView():
    record=billsTV.get_children()
    for element in record:
        billsTV.delete(element)
    for row in itemList:
        billsTV.insert('','end',text=row['name'],value=(row["rate"],row["quantity"],row["cost"]))

def getItemList():
    record=updateTV.get_children()
    for element in record:
        updateTV.delete(element)
    conn=pymysql.connect(host="localhost",user="root",password="",database="billservice")
    cursor=conn.cursor(pymysql.cursors.DictCursor)
    query="select * from itemlist"
    cursor.execute(query)
    data=cursor.fetchall()
    for row in data:
        updateTV.insert('','end',text=row['nameid'],values=(row['name'],row['rate'],row['type'],row['storetype']))
    updateTV.bind("<Double-l>",OnDoubleClick)
    conn.close()
        

def print_bill():
    global itemList
    global totalCost
    print("=================================recept============================\n")
    print("===================================================================")
    print("{:<20}{:<10}{:<15}{:<10}".format("Name","Rate","Quantity","Cost"))
    print("====================================================================")
    for item in itemList:
        print("{:<20}{:<10}{:<15}{:<10}".format(item["name"],item["rate"],item["quantity"],item["cost"]))
    print("====================================================================")
    print("{:<20}{:<10}{:<15}{:<10}".format("TotalCost"," "," ",totalCost))

    itemList=[]
    totalCost=0.0
    updateListView()
    totalCostVar.set("Total Cost ={}".format(totalCost))
    
#=============================function for logout=============
def logout():
    remove_all_widgets()
    loginWindow()

def gotoupdateitem():
    remove_all_widgets()
    updateitemwindow()

#==================================function to read from list of item==========
def movetoBills():
    remove_all_widgets()
    viewAllBills()
    
#=============================function to read data from list of item============
def readalldata():
    global options
    global rateDict
    global itemVariable
    global itemRate
    global rateVar
    options=[]
    rateDict={}
    conn=pymysql.connect(host="localhost",user="root",password="",database="billservice")
    cursor=conn.cursor(pymysql.cursors.DictCursor)

    query="select * from itemlist"
    cursor.execute(query)
    data=cursor.fetchall()
    #data=[item for t in data1 for item in t]
    count=0
    for i in data:
        count+=1
        options.append(i['nameid'])
        rateDict[i['nameid']]=i['rate']
        itemVariable.set(options[0])
        itemRate=int(rateDict[options[0]])
    conn.close()
    rateVar.set("%.2f"%itemRate)
    if count==0:
        remove_all_widgets()
        itemaddWindow()
    else:
        remove_all_widgets()
        mainwindow()

def  optionMenuListner(event):
    global itemVariable
    global rateDict
    global itemRate
    item=itemVariable.get()
    itemRate =int(rateDict[item])
    rateVar.set("%.2f"%itemRate)
    
#===================function to remove all widget======================
def remove_all_widgets():
    global window
    for widget in window.winfo_children():
        widget.destroy()

#===============================update all bill data=====================
def updateBillData():
    record=billsTV.get_children()
    for element in record:
        billsTV.delete(element)    
    conn=pymysql.connect(host="localhost",user="root",password="",database="billservice")
    cursor=conn.cursor(pymysql.cursors.DictCursor)
    query="select * from bill"
    cursor.execute(query)
    data=cursor.fetchall()
    for row in data:
        billsTV.insert('','end',text=row['name'],value=(row["rate"],row["quantity"],row["cost"]))
    conn.close()
#============function for call itemaddWindow=================
def addeventListner():
    remove_all_widgets()
    itemaddWindow()
#=============function for add new itom============================

def addItem():
    global addItemNameVar
    global addItemRateVar
    global addItemTypeVar
    global storedTypeVar
    name=addItemNameVar.get()
    rate=addItemRateVar.get()
    Type=addItemTypeVar.get()
    storeType=storedTypeVar.get()
    nameid=name.replace(" ","_")
    conn=pymysql.connect(host="localhost",user="root",password="",database="billservice")
    cursor=conn.cursor()
    query="insert into itemlist(name,nameid,rate,type,storetype)values('{}','{}','{}','{}','{}')".format(name,nameid,rate,Type,storeType)
    cursor.execute(query)
    conn.commit()
    conn.close()
    addItemNameVar.set("")
    addItemRateVar.set("")
    addItemTypeVar.set("")

def updateitem():
    global addItemNameVar
    global addItemRateVar
    global addItemTypeVar
    global storedTypeVar
    global updateItemId
    name=addItemNameVar.get()
    rate=addItemRateVar.get()
    Type=addItemTypeVar.get()
    storeType=storedTypeVar.get()
    conn=pymysql.connect(host="localhost",user="root",password="",database="billservice")
    cursor=conn.cursor()
    query="update itemlist set name='{}',rate='{}',type='{}',storetype='{}' where nameid='{}'".format(name,rate,Type,storeType,updateItemId) 
    cursor.execute(query)
    conn.commit()
    conn.close()

    addItemNameVar.set("")
    addItemRateVar.set("")
    addItemTypeVar.set("")
    getItemList()
    
#===================================================admin login function==================
def adminlogin():
    global usernameVar
    global passwordVar

    username=usernameVar.get()
    password=passwordVar.get()
    conn=pymysql.connect(host="localhost",user="root",password="",database="billservice")
    cursor=conn.cursor()
    query="select * from users"
    cursor.execute(query)
    data=cursor.fetchall()
    data1=[item for t in data for item in t]
    if data1[0]==username and data1[1]==password:
        usernameVar.set('')
        passwordVar.set('')
        readalldata()
        
    else:
        messagebox.showerror("invalid user","credentials enter are invalid")
        usernameVar.set('')
        passwordVar.set('')
    
    


def loginWindow():
    titleLabel=Label(window,text="Restorent Billing System",font="Arial 40",fg="green")
    titleLabel.grid(row=0,column=0,columnspan=4,padx=(40,0),pady=(10,0))

    loginLabel=Label(window,text="Admin Login",font="Arial 30")
    loginLabel.grid(row=1,column=2,padx=(50,0), columnspan=2,pady=10)

    usernameLabel=Label(window,text="Username")
    usernameLabel.grid(row=2,column=2)

    passwordlabel=Label(window,text="Password")
    passwordlabel.grid(row=3,column=2)

    usernameEntry=Entry(window,textvariable=usernameVar)
    usernameEntry.grid(row=2,column=3,padx=20,pady=5)

    passwordEntry=Entry(window,textvariable=passwordVar,show="*")
    passwordEntry.grid(row=3,column=3,padx=20,pady=5)

    loginButton=Button(window,text="login",width=20,height=2,command=lambda:adminlogin())
    loginButton.grid(row=4,column=2,columnspan=2,pady=5)

def mainwindow():
    global billsTV
    titleLabel=Label(window,text="Restorent Billing System",font="Arial 30",fg="green")
    titleLabel.grid(row=0,column=1,columnspan=3,padx=(40,0),pady=(10,0))

    addnewItem=Button(window,text="Add Item",width=15,height=2,command=lambda:addeventListner())
    addnewItem.grid(row=1,column=0,padx=(10,0),pady=(10,0))

    updateItem=Button(window,text="update Item",width=15,height=2,command=lambda:gotoupdateitem())
    updateItem.grid(row=1,column=1,padx=(10,0),pady=(10,0))

    showallEntry=Button(window,text="Show Entries",width=15,height=2,command=lambda:movetoBills())
    showallEntry.grid(row=1,column=2,padx=(10,0),pady=(10,0))
    
    logoutBtn=Button(window,text="Logout",width=15,height=2,command=lambda:logout())
    logoutBtn.grid(row=1,column=4,pady=(10,0))

    itemLabel=Label(window,text="Select Item")
    itemLabel.grid(row=2,column=0,padx=(5,0),pady=(10,0))

    itemDropDown=OptionMenu(window,itemVariable,*options,command=optionMenuListner)
    itemDropDown.grid(row=2,column=1,padx=(10,0),pady=(10,0))

    rateLabel=Label(window,text="Rate")
    rateLabel.grid(row=2,column=2,padx=(10,0),pady=(10,0))
    itemValue=Label(window,textvariable=rateVar)
    itemValue.grid(row=2,column=3,padx=(10,0),pady=(10,0))

    quantityLabel=Label(window,text="Quantity")
    quantityLabel.grid(row=3,column=0,padx=(5,0),pady=(10,0))
    quantityEntry=Entry(window,textvariable=quantityVar)
    quantityEntry.grid(row=3,column=1,padx=(5,0),pady=(10,0))

    costLabel=Label(window,text="Cost")
    costLabel.grid(row=3,column=2,padx=(10,0),pady=(10,0))
    costEntry=Entry(window,textvariable=costVar)
    costEntry.grid(row=3,column=3,padx=(10,0),pady=(10,0))

    buttonBill=Button(window,text="Gadd to list",width=15,command=lambda:generate_bill())
    buttonBill.grid(row=3,column=4,padx=(5,0),pady=(10,0))


    buttonBill=Button(window,text="Generate Bills",width=15,command=lambda:print_bill())
    buttonBill.grid(row=6,column=4)

    billLable=Label(window,text="Bills",font="Arial 25")
    billLable.grid(row=4,column=2)

    billsTV=ttk.Treeview(window,height=15,columns=("Rate","Quantity","Cost"))
    billsTV.grid(row=5,column=0,columnspan=5)
    scrollBar=Scrollbar(window,orient="vertical",command=billsTV.yview)
    scrollBar.grid(row=5,column=4,sticky="NSE")

    billsTV.configure(yscrollcommand=scrollBar.set)

    billsTV.heading('#0',text="Item Name")
    billsTV.heading('#1',text="Rate")
    billsTV.heading('#2',text="Quantity")
    billsTV.heading('#3',text="Cost")

    totalCostLabel=Label(window,textvariable=totalCostVar)
    totalCostLabel.grid(row=6,column=1)
    updateListView()
    
def itemaddWindow():
    backButton=Button(window,text="back",command=lambda:readalldata())
    backButton.grid(row=0,column=1)
    
    titleLabel=Label(window,text="Restorent Billing System",font="Arial 30",fg="green")
    titleLabel.grid(row=0,column=2,columnspan=4,padx=(200,0),pady=(10,0))

    itemNameLabel=Label(window,text="Name")
    itemNameLabel.grid(row=1,column=1,padx=(5,0),pady=(10,0))
    itemNameEntry=Entry(window,textvariable=addItemNameVar)
    itemNameEntry.grid(row=1,column=2,pady=(10,0)) 

    itemRateLabel=Label(window,text="Rate")
    itemRateLabel.grid(row=1,column=3,pady=(10,0))
    itemRateEntry=Entry(window,textvariable=addItemRateVar)
    itemRateEntry.grid(row=1,column=4,pady=(10,0))

    itemTypeLabel=Label(window,text="Type")
    itemTypeLabel.grid(row=2,column=1,pady=(10,0))
    itemTypeEntry=Entry(window,textvariable=addItemTypeVar)
    itemTypeEntry.grid(row=2,column=2,pady=(10,0))

    storedTypeLabel=Label(window,text="Stored Type")
    storedTypeLabel.grid(row=2,column=3,pady=(10,0))
    storedTypeEntry=OptionMenu(window,storedTypeVar,*StoreOption)
    storedTypeEntry.grid(row=2,column=4,pady=(10,0))

    addItemButton=Button(window,text="Add Item",width=20,height=2,command=lambda:addItem())
    addItemButton.grid(row=3,column=3,pady=(10,0))
def updateitemwindow():
    global updateTV
    backButton=Button(window,text="back",command=lambda:readalldata())
    backButton.grid(row=0,column=0)
    
    titleLabel=Label(window,text="Restorent Billing System",font="Arial 30",fg="green")
    titleLabel.grid(row=0,column=1,columnspan=4,padx=(200,0),pady=(10,0))

    itemNameLabel=Label(window,text="Name")
    itemNameLabel.grid(row=1,column=1,padx=(5,0),pady=(10,0))
    itemNameEntry=Entry(window,textvariable=addItemNameVar)
    itemNameEntry.grid(row=1,column=2,pady=(10,0)) 

    itemRateLabel=Label(window,text="Rate")
    itemRateLabel.grid(row=1,column=3,pady=(10,0))
    itemRateEntry=Entry(window,textvariable=addItemRateVar)
    itemRateEntry.grid(row=1,column=4,pady=(10,0))

    itemTypeLabel=Label(window,text="Type")
    itemTypeLabel.grid(row=2,column=1,pady=(10,0))
    itemTypeEntry=Entry(window,textvariable=addItemTypeVar)
    itemTypeEntry.grid(row=2,column=2,pady=(10,0))

    storedTypeLabel=Label(window,text="Stored Type")
    storedTypeLabel.grid(row=2,column=3,pady=(10,0))
    storedTypeEntry=OptionMenu(window,storedTypeVar,*StoreOption)
    storedTypeEntry.grid(row=2,column=4,pady=(10,0))


    addItemButton=Button(window,text="update item",width=20,height=2,command=lambda:updateitem())
    addItemButton.grid(row=3,column=3,pady=(10,0))

    updateTV=ttk.Treeview(window,height=15,columns=("Name","Rate","Type","Store_type"))
    updateTV.grid(row=4,column=1,columnspan=5)
    scrollBar=Scrollbar(window,orient="vertical",command=billsTV.yview)
    scrollBar.grid(row=4,column=5,sticky="NSE")
    updateTV.configure(yscrollcommand=scrollBar.set)

    updateTV.heading('#0',text="Item Id")
    updateTV.heading('#1',text="Item Name")
    updateTV.heading('#2',text="Rate")
    updateTV.heading('#3',text="Type")
    updateTV.heading('#4',text="Store Type")
    getItemList()

def viewAllBills():
    global billsTV
    backButton=Button(window,text="back",command=lambda:readalldata())
    backButton.grid(row=0,column=0)
    
    titleLabel=Label(window,text="Restorent Billing System",font="Arial 30",fg="green")
    titleLabel.grid(row=0,column=1,columnspan=4,padx=(200,0),pady=(10,0))

    billsTV=ttk.Treeview(window,height=15,columns=("Rate","Quantity","Cost"))
    billsTV.grid(row=1,column=1,columnspan=5)
    scrollBar=Scrollbar(window,orient="vertical",command=billsTV.yview)
    scrollBar.grid(row=1,column=5,sticky="NSE")

    billsTV.configure(yscrollcommand=scrollBar.set)

    billsTV.heading('#0',text="Item Name")
    billsTV.heading('#1',text="Rate")
    billsTV.heading('#2',text="Quantity")
    billsTV.heading('#3',text="Cost")
    updateBillData()
    
loginWindow()
window.mainloop()
  
