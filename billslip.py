# import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database import connect_db
from tool_ import isStatusOK,loadConfig
import os
from PIL import ImageTk,Image
class billslip:
    def __init__(self,root) -> None:
        self.root=root
        self.ROOT_DIR = loadConfig()['images']
        self.ROOT_PATH= loadConfig()['path']
        self.iconimg=ImageTk.PhotoImage(file=f'{self.ROOT_DIR}icon.png')
        self.root.iconphoto(False,self.iconimg)
        
        self.root.geometry("1100x500+220+130")
        self.root.title("Bill Slip @Inventory Management System | Developed by KG")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()
        self.var_creation()

        ##===============Label Frame====================================
        searchFrame=LabelFrame(self.root,text="Search Invoices",bg="white",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE)
        searchFrame.place(x=50,y=40,width=650,height=65)

        lbl_invoice=Label(searchFrame,text="Invoice",justify=CENTER,font=("goudy old style",15),bg="white")
        lbl_invoice.place(x=10,y=5,width=120)

        txt_search=Entry(searchFrame,textvariable=self.var_inv_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=140,y=5)
        btn_search=Button(searchFrame,command=self.search,text="Search",font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=3,width=120,height=30)
        btn_clear=Button(searchFrame,command=self.clear,text="Clear",font=("goudy old style",15),bg="gray",fg="white",cursor="hand2").place(x=490,y=3,width=120,height=30)

        #===================Employee Details==============================
        title_bill= Label(self.root,text="Bill lists and Details",bg="#0f4d7d",fg="white",font=("goudy old style",15,"bold")).place(x=5,y=10,width=1090)

        
        ##==========table frame====================================
        bill_frame= Frame(self.root,bd=3,relief=RIDGE,bg="#ff0011")
        bill_frame.place(x=20,y=110,height=380,width=700)

        frame_left=Frame(bill_frame,bd=4,relief=RIDGE,bg="white")
        frame_left.place(x=3,y=2,width=330,height=370)

        scrolly= Scrollbar(frame_left,orient=VERTICAL)
        self.list_sale=Listbox(frame_left,yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.list_sale.yview)
        self.list_sale.pack(fill=BOTH,expand=1)
        self.list_sale.bind('<ButtonRelease-1>',self.get_data)

        frame_right=Frame(bill_frame,bd=4,relief=RIDGE,bg="white")
        frame_right.place(x=340,y=2,width=350,height=370)

        lbl_p= Label(frame_right,text="Billing Area",font=("Elephant",16,"bold"),bg="#009688",fg="white")
        lbl_p.pack(side=TOP,fill=X)
        scrolly1= Scrollbar(frame_right,orient=VERTICAL)
        scrolly1.pack(side=RIGHT,fill=Y)

        self.txt_bill=Text(frame_right,yscrollcommand=scrolly1.set)
        self.txt_bill.pack(fill=BOTH,expand=1)
        scrolly1.config(command=self.txt_bill.yview)
        
        ############### animate image#########################
        self.sideimg=Image.open(f'{self.ROOT_DIR}parts\\1.png')
        self.sideimg=self.sideimg.resize((350,300),Image.LANCZOS)
        self.sideimg=ImageTk.PhotoImage(self.sideimg)
        
        self.lbl_image=Label(self.root,image=self.sideimg,bg="lightyellow")
        self.lbl_image.place(x=730,y=130)
        self.counter=0
        self.files_=os.listdir(f'{self.ROOT_DIR}parts\\')
        self.animatePics()
        self.show()
    def show(self):
        del self.bill_list[:]
        self.inv_files=os.listdir(f'{self.ROOT_PATH}invoices')
        # print(self.inv_files)
        self.list_sale.delete(0,END)
        for d in self.inv_files:
            if d.split('.')[-1]=='txt':
                self.list_sale.insert(END,d)
                self.bill_list.append(d.split('.')[0])
    def get_data(self,ev):
        index_=self.list_sale.curselection()
        file_name=self.list_sale.get(index_)
        print(file_name)
        self.txt_bill.config(state=NORMAL)
        self.txt_bill.delete('1.0',END)
        with open(f'{self.ROOT_PATH}invoices\\{file_name}','r') as fi:
            txt=fi.read()
            self.txt_bill.insert(END,txt)
            self.txt_bill.config(state=DISABLED)
            fi.close()
    def animatePics(self):
        if self.counter<len(self.files_):
            self.animimg=Image.open(f'{self.ROOT_DIR}parts\\{self.files_[self.counter]}')
            self.animimg=self.animimg.resize((350,300),Image.LANCZOS)
            self.animimg=ImageTk.PhotoImage(self.animimg)
            self.lbl_image.config(image=self.animimg)
            self.counter+=1
        else: self.counter=0           
        self.lbl_image.after(3000,self.animatePics)
    def clear(self):
        self.show()
        self.txt_bill.config(state=NORMAL)
        self.var_inv_searchtxt.set("")
        self.txt_bill.delete('1.0',END)
    def search(self):
        try:
            if self.var_inv_searchtxt.get()=="":
                messagebox.showerror("Error","Invoice Number should be filled",parent=self.root)
            else:
                if self.var_inv_searchtxt.get() in self.bill_list:
                    file_=open(f'{self.ROOT_PATH}invoices\\{self.var_inv_searchtxt.get()}.txt','r')
                    self.txt_bill.config(state=NORMAL)
                    self.txt_bill.delete('1.0',END)
                    for f in file_:
                        self.txt_bill.insert(END,f)
                    file_.close()

                else:
                    messagebox.showerror("Error","Invalid invoice number",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",str(ex),parent=self.root)

    def var_creation(self):
        self.var_inv_searchtxt=StringVar()
        self.bill_list=[]

if __name__=="__main__":
    root= Tk()
    app= billslip(root)
    root.mainloop()