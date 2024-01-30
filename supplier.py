import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database import connect_db
from tool_ import isStatusOK,loadConfig
import os
from PIL import ImageTk
class supplier:
    def __init__(self,root) -> None:
        self.root=root
        self.ROOT_DIR = loadConfig()['images']
        self.iconimg=ImageTk.PhotoImage(file=f'{self.ROOT_DIR}\\icon1.png')
        self.root.iconphoto(False,self.iconimg)

        self.root.geometry("1100x500+220+130")
        self.root.title("Supplier @Inventory Management System | Developed by KG")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()
        self.var_creation()

        ##===============Label Frame====================================
        searchFrame=LabelFrame(self.root,text="Search Supplier",bg="white",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE)
        searchFrame.place(x=400,y=40,width=570,height=65)

        cmb_search=ttk.Combobox(searchFrame,textvariable=self.var_sup_searchby,values=("Select","supid","name","contact","companyname","companyphone","Address"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=5,width=180)
        cmb_search.current(0)

        txt_search=Entry(searchFrame,textvariable=self.var_sup_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=5)
        btn_search=Button(searchFrame,command=self.search,text="Search",font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=3,width=150,height=30)

        #===================Employee Details==============================
        title_supplier= Label(self.root,text="Supplier Details",bg="#0f4d7d",fg="white",font=("goudy old style",15,"bold")).place(x=5,y=10,width=1090)

        lbl_id= Label(self.root,text="SupID:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=50)
        lbl_name= Label(self.root,text="Name:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=90)
        lbl_contact= Label(self.root,text="Contact:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=130)
        
        txt_id= Entry(self.root,textvariable=self.var_sup_id,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=170,y=50,width=180)       
        txt_name= Entry(self.root,textvariable=self.var_sup_salename,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=170,y=90,width=180)
        txt_contact= Entry(self.root,textvariable=self.var_sup_contact,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=170,y=130,width=180)

        lbl_cmpname= Label(self.root,text="CmpName:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=170)
        lbl_cmpphone= Label(self.root,text="CmpPhone:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=210)
        txt_cmpname= Entry(self.root,textvariable=self.var_sup_cmpname,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=170,y=170,width=180)
        txt_cmpphone= Entry(self.root,textvariable=self.var_sup_cmpphone,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=170,y=210,width=180)
        lbl_remark= Label(self.root,text="Remark:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=250)
        txt_remark= Entry(self.root,textvariable=self.var_sup_remark,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=170,y=250,width=180)


        lbl_address= Label(self.root,text="Address:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=290)
        self.txt_address= Text(self.root,font=("goudy old style",15,"bold"),bg="lightyellow")
        self.txt_address.place(x=170,y=290,width=180,height=80)

        ##================Button Fram===========================
        btn_save=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="#33bbf9",fg="white",cursor="hand2").place(x=50,y=400,width=115,height=28)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="#ff5722",fg="white",cursor="hand2").place(x=200,y=400,width=115,height=28)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="#009688",fg="white",cursor="hand2").place(x=50,y=440,width=115,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=200,y=440,width=115,height=28)

        ##==========table frame====================================
        sup_frame= Frame(self.root,bd=3,relief=RIDGE)
        sup_frame.place(x=400,y=110,height=390,width=700)
        scrolly=Scrollbar(sup_frame,orient=VERTICAL)
        scrollx=Scrollbar(sup_frame,orient=HORIZONTAL)
        self.sup_table=ttk.Treeview(sup_frame,columns=("sr","sid","name","con","cpname","cpcon","addr","rem"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.sup_table.xview)
        scrolly.config(command=self.sup_table.yview)
        self.sup_table.heading("sr",text="Sr.")
        self.sup_table.heading("sid",text="SupID")
        self.sup_table.heading("name",text="SalePersonName")
        self.sup_table.heading("con",text="SalepersonPhone")
        self.sup_table.heading("cpname",text="CompanyName")
        self.sup_table.heading("cpcon",text="CompanyContact")
        self.sup_table.heading("addr",text="Address")
        self.sup_table.heading("rem",text="Remark")
        
        

        self.sup_table["show"]="headings"
        self.sup_table.column("sr",width=10)
        self.sup_table.column("sid",width=90)
        self.sup_table.column("name",width=100)
        self.sup_table.column("con",width=100)
        self.sup_table.column("cpname",width=100)
        self.sup_table.column("cpcon",width=100)
        self.sup_table.column("rem",width=100)
        self.sup_table.column("addr",width=100)
        self.sup_table.pack(fill=BOTH,expand=1)
        self.sup_table.bind('<ButtonRelease-1>',self.getdata)
        self.show()
    def show(self):
        con=connect_db()
        mycur= con.cursor()
        try:
            sql="SELECT * FROM supplier"
            mycur.execute(sql)
            rows=mycur.fetchall()
            self.sup_table.delete(*self.sup_table.get_children())
            for row in rows: self.sup_table.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    def getdata(self,ev):
        try:
            f= self.sup_table.focus()
            content= (self.sup_table.item(f))
            row=content['values']
           
            self.var_sup_id.set(row[1])
            self.var_sup_salename.set(row[2])
            self.var_sup_contact.set(row[3])
            self.var_sup_cmpname.set(row[4])
            self.var_sup_cmpphone.set(str(row[5]))
            self.var_sup_remark.set(row[7])
            self.txt_address.delete('1.0',END)
            self.txt_address.insert(END,row[6])

        except IndexError as ex:
            messagebox.showerror("Ops!","There is no record on table or Be Careful to click on row",parent=self.root)
    def add(self):
        con=connect_db() #module from database.py
        mycur= con.cursor()
 
        try:
            if self.var_sup_id.get()=="":
                messagebox.showerror("Error","Supplier ID missing!",parent=self.root)
            else:
                sql="SELECT * FROM supplier where supid=%s"
                val=(self.var_sup_id.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Duplicate supplier\'s id",parent=self.root)
                else:
                    sql="INSERT INTO supplier(supid,name,contact,companyName,companyPhone,address,remark)VALUES(%s,%s,%s,%s,%s,%s,%s)"
                    val=(self.var_sup_id.get(),self.var_sup_salename.get(),
                         self.var_sup_contact.get(),self.var_sup_cmpname.get(),
                         self.var_sup_cmpphone.get(),self.txt_address.get('1.0',END),
                         self.var_sup_remark.get()
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
            if self.var_sup_id.get()=="":
                messagebox.showerror("Error","Supplier\'s ID missing!",parent=self.root)
            else:
                sql="SELECT supid FROM supplier where supid=%s"
                val=(self.var_sup_id.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Supplier\'s ID",parent=self.root)
                else:
                    # "eid","name","nrc","gen","cont","dob","type","sal","addr"
                    sql="UPDATE supplier SET name=%s,contact=%s,companyName=%s,companyPhone=%s,address=%s,remark=%s where supid=%s"
                    val=(self.var_sup_salename.get(),self.var_sup_contact.get(),
                         self.var_sup_cmpname.get(),self.var_sup_cmpphone.get(),
                         self.txt_address.get('1.0',END),
                         self.var_sup_remark.get(),
                         self.var_sup_id.get()

                         )
                    
        ##### isStatusOK is checking whether one of the fields missing of not
                    if self.isStatusOK(val):
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
            if self.var_sup_id.get()=="":
                messagebox.showerror("Error","Supplier ID missing!",parent=self.root)
            else:
                sql="SELECT supid FROM supplier where supid=%s"
                val=(self.var_sup_id.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row==None:
                    messagebox.showerror("Error","There is no record found with your Supplier\'s ID",parent=self.root)
                else:
                    ans=messagebox.askyesno("Confirmation",f"Are you sure want to Delete {self.var_sup_id.get()}?")
                    if ans==True:
                        mycur.execute("DELETE FROM supplier where supid=%s",(self.var_sup_id.get(),))
                        con.commit()
                        con.close()
                        messagebox.showinfo("Success","Your Record has been Deleted from Database!",parent=self.root)
                        self.clear()
                        self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    def clear(self):
        self.var_sup_searchby.set("Select")
        self.var_sup_searchtxt.set("")
        self.var_sup_id.set("")
        self.var_sup_salename.set("")
        self.var_sup_cmpname.set("")
        self.var_sup_cmpphone.set("")
        self.var_sup_contact.set("")
        self.var_sup_remark.set("")
        self.txt_address.delete('1.0',END)
        self.show()
    def search(self):
        con=connect_db()
        mycur= con.cursor()
        try:
            if self.var_sup_searchby.get()=="Select":
                messagebox.showerror("Error","Choose some option in \"Search By option\"",parent=self.root)
            elif self.var_sup_searchtxt.get()=="":
                #self.var_emp_searchtxt.get()==""
                messagebox.showerror("Error","Search input should be filled",parent=self.root)
            else:
                mycur.execute("SELECT * FROM supplier where "+self.var_sup_searchby.get()+" Like '%"+self.var_sup_searchtxt.get()+"%'")
                rows= mycur.fetchall()

                if len(rows)!=0:
                    self.sup_table.delete(*self.sup_table.get_children())
                    for row in rows:
                        self.sup_table.insert('',END,values=row)
                else:
                    messagebox.showinfo("Information","No record found on system",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"We got some error at supplier {ex}",parent=self.root)
      
    def var_creation(self):
        self.var_sup_searchby=StringVar()
        self.var_sup_searchtxt=StringVar()
        self.var_sup_id=StringVar()
        self.var_sup_salename=StringVar()
        self.var_sup_cmpname=StringVar()
        self.var_sup_cmpphone=StringVar()
        self.var_sup_contact=StringVar()
        self.var_sup_remark=StringVar()
        # self.var_sup_remark="_"

if __name__=="__main__":
    root= Tk()
    app= supplier(root)
    root.mainloop()