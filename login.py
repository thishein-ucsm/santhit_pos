import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image,ImageTk
from os import path
from database import *
from tool_ import *
from ims import IMS
from signup import *
from bill import *
from forget_pass import forget_
class login:
    def __init__(self,root) -> None:
        self.root=root
        self.createVariable()
        self.ROOT_DIR=loadConfig()['images']
        
        
        self.iconimg=ImageTk.PhotoImage(file=f"{self.ROOT_DIR}icon.png")
        self.root.iconphoto(False,self.iconimg)
        
        self.root.geometry("700x500+300+100")
        self.root.title("Inventory Management System | Developed by KG")
        self.root.config(bg="#fafafa")
        self.root.resizable(0,0)
        
        self.sideimg=ImageTk.PhotoImage(file=f"{self.ROOT_DIR}logo1.jpg")
        lbl_img=Label(self.root,image=self.sideimg,bd=0,bg="white")
        lbl_img.place(x=50,y=40)


        contentFrame=LabelFrame(self.root,bg="white",bd=2,relief=RIDGE)
        contentFrame.place(x=350,y=40,width=300,height=400)
        
        lbl_title=Label(contentFrame,text="Login",font=("Elephant",30,"bold"),bg="white")
        lbl_title.place(x=80,y=20)

        lbl_user=Label(contentFrame,text="Username",font=("times new roman",13),bg="white")
        lbl_user.place(x=50,y=100)
        txt_user=Entry(contentFrame,textvariable=self.var_user,bg="#fafafa")
        txt_user.place(x=50,y=130,width=200,height=25)

        lbl_password=Label(contentFrame,text="Password",font=("times new roman",13),bg="white")
        lbl_password.place(x=50,y=160)
        txt_pass=Entry(contentFrame,textvariable=self.var_pass,font=("Segoe MDL2 Assets",9),bg="#fafafa",show="\uE192")
        txt_pass.place(x=50,y=190,width=200,height=25)
        txt_pass.bind('<Return>',self.dologin)
        btn_login = Button(contentFrame,text="Login",command=self.checkUserCredential,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2")
        btn_login.place(x=50,y=240,width=200,height=28)
        lbl_or1=Label(contentFrame,text="________OR________",font=("times new roman",15,"bold"),bg="white",fg="lightgray")
        lbl_or1.place(x=50,y=270)
        btn_forget = Button(contentFrame,text="Forget Password?",command=self.forgetPassword,font=("goudy old style",15),bd=0,bg="white",fg="#00759e",activebackground="white",activeforeground="#00759e",cursor="hand2")
        btn_forget.place(x=50,y=300,width=200,height=25)
        lbl_or2=Label(contentFrame,text="________OR________",font=("times new roman",15,"bold"),bg="white",fg="lightgray")
        lbl_or2.place(x=50,y=330)
        btn_create = Button(contentFrame,text="Need New?",command=self.createUser,font=("goudy old style",15),bd=0,bg="white",fg="#00759e",activebackground="white",activeforeground="#00759e",cursor="hand2")
        btn_create.place(x=50,y=360,width=200,height=25)
    def dologin(self,event):
        self.checkUserCredential()
    def checkUserCredential(self):
        con=connect_db()
        mycur= con.cursor()
        sql="SELECT name from user where username=%s and password=%s "
        val=(self.var_user.get(),self.var_pass.get())
        if isStatusOK(val):
            mycur.execute(sql,val)
            row= mycur.fetchone()
            if row==None:
                messagebox.showinfo("Info","Invalid Username/password!",parent=self.root)
            else:
                status,usertype=self.checkStatus(self.var_user.get(),self.var_pass.get())
                # usertype=self.checkStatus(self.var_user.get(),self.var_pass.get())[1]
                # print(status,usertype)
                if status:
                    self.root.destroy()
                    app= Tk()

                    if usertype=="Cashier":
                        bill(app,row[0])
                    elif usertype=="Admin":
                        IMS(app,row[0])
                else:
                    messagebox.showerror("Error!","The user is not active.",parent=self.root)

        else:
            messagebox.showerror("Error","Please type both username and password!",parent=self.root)
    def createUser(self):
        self.root.destroy()
        root=Tk()
        app=signup(root)
        root.mainloop()
    def forgetPassword(self):
        self.root.destroy()
        new_win=Tk()
        forget_(new_win)
    def createVariable(self):
        self.var_user=StringVar()
        self.var_pass=StringVar()
        self.ROOT_DIR = ""

    def checkStatus(self,username,password):
        con=connect_db()
        mycur=con.cursor()
        sql="SELECT status,usertype FROM user where username=%s and password=%s"
        val=(username,password)
        mycur.execute(sql,val)
        row=mycur.fetchone()
        if row[0]=="active" and row[1].lower()=="cashier":
            return (True,"Cashier")
        elif row[0]=="inactive" :
            return (False,"")
        else: return (True,"Admin")

if __name__=="__main__":
    root= Tk()
    app= login(root)
    root.mainloop()