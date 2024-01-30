from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import os
from database import *
from tool_ import *
from ims import IMS
from signup import *
class forget_:
    def __init__(self,root) -> None:
        self.root=root
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.iconimg=ImageTk.PhotoImage(file=f'{self.ROOT_DIR}\\images\\icon1.png')
        self.root.iconphoto(False,self.iconimg)
        
        self.root.geometry("700x500+300+100")
        self.root.title("Inventory Management System | Developed by KG")
        self.root.config(bg="#fafafa")
        self.root.resizable(0,0)
        self.createVariable()
        self.sideimg=ImageTk.PhotoImage(file=f'{self.ROOT_DIR}\\images\\Background.png')
        lbl_img=Label(self.root,image=self.sideimg,bd=0)
        lbl_img.place(x=50,y=40)
        self.contentFrame=LabelFrame(self.root,bg="white",bd=2,relief=RIDGE)
        self.contentFrame.place(x=350,y=40,width=300,height=400)
        
        # login content frame
        lbl_title=Label(self.contentFrame,text="Reset",font=("Elephant",30,"bold"),bg="white")
        lbl_title.place(x=80,y=20)

        lbl_user=Label(self.contentFrame,text="Username",font=("times new roman",13),bg="white")
        lbl_user.place(x=50,y=90)
        txt_user=Entry(self.contentFrame,textvariable=self.var_user,bg="#fafafa")
        txt_user.place(x=50,y=120,width=200,height=25)
        lbl_name=Label(self.contentFrame,text="Name",font=("times new roman",13),bg="white")
        lbl_name.place(x=50,y=150)
        txt_name=Entry(self.contentFrame,textvariable=self.var_name,bg="#fafafa")
        txt_name.place(x=50,y=180,width=200,height=25)


        lbl_password=Label(self.contentFrame,text="Email",font=("times new roman",13),bg="white")
        lbl_password.place(x=50,y=210)
        txt_email=Entry(self.contentFrame,textvariable=self.var_email,font=("Segoe MDL2 Assets",13),bg="#fafafa")
        txt_email.place(x=50,y=240,width=200,height=25)
        # lbl_new_pass=Label(self.contentFrame,text="New Password",font=("times new roman",13),bg="white")
        # lbl_new_pass.place(x=50,y=270)
        # txt_new_pass=Entry(self.contentFrame,textvariable=self.var_new_pass,font=("Segoe MDL2 Assets",9),bg="#fafafa",show="\uE192")
        # txt_new_pass.place(x=50,y=300,width=200,height=25)
        txt_email.bind('<Return>',self.dologin)
        btn_login = Button(self.contentFrame,text="Reset",command=self.reset,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2")
        btn_login.place(x=50,y=350,width=200,height=28)
        # lbl_or1=Label(self.contentFrame,text="________OR________",font=("times new roman",15,"bold"),bg="white",fg="lightgray")
        # lbl_or1.place(x=50,y=270)
        # btn_forget = Button(self.contentFrame,text="Forget Password?",command=self.forgetPassword,font=("goudy old style",15),bd=0,bg="white",fg="#00759e",activebackground="white",activeforeground="#00759e",cursor="hand2")
        # btn_forget.place(x=50,y=300,width=200,height=25)
        # lbl_or2=Label(self.contentFrame,text="________OR________",font=("times new roman",15,"bold"),bg="white",fg="lightgray")
        
        # lbl_or2.place(x=50,y=330)
        # btn_create = Button(self.contentFrame,text="Need New?",command=self.createUser,font=("goudy old style",15),bd=0,bg="white",fg="#00759e",activebackground="white",activeforeground="#00759e",cursor="hand2")
        # btn_create.place(x=50,y=360,width=200,height=25)
    def dologin(self,event):
        self.reset()
    def reset(self):
        con=connect_db()
        mycur= con.cursor()
        sql="SELECT name from user where username=%s and name=%s and email=%s "
        val=(self.var_user.get(),self.var_name.get(),self.var_email.get())
        if isStatusOK(val):
            mycur.execute(sql,val)
            row= mycur.fetchone()
            if row==None:
                messagebox.showinfo("Info","Invalid Username/name/email!",parent=self.root)
            else:
                if self.checkStatus(self.var_user.get(),self.var_name.get(),self.var_email.get()):
                    self.resetPage()
                    # if messagebox.askyesno("Reset?","Are you sure you want to reset your password?"):
                        # sql="UPDATE user SET password=%s,status=default where username=%s and name=%s and email=%s"
                        # val=(self.var_new_pass.get(),self.var_user.get(),self.var_name.get(),self.var_email.get())
                        # mycur.execute(sql,val)
                        # con.commit()
                        # con.close()
                        # messagebox.showinfo("Reset","Successfully reseted your password.\nPlease contact the admin for activation.")
                        # ent_list=[self.var_user,self.var_name,self.var_email,self.var_new_pass]
                        
                        # clear(ent_list,None)
                    # self.root.destroy()
                    # ims= Tk()
                    # app= IMS(ims,row[0])
                    # # messagebox.showinfo("Info","Successfully Login!",parent=self.root)
                    # ims.mainloop()
                else:
                    messagebox.showerror("Error!","The user is not active.",parent=self.root)

        else:
            messagebox.showerror("Error","Please type both username and password!",parent=self.root)
    def resetPage(self):
        self.contentFrame.place_forget()
        self.resetFrame=LabelFrame(self.root,bg="white",bd=2,relief=RIDGE)
        self.resetFrame.place(x=350,y=40,width=300,height=400)       
        lbl_title=Label(self.resetFrame,text="Create",font=("Elephant",30,"bold"),bg="white")
        lbl_title.place(x=80,y=20)
        lbl_user=Label(self.resetFrame,text="New Password",font=("times new roman",13),bg="white")
        lbl_user.place(x=50,y=90)
        txt_user=Entry(self.resetFrame,textvariable=self.var_new_pass,bg="#fafafa",show="\uE192")
        txt_user.place(x=50,y=120,width=200,height=25)
        lbl_name=Label(self.resetFrame,text="Confirm New Password",font=("times new roman",13),bg="white")
        lbl_name.place(x=50,y=150)
        txt_name=Entry(self.resetFrame,textvariable=self.var_c_new_pass,bg="#fafafa",show="\uE192")
        txt_name.place(x=50,y=180,width=200,height=25)


        # lbl_password=Label(self.resetFrame,text="Email",font=("times new roman",13),bg="white")
        # lbl_password.place(x=50,y=210)
        # txt_email=Entry(self.resetFrame,textvariable=self.var_email,font=("Segoe MDL2 Assets",13),bg="#fafafa")
        # txt_email.place(x=50,y=240,width=200,height=25)
        # lbl_new_pass=Label(self.contentFrame,text="New Password",font=("times new roman",13),bg="white")
        # lbl_new_pass.place(x=50,y=270)
        # txt_new_pass=Entry(self.contentFrame,textvariable=self.var_new_pass,font=("Segoe MDL2 Assets",9),bg="#fafafa",show="\uE192")
        # txt_new_pass.place(x=50,y=300,width=200,height=25)
        # txt_email.bind('<Return>',self.dologin)
        btn_update = Button(self.resetFrame,text="Update",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2")
        btn_update.place(x=50,y=350,width=200,height=28)
    def update(self):
        con=connect_db()
        mycur= con.cursor()    
        if messagebox.askyesno("Reset?","Are you sure you want to reset your password?"):
            sql="UPDATE user SET password=%s,status=default where username=%s and name=%s and email=%s"
            val=(self.var_new_pass.get(),self.var_user.get(),self.var_name.get(),self.var_email.get())
            mycur.execute(sql,val)
            con.commit()
            con.close()
            messagebox.showinfo("Reset","Successfully reseted your password.\nPlease contact the admin for activation.")
            ent_list=[self.var_user,self.var_name,self.var_email,self.var_new_pass]
            
            clear(ent_list,None)
    def createUser(self):
        self.root.destroy()
        root=Tk()
        app=signup(root)
        root.mainloop()
    def forgetPassword(self):
        messagebox.showinfo("Info ","Password forget",parent=self.root)
    def createVariable(self):
        self.var_user=StringVar()
        self.var_email=StringVar()
        self.var_name=StringVar()
        self.var_new_pass=StringVar()
        self.var_c_new_pass=StringVar()
    def checkStatus(self,username,name,email):
        con=connect_db()
        mycur=con.cursor()
        sql="SELECT status FROM user where username=%s and name=%s and email=%s"
        val=(username,name,email)
        mycur.execute(sql,val)
        row=mycur.fetchone()
        if row[0]=="active":
            return True
        else: return False

if __name__=="__main__":
    root= Tk()
    app= forget_(root)
    root.mainloop()