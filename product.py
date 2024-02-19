import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database import connect_db
from tool_ import generate_timestamp, isStatusOK,loadConfig, openCalendar
from PIL import ImageTk
import os
import datetime as dt
from tkcalendar import Calendar
class product:
    def __init__(self,root) -> None:
        self.root=root
        self.ROOT_DIR = loadConfig()['images']        
        self.iconimg=ImageTk.PhotoImage(file=f'{self.ROOT_DIR}icon.png')
        self.root.iconphoto(False,self.iconimg)
        self.root.geometry("1100x500+220+130")
        self.root.title("Product @Inventory Management System | Developed by KG")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()
        self.var_creation()

         ##===============Label Frame====================================
        searchFrame=LabelFrame(self.root,text="Search Product",bg="white",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE)
        searchFrame.place(x=400,y=40,width=570,height=65)

        cmb_search=ttk.Combobox(searchFrame,textvariable=self.var_pro_searchby,values=("Select","pid","name","description","qty","status","category","supplier","created_time","remark"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=5,width=180)
        cmb_search.current(0)

        txt_search=Entry(searchFrame,textvariable=self.var_pro_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=5)
        btn_search=Button(searchFrame,command=self.search,text="Search",font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=3,width=150,height=30)
 #===================Employee Details==============================
        title_product= Label(self.root,text="Product Details",bg="#0f4d7d",fg="white",font=("goudy old style",15,"bold")).place(x=5,y=10,width=1090)
        lbl_list=["PID:","Name:","Description:","Quantity:","SellingPrice","Status","Category:","Supplier:","CreatedTime:","Remark:"]
        ent_list=[self.var_pid,self.var_name,self.var_description,self.var_qty,self.var_price]

        y=50
        for i in lbl_list:
            Label(self.root,text=i,bg="white",font=("goudy old style",15,"bold")).place(x=50,y=y)
            y+=38
        y=50
        for i in ent_list:
            Entry(self.root,textvariable=i,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=170,y=y,width=180)
            y+=38
        # print(y)
        # Label(self.root,text="Status",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=210)    
        self.cmb_status=ttk.Combobox(self.root,textvariable=self.var_status,values=("Select","Active","Inactive","Out of Stock"),state='readonly',justify=CENTER,font=("goudy old style",15))
        self.cmb_status.place(x=170,y=240,width=180)
        self.cmb_status.current(0)
        self.cmb_cat=ttk.Combobox(self.root,textvariable=self.var_category,values=("Select",),state='readonly',justify=CENTER,font=("goudy old style",15))
        self.cmb_cat.place(x=170,y=278,width=180)
        self.cmb_cat.current(0)
        self.cmb_sup=ttk.Combobox(self.root,textvariable=self.var_supplier,values=("Select",),state='readonly',justify=CENTER,font=("goudy old style",15))
        self.cmb_sup.place(x=170,y=316,width=180)
        self.cmb_sup.current(0)
        txt_ctime= Entry(self.root,textvariable=self.var_created_time,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=170,y=355,width=180)
        txt_remark= Entry(self.root,textvariable=self.var_remark,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=170,y=392,width=180)
        self.btn_date_picker=Button(self.root,text="\uE1DC",command=lambda:openCalendar(self.root,self.var_created_time,self.btn_date_picker),font=("Segoe MDL2 Assets",14),bg="white")
        self.btn_date_picker.place(x=355,y=355,width=30)
        ##================Button Frame===========================
        btn_save=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="#33bbf9",fg="white",cursor="hand2").place(x=20,y=460,width=90,height=28)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="#ff5722",fg="white",cursor="hand2").place(x=115,y=460,width=90,height=28)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="#009688",fg="white",cursor="hand2").place(x=210,y=460,width=90,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=305,y=460,width=90,height=28)

        #==========table frame====================================
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
        self.pro_table.heading("2",text="PID")
        self.pro_table.heading("3",text="Name")
        self.pro_table.heading("4",text="Description")
        self.pro_table.heading("5",text="Qty")
        self.pro_table.heading("7",text="SellPrice")
        self.pro_table.heading("8",text="Status")
        self.pro_table.heading("9",text="Category")
        self.pro_table.heading("10",text="Supplier")
        self.pro_table.heading("11",text="Time")
        self.pro_table.heading("12",text="Remark")
        
        self.pro_table["show"]="headings"
        self.pro_table.column("1",width=10)
        self.pro_table.column("2",width=70)
        self.pro_table.column("3",width=100)
        self.pro_table.column("4",width=150)
        self.pro_table.column("5",width=50,anchor="e")
        self.pro_table.column("7",width=70,anchor="e")
        self.pro_table.column("8",width=70)
        self.pro_table.column("9",width=100)
        self.pro_table.column("10",width=100)
        self.pro_table.column("11",width=70)
        self.pro_table.column("12",width=50)

        self.pro_table.pack(fill=BOTH,expand=1)
        self.pro_table.bind('<ButtonRelease-1>',self.getdata)

        self.update_combo()
        self.show()
    def update_combo(self):
        namelist=[]
        con=connect_db()
        mycur=con.cursor()
        sql="SELECT name from category"
        mycur.execute(sql)
        rows=mycur.fetchall()
        for row in rows:
            namelist.append(row[0])
        if mycur.rowcount>0:
            self.cmb_cat.config(values=namelist)
        else:
            self.cmb_cat.config(values="Empty")
        
        sql="SELECT name from supplier"
        mycur.execute(sql)
        rows=mycur.fetchall()
        namelist.clear()
        for row in rows:
            namelist.append(row[0])
        if mycur.rowcount>0:
            self.cmb_sup.config(values=namelist)
        else:
            self.cmb_sup.config(values="Empty")
    def getdata(self,ev):
        try:
            f= self.pro_table.focus()
            content= (self.pro_table.item(f))
            row=content['values']
            self.var_pid.set(row[1])
            self.var_name.set(row[2])
            self.var_description.set(row[3])
            self.var_qty.set(row[4])
            self.var_price.set(row[5])
            # self.var_sellingprice.set(row[6])
            self.var_status.set(row[6])
            self.var_category.set(str(row[7]))
            self.var_supplier.set(row[8])
            self.var_created_time.set(row[9])
            self.var_remark.set(row[10])


        except IndexError as ex:
            pass
            # messagebox.showerror("Ops!","There is no record on table or Be Careful to click on row",parent=self.root)
    def show(self):
        con=connect_db()
        mycur= con.cursor()
        try:
            sql="SELECT * FROM product"
            mycur.execute(sql)
            rows=mycur.fetchall()
            # print(rows)
            self.pro_table.delete(*self.pro_table.get_children())
            for row in rows:
               self.pro_table.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error1",f"Error due to : {str(ex)}",parent=self.root)
    def add(self):
        con=connect_db() #module from database.py
        mycur= con.cursor()
 
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Product ID missing!",parent=self.root)
            else:
                sql="SELECT * FROM product where pid=%s"
                val=(self.var_pid.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Duplicate product\'s id",parent=self.root)
                    
                else:
                    sql="INSERT INTO product(pid,name,description,qty,price,status,category,supplier,created_time,remark) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    val=(self.var_pid.get(),self.var_name.get(),
                         self.var_description.get(),self.var_qty.get(),
                         self.var_price.get(),self.var_status.get(),
                         self.var_category.get(),self.var_supplier.get(),
                         self.var_created_time.get(),self.var_remark.get()
                         )
                    
        ##### isStatusOK is checking whether one of the fields missing of not
                    if isStatusOK(val):
                        mycur.execute(sql,val)
                        con.commit()
                        self.clear()
                        messagebox.showinfo("Message","Successfully inserted into Database!",parent=self.root)
                        self.show()
                        con.close()
                    else:
                        messagebox.showerror("Error","You are missing some data!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error2",f"Error due to : {(ex)}",parent=self.root)
    def update(self):
        con=connect_db() #module from database.py
        mycur= con.cursor()
 
        # calling create_emp from database.py
        # create_emp()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Product\'s ID missing!",parent=self.root)
            else:
                sql="SELECT pid FROM product where pid=%s"
                val=(self.var_pid.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product\'s ID",parent=self.root)
                else:
                    # "eid","name","nrc","gen","cont","dob","type","sal","addr"
                    sql="UPDATE product SET name=%s,description=%s,qty=%s,price=%s,status=%s,category=%s,supplier=%s,created_time=%s,remark=%s where pid=%s"
                    val=(self.var_name.get(),self.var_description.get(),
                         self.var_qty.get(),self.var_price.get(),
                         self.var_status.get(),self.var_category.get(),
                         self.var_supplier.get(),self.var_created_time.get(),
                         self.var_remark.get(),
                         self.var_pid.get())
                    
        ##### isStatusOK is checking whether one of the fields missing of not
                    if isStatusOK(val):
                        mycur.execute(sql,val)
                        con.commit()
                        messagebox.showinfo("Message","Successfully updated into Database!",parent=self.root)
                        self.clear()
                        self.show()
                        con.close()
                    else:
                        messagebox.showerror("Error","You are missing some data!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error3",f"Error due to : {str(ex)}",parent=self.root)
    def delete(self):
        con=connect_db() #module from database.py
        mycur= con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Product ID missing!",parent=self.root)
            else:
                sql="SELECT pid FROM product where pid=%s"
                val=(self.var_pid.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row==None:
                    messagebox.showerror("Error","There is no record found with your Product\'s ID",parent=self.root)
                else:
                    ans=messagebox.askyesno("Confirmation",f"Are you sure want to Delete {self.var_pid.get()}?",parent=self.root)
                    if ans==True:
                        mycur.execute("DELETE FROM product where pid=%s",(self.var_pid.get(),))
                        con.commit()
                        con.close()
                        messagebox.showinfo("Success","Your Record has been Deleted from Database!",parent=self.root)
                        self.clear()
                        self.show()

        except Exception as ex:
            messagebox.showerror("Error4",f"Error due to : {str(ex)}",parent=self.root)
    def clear(self):
        self.var_pro_searchby.set("Select")
        self.var_pro_searchtxt.set("")
        self.var_pid.set("")
        self.var_name.set("")
        self.var_description.set("")
        self.var_qty.set("")
        self.var_price.set("")
        self.var_status.set("Select")
        self.var_category.set("Select")
        self.var_supplier.set("Select")
        self.var_created_time.set(generate_timestamp("%d/%m/%Y"))
        self.var_remark.set("")

        self.show()
    def search(self):
        con=connect_db()
        mycur= con.cursor()
        try:
            if self.var_pro_searchby.get()=="Select":
                messagebox.showerror("Error","Choose some option in \"Search By option\"",parent=self.root)
            elif self.var_pro_searchtxt.get()=="":
                #self.var_emp_searchtxt.get()==""
                messagebox.showerror("Error","Search input should be filled",parent=self.root)
            else:
                mycur.execute("SELECT * FROM product where "+self.var_pro_searchby.get()+" Like '%"+self.var_pro_searchtxt.get()+"%'")
                rows= mycur.fetchall()

                if len(rows)!=0:
                    self.pro_table.delete(*self.pro_table.get_children())
                    for row in rows:
                        self.pro_table.insert('',END,values=row)
                else:
                    messagebox.showinfo("Information","No record found on system",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",str(ex),parent=self.root)
    def var_creation(self):
        self.var_pro_searchby=StringVar()
        self.var_pro_searchtxt=StringVar()
        self.var_pid=StringVar()
        self.var_name=StringVar()
        self.var_description=StringVar()
        self.var_qty=StringVar()
        self.var_price=StringVar()
        self.var_status=StringVar()
        self.var_category=StringVar()
        self.var_supplier=StringVar()
        self.var_created_time=StringVar()
        self.var_created_time.set(generate_timestamp("%d/%m/%Y"))
        self.var_remark=StringVar()
    
if __name__=="__main__":
    root= Tk()
    app= product(root)
    root.mainloop()