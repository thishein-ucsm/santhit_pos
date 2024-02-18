from os import path
import os
from tkinter import messagebox
from PIL import ImageTk
from tkinter import *
import datetime as dt
from tkinter import ttk
from database import connect_db
from tool_ import isStatusOK, loadConfig
import tempfile
class bill:
    def __init__(self,root,user="guest") -> None:
        self.root=root
        self.user=user
        self.new_win=None
        self.ROOT_DIR = loadConfig()['images']
        self.ROOT_PATH = loadConfig()['path']

        self.root.geometry("1350x700+0+0")
        self.root.title("Billing @Inventory Management System | Developed by KG")
        self.root.config(bg="lightblue")

        self.iconimg=ImageTk.PhotoImage(file=f'{self.ROOT_DIR}icon.png')
        self.root.iconphoto(False,self.iconimg)

        image_ = path.abspath(path.join(self.ROOT_DIR, 'logo1.jpg'))

        self.sideimg=ImageTk.PhotoImage(file=image_)

        self.title=Label(self.root,image=self.sideimg,text="SanThit - Inventory Management System ",compound=LEFT,font=("times new roman",39,"bold"),bg="#010c48",fg="white",anchor=W,padx=20).place(x=0,y=0,relwidth=1,height=70)
        self.lbl_clock=Label(self.root,text=f"Welcome to Inventory Management System\t\tDate: DD-MM-YYYY\t\t Time: HH:MM:SS\t\t Auth: {self.user.capitalize()}",font=("times new roman",15,"bold"),bg="#4D636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        self.btn_logout=Button(self.root,text="Log Out",command=self.logout,font=("times new roman",15,"bold"),bg="#4caf50",fg="white",anchor=W,padx=20,cursor="hand2").place(x=1170,y=10,width=120,height=50)
        self.update_time()
        self.createVariable()
        self.showProductFrame()
        self.showSaleFrame()
        self.showBillFrame()
        footer=Label(self.root,text="IMS-Inventory Management System | Developed By KG for any technical issues call us 0997xxxx393 ",font=("times new roman",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
    def showProductFrame(self):
        frame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        frame.place(x=7,y=102,width=440,height=571)
        lbl_p= Label(frame,text="All Products",font=("Elephant",16,"bold"),bg="#009688",fg="white")
        lbl_p.pack(side=TOP,fill=X)

        frame_p_search=Frame(frame,bd=2,relief=RAISED,bg="white")
        frame_p_search.place(x=2,y=35,width=430,height=80)
        lbl_searchtxt= Label(frame_p_search,text="Search Product | By Name ",font=("times new roman",15,"bold"),bg="white",fg="#0055ff")
        lbl_searchtxt.place(x=5,y=5,width=300,height=28)
        self.btn_showall=Button(frame_p_search,text="Show All",command=self.showAll,font=("goudy old style",15),bg="#33bbf9",fg="white",cursor="hand2")
        self.btn_showall.place(x=325,y=5,width=90,height=28)
        lbl_byname= Label(frame_p_search,text="Product Name ",font=("times new roman",15,"bold"),bg="white",fg="#0055ff")
        lbl_byname.place(x=5,y=40,width=130,height=28)
        txt_p_name = Entry(frame_p_search,textvariable=self.var_search_pname,font=("goudy old style",14,"bold"),fg="#111199",bg="lightblue")
        txt_p_name.place(x=140,y=40,width=180,height=28)
        txt_p_name.bind('<Return>',lambda e:self.showProductbyName())
        self.btn_search=Button(frame_p_search,text="Search",command=self.showProductbyName,font=("goudy old style",15),bg="#ff5722",fg="white",cursor="hand2")
        self.btn_search.place(x=325,y=40,width=90,height=28)
    
        frame_p_table=Frame(frame,bd=2,relief=RIDGE,bg="white")
        frame_p_table.place(x=2,y=120,width=430,height=410)
        scrolly=Scrollbar(frame_p_table,orient=VERTICAL)
        scrollx=Scrollbar(frame_p_table,orient=HORIZONTAL)
        self.prod_table=ttk.Treeview(frame_p_table,columns=("1","2","3","4","5"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.prod_table.xview)
        scrolly.config(command=self.prod_table.yview)
        self.prod_table.heading("1",text="PID.")
        self.prod_table.heading("2",text="Name")
        self.prod_table.heading("3",text="Price")
        self.prod_table.heading("4",text="Qty")
        self.prod_table.heading("5",text="Status")
        

        self.prod_table["show"]="headings"
        self.prod_table.column("1",width=50)
        self.prod_table.column("2",width=150)
        self.prod_table.column("3",width=50,anchor="e")
        self.prod_table.column("4",width=30,anchor="center")
        self.prod_table.column("5",width=80,anchor="center")
        
        self.prod_table.pack(fill=BOTH,expand=1)
        lbl_p= Label(frame,text="Note: Enter 0(zero)QTY to remove product from Cart ",font=("times new roman",12),bg="white",fg="red")
        lbl_p.pack(side=BOTTOM,fill=X)
        self.prod_table.bind('<Double-Button-1>',self.getdata)

        self.showAll()
    def showSaleFrame(self):
        frame_mid=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        frame_mid.place(x=454,y=102,width=540,height=100)
        lbl_p= Label(frame_mid,text="Customer Details",font=("Elephant",16,"bold"),bg="#009688",fg="white")
        lbl_p.pack(side=TOP,fill=X)
        lbl_name=Label(frame_mid,text=" Name: ",font=("goudy old style",15,"bold"),bg="white",fg="black")
        lbl_name.place(x=7,y=45,width=75,height=28)
        self.txt_name = Entry(frame_mid,textvariable=self.var_cname,font=("goudy old style",14,"bold"),bg="lightblue")
        self.txt_name.place(x=80,y=45,width=190,height=28)
        lbl_ph=Label(frame_mid,text=" Contact: ",font=("goudy old style",15,"bold"),bg="white",fg="black")
        lbl_ph.place(x=280,y=45,width=70,height=28)
        self.txt_ph = Entry(frame_mid,textvariable=self.var_cphone,font=("goudy old style",14,"bold"),bg="lightblue")
        self.txt_ph.place(x=360,y=45,width=150,height=28)
        
        frame_mid2=Frame(self.root,bd=4,relief=RIDGE,bg="#9900ff")
        frame_mid2.place(x=454,y=204,width=540,height=360)
        
        ############### calculator#######################
        
        frame_cal=Frame(frame_mid2,bd=2,relief=RIDGE,bg="white")
        frame_cal.place(x=0,y=1,width=200,height=350)

        txt_input= Entry(frame_cal,textvariable=self.var_cal_input,font=("arial",15,"bold"),justify=RIGHT,width=16,bd=10,relief=GROOVE,bg="black",state="readonly",readonlybackground="lightblue")
        txt_input.grid(row=0,columnspan=4)
        
        btn_9= Button(frame_cal,text=9,command=lambda: self.get_cal_input(9),bd=4,width=3,pady=8,font=("arial",15,"bold"),cursor="hand2")
        btn_8= Button(frame_cal,text=8,command=lambda: self.get_cal_input(8),bd=4,width=3,pady=8,font=("arial",15,"bold"),cursor="hand2")
        btn_7= Button(frame_cal,text=7,command=lambda: self.get_cal_input(7),bd=4,width=3,pady=8,font=("arial",15,"bold"),cursor="hand2")
        btn_6= Button(frame_cal,text=6,command=lambda: self.get_cal_input(6),bd=4,width=3,pady=8,font=("arial",15,"bold"),cursor="hand2")
        btn_5= Button(frame_cal,text=5,command=lambda: self.get_cal_input(5),bd=4,width=3,pady=8,font=("arial",15,"bold"),cursor="hand2")
        btn_4= Button(frame_cal,text=4,command=lambda: self.get_cal_input(4),bd=4,width=3,pady=8,font=("arial",15,"bold"),cursor="hand2")
        btn_3= Button(frame_cal,text=3,command=lambda: self.get_cal_input(3),bd=4,width=3,pady=8,font=("arial",15,"bold"),cursor="hand2")
        btn_2= Button(frame_cal,text=2,command=lambda: self.get_cal_input(2),bd=4,width=3,pady=8,font=("arial",15,"bold"),cursor="hand2")
        btn_1= Button(frame_cal,text=1,command=lambda: self.get_cal_input(1),bd=4,width=3,pady=8,font=("arial",15,"bold"),cursor="hand2")
        btn_0= Button(frame_cal,text=0,command=lambda: self.get_cal_input(0),bd=4,width=3,pady=8,font=("arial",15,"bold"),cursor="hand2")
       
        btn_plus= Button(frame_cal,text="+",command=lambda: self.get_cal_input("+"),bd=4,width=3,pady=8,font=("arial",15,"bold"),cursor="hand2")
        btn_minus= Button(frame_cal,text="-",command=lambda: self.get_cal_input("-"),bd=4,width=3,pady=8,font=("arial",15,"bold"),cursor="hand2")
        btn_prod= Button(frame_cal,text="*",command=lambda: self.get_cal_input("*"),bd=4,width=3,pady=8,font=("arial",15,"bold"),cursor="hand2")
        btn_div= Button(frame_cal,text="/",command=lambda: self.get_cal_input("/"),bd=4,width=3,pady=8,font=("arial",15,"bold"),cursor="hand2")
        btn_mod= Button(frame_cal,text="%",command=lambda: self.get_cal_input("%"),bd=4,width=3,pady=8,font=("arial",15,"bold"),cursor="hand2")
        btn_c= Button(frame_cal,text="C",command=self.clearCal,bd=4,width=3,pady=8,font=("arial",15,"bold"),cursor="hand2")
        btn_ce= Button(frame_cal,text="Ce",bd=4,width=3,pady=8,font=("arial",15,"bold"),cursor="hand2")

        btn_eq= Button(frame_cal,text="=",command=self.calculate,bd=4,width=3,pady=8,font=("arial",15,"bold"))
        btn_left_p= Button(frame_cal,text="(",command=lambda: self.get_cal_input("("),bd=4,width=3,pady=8,font=("arial",15,"bold"))
        btn_right_p= Button(frame_cal,text=")",command=lambda: self.get_cal_input(")"),bd=4,width=3,pady=8,font=("arial",15,"bold"))

        btn_ce.grid(row=1,column=0)
        btn_c.grid(row=1,column=1)
        btn_mod.grid(row=1,column=2)
        btn_div.grid(row=1,column=3)


        btn_7.grid(row=2,column=0)
        btn_8.grid(row=2,column=1)
        btn_9.grid(row=2,column=2)
        btn_prod.grid(row=2,column=3)

        btn_4.grid(row=3,column=0)
        btn_5.grid(row=3,column=1)
        btn_6.grid(row=3,column=2)
        btn_minus.grid(row=3,column=3)

        btn_1.grid(row=4,column=0)
        btn_2.grid(row=4,column=1)
        btn_3.grid(row=4,column=2)
        btn_plus.grid(row=4,column=3)

        btn_left_p.grid(row=5,column=0)
        btn_0.grid(row=5,column=1)
        btn_right_p.grid(row=5,column=2)
        btn_eq.grid(row=5,column=3)

        ############## table #######################################
        frame_p_table=Frame(frame_mid2,bd=2,relief=RIDGE,bg="white")
        frame_p_table.place(x=202,y=1,width=330,height=350)
        self.lbl_p_total=Label(frame_p_table,text="Cart\t\t\tTotal Product(s): [0]")
        self.lbl_p_total.pack(side=TOP,fill=X)
        
        scrolly=Scrollbar(frame_p_table,orient=VERTICAL)
        scrollx=Scrollbar(frame_p_table,orient=HORIZONTAL)
        self.cart_table=ttk.Treeview(frame_p_table,columns=("1","2","3","4"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.prod_table.xview)
        scrolly.config(command=self.prod_table.yview)
        self.cart_table.heading("1",text="PID.")
        self.cart_table.heading("2",text="Name")
        self.cart_table.heading("3",text="Price")
        self.cart_table.heading("4",text="Qty")
        # self.cart_table.heading("5",text="Status")
        

        self.cart_table["show"]="headings"
        self.cart_table.column("1",width=30)
        self.cart_table.column("2",width=150)
        self.cart_table.column("3",width=40,anchor="e")
        self.cart_table.column("4",width=10,anchor="center")
        # self.cart_table.column("5",width=80)
        self.cart_table.pack(fill=BOTH,expand=1)
        self.cart_table.bind('<Double-Button-1>',self.getdata)


        frame_mid3=Frame(self.root,bd=4,relief=RAISED)
        frame_mid3.place(x=454,y=567,width=540,height=105)

        Label(frame_mid3,text="Product Name",font=("times new roman",15,"bold")).place(x=2,y=2,width=200,height=18)
        Label(frame_mid3,text="Price/Qty",font=("times new roman",15,"bold")).place(x=210,y=2,width=100,height=18)
        Label(frame_mid3,text="Quantity",font=("times new roman",15,"bold")).place(x=350,y=2,width=100,height=18)
        txt_name = Entry(frame_mid3,textvariable=self.var_p_name,font=("goudy old style",14,"bold"),bg="lightblue",state="readonly",readonlybackground="gray")
        txt_name.place(x=5,y=30,width=200,height=28)
        txt_price = Entry(frame_mid3,textvariable=self.var_p_price,justify="right",font=("goudy old style",14,"bold"),bg="lightblue",state="readonly",readonlybackground="gray")
        txt_price.place(x=210,y=30,width=130,height=28)
        self.txt_qty = Entry(frame_mid3,textvariable=self.var_p_qty,font=("goudy old style",14,"bold"),bg="lightblue")
        self.txt_qty.place(x=350,y=30,width=150,height=28)
        self.txt_qty.bind('<Return>',lambda e:self.add_cart())
        self.lbl_stock_left = Label(frame_mid3,text="In Stock [---]",font=("times new roman",14))
        self.lbl_stock_left.place(x=5,y=70,width=150,height=20)
        btn_clear=Button(frame_mid3,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=220,y=65,width=100,height=28)
        btn_add_cart=Button(frame_mid3,text="Add/Update Cart",command=self.add_cart,font=("goudy old style",15),bg="orange",fg="white",cursor="hand2").place(x=340,y=65,width=180,height=28)
    def showBillFrame(self):
        frame_right1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        frame_right1.place(x=999,y=102,width=350,height=421)
        lbl_p= Label(frame_right1,text="Billing Area",font=("Elephant",16,"bold"),bg="#009688",fg="white")
        lbl_p.pack(side=TOP,fill=X)
        scrolly= Scrollbar(frame_right1,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill=Text(frame_right1,yscrollcommand=scrolly.set)
        self.txt_bill.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill.yview)
        

        frame_right2=Frame(self.root,bd=4,relief=RAISED)
        frame_right2.place(x=999,y=525,width=350,height=148)
        self.lbl_amt=Label(frame_right2,text="Bill Amount\n[0]",font=("goudy old style",14,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amt.place(x=2,y=5,width=115,height=70)
        self.lbl_dis=Label(frame_right2,text="Discount\n[5%]",font=("goudy old style",14,"bold"),bg="#8bc34a",fg="white")
        self.lbl_dis.place(x=118,y=5,width=110,height=70)
        self.lbl_netamt=Label(frame_right2,text="Net Pay\n[0]",font=("goudy old style",14,"bold"),bg="#607d8b",fg="white")
        self.lbl_netamt.place(x=230,y=5,width=110,height=70)
        self.btn_print=Button(frame_right2,text="Print",command=self.print_,font=("goudy old style",14,"bold"),bg="lightgreen",fg="Blue")
        self.btn_print.place(x=2,y=78,width=115,height=50)
        self.btn_clearall=Button(frame_right2,text="ClearAll",command=self.clear,font=("goudy old style",14,"bold"),bg="gray",fg="white")
        self.btn_clearall.place(x=118,y=78,width=110,height=50)
        self.btn_generate=Button(frame_right2,text="Generate",command=self.generate_bill,font=("goudy old style",14,"bold"),bg="#009688",fg="white")
        self.btn_generate.place(x=230,y=78,width=110,height=50)
    def showAll(self):
        self.var_search_pname.set("")
        con=connect_db()
        mycur= con.cursor()
        try:
            sql="SELECT pid,name,price,qty,status FROM product"
            mycur.execute(sql)
            rows=mycur.fetchall()
            self.prod_table.delete(*self.prod_table.get_children())
            for row in rows:
                self.prod_table.insert('',END,values=row)
            con.close()    
        except Exception as ex:
            messagebox.showerror("Error1",f"Error due to : {str(ex)}",parent=self.root)
    def showProductbyName(self):
        con=connect_db()
        mycur= con.cursor()
        try:
            if self.var_search_pname.get()=="":
                #self.var_emp_searchtxt.get()==""
                messagebox.showerror("Error","Product Name should be filled",parent=self.root)
            else:
                # "SELECT pid,name,price,qty,status FROM product WHERE name LIKE %s"
                mycur.execute("SELECT pid,name,price,qty,status FROM product where name Like '%"+self.var_search_pname.get()+"%'")
                rows= mycur.fetchall()

                if len(rows)!=0:
                    self.prod_table.delete(*self.prod_table.get_children())
                    for row in rows:
                        self.prod_table.insert('',END,values=row)
                else:
                    self.prod_table.delete(*self.prod_table.get_children())
                    messagebox.showinfo("Information","No record found on system",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",str(ex),parent=self.root)
    def get_cal_input(self,num):
        temp=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(temp)
    def calculate(self):
        temp=self.var_cal_input.get()
        self.var_cal_input.set(eval(temp))
    def clearCal(self):
        self.var_cal_input.set('')
    def getdata(self,ev):
        f= self.prod_table.focus()
        content= (self.prod_table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_p_name.set(row[1])
        self.var_p_price.set(row[2])
        self.lbl_stock_left.config(text=f"In Stock [{row[3]}]")
        self.var_stock_left.set(row[3])
        self.txt_qty.focus_set()
    def add_cart(self):
        if self.var_p_name.get()=="" or self.var_p_price.get()=="" or self.var_p_qty.get()=="":
            messagebox.showerror("Error","Product name/Price/Qty should not be missing!",parent=self.root)
        if int(self.var_p_qty.get())>int(self.var_stock_left.get()):
            messagebox.showinfo("Sorry","Insufficient Stock!",parent=self.root)
        else:
            ############# check and repair minus qty
            if int(self.var_p_qty.get())<0:
                self.var_p_qty.set(abs(int(self.var_p_qty.get())))  

            cal_price=int(self.var_p_qty.get())*int(self.var_p_price.get())
            cal_price=int(cal_price)
            cart_data=[self.var_pid.get(),self.var_p_name.get(),cal_price,self.var_p_qty.get()]
            isAlreadyAdded='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    isAlreadyAdded="yes"
                    break
                else:
                    index_+=1    
            if isAlreadyAdded=='yes':
                ans=messagebox.askyesno("Confirm","You already added product to cart! Do you want to update?",parent=self.root)
                if ans:
                    if self.var_p_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        self.cart_list[index_][2]=cal_price
                        self.cart_list[index_][3]=self.var_p_qty.get()
                        self.var_p_name.set("")
                        self.var_p_price.set("")
                        self.var_p_qty.set("")
            else:
                self.cart_list.append(cart_data)
                self.lbl_stock_left.config(text="In Stock [---]")

                self.var_p_name.set("")
                self.var_p_price.set("")
                self.var_p_qty.set("")

                # to remove active selection on product table
                self.prod_table.selection_remove(self.prod_table.selection())
            self.show_cart()

            
            self.bill_updates()
            self.txt_name.focus_set()
            
    def show_cart(self):
        try:
            self.cart_table.delete(*self.cart_table.get_children())
            for row in self.cart_list:
                self.cart_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    def bill_updates(self):
        self.bill_amt=0
        self.net_amt=0
        for row in self.cart_list:
            self.bill_amt=self.bill_amt+int(row[2])
        self.discount=int((self.bill_amt*5)/100)
        self.net_amt=int(self.bill_amt-(self.bill_amt*5)/100)
        self.lbl_amt.config(text=f"Bill Amt(ks.)\n[{str(self.bill_amt)}]")
        self.lbl_netamt.config(text=f"Net Amt(ks.)\n[{str(self.net_amt)}]")
        self.lbl_p_total.config(text=f"Cart\t\t\tTotal Product(s): [{len(self.cart_list)}]")
    def generate_bill(self):
        if self.var_cname.get()=="" or self.var_cphone.get()=="":
            messagebox.showerror("Error","Customer Details should be provided!",parent=self.root)
        else:
            self.generate_voucherid()
            self.createSaleOrder()
            self.bill_top()
            self.bill_middle()
            self.bill_bottom()
            self.exportFile()

    def createSaleOrder(self):
        con=connect_db() #module from database.py
        mycur= con.cursor()
 
        try:
            print(self.cart_list)
            for so in self.cart_list:
                sql="INSERT INTO saleorder(voucherid,cid,cname,pid,qty,total,date) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                val1=(str(self.invoice),"custID","CustName",so[0],so[3],so[2],self.date_)

                sql_req_qty="select qty from product where pid=%s"
                val2=(so[0],)
                print(val2)

                sql_qty_upd="UPDATE product set qty=%s where pid=%s"
              

           
                if isStatusOK(val1):
                    mycur.execute(sql,val1)
                    con.commit()
                    # messagebox.showinfo("Message","Successfully inserted into Database!",parent=self.root)
                else:
                    messagebox.showerror("Error","You are missing some data!",parent=self.root)

                if isStatusOK(val2):
                    mycur.execute(sql_req_qty,val2)
                    total_qty=mycur.fetchone()
                    sold_qty=so[3]
                    remain_qty=int(total_qty[0])-int(sold_qty)
                    val3=(remain_qty,so[0])
                    mycur.execute(sql_qty_upd,val3)

                    con.commit()
                    self.showAll()
                    # messagebox.showinfo("Message","Successfully inserted into Database!",parent=self.root)
                else:
                    messagebox.showerror("Error","You are missing some data!",parent=self.root)

            con.close()

        except Exception as ex:
            messagebox.showerror("Error2",f"Error due to : {(ex)}",parent=self.root)
    def generate_voucherid(self):
        today=dt.datetime.now()
        date_=today.strftime("%d%m%y") 
        time_=today.strftime("%H%M%S")
        self.invoice=(time_)+"_"+(date_)
        self.date_=str(today.strftime("%d-%m-%y"))
    def bill_top(self):
        
        bill_top_text=f'''
\t\tSanThit
\t\tStore
\t09-978888052,09-974455393,
\t\t09-797779445
\t{str("*"*25)}
Customer Name: {self.var_cname.get()}
Contact No. {self.var_cphone.get()}
Invoice No.{str(self.invoice)}\t\t\tDate: {self.date_}
{str("="*40)}
Product Name\t\t\tQTY\tPrice
{str("="*40)}
'''
        self.txt_bill.delete('1.0',END)
        self.txt_bill.insert('1.0',bill_top_text)
    def bill_middle(self):
        for r in self.cart_list:
            name=r[1]
            qty=r[3]
            price=int(r[2])*int(qty)
            self.txt_bill.insert(END,"\n"+name+"\t\t\t"+r[3]+"\t"+str(r[2]))  
            self.print_status=1    
    def bill_bottom(self):
        bill_btm=f'''
{str("="*40)}
Bill Amount\t\t\tKs.{self.bill_amt}
Discount\t\t\tKs.{self.discount}
Net Pay\t\t\tKs.{self.net_amt}
{str("="*40)}\n
Thank you for purchasing to SanThit Shop
'''
        self.txt_bill.insert(END,bill_btm)
    def exportFile(self):
        with open(f'{self.ROOT_PATH}invoices\\{self.invoice}.txt','w') as fi:
            fi.write(self.txt_bill.get('1.0',END))
            fi.close()
        messagebox.showinfo("Success","Bill Slip has been saved",parent=self.root)
    def update_time(self):
        today=dt.datetime.now()
        date_=today.strftime("%d-%b-%Y") 
        time_=today.strftime("%H:%M:%S")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\tDate: {date_}\t\t Time: {time_}\t\tAuth: {self.user.capitalize()}")
        self.lbl_clock.after(1000,self.update_time)
    def logout(self):
            from login import login as loin
            self.root.destroy()
            root=Tk()
            app=loin(root)
            root.mainloop()
    def createVariable(self):
        self.invoice=StringVar()
        self.date_=StringVar()
        self.var_cname=StringVar()
        self.var_cphone=StringVar()
        self.var_p_name=StringVar()
        self.var_search_pname=StringVar()
        self.var_pid=StringVar()
        self.var_p_price=StringVar()
        self.var_p_qty=StringVar()
        self.var_stock_left=StringVar()
        self.var_cal_input=StringVar()
        self.cart_list=[]
        self.print_status=0
    def clear(self):
        self.txt_bill.delete('1.0',END)
        self.cart_table.delete(*self.cart_table.get_children())
        # to remove active selection on product table
        self.prod_table.selection_remove(self.prod_table.selection())

        self.lbl_amt.config(text="Bill Amt(ks.)\n[0]")
        self.lbl_netamt.config(text="Net Amt(ks.)\n[0]")
        self.lbl_stock_left.config(text="In Stock [---]")
        self.lbl_p_total.config(text="Cart\t\t\tTotal Product(s): [0]")


        self.cart_list=[]
        self.var_cname.set("")
        self.var_cphone.set("")
        self.var_p_name.set("")
        self.var_p_price.set("")
        self.var_p_qty.set("")
    def print_(self):
        if self.print_status==1:
            messagebox.showinfo("Information","Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp(".txt")
            open(new_file,"w").write(self.txt_bill.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror("Error","Failed to print")    
if __name__=="__main__":
    root= Tk()
    app= bill(root)
    root.mainloop()