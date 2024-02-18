import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from typing import Any
from database import connect_db
from tool_ import generate_time, generate_timestamp, isStatusOK,loadConfig,   value_with_commas, value_without_commas
from PIL import ImageTk
import os
from tkcalendar import Calendar

class wallet:
        def __init__(self,root) -> None:
            self.root=root
            self.ROOT_DIR = loadConfig()['images'] 
                
            self.iconimg=ImageTk.PhotoImage(file=f'{self.ROOT_DIR}icon.png')
            self.root.iconphoto(False,self.iconimg)
            self.root.geometry("1100x500+220+130")
            self.root.title("Buy @Inventory Management System | Developed by KG")
            self.root.config(bg="white")
            self.root.resizable(False,False)
            self.root.focus_force()
            self.var_creation()

            ##===============Label Frame====================================
            searchFrame=LabelFrame(self.root,text="Search Wallet",bg="white",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE)
            searchFrame.place(x=400,y=40,width=570,height=65)
            cmb_search=ttk.Combobox(searchFrame,textvariable=self.var_wallet_searchby,values=("Select","description","deposit","withdraw","type","date","exp_date","created_time"),state='readonly',justify=CENTER,font=("goudy old style",15))
            cmb_search.place(x=10,y=5,width=180)
            cmb_search.current(0)

            txt_search=Entry(searchFrame,textvariable=self.var_wallet_searchtxt,font=("goudy old style",15),justify=CENTER,bg="lightyellow").place(x=200,y=5)
            btn_search=Button(searchFrame,command=self.search,text="Search",font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=3,width=150,height=30)
            #===================Employee Details==============================
            title_wallet= Label(self.root,text="Wallet Details",bg="#0f4d7d",fg="white",font=("goudy old style",15,"bold")).place(x=5,y=10,width=1090)
            self.lbl_balance=Label(self.root,text=self.get_balance(),bg="light green",font=("goudy old style",40,"bold"))
            self.lbl_balance.place(x=60,y=45)
            lbl_list=["Date","Description","Deposit","Withdraw","Balance"]
            lbl_y=130
            for i in lbl_list:
                Label(self.root,text=i,bg="white",font=("goudy old style",15,"bold")).place(x=30,y=lbl_y)
                lbl_y+=50

            Entry(self.root,textvariable=self.var_date,state="readonly",font=("goudy old style",15,"bold"),readonlybackground="lightyellow").place(x=150,y=130,width=180)
            self.btn_date_picker=Button(self.root,text="\uE1DC",command=None,font=("Segoe MDL2 Assets",14),bg="white")
            self.btn_date_picker.place(x=355,y=130,width=30)
            self.btn_date_picker.config(command=lambda :self.openCalendar(self.var_date))
            en_list=[self.var_description,self.var_deposit,self.var_withdraw,self.var_type]
            en_y=180
            for i in en_list:
                 Entry(self.root,textvariable=i,state="normal",font=("goudy old style",15,"bold"),background="lightyellow").place(x=150,y=en_y,width=180)
                 en_y+=50
        
            btn_save=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="#33bbf9",fg="white",cursor="hand2").place(x=70,y=420,width=115,height=28)
            btn_update=Button(self.root,text="Update",command=self.update,state="normal",font=("goudy old style",15),bg="#ff5722",fg="white",cursor="hand2")
            btn_update.place(x=220,y=420,width=115,height=28)
            btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="#009688",fg="white",cursor="hand2").place(x=70,y=460,width=115,height=28)
            btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=220,y=460,width=115,height=28)
            
            emp_frame= Frame(self.root,bd=3,relief=RIDGE)
            emp_frame.place(x=400,y=110,height=390,width=700)
            scrolly=Scrollbar(emp_frame,orient=VERTICAL)
            scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)
            self.pro_table=ttk.Treeview(emp_frame,columns=("1","2","3","4","5","6"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
            scrollx.pack(side=BOTTOM,fill=X)
            scrolly.pack(side=RIGHT,fill=Y)
            scrollx.config(command=self.pro_table.xview)
            scrolly.config(command=self.pro_table.yview)

            self.pro_table.heading("1",text="ID")
            self.pro_table.heading("2",text="Date")
            self.pro_table.heading("3",text="Description")
            self.pro_table.heading("4",text="Deposit")
            self.pro_table.heading("5",text="Withdraw")
            self.pro_table.heading("6",text="Balance")
            
            self.pro_table["show"]="headings"
            self.pro_table.column("1",width=100)
            self.pro_table.column("2",width=80)
            self.pro_table.column("3",width=180)
            self.pro_table.column("4",width=100,anchor="e")
            self.pro_table.column("5",width=100,anchor="e")
            self.pro_table.column("6",width=100,anchor="e")

            self.pro_table.pack(fill=BOTH,expand=1)
            self.pro_table.bind('<ButtonRelease-1>',self.getdata)
            self.show()

        def getdata(self,event):
            try:
                f= self.pro_table.focus()
                content= (self.pro_table.item(f))
                row=content['values']
                self.var_id.set(row[0])
                self.var_description.set(row[2])
                self.var_deposit.set(value_with_commas(row[3]))
                self.var_withdraw.set(value_with_commas(row[4]))
                self.var_type.set(row[5])
                self.var_date.set(row[1])
            except IndexError as ex:
                messagebox.showerror("Just Click on row!","There is no record on table or Be Careful to click on row",parent=self.root)
        def show(self):
                con=connect_db()
                mycur= con.cursor()
                try:
                    sql="SELECT id,date,description,deposit,withdraw,balance FROM wallet"
                    mycur.execute(sql)
                    rows=mycur.fetchall()
                    self.pro_table.delete(*self.pro_table.get_children())
                    for row in rows:
                        self.pro_table.insert('',END,values=row)
                    self.lbl_balance.config(text=value_with_commas(self.get_balance()))
                except Exception as ex:
                    messagebox.showerror("Error1",f"Error due to : {str(ex)}",parent=self.root)
        def add(self):
            con=connect_db()
            mycur=con.cursor()
            try:
                var_tuple=(self.var_description.get(),
                                self.var_deposit.get(),self.var_withdraw.get(),
                                self.var_date.get(),
                                )
                if isStatusOK(var_tuple):
                    if self.var_withdraw.get().isdigit() and self.var_deposit.get().isdigit():
                        created_time=generate_time()
                        if created_time==False:
                            messagebox.showerror("Error!","Cannot sync with sever.\n Check your internet connection and try again.\n(This can also occur due to sever error.)",parent=self.root)
                        else:
                            self.save_wallet()
                            self.clear()
                            messagebox.showinfo("Message","Successfully inserted into Database!",parent=self.root)

                            self.show()
                            con.close() 
                    else:
                        messagebox.showerror("Amount Input Error","Deposit and Withdraw must be digits(0-9).",parent=self.root)

                else:
                    messagebox.showerror("Error1","You are missing some data!",parent=self.root)
            except Exception as ex:
                messagebox.showerror("Error2",f"Error due to : {(ex)}",parent=self.root)
        def update(self):
            con=connect_db()
            mycur=con.cursor()
            try:
                var_tuple=(self.var_description.get(),
                            self.var_deposit.get(),self.var_withdraw.get(),
                            self.var_type.get(),
                            self.var_date.get(),
                        )
             
                if isStatusOK(var_tuple):
                    self.var_deposit.set(value_without_commas(self.var_deposit.get()))
                    self.var_withdraw.set(value_without_commas(self.var_withdraw.get()))
                    
                    if self.var_deposit.get().isdigit() and self.var_withdraw.get().isdigit():
                        self.update_wallet()
                        messagebox.showinfo("Update OK","Successfully updated into Database!",parent=self.root)
                        self.clear()

                        self.show()
                        con.close() 
                    else:
                        messagebox.showerror("Amount Input Error","Deposit and Withdraw must be digits(0-9).",parent=self.root)

            except Exception as ex:
                messagebox.showerror("Error3",f"Error due to : {str(ex)}",parent=self.root)
        def delete(self):
            con=connect_db() #module from database.py
            mycur=con.cursor()
            try:
                var_tuple=(self.var_id.get(),)
                if isStatusOK(var_tuple):
                    if messagebox.askyesno("Confirmation","Are you sure want to delete the item?",parent=self.root):
                        self.delete_wallet()
                        messagebox.showinfo("Success","Your Record has been Deleted from Database!",parent=self.root)
                        self.clear()
                        self.show()
                                         
            except Exception as ex:
                messagebox.showerror("Error3",f"Error due to : {str(ex)}",parent=self.root)
        def save_wallet(self):
            self.var_id.set(generate_timestamp("%y%m%d%H%M%S"))
            deposit=self.var_deposit.get()
            withdraw=self.var_withdraw.get()
            date_=self.var_date.get()
            con=connect_db()
            mycur= con.cursor()
            sql=f"select balance from wallet order by sr desc limit 1"
            mycur.execute(sql)
            row=mycur.fetchone()
            if row==None:
                balance=0+int(deposit)-int(withdraw)
            else:
                balance=int(row[0])+int(deposit)-int(withdraw)
            sql="insert into wallet(id,description,deposit,withdraw,balance,date) values (%s,%s,%s,%s,%s,%s)"
            val=(self.var_id.get(),self.var_description.get(),deposit,withdraw,balance,date_)
            mycur.execute(sql,val)
            con.commit()
            con.close()
        def update_wallet(self):
            deposit=self.var_deposit.get()
            withdraw=self.var_withdraw.get()
            con=connect_db()
            mycur=con.cursor()
            # request old balance, deposit, withdraw
            sql="select sr,deposit,withdraw,balance from wallet where id=%s"
            val=(self.var_id.get(),)
            mycur.execute(sql,val)
            result=mycur.fetchone()
            sr=0
            old_depo=0
            old_with=0
            old_bal=0
            if result:
                sr=result[0]
                old_depo=int(result[1])
                old_with=int(result[2])
                old_bal=int(result[3])

                old_dif=old_depo-old_with
                new_dif=int(self.var_deposit.get())-int(self.var_withdraw.get())
                adj=0
                if old_dif != new_dif:
                    adj=old_dif-new_dif
                    if adj>0:
                        old_bal-=abs(adj)
                        self.adjust_wallet(sr,abs(adj),"minus")
                    elif adj<0:
                        old_bal+=abs(adj)
                        self.adjust_wallet(sr,abs(adj),"plus")

                    sql="update wallet set description=%s,deposit=%s,withdraw=%s,balance=%s,date=%s where sr=%s"
                    val=(self.var_description.get(),self.var_deposit.get(),self.var_withdraw.get(),old_bal,self.var_date.get(),sr)
                    mycur.execute(sql,val)
                    con.commit()
                else:
                    sql="update wallet set description=%s,date=%s where sr=%s"
                    val=(self.var_description.get(),self.var_date.get(),sr)
                    mycur.execute(sql,val)
                    con.commit()
                con.close()
        def delete_wallet(self):
            con=connect_db()
            mycur=con.cursor()
            #call adj function and then delete
            con=connect_db()
            mycur=con.cursor()
            sql="select sr,deposit,withdraw from wallet where id=%s"
            val=(self.var_id.get(),)

            mycur.execute(sql,val)
            result=mycur.fetchone()
            sr=0
            dpo=0
            wd=0
            if result:
                sr=int(result[0])
                dpo=int(result[1])
                wd=int(result[2])

                adj_amt=0
                if dpo>wd:
                    adj_amt=dpo-wd
                    self.adjust_wallet(sr,adj_amt,"minus")
                elif wd>dpo:
                    adj_amt=wd-dpo
                    self.adjust_wallet(sr,adj_amt,"plus")
            else:
                messagebox.showerror("Error","There's no record in the database!",parent=self.root)
            sql="delete from wallet where id=%s"
            val=(self.var_id.get(),)
            mycur.execute(sql,val)
            con.commit()
            con.close()
        def adjust_wallet(self,index_,amt:int,opr):
            con=connect_db()
            mycur=con.cursor()
            sql="select sr,balance from wallet where sr>%s"
            val=(index_,)
            mycur.execute(sql,val)
            a=mycur.fetchall()
            for i in a:
                cur_bal=int(i[1])
                if opr=="minus":
                    cur_bal-=abs(amt)
                elif opr=="plus":
                    cur_bal+=abs(amt)

                sql="update wallet set balance=%s where sr=%s"
                val=(cur_bal,i[0])
                mycur.execute(sql,val)
                con.commit()
                con.close()
        def get_balance(self):
            con=connect_db()
            mycur=con.cursor()
            sql="select balance from wallet order by sr desc limit 1"
            mycur.execute(sql)
            a=mycur.fetchone()
            con.close()
            if a==None:
                return 0
            return int(a[0])
        def clear(self):
             self.var_description.set("")
             self.var_deposit.set("")
             self.var_withdraw.set("")
             self.var_type.set("")
             self.var_date.set("")
             self.var_id.set("")
             self.show()
        def search(self):
            pass
        def var_creation(self):
            self.var_wallet_searchby=StringVar()
            self.var_wallet_searchtxt=StringVar()
            self.var_description=StringVar()
            self.var_deposit=StringVar()
            self.var_withdraw=StringVar()
            self.var_type=StringVar()
            self.var_date=StringVar()
            self.var_id=StringVar()
        def openCalendar(self,date_type):
            self.cal_win=Toplevel(self.root)
            self.cal_win.title("Calendar")
            x=self.btn_date_picker.winfo_rootx()
            y=self.btn_date_picker.winfo_rooty()
            self.cal_win.iconphoto(False,self.iconimg)
            self.cal_win.geometry(f"200x220+{x-100}+{y-250}")
            self.cal_win.resizable(0,0)
            self.cal = Calendar(self.cal_win, date_pattern="dd/MM/yyyy",selectmode = 'day',year = 2023, month = 10,day = 23)
            self.cal.pack(side=TOP,fill=X)
            ok = Button(self.cal_win,command=lambda :self.setDate(date_type),text="OK",bg="orange",fg="blue")
            ok.pack(side=BOTTOM,padx=5)
        def setDate(self,date_btn):
            date_btn.set(self.cal.get_date())
            self.cal_win.destroy()     
if __name__=="__main__":
    root= Tk()
    app= wallet(root)
    root.mainloop()