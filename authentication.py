import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database import connect_db
from tool_ import isStatusOK,loadConfig
import os
from PIL import ImageTk
class authentication:
    def __init__(self,root) -> None:
        self.root=root
        self.ROOT_DIR = loadConfig()['images']
        self.iconimg=ImageTk.PhotoImage(file=f'{self.ROOT_DIR}icon.png')
        self.root.iconphoto(False,self.iconimg)
        
        self.root.geometry("1100x500+220+130")
        self.root.title("Authentication @Inventory Management System | Developed by KG")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()
        self.var_creation()

        ##===============Label Frame====================================
        searchFrame=LabelFrame(self.root,text="Search User",bg="white",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE)
        searchFrame.place(x=400,y=40,width=570,height=65)

        cmb_search=ttk.Combobox(searchFrame,textvariable=self.var_user_searchby,values=("Select","userid","name","username","password","email","status","created_time","usertype"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=5,width=180)
        cmb_search.current(0)

        txt_search=Entry(searchFrame,textvariable=self.var_user_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=5)
        btn_search=Button(searchFrame,command=self.search,text="Search",font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=3,width=150,height=30)

        #===================Employee Details==============================
        title_supplier= Label(self.root,text="User Details",bg="#0f4d7d",fg="white",font=("goudy old style",15,"bold")).place(x=5,y=10,width=1090)

        lbl_id= Label(self.root,text="UserID:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=50)
        lbl_name= Label(self.root,text="Name:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=90)
        lbl_username= Label(self.root,text="Username:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=130)
        
        txt_id= Entry(self.root,textvariable=self.var_user_id,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=170,y=50,width=180)       
        txt_name= Entry(self.root,textvariable=self.var_name,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=170,y=90,width=180)
        txt_username= Entry(self.root,textvariable=self.var_username,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=170,y=130,width=180)
        cmb_status=ttk.Combobox(self.root,textvariable=self.var_status,values=("Select","active","inactive"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_status.place(x=170,y=250,width=180)
        cmb_status.current(0)
        lbl_email=Label(self.root,text="Email:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=210)
        lbl_status= Label(self.root,text="Status:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=250)
        txt_email= Entry(self.root,textvariable=self.var_email,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=170,y=210,width=180)

        # lbl_cmpphone= Label(self.root,text="CmpPhone:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=210)
        # txt_cmpname= Entry(self.root,textvariable=self.var_cus_cmpname,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=170,y=170,width=180)
        # txt_cmpphone= Entry(self.root,textvariable=self.var_cus_cmpphone,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=170,y=210,width=180)
        lbl_pass= Label(self.root,text="Password:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=170)
        txt_pass= Entry(self.root,textvariable=self.var_password,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=170,y=170,width=180)


        lbl_created_time= Label(self.root,text="CreatedTime:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=290)
        # self.txt_address= Text(self.root,font=("goudy old style",15,"bold"),bg="lightyellow")
        # self.txt_address.place(x=170,y=250,width=180,height=100)
        txt_created_time= Entry(self.root,textvariable=self.var_user_created_time,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=170,y=290,width=180)
        lbl_usertype= Label(self.root,text="UserType:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=330)
        
        cmb_usertype=ttk.Combobox(self.root,textvariable=self.var_usertype,values=("Select","administrator","accountant","cashier","user"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_usertype.place(x=170,y=330,width=180)
        cmb_usertype.current(0)
        ##================Button Fram===========================
        btn_save=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="#33bbf9",fg="white",cursor="hand2").place(x=50,y=400,width=115,height=28)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="#ff5722",fg="white",cursor="hand2").place(x=200,y=400,width=115,height=28)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="#009688",fg="white",cursor="hand2").place(x=50,y=440,width=115,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=200,y=440,width=115,height=28)

        ##==========table frame====================================
        user_frame= Frame(self.root,bd=3,relief=RIDGE)
        user_frame.place(x=400,y=110,height=390,width=700)
        scrolly=Scrollbar(user_frame,orient=VERTICAL)
        scrollx=Scrollbar(user_frame,orient=HORIZONTAL)
        self.user_table=ttk.Treeview(user_frame,columns=("sr","userid","name","username","password","email","status","created_time","usertype"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.user_table.xview)
        scrolly.config(command=self.user_table.yview)
        self.user_table.heading("sr",text="Sr.")
        self.user_table.heading("userid",text="UserID")
        self.user_table.heading("name",text="Name")
        self.user_table.heading("username",text="username")
        self.user_table.heading("password",text="Password")
        self.user_table.heading("email",text="Email")

        self.user_table.heading("status",text="Status")
        self.user_table.heading("created_time",text="CreatedTime")
        self.user_table.heading("usertype",text="UserType")

        
        

        self.user_table["show"]="headings"
        self.user_table.column("sr",width=10)
        self.user_table.column("userid",width=90)
        self.user_table.column("name",width=100)
        self.user_table.column("username",width=100)
        self.user_table.column("password",width=130)
        self.user_table.column("email",width=170)

        self.user_table.column("status",width=100)
        self.user_table.column("created_time",width=100)
        self.user_table.column("usertype",width=100)

        self.user_table.pack(fill=BOTH,expand=1)
        self.user_table.bind('<ButtonRelease-1>',self.getdata)
        self.show()
    def show(self):
        con=connect_db()
        mycur= con.cursor()
        try:
            sql="SELECT * FROM user"
            mycur.execute(sql)
            rows=mycur.fetchall()
            self.user_table.delete(*self.user_table.get_children())
            for row in rows:
               self.user_table.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    def getdata(self,ev):
        try:
            f= self.user_table.focus()
            content= (self.user_table.item(f))
            row=content['values']
            
            self.var_user_id.set(row[1])
            self.var_name.set(row[2])
            self.var_username.set(row[3])
            self.var_password.set(row[4])
            self.var_email.set(row[5])
            self.var_status.set(row[6])
            self.var_user_created_time.set(row[7])
            self.var_usertype.set(row[8])


        except IndexError as ex:
            messagebox.showerror("Ops!","There is no record on table or Be Careful to click on row",parent=self.root)
    def add(self):
        con=connect_db() #module from database.py
        mycur= con.cursor()
 
        try:
            if self.var_user_id.get()=="":
                messagebox.showerror("Error","User ID missing!",parent=self.root)
            else:
                sql="SELECT * FROM user where userid=%s"
                val=(self.var_user_id.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Duplicate user\'s id",parent=self.root)
                else:
                    sql="INSERT INTO user(userid,name,username,password,email,status,created_time,usertype)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                    val=(self.var_user_id.get(),self.var_name.get(),
                         self.var_username.get(),self.var_password.get(),
                         self.var_email.get(),self.var_status.get(),
                         self.var_user_created_time.get(),self.var_usertype.get()
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
            if self.var_user_id.get()=="":
                messagebox.showerror("Error","User\'s ID missing!",parent=self.root)
            else:
                sql="SELECT userid FROM user where userid=%s"
                val=(self.var_user_id.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid User\'s ID",parent=self.root)
                else:
                    # "eid","name","nrc","gen","cont","dob","type","sal","addr"
                    sql="UPDATE user SET name=%s,username=%s,password=%s,email=%s,status=%s,created_time=%s,usertype=%s where userid=%s"
                    val=(self.var_name.get(),self.var_username.get(),
                         self.var_password.get(),self.var_email.get(),
                         self.var_status.get(),self.var_user_created_time.get(),
                         self.var_usertype.get(),self.var_user_id.get()

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
            if self.var_username.get()=="":
                messagebox.showerror("Error","Username missing!",parent=self.root)
            else:
                sql="SELECT userid FROM user where username=%s"
                val=(self.var_username.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row==None:
                    messagebox.showerror("Error","There is no record found with your User\'s ID",parent=self.root)
                else:
                    ans=messagebox.askyesno("Confirmation",f"Are you sure want to Delete {self.var_username.get()}?",parent=self.root)
                    if ans==True:
                        mycur.execute("DELETE FROM user where username=%s",(self.var_username.get(),))
                        con.commit()
                        con.close()
                        messagebox.showinfo("Success","Your Record has been Deleted from Database!",parent=self.root)
                        self.clear()
                        self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    def clear(self):
        self.var_user_searchby.set("Select")
        self.var_user_searchtxt.set("")
        self.var_user_id.set("")
        self.var_name.set("")
        self.var_username.set("")
        self.var_password.set("")
        self.var_email.set("")
        self.var_status.set("Select")
        self.var_user_created_time.set("")
        self.var_usertype.set("")

        self.show()
    def search(self):
        con=connect_db()
        mycur= con.cursor()
        try:
            if self.var_user_searchby.get()=="Select":
                messagebox.showerror("Error","Choose some option in \"Search By option\"",parent=self.root)
            elif self.var_user_searchtxt.get()=="":
                #self.var_emp_searchtxt.get()==""
                messagebox.showerror("Error","Search input should be filled",parent=self.root)
            else:
                mycur.execute("SELECT * FROM user where "+self.var_user_searchby.get()+" Like '%"+self.var_user_searchtxt.get()+"%'")
                rows= mycur.fetchall()

                if len(rows)!=0:
                    self.user_table.delete(*self.user_table.get_children())
                    for row in rows:
                        self.user_table.insert('',END,values=row)
                else:
                    messagebox.showinfo("Information","No record found on system",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",str(ex),parent=self.root)   
    def var_creation(self):
        self.var_user_searchby=StringVar()
        self.var_user_searchtxt=StringVar()
        self.var_user_id=StringVar()
        self.var_name=StringVar()
        self.var_status=StringVar()
        self.var_username=StringVar()
        self.var_password=StringVar()
        self.var_user_created_time=StringVar()
        self.var_email=StringVar()
        self.var_usertype=StringVar()
        # self.var_password="_"

if __name__=="__main__":
    root= Tk()
    app= authentication(root)
    root.mainloop()