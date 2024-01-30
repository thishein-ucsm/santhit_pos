import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database import connect_db
from tool_ import loadConfig,isStatusOK
from PIL import ImageTk,Image
class category:
    def __init__(self,root) -> None:
        self.root=root
        self.ROOT_DIR = loadConfig()['images']
        self.iconimg=ImageTk.PhotoImage(file=f'{self.ROOT_DIR}icon.png')
        self.root.iconphoto(False,self.iconimg)

        self.root.geometry("1100x500+220+130")
        self.root.title("Category @Inventory Management System | Developed by KG")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()
        self.var_creation()

        ##===============Label Frame====================================
        searchFrame=LabelFrame(self.root,text="Search Category",bg="white",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE)
        searchFrame.place(x=400,y=40,width=570,height=65)

        cmb_search=ttk.Combobox(searchFrame,textvariable=self.var_cat_searchby,values=("Select","catid","name"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=5,width=180)
        cmb_search.current(0)

        txt_search=Entry(searchFrame,textvariable=self.var_cat_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=5)
        btn_search=Button(searchFrame,command=self.search,text="Search",font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=3,width=150,height=30)

        #===================Category Details==============================
        title_= Label(self.root,text="Category Details",bg="#0f4d7d",fg="white",font=("goudy old style",15,"bold")).place(x=5,y=10,width=1090)

        lbl_id= Label(self.root,text="CatID:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=50)
        lbl_name= Label(self.root,text="Name:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=90)
        # lbl_contact= Label(self.root,text="Contact:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=130)
        
        txt_id= Entry(self.root,textvariable=self.var_cat_id,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=170,y=50,width=180)       
        txt_name= Entry(self.root,textvariable=self.var_cat_name,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=170,y=90,width=180)

        self.sideimg=Image.open(f'{self.ROOT_DIR}parts\\1.png')
        self.sideimg=self.sideimg.resize((350,300),Image.LANCZOS)
        self.sideimg=ImageTk.PhotoImage(self.sideimg)
        
        self.lbl_image=Label(self.root,image=self.sideimg,bg="lightyellow")
        self.lbl_image.place(x=30,y=130)
        self.counter=0
        self.files_=os.listdir(f'{self.ROOT_DIR}parts\\')
        self.animatePics()
        ##================Button Frame===========================
        btn_save=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="#33bbf9",fg="white",cursor="hand2").place(x=50,y=400,width=115,height=28)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="#ff5722",fg="white",cursor="hand2").place(x=200,y=400,width=115,height=28)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="#009688",fg="white",cursor="hand2").place(x=50,y=440,width=115,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=200,y=440,width=115,height=28)

        ##==========table frame====================================
        cat_frame= Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=400,y=110,height=390,width=700)
        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)
        self.cat_table=ttk.Treeview(cat_frame,columns=("sr","catid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.cat_table.xview)
        scrolly.config(command=self.cat_table.yview)
        self.cat_table.heading("sr",text="Sr.")
        self.cat_table.heading("catid",text="CatID")
        self.cat_table.heading("name",text="CategoryName")
        
        self.cat_table["show"]="headings"
        self.cat_table.column("sr",width=10)
        self.cat_table.column("catid",width=30)
        self.cat_table.column("name",width=300)
        self.cat_table.pack(fill=BOTH,expand=1)
        self.cat_table.bind('<ButtonRelease-1>',self.getdata)
        self.show()
    def show(self):
        con=connect_db()
        mycur= con.cursor()
        try:
            sql="SELECT * FROM category"
            mycur.execute(sql)
            rows=mycur.fetchall()
            self.cat_table.delete(*self.cat_table.get_children())
            for row in rows:
               self.cat_table.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    def getdata(self,ev):
        try:
            f= self.cat_table.focus()
            content= (self.cat_table.item(f))
            row=content['values']
            self.var_cat_id.set(row[1])
            self.var_cat_name.set(row[2])

        except IndexError as ex:
            messagebox.showerror("Ops!","There is no record on table or Be Careful to click on row",parent=self.root)
    def add(self):
        con=connect_db() #module from database.py
        mycur= con.cursor()
 
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error","Category ID missing!",parent=self.root)
            else:
                sql="SELECT * FROM category where catid=%s"
                val=(self.var_cat_id.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Duplicate category\'s id",parent=self.root)
                else:
                    sql="INSERT INTO category(catid,name)VALUES(%s,%s)"
                    val=(self.var_cat_id.get(),self.var_cat_name.get())
                    
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
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error","Category\'s ID missing!",parent=self.root)
            else:
                sql="SELECT catid FROM category where catid=%s"
                val=(self.var_cat_id.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Category\'s ID",parent=self.root)
                else:
                    # "eid","name","nrc","gen","cont","dob","type","sal","addr"
                    sql="UPDATE category SET name=%s where catid=%s"
                    val=(self.var_cat_name.get(),
                         self.var_cat_id.get()

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
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error","Category ID missing!",parent=self.root)
            else:
                sql="SELECT catid FROM category where catid=%s"
                val=(self.var_cat_id.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row==None:
                    messagebox.showerror("Error","There is no record found with your Category\'s ID",parent=self.root)
                else:
                    ans=messagebox.askyesno("Confirmation",f"Are you sure want to Delete {self.var_cat_id.get()}?",parent=self.root)
                    if ans==True:
                        mycur.execute("DELETE FROM category where catid=%s",(self.var_cat_id.get(),))
                        con.commit()
                        con.close()
                        messagebox.showinfo("Success","Your Record has been Deleted from Database!",parent=self.root)
                        self.clear()
                        self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    def clear(self):
        self.var_cat_searchby.set("Select")
        self.var_cat_searchtxt.set("")
        self.var_cat_id.set("")
        self.var_cat_name.set("")
        self.show()
    def search(self):
        con=connect_db()
        mycur= con.cursor()
        try:
            if self.var_cat_searchby.get()=="Select":
                messagebox.showerror("Error","Choose some option in \"Search By option\"",parent=self.root)
            elif self.var_cat_searchtxt.get()=="":
                #self.var_emp_searchtxt.get()==""
                messagebox.showerror("Error","Search input should be filled",parent=self.root)
            else:
                mycur.execute("SELECT * FROM category where "+self.var_cat_searchby.get()+" Like '%"+self.var_cat_searchtxt.get()+"%'")
                rows= mycur.fetchall()

                if len(rows)!=0:
                    self.cat_table.delete(*self.cat_table.get_children())
                    for row in rows:
                        self.cat_table.insert('',END,values=row)
                else:
                    messagebox.showinfo("Information","No record found on system",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",str(ex),parent=self.root)  
    def animatePics(self):
        if self.counter<len(self.files_):
            self.animimg=Image.open(f'{self.ROOT_DIR}parts\\{self.files_[self.counter]}')
            self.animimg=self.animimg.resize((350,250),Image.LANCZOS)
            self.animimg=ImageTk.PhotoImage(self.animimg)
            self.lbl_image.config(image=self.animimg)
            self.counter+=1
        else: self.counter=0           
        self.lbl_image.after(3000,self.animatePics)
    def var_creation(self):
        self.var_cat_searchby=StringVar()
        self.var_cat_searchtxt=StringVar()
        self.var_cat_id=StringVar()
        self.var_cat_name=StringVar()

        # self.var_cat_remark="_"

if __name__=="__main__":
    root= Tk()
    app= category(root)
    root.mainloop()