from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import os

from database import *
from tool_ import *
from ims import IMS
# from login import login as loin
class signup:
    def __init__(self,root) -> None:
        self.root=root
        self.ROOT_DIR = loadConfig()['images']
        self.iconimg=ImageTk.PhotoImage(file=f'{self.ROOT_DIR}icon.png')
        self.root.iconphoto(False,self.iconimg)
        
        self.root.geometry("700x500+300+100")
        self.root.title("TetLu Inventory Management System | Developed by KG")
        self.root.config(bg="#fafafa")
        self.root.resizable(0,0)
        self.createVariable()
        self.sideimg=ImageTk.PhotoImage(file=f'{self.ROOT_DIR}logo.jpg')
        lbl_img=Label(self.root,image=self.sideimg,bd=0)
        lbl_img.place(x=50,y=40)
        contentFrame=LabelFrame(self.root,bg="white",bd=2,relief=RIDGE)
        contentFrame.place(x=350,y=40,width=300,height=430)
        
        # login content frame
        lbl_title=Label(contentFrame,text="SignUp",font=("Elephant",30,"bold"),bg="white")
        lbl_title.place(x=80,y=10)

        lbl_user=Label(contentFrame,text="Username",font=("times new roman",13),bg="white")
        lbl_user.place(x=50,y=90)
        txt_user=Entry(contentFrame,textvariable=self.var_user,bg="#fafafa")
        txt_user.place(x=50,y=120,width=200,height=25)

        lbl_password=Label(contentFrame,text="Password",font=("times new roman",13),bg="white")
        lbl_password.place(x=50,y=150)
        txt_pass=Entry(contentFrame,textvariable=self.var_pass,font=("Segoe MDL2 Assets",9),bg="#fafafa",show="\uE192")
        txt_pass.place(x=50,y=180,width=200,height=25)
        
        lbl_cpassword=Label(contentFrame,text="Confirm Password",font=("times new roman",13),bg="white")
        lbl_cpassword.place(x=50,y=210)
        txt_cpass=Entry(contentFrame,textvariable=self.var_cpass,font=("Segoe MDL2 Assets",9),bg="#fafafa",show="\uE192")
        txt_cpass.place(x=50,y=240,width=200,height=25)
        txt_cpass.bind('<Return>',self.doCreate)
       
        btn_create = Button(contentFrame,text="Create",command=self.checkUserCredential,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2")
        btn_create.place(x=50,y=290,width=200,height=28)
        
        lbl_or2=Label(contentFrame,text="________OR________",font=("times new roman",15,"bold"),bg="white",fg="lightgray")
        lbl_or2.place(x=50,y=330)
        btn_login = Button(contentFrame,text="Already created?",command=self.doLogin,font=("goudy old style",15),bd=0,bg="white",fg="#00759e",activebackground="white",activeforeground="#00759e",cursor="hand2")
        btn_login.place(x=50,y=370,width=200,height=25)
    def doCreate(self,event):
        self.checkUserCredential()
    def checkUserCredential(self):
        con=connect_db()
        mycur= con.cursor()
        sql="SELECT name from user where username=%s"
        val=(self.var_user.get(),)
        if isStatusOK(val):
            mycur.execute(sql,val)
            row= mycur.fetchone()
            val=(self.var_user.get(),self.var_pass.get(),self.var_cpass.get())
            if row!=None:
                messagebox.showinfo("Info","Username already exists!",parent=self.root)
            elif len(self.var_pass.get())<8:
                messagebox.showerror("Error","Password must be at least 8 characters",parent=self.root)
            else:
                if isStatusOK(val) and isMatch(val[1],val[2]) :
                    
                    # self.root.destroy()
                    # ims= Tk()
                    # app= IMS(ims,row[0])
                    userid=generate_id("user","userid")
                    sql="INSERT INTO user(userid,username,password)VALUES(%s,%s,%s)"
                    val=(userid,self.var_user.get(),self.var_pass.get())
                    mycur.execute(sql,val)
                    con.commit()
                    con.close()
                    messagebox.showinfo("Info","Successfully created and inform to your admin to get activate account!",parent=self.root)
                    # root.mainloop()
                else:
                    messagebox.showerror("Info","Doesn't match or type both passsword and confirm password!",parent=self.root)

        else:
            messagebox.showerror("Error","Please type all the fields",parent=self.root)
    def doLogin(self):
        from login import login as loin
        self.root.destroy()
        root=Tk()
        app=loin(root)
        root.mainloop()
        
    def createVariable(self):
        self.var_user=StringVar()
        self.var_pass=StringVar()
        self.var_cpass=StringVar()
if __name__=="__main__":
    root= Tk()
    app= signup(root)
    root.mainloop()