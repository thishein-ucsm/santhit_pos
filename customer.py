import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database import connect_db
from tool_ import isStatusOK,loadConfig
import os
from PIL import ImageTk
class customer:
    def __init__(self,root) -> None:
        self.root=root
        self.ROOT_DIR = loadConfig()['images']
        self.iconimg=ImageTk.PhotoImage(file=f'{self.ROOT_DIR}icon.png')
        self.root.iconphoto(False,self.iconimg)
        
        self.root.geometry("1100x500+220+130")
        self.root.title("Customer @Inventory Management System | Developed by KG")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()
        self.var_creation()

        ##===============Label Frame====================================
        searchFrame=LabelFrame(self.root,text="Search Customer",bg="white",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE)
        searchFrame.place(x=400,y=40,width=570,height=65)

        cmb_search=ttk.Combobox(searchFrame,textvariable=self.var_cus_searchby,values=("Select","cusid","name","custype","contact","Address"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=5,width=180)
        cmb_search.current(0)

        txt_search=Entry(searchFrame,textvariable=self.var_cus_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=5)
        btn_search=Button(searchFrame,command=self.search,text="Search",font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=3,width=150,height=30)

        #===================Employee Details==============================
        title_supplier= Label(self.root,text="Customer Details",bg="#0f4d7d",fg="white",font=("goudy old style",15,"bold")).place(x=5,y=10,width=1090)

        lbl_id= Label(self.root,text="CusID:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=50)
        lbl_name= Label(self.root,text="Name:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=90)
        lbl_contact= Label(self.root,text="Contact:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=130)
        
        txt_id= Entry(self.root,textvariable=self.var_cus_id,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=170,y=50,width=180)       
        txt_name= Entry(self.root,textvariable=self.var_cus_name,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=170,y=90,width=180)
        txt_contact= Entry(self.root,textvariable=self.var_cus_contact,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=170,y=130,width=180)
        cmb_cus_type=ttk.Combobox(self.root,textvariable=self.var_cus_type,values=("Select","Cash","Credit","Walk in"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_cus_type.place(x=170,y=170,width=180)
        cmb_cus_type.current(0)
        lbl_cmpname= Label(self.root,text="CusType:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=170)
        # lbl_cmpphone= Label(self.root,text="CmpPhone:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=210)
        # txt_cmpname= Entry(self.root,textvariable=self.var_cus_cmpname,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=170,y=170,width=180)
        # txt_cmpphone= Entry(self.root,textvariable=self.var_cus_cmpphone,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=170,y=210,width=180)
        lbl_remark= Label(self.root,text="Remark:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=210)
        txt_remark= Entry(self.root,textvariable=self.var_cus_remark,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=170,y=210,width=180)


        lbl_address= Label(self.root,text="Address:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=250)
        self.txt_address= Text(self.root,font=("goudy old style",15,"bold"),bg="lightyellow")
        self.txt_address.place(x=170,y=250,width=180,height=100)

        ##================Button Fram===========================
        btn_save=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="#33bbf9",fg="white",cursor="hand2").place(x=50,y=400,width=115,height=28)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="#ff5722",fg="white",cursor="hand2").place(x=200,y=400,width=115,height=28)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="#009688",fg="white",cursor="hand2").place(x=50,y=440,width=115,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=200,y=440,width=115,height=28)

        ##==========table frame====================================
        cus_frame= Frame(self.root,bd=3,relief=RIDGE)
        cus_frame.place(x=400,y=110,height=390,width=700)
        scrolly=Scrollbar(cus_frame,orient=VERTICAL)
        scrollx=Scrollbar(cus_frame,orient=HORIZONTAL)
        self.cus_table=ttk.Treeview(cus_frame,columns=("sr","cid","name","con","custype","addr","rem"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.cus_table.xview)
        scrolly.config(command=self.cus_table.yview)
        self.cus_table.heading("sr",text="Sr.")
        self.cus_table.heading("cid",text="CusID")
        self.cus_table.heading("name",text="CustomerName")
        self.cus_table.heading("con",text="Contact")
        self.cus_table.heading("custype",text="CustomerType")
        self.cus_table.heading("addr",text="Address")
        self.cus_table.heading("rem",text="Remark")
        
        

        self.cus_table["show"]="headings"
        self.cus_table.column("sr",width=10)
        self.cus_table.column("cid",width=90)
        self.cus_table.column("name",width=100)
        self.cus_table.column("con",width=100)
        self.cus_table.column("custype",width=100)
        self.cus_table.column("rem",width=100)
        self.cus_table.column("addr",width=100)
        self.cus_table.pack(fill=BOTH,expand=1)
        self.cus_table.bind('<ButtonRelease-1>',self.getdata)
        self.show()
    def show(self):
        con=connect_db()
        mycur= con.cursor()
        try:
            sql="SELECT * FROM customer"
            mycur.execute(sql)
            rows=mycur.fetchall()
            self.cus_table.delete(*self.cus_table.get_children())
            for row in rows:
               self.cus_table.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    def getdata(self,ev):
        try:
            f= self.cus_table.focus()
            content= (self.cus_table.item(f))
            row=content['values']

            
            self.var_cus_id.set(row[1])
            self.var_cus_name.set(row[2])
            self.var_cus_contact.set(row[3])
            self.var_cus_type.set(row[4])
            self.var_cus_remark.set(row[6])
            self.txt_address.delete('1.0',END)
            self.txt_address.insert(END,row[5])

        except IndexError as ex:
            messagebox.showerror("Ops!","There is no record on table or Be Careful to click on row",parent=self.root)
    def add(self):
        con=connect_db() #module from database.py
        mycur= con.cursor()
 
        try:
            if self.var_cus_id.get()=="":
                messagebox.showerror("Error","Customer ID missing!",parent=self.root)
            else:
                sql="SELECT * FROM customer where cusid=%s"
                val=(self.var_cus_id.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Duplicate customer\'s id",parent=self.root)
                else:
                    sql="INSERT INTO customer(cusid,name,contact,custype,address,remark)VALUES(%s,%s,%s,%s,%s,%s)"
                    val=(self.var_cus_id.get(),self.var_cus_name.get(),
                         self.var_cus_contact.get(),
                         self.var_cus_type.get(),self.txt_address.get('1.0',END),
                         self.var_cus_remark.get()
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
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    def update(self):
        con=connect_db() #module from database.py
        mycur= con.cursor()
 
        # calling create_emp from database.py
        # create_emp()
        try:
            if self.var_cus_id.get()=="":
                messagebox.showerror("Error","Customer\'s ID missing!",parent=self.root)
            else:
                sql="SELECT cusid FROM customer where cusid=%s"
                val=(self.var_cus_id.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Customer\'s ID",parent=self.root)
                else:
                    # "eid","name","nrc","gen","cont","dob","type","sal","addr"
                    sql="UPDATE customer SET name=%s,contact=%s,custype=%s,address=%s,remark=%s where cusid=%s"
                    val=(self.var_cus_name.get(),self.var_cus_contact.get(),
                         self.var_cus_type.get(),
                         self.txt_address.get('1.0',END),
                         self.var_cus_remark.get(),
                         self.var_cus_id.get()

                         )
                    
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
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    def delete(self):
        con=connect_db() #module from database.py
        mycur= con.cursor()
        try:
            if self.var_cus_id.get()=="":
                messagebox.showerror("Error","Customer ID missing!",parent=self.root)
            else:
                sql="SELECT cusid FROM customer where cusid=%s"
                val=(self.var_cus_id.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row==None:
                    messagebox.showerror("Error","There is no record found with your Customer\'s ID",parent=self.root)
                else:
                    ans=messagebox.askyesno("Confirmation",f"Are you sure want to Delete {self.var_cus_id.get()}?",parent=self.root)
                    if ans==True:
                        mycur.execute("DELETE FROM customer where cusid=%s",(self.var_cus_id.get(),))
                        con.commit()
                        con.close()
                        messagebox.showinfo("Success","Your Record has been Deleted from Database!",parent=self.root)
                        self.clear()
                        self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    def clear(self):
        self.var_cus_searchby.set("Select")
        self.var_cus_searchtxt.set("")
        self.var_cus_id.set("")
        self.var_cus_name.set("")
        self.var_cus_type.set("Select")
        self.var_cus_contact.set("")
        self.var_cus_remark.set("")
        self.txt_address.delete('1.0',END)
        self.show()
    def search(self):
        con=connect_db()
        mycur= con.cursor()
        try:
            if self.var_cus_searchby.get()=="Select":
                messagebox.showerror("Error","Choose some option in \"Search By option\"",parent=self.root)
            elif self.var_cus_searchtxt.get()=="":
                #self.var_emp_searchtxt.get()==""
                messagebox.showerror("Error","Search input should be filled",parent=self.root)
            else:
                mycur.execute("SELECT * FROM customer where "+self.var_cus_searchby.get()+" Like '%"+self.var_cus_searchtxt.get()+"%'")
                rows= mycur.fetchall()

                if len(rows)!=0:
                    self.cus_table.delete(*self.cus_table.get_children())
                    for row in rows:
                        self.cus_table.insert('',END,values=row)
                else:
                    messagebox.showinfo("Information","No record found on system",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",str(ex),parent=self.root)

    def var_creation(self):
        self.var_cus_searchby=StringVar()
        self.var_cus_searchtxt=StringVar()
        self.var_cus_id=StringVar()
        self.var_cus_name=StringVar()
        self.var_cus_type=StringVar()
        self.var_cus_contact=StringVar()
        self.var_cus_remark=StringVar()
        # self.var_cus_remark="_"

if __name__=="__main__":
    root= Tk()
    app= customer(root)
    root.mainloop()