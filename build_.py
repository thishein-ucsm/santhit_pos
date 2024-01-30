import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database import connect_db
from tool_ import isStatusOK,loadConfig
import os
from PIL import ImageTk,Image
from tkcalendar import Calendar

class buildeng:
    def __init__(self,root) -> None:
        self.root=root
        self.var_creation()

        self.iconimg=ImageTk.PhotoImage(file=f'{self.ROOT_DIR_images}icon.png')
        self.root.iconphoto(False,self.iconimg)
        
        self.root.geometry("1100x500+220+130")
        self.root.title("Builder @Inventory Management System | Developed by KG")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()
        title_build= Label(self.root,text="Grow and Shine",bg="#0f4d7d",fg="white",font=("goudy old style",15,"bold")).place(x=5,y=10,width=1090)
        
        left_frame=Frame(self.root,bg="lightgray",relief="flat")
        left_frame.place(x=50,y=50,width=400,height=400)
        lbl_build=Label(left_frame,text="Reshaping Devices",relief=RAISED,bg="#0f4d7d",fg="white",font=("goudy old style",15,"bold"))
        lbl_build.pack(side=TOP,padx=5,pady=5,fill=X)
        lbl_date=Label(left_frame,text="Created Date",bg="lightgray")
        lbl_date.place(x=5,y=40,width=100)
        txt_ctime= Entry(left_frame,textvariable=self.var_created_time,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=110,y=40,width=180)
        self.btn_date_picker=Button(left_frame,text="\uE1DC",command=self.openCalendar,font=("Segoe MDL2 Assets",14),bg="white")
        self.btn_date_picker.place(x=295,y=38,width=30)
        lbl_to_build=Label(left_frame,text="To build",bg="lightgray")
        lbl_to_build.place(x=5,y=80,width=100)
        self.cmb_to_build=ttk.Combobox(left_frame,textvariable=self.var_to_build,values=("Select",),state='readonly',justify=CENTER,font=("goudy old style",15))
        self.cmb_to_build.place(x=110,y=80,width=180)
        self.cmb_to_build.current(0)
        self.cmb_to_build.bind('<<ComboboxSelected>>',self.popCombo)
        lbl_date=Label(left_frame,text="Spare Item",bg="lightgray")
        lbl_date.place(x=5,y=120,width=100)
        self.cmb_aux=ttk.Combobox(left_frame,textvariable=self.var_aux,values=("Select",),state='readonly',justify=CENTER,font=("goudy old style",15))
        self.cmb_aux.place(x=110,y=120,width=180)
        self.cmb_aux.current(0)
        self.cmb_aux.bind('<<ComboboxSelected>>',self.popCombo2)

        lbl_cost=Label(left_frame,text="Cost",bg="lightgray")
        lbl_cost.place(x=5,y=160,width=100)

        self.txt_cost= Spinbox(left_frame,from_=0,to=500000,increment=100,justify=RIGHT)
        self.txt_cost.place(x=110,y=160,width=180)
        lbl_rmk=Label(left_frame,text="Remark",bg="lightgray")
        lbl_rmk.place(x=5,y=200,width=100)
        txt_remark= Entry(left_frame,textvariable=self.var_remark,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=110,y=200,width=180)
        
        btn_frame= Frame(left_frame,bg="white")
        btn_frame.place(x=2,y=300,width=395,height=38)
        btn_save=Button(btn_frame,text="Save",command=self.add,font=("goudy old style",15),bg="#33bbf9",fg="white",cursor="hand2").place(x=5,y=5,width=90,height=28)
        btn_update=Button(btn_frame,text="Update",command=self.update,font=("goudy old style",15),bg="#ff5722",fg="white",cursor="hand2").place(x=103,y=5,width=90,height=28)
        btn_delete=Button(btn_frame,text="Delete",command=self.delete,font=("goudy old style",15),bg="#009688",fg="white",cursor="hand2").place(x=200,y=5,width=90,height=28)
        btn_clear=Button(btn_frame,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=300,y=5,width=90,height=28)

        right_frame=Frame(self.root,bg="lightgray")
        right_frame.place(x=555,y=50,width=500,height=400)

        right_main= Frame(right_frame,bg="white")
        right_main.place(x=150,y=2,width=200,height=200)
        self.right_aux= Frame(right_frame,bg="lightblue",relief="raised")
        self.right_aux.place(x=5,y=204,width=490,height=190)
        self.showGallery()
        self.comboData()
    def comboData(self):
        conn=connect_db()
        sql_="select pid,name from product"
        cur=conn.cursor()
        cur.execute(sql_)
        result= cur.fetchall()
        self.list_combo.clear()
        for i in result:
            self.list_combo.append(f'{i[0]} : < {i[1]} >')
        self.cmb_to_build.config(values=self.list_combo)
        
        # print(self.list_combo)
    def popCombo(self,event):
        self.list_aux.clear()
        self.list_aux=self.list_combo.copy()
        temp=self.var_to_build.get()
        if temp in self.list_aux:
            self.list_aux.remove(temp)
        id_=self.extractID(self.var_to_build)
        self.showMainItem(id_)
        self.cmb_aux.config(values=self.list_aux)
    def popCombo2(self,event):
        self.extractID(self.var_aux)
    def extractID(self,cmb):
        temp=cmb.get()
        temp=temp.split(":")
        cmb.set(temp[0])
        return temp[0]
    def showMainItem(self,id_):
        pass
    def add(self):
        pass
    def update(self):
        pass
    def delete(self):
        pass
    def clear(self):
        self.var_created_time.set("")
        self.txt_cost.delete(0,"end")
        self.txt_cost.insert(0,"0")
        self.var_to_build.set("Select")
        self.var_aux.set("Select")
    def openCalendar(self):
        self.cal_win=Toplevel(self.root)
        self.cal_win.title("Calendar")
        x=self.btn_date_picker.winfo_rootx()
        y=self.btn_date_picker.winfo_rooty()
        self.cal_win.iconphoto(False,self.iconimg)

        self.cal_win.geometry(f"200x220+{x+50}+{y-50}")
        self.cal_win.resizable(0,0)
        year_ = int(datetime.datetime.now().strftime('%Y'))
        month_ = int(datetime.datetime.now().strftime('%m'))
        day_ = int(datetime.datetime.now().strftime('%d'))

        self.cal = Calendar(self.cal_win, date_pattern="dd/MM/yyyy",selectmode = 'day',year = year_, month = month_,day = day_)
        self.cal.pack(side=TOP,fill=X)
        ok = Button(self.cal_win,command=self.setDate,text="OK",bg="orange",fg="blue")
        ok.pack(side=BOTTOM,padx=5)
    def setDate(self):
        self.var_created_time.set(self.cal.get_date())
        self.cal_win.destroy()
    def showGallery(self):
        self.canvas = tk.Canvas(self.right_aux, width=200, height=200)
        self.canvas.pack()
        self.scrollbar = ttk.Scrollbar(self.right_aux, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")
        self.scrollbar.set(0, 1)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.bind("<MouseWheel>", self.change_image)
        self.current_index = 0
        self.show_image(self.current_index)
    def show_image(self,image_index):
        self.canvas.delete("all")  # Clear the canvas
        img_=Image.open(f'{self.ROOT_DIR_images}parts\\{self.files_[image_index]}')
        img_=img_.resize((200,200),Image.LANCZOS)

        image = ImageTk.PhotoImage(img_)
        self.canvas.create_image(0, 0, anchor="nw", image=image)
        self.canvas.image = image  
    def change_image(self,event):
        delta = event.delta
        if delta < 0:
            self.current_index = (self.current_index + 1) % len(self.files_)
        else:
            self.current_index = (self.current_index - 1) % len(self.files_)
        self.show_image(self.current_index)
        self.update_scrollbar()
    def update_scrollbar(self):
        self.scrollbar.set(self.current_index, self.current_index + 1)
    def var_creation(self):
        self.ROOT_DIR_images=loadConfig()['images']
        self.ROOT_DIR=loadConfig()['path']

        # auxiliry file name should be created in files
        self.files_=os.listdir(f'{self.ROOT_DIR_images}parts\\')
        self.list_combo=[]
        self.list_aux=[]
        self.var_created_time=StringVar()
        self.var_to_build=StringVar()
        self.var_aux=StringVar()
        self.var_remark=StringVar()
        self.var_remark.set("-")

        self.bill_list=[]

if __name__=="__main__":
    root= Tk()
    app= buildeng(root)
    root.mainloop()


    