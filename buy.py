import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
# from typing import Any
from database import connect_db
from tool_ import *
from PIL import ImageTk
import datetime as dt
import os
from tkcalendar import Calendar

class buy:
    def __init__(self,root) -> None:
        self.root=root
        self.ROOT_DIR = loadConfig()['images'] 
              
        self.iconimg=ImageTk.PhotoImage(file=f'{self.ROOT_DIR}icon.png')
        self.root.iconphoto(False,self.iconimg)
        self.root.geometry("1100x500+220+130")
        self.root.title("Buy @Inventory Management System | Developed by KG")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()
        self.var_creation()

        ##===============Label Frame====================================
        searchFrame=LabelFrame(self.root,text="Search Product",bg="white",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE)
        searchFrame.place(x=400,y=40,width=570,height=65)
        cmb_search=ttk.Combobox(searchFrame,textvariable=self.var_buy_searchby,values=("Select","pid","buyid","name","description","category","cost","quantity","supplier","date","exp_date"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=5,width=180)
        cmb_search.current(0)

        txt_search=Entry(searchFrame,textvariable=self.var_buy_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=5)
        btn_search=Button(searchFrame,command=self.search,text="Search",font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=3,width=150,height=30)
    
#===================Employee Details==============================
        title_buy= Label(self.root,text="Buy Details",bg="#0f4d7d",fg="white",font=("goudy old style",15,"bold")).place(x=5,y=10,width=1090)
        lbl_list=["PID:","BuyID:","Name:","Description:","Cost:","SellingPrice","Quantity:","Supplier:","Date:","Exp_date:"]
        y=50
        for i in lbl_list:
            Label(self.root,text=i,bg="white",font=("goudy old style",15,"bold")).place(x=50,y=y)
            y+=40
        
        self.cmb_pid=ttk.Combobox(self.root,textvariable=self.var_pid,values=("Select",),state='readonly',justify=CENTER,font=("goudy old style",15))
        self.cmb_pid.place(x=170,y=50,width=180)
        self.cmb_pid.current(0)
        self.cmb_pid.bind('<<ComboboxSelected>>',self.popCombo)
        Entry(self.root,textvariable=self.var_buyid,state="readonly",font=("goudy old style",15,"bold"),readonlybackground="lightyellow").place(x=170,y=90,width=180)
        Entry(self.root,textvariable=self.var_name,state="readonly",font=("goudy old style",15,"bold"),readonlybackground="lightyellow").place(x=170,y=130,width=180)
        Entry(self.root,textvariable=self.var_description,state="readonly",font=("goudy old style",15,"bold"),readonlybackground="lightyellow").place(x=170,y=170,width=180)
        Button(self.root,text="\u21BA",command=lambda:self.var_buyid.set(generate_id("buy","buyid"))).place(x=355,y=90)
        self.cmb_categroy=ttk.Combobox(self.root,textvariable=self.var_category,values=("Select"),state="readonly",justify=CENTER,font=("goudy old style",15))
        # self.cmb_categroy.place(x=170,y=210,width=180)
        # self.cmb_categroy.current(0)
        
        Entry(self.root,textvariable=self.var_cost,state="normal",font=("goudy old style",15,"bold"),background="lightyellow").place(x=170,y=210,width=180)

        Entry(self.root,textvariable=self.var_price,state="normal",font=("goudy old style",15,"bold"),background="lightyellow").place(x=170,y=250,width=180)
        Entry(self.root,textvariable=self.var_qty,state="normal",font=("goudy old style",15,"bold"),background="lightyellow").place(x=170,y=290,width=180)
        
        self.cmb_supplier=ttk.Combobox(self.root,textvariable=self.var_sup,values=("Select"),state="readonly",justify=CENTER,font=("goudy old style",15))
        self.cmb_supplier.place(x=170,y=330,width=180)
        self.cmb_supplier.current(0)
        Entry(self.root,textvariable=self.var_date,state="readonly",font=("goudy old style",15,"bold"),readonlybackground="lightyellow").place(x=170,y=370,width=180)
        Entry(self.root,textvariable=self.var_exp_date,state="readonly",font=("goudy old style",15,"bold"),readonlybackground="lightyellow").place(x=170,y=410,width=180)
        self.btn_date_picker=Button(self.root,text="\uE1DC",command=lambda :openCalendar(self.root,self.var_date,self.btn_date_picker),font=("Segoe MDL2 Assets",14),bg="white")
        self.btn_date_picker.place(x=355,y=367,width=30)

        self.btn_exp_picker=Button(self.root,text="\uE1DC",command=lambda :openCalendar(self.root,self.var_exp_date,self.btn_exp_picker),font=("Segoe MDL2 Assets",14),bg="white")
        self.btn_exp_picker.place(x=355,y=407,width=30)

        
        btn_save=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="#33bbf9",fg="white",cursor="hand2").place(x=20,y=450,width=90,height=28)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="#ff5722",fg="white",cursor="hand2").place(x=115,y=450,width=90,height=28)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="#009688",fg="white",cursor="hand2").place(x=210,y=450,width=90,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=305,y=450,width=90,height=28)

        emp_frame= Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=400,y=110,height=390,width=700)
        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)
        self.pro_table=ttk.Treeview(emp_frame,columns=("1","2","3","4","5","7","8","9","10","11","12"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.pro_table.xview)
        scrolly.config(command=self.pro_table.yview)
        self.pro_table.heading("1",text="Sr.")
        self.pro_table.heading("2",text="ProID")
        self.pro_table.heading("3",text="BuyID")

        self.pro_table.heading("4",text="Name")
        self.pro_table.heading("5",text="Description")
        self.pro_table.heading("7",text="Category")

        self.pro_table.heading("8",text="Cost")
        self.pro_table.heading("9",text="Quantity")
        self.pro_table.heading("10",text="Supplier")

        self.pro_table.heading("11",text="Date")
        self.pro_table.heading("12",text="ExpDate")
        
        self.pro_table["show"]="headings"
        self.pro_table.column("1",width=10)
        self.pro_table.column("2",width=70)
        self.pro_table.column("3",width=70)
        self.pro_table.column("4",width=100)
        self.pro_table.column("5",width=100)

        self.pro_table.column("7",width=100)
        self.pro_table.column("8",width=70)
        self.pro_table.column("9",width=80)
        self.pro_table.column("10",width=100)
        self.pro_table.column("11",width=100)
        self.pro_table.column("12",width=100)

        self.pro_table.pack(fill=BOTH,expand=1)
        self.pro_table.bind('<ButtonRelease-1>',self.getdata)
        update_combo("product","pid",self.cmb_pid)
        update_combo("category","name",self.cmb_categroy)
        update_combo("supplier","name",self.cmb_supplier)
        # self.cmb_pid.bind("<<ComboboxSelected>>",lambda a:self.cmb_select(a,self.var_pid.get()))
        self.show()
        self.comboData()
    def getdata(self,ev):
        try:
            f= self.pro_table.focus()
            content= (self.pro_table.item(f))
            row=content['values']
            self.var_pid.set(row[1])
            self.var_buyid.set(row[2])
            self.var_name.set(row[3])
            self.var_description.set(row[4])
            self.var_category.set(row[5])
            self.var_cost.set(row[6])
            self.var_qty.set(str(row[7]))
            self.var_sup.set(row[8])
            self.var_date.set(row[9])
            self.var_exp_date.set(row[10])


        except IndexError as ex:
            messagebox.showerror("Ops!","There is no record on table or Be Careful to click on row",parent=self.root)
    def add(self):
        con=connect_db() #module from database.py
        mycur= con.cursor()
 
        try:
            if self.var_buyid.get()=="":
                messagebox.showerror("Error","Buy ID missing!",parent=self.root)
            else:
                sql="SELECT * FROM buy where buyid=%s"
                val=(self.var_buyid.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Duplicate buy\'s id",parent=self.root)
                    
                else:
                    sql="INSERT INTO buy(pid,buyid,name,description,category,cost,quantity,supplier,date,expdate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    val=(self.var_pid.get(),self.var_buyid.get(),self.var_name.get(),
                            self.var_description.get(),self.var_category.get(),
                            self.var_cost.get(),self.var_qty.get(),
                            self.var_sup.get(),self.var_date.get(),
                            self.var_exp_date.get()
                            )
                    # print(val)
                    
        ##### isStatusOK is checking whether one of the fields missing of not
                    if isStatusOK(val):
                        temp=(self.var_cost.get(),self.var_qty.get())
                        if check_digit(temp):
                            mycur.execute(sql,val)
                            con.commit()
                            print("ok1")
                            sql="select qty from product where pid=%s"
                            val=(self.var_pid.get(),)
                            mycur.execute(sql,val)
                            a=mycur.fetchone()
                            b=int(a[0])+int(self.var_qty.get())
                            print("ok2")
                            sql="update product set qty=%s where pid=%s"
                            val=(b,self.var_pid.get())
                            mycur.execute(sql,val)
                            con.commit()
                            con.close()
                            print("ok3")
                            withdraw=int(self.var_cost.get())*int(self.var_qty.get())
                            save_to_wallet(self.var_buyid.get(),"0",withdraw,self.var_date.get())
                            self.clear()
                            messagebox.showinfo("Message","Successfully inserted into Database!",parent=self.root)

                            self.show()
                            con.close() 
                        else:
                            messagebox.showerror("Error","You can only put digits in amount entries.",parent=self.root)
                    else:
                        messagebox.showerror("Error","You are missing some data!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error2",f"Error due to : {(ex)}",parent=self.root)
    def show(self):
        con=connect_db()
        mycur= con.cursor()
        try:
            sql="SELECT * FROM buy"
            mycur.execute(sql)
            rows=mycur.fetchall()
            self.pro_table.delete(*self.pro_table.get_children())
            for row in rows:
               self.pro_table.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error1",f"Error due to : {str(ex)}",parent=self.root)
    def update(self):
        con=connect_db() #module from database.py
        mycur= con.cursor()
 
        # calling create_emp from database.py
        # create_emp()
        try:
            if self.var_buyid.get()=="":
                messagebox.showerror("Error","Buy\'s ID missing!",parent=self.root)
            else:
                sql="SELECT buyid FROM buy where buyid=%s"
                val=(self.var_buyid.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Buy\'s ID",parent=self.root)
                else:
                    val=(self.var_category.get(),self.var_cost.get(),
                                self.var_qty.get(),self.var_sup.get(),
                                self.var_date.get(),self.var_exp_date.get(),
                                self.var_buyid.get())
                    if isStatusOK(val):
                        temp=(self.var_cost.get(),self.var_qty.get())
                        if check_digit(temp):
                            
                            sql="select quantity from buy where buyid=%s"
                            val=(self.var_buyid.get(),)
                            mycur.execute(sql,val)
                            a=mycur.fetchone()
                            b=int(self.var_qty.get())
                            c=int(a[0])-b
                            sql="select qty from product where pid=%s"
                            val=(self.var_pid.get(),)
                            mycur.execute(sql,val)
                            d=mycur.fetchone()
                            e=int(d[0])-c
                            sql="UPDATE buy SET category=%s,cost=%s,quantity=%s,supplier=%s,date=%s,expdate=%s where buyid=%s"
                            val=(self.var_category.get(),self.var_cost.get(),
                                self.var_qty.get(),self.var_sup.get(),
                                self.var_date.get(),self.var_exp_date.get(),
                                self.var_buyid.get())
                            mycur.execute(sql,val)
                            con.commit()
                            sql="update product set qty=%s where pid=%s"
                            val=(e,self.var_pid.get(),)
                            mycur.execute(sql,val)
                            con.commit()
                            con.close()
                            # print(self.var_buyid.get())
                            con=connect_db()
                            mycur=con.cursor()
                            defg="select withdraw from wallet where description=%s"
                            abcd=(self.var_buyid.get(),)
                            mycur.execute(defg,abcd)
                            org_cost=mycur.fetchone()
                            # print(org_cost)
                            new_cost=int(self.var_cost.get())*int(self.var_qty.get())
                            withdraw_dif=int(org_cost[0])-new_cost
                            # print(int(org_cost[0]),new_cost)
                            
                            # update_wallet(self.var_buyid.get(),0,withdraw,self.var_date.get(),0,new_cost)
                            # print(withdraw_dif)
                            update_wallet(self.var_buyid.get(),0,new_cost,self.var_date.get(),0,withdraw_dif)

                            self.clear()
                            messagebox.showinfo("Message","Successfully inserted into Database!",parent=self.root)

                            self.show()
                            con.close() 
                        else:
                            messagebox.showerror("Error","You can only put digits in amount entries.",parent=self.root)

                    

        except Exception as ex:
            messagebox.showerror("Error3",f"Error due to : {str(ex)}",parent=self.root)
    def delete(self):
        con=connect_db() #module from database.py
        mycur=con.cursor()
        try:
            if self.var_buyid.get()=="":
                messagebox.showerror("Error","Buy ID missing!",parent=self.root)
            else:
                sql="SELECT quantity FROM buy where buyid=%s"
                val=(self.var_buyid.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row==None:
                    messagebox.showerror("Error","There is no record found with your Buy\'s ID",parent=self.root)
                else:
                    a=int(row[0])
                    ans=messagebox.askyesno("Confirmation",f"Are you sure want to Delete {self.var_buyid.get()}?",parent=self.root)
                    if ans==True:
                        mycur.execute("DELETE FROM buy where buyid=%s",(self.var_buyid.get(),))
                        con.commit()
                        mycur.execute("select qty from product where pid=%s",(self.var_pid.get(),))
                        temp=mycur.fetchone()
                        b=int(temp[0])
                        c=b-a
                        mycur.execute("update product set qty=%s where pid=%s",(c,self.var_pid.get()))
                        con.commit()
                        sql="select withdraw from wallet where description=%s"
                        val=(self.var_buyid.get(),)
                        mycur.execute(sql,val)
                        x=mycur.fetchone()
                        delete_wallet(self.var_buyid.get(),0,x[0])
                        messagebox.showinfo("Success","Your Record has been Deleted from Database!",parent=self.root)
                        self.clear()
                        self.show()

        except Exception as ex:
            messagebox.showerror("Error4",f"Error due to : {str(ex)}",parent=self.root)
    def clear(self):
        self.var_buy_searchby.set("Select")
        self.var_buy_searchtxt.set("")
        self.var_pid.set("Select")
        self.var_buyid.set(generate_id("buy","buyid"))
        self.var_name.set("")
        self.var_description.set("")
        self.var_cost.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_category.set("Select")
        self.var_sup.set("Select")
        self.var_date.set("")
        self.var_exp_date.set("")

        self.show()
    def cmb_select(self,event,id):
        con=connect_db()
        mycur=con.cursor()
        sql="select name,description,category,supplier from product where pid=%s"
        val=(id,)
        mycur.execute(sql,val)
        a=mycur.fetchone()
        self.var_name.set(a[0])
        self.var_description.set(a[1])
        self.var_category.set(a[2])
        self.var_sup.set(a[3])
    def var_creation(self):
        self.var_buy_searchby=StringVar()
        self.var_buy_searchtxt=StringVar()

        self.var_pid=StringVar()
        self.var_buyid=StringVar()
        self.var_name=StringVar()
        self.var_description=StringVar()
        self.var_category=StringVar()
        self.var_cost=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_sup=StringVar()
        self.var_date=StringVar()
        self.var_exp_date=StringVar()
        self.var_buyid.set(generate_id("buy","buyid"))
        self.list_combo=[]
        self.list_aux=[]
        self.var_created_time=StringVar()
        self.var_to_build=StringVar()
        self.var_aux=StringVar()
    def search(self):
        con=connect_db()
        mycur= con.cursor()
        try:
            if self.var_buy_searchby.get()=="Select":
                messagebox.showerror("Error","Choose some option in \"Search By option\"",parent=self.root)
            elif self.var_buy_searchtxt.get()=="":
                #self.var_emp_searchtxt.get()==""
                messagebox.showerror("Error","Search input should be filled",parent=self.root)
            else:
                mycur.execute("SELECT * FROM buy where "+self.var_buy_searchby.get()+" Like '%"+self.var_buy_searchtxt.get()+"%'")
                rows= mycur.fetchall()

                if len(rows)!=0:
                    self.pro_table.delete(*self.pro_table.get_children())
                    for row in rows:
                        self.pro_table.insert('',END,values=row)
                else:
                    messagebox.showinfo("Information","No record found on system",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",str(ex),parent=self.root)
    
    def comboData(self):
        conn=connect_db()
        sql_="select pid,name from product"
        cur=conn.cursor()
        cur.execute(sql_)
        result= cur.fetchall()
        self.list_combo.clear()
        for i in result:
            self.list_combo.append(f'{i[0]} : < {i[1]} >')
        self.cmb_pid.config(values=self.list_combo)
        
        # print(self.list_combo)
    def popCombo(self,event):
        id_=self.extractID(self.var_pid)
        self.var_pid.set(id_)
        con=connect_db()
        mycur=con.cursor()
        sql="select name,description,category,supplier from product where pid=%s"
        val=(id_,)
        mycur.execute(sql,val)
        data= mycur.fetchone()
        if data !=None:            
            self.var_name.set(data[0])
            self.var_description.set(data[1])
            self.var_category.set(data[2])
            self.var_sup.set(data[3])
    def extractID(self,cmb):
        temp=cmb.get()
        temp=temp.split(":")
        cmb.set(temp[0])
        # we need to strip temp[0] white space
        return str(temp[0]).strip()

if __name__=="__main__":
    root= Tk()
    app= buy(root)
    root.mainloop()