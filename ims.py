from tkinter import *

from dboperation import dboperation
from buy import *
from build_ import *
from bill import *
from employee import *
from supplier import *
from database import *
from category import *
from product import *
from customer import *
from billslip import *
from report import reporter_
import datetime as dt
from PIL import ImageTk,Image
from tool_ import *
from authentication import *
class IMS:
    def __init__(self,root,user="guest") -> None:
        self.root=root
        self.user=user
        self.new_win=None
        self.ROOT_DIR = loadConfig()['images']

        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System | Developed by KG")
        self.root.config(bg="white")

        self.iconimg=ImageTk.PhotoImage(file=f'{self.ROOT_DIR}icon.png')
        self.root.iconphoto(False,self.iconimg)
        image_ = path.abspath(path.join(self.ROOT_DIR, 'logo1.jpg'))

        
        # image_=ImageTk.PhotoImage(file=f'{self.ROOT_DIR}\\logo1.jpg')

        # self.animimg=Image.open(f'{self.ROOT_DIR}parts\\1.png')
        # self.animimg=self.animimg.resize((350,250),Image.LANCZOS)
        # self.sideimg=ImageTk.PhotoImage(self.animimg)

        self.sideimg=ImageTk.PhotoImage(file=image_)
        self.title=Label(self.root,image=self.sideimg,text="SanThit - Inventory Management System ",compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor=W,padx=20).place(x=0,y=0,relwidth=1,height=70)
        self.lbl_clock=Label(self.root,text=f"Welcome to Inventory Management System\t\tDate: DD-MM-YYYY\t\t Time: HH:MM:SS\t\t Auth: {self.user.capitalize()}",font=("times new roman",15,"bold"),bg="#4D636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        self.btn_logout=Button(self.root,text="Log Out",command=self.logout,font=("times new roman",15,"bold"),bg="#4caf50",fg="white",anchor=W,padx=20,cursor="hand2").place(x=1200,y=10,width=120,height=50)
        
        self.showMenu()
        self.setQuickActions()

                
        self.lbl_employee=Label(self.root,text="Total Employees\n[ 0 ]",bg="#33bbf9",fg="white",bd=5,relief=RIDGE,font=("goudy old style",20,"bold"))
        self.lbl_employee.place(x=300,y=120,width=300,height=150)
        self.lbl_supplier=Label(self.root,text="Total Suppliers\n[ 0 ]",bg="#ff5722",fg="white",bd=5,relief=RIDGE,font=("goudy old style",20,"bold"))
        self.lbl_supplier.place(x=650,y=120,width=300,height=150)
        self.lbl_customer=Label(self.root,text="Total Customers\n[ 0 ]",bg="#009688",fg="white",bd=5,relief=RIDGE,font=("goudy old style",20,"bold"))
        self.lbl_customer.place(x=1000,y=120,width=300,height=150)
        self.lbl_product1=Label(self.root,text="Total Products\n[ 0 ]",bg="#607d8b",fg="white",bd=5,relief=RIDGE,font=("goudy old style",20,"bold"))
        self.lbl_product1.place(x=300,y=300,width=300,height=150)
        self.lbl_sale1=Label(self.root,text="Total Sales\n[ 0 ]",bg="#ffc107",fg="white",bd=5,relief=RIDGE,font=("goudy old style",20,"bold"))
        self.lbl_sale1.place(x=650,y=300,width=300,height=150)
        self.lbl_belowqty=Label(self.root,text="[ 0 ] items <10",bg="#ff5555",fg="white",bd=5,relief=RIDGE,font=("goudy old style",20,"bold"))
        self.lbl_belowqty.place(x=1000,y=300,width=300,height=150)
        self.lbl_category=Label(self.root,text="Total Categories\n[ 0 ]",bg="#627d1c",fg="white",bd=5,relief=RIDGE,font=("goudy old style",20,"bold"))
        self.lbl_category.place(x=300,y=480,width=300,height=150)
        self.lbl_sale1=Label(self.root,text="Total Credit Sales\n[ 0 ]",bg="#127e7f",fg="white",bd=5,relief=RIDGE,font=("goudy old style",20,"bold"))
        self.lbl_sale1.place(x=650,y=480,width=300,height=150)
        self.lbl_belowqty=Label(self.root,text="[ 0 ] items <10",bg="#6a7efa",fg="white",bd=5,relief=RIDGE,font=("goudy old style",20,"bold"))
        self.lbl_belowqty.place(x=1000,y=480,width=300,height=150)
        self.update_time()
        create_tables()

        self.update_data()

        footer=Label(self.root,text="IMS-Inventory Management System | Developed By KG for any technical issues call us 0997xxxx393 ",font=("times new roman",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
    def update_data(self):
        self.update_total("employee",self.lbl_employee)
        self.update_total("supplier",self.lbl_supplier)
        self.update_total("customer",self.lbl_customer)
        self.update_total("category",self.lbl_category)
        self.update_total("product",self.lbl_product1)
        self.lbl_category.after(3000,self.update_data)
    def update_total(self,name,lbl):
        conn=connect_db()
        mycur=conn.cursor()
        mycur.execute(f"SELECT name FROM {name}")
        mycur.fetchall()
        if mycur.rowcount > 0:
            lbl.config(text=f"Total {name.capitalize()}\n[ {mycur.rowcount} ]")
    def update_time(self):
        today=dt.datetime.now()
        date_=today.strftime("%d-%b-%Y") 
        time_=today.strftime("%H:%M:%S")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\tDate: {date_}\t\t Time: {time_}\t\tAuth: {self.user.capitalize()}")
        self.lbl_clock.after(1000,self.update_time)
    def showMenu(self):
        
        self.LeftMenu= Frame(self.root,bd=3,relief=RIDGE,bg="#ff0011")
        self.LeftMenu.place(x=2,y=102,width=185,height=575)
        self.lbl_menu=Label(self.LeftMenu,text="Menu",font=("Elephant",20,"bold"),bg="#009688",fg="#ffc107").pack(side=TOP,fill=X)

        self.canvas=Canvas(self.LeftMenu,bg="yellow")
        self.canvas.pack(side=LEFT,fill=BOTH,expand=True)
        scrollbar = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.btn_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.btn_frame, anchor="nw")


        self.btn_buy=Button(self.btn_frame,text="Buy",command=lambda : self.openPage(self.btn_buy,self.buyPage),font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2")
        self.btn_buy.pack(side=TOP,fill=X)
        self.btn_sell=Button(self.btn_frame,text="Sell",command=lambda : self.openPage(self.btn_sell,self.billPage),font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2")
        self.btn_sell.pack(side=TOP,fill=X)
        self.btn_product=Button(self.btn_frame,text="Product",command=lambda: self.openPage(self.btn_product,self.productPage),font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2")
        self.btn_product.pack(side=TOP,fill=X)
        # self.btn_build=Button(self.btn_frame,text="Build",command=lambda: self.openPage(self.btn_build,self.buildPage),font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2")
        # self.btn_build.pack(side=TOP,fill=X)
        self.btn_category=Button(self.btn_frame,text="Category",command=lambda: self.openPage(self.btn_category,self.categoryPage),font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2")
        self.btn_category.pack(side=TOP,fill=X)
        self.btn_receivable=Button(self.btn_frame,text="Receivable",font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2")
        self.btn_receivable.pack(side=TOP,fill=X)

        self.btn_wallet=Button(self.btn_frame,text="Wallet",font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2")
        self.btn_wallet.pack(side=TOP,fill=X)
        
        self.btn_employee=Button(self.btn_frame,text="Employee",command=lambda: self.openPage(self.btn_employee,self.employeePage),font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2")
        self.btn_employee.pack(side=TOP,fill=X)
        # self.btn_employee.bind('<Enter>',lambda event: self.btn_employee.config(bg="Lightblue"))

        self.btn_supplier=Button(self.btn_frame,text="Supplier",command=lambda: self.openPage(self.btn_supplier,self.supplierPage),font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2")
        self.btn_supplier.pack(side=TOP,fill=X)
        self.btn_customer=Button(self.btn_frame,text="Customer",command=lambda: self.openPage(self.btn_customer,self.customerPage),font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2")
        self.btn_customer.pack(side=TOP,fill=X)
        self.btn_saleslip=Button(self.btn_frame,text="Slips",command=lambda: self.openPage(self.btn_saleslip,self.slipPage),font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2")
        self.btn_saleslip.pack(side=TOP,fill=X)
        
        self.btn_auth=Button(self.btn_frame,text="Authentication",command=lambda: self.openPage(self.btn_auth,self.authenticationPage),font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2")
        self.btn_auth.pack(side=TOP,fill=X)
        self.btn_report=Button(self.btn_frame,text="Report",command=lambda:self.openPage(self.btn_report,self.reportPage),font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2")
        self.btn_report.pack(side=TOP,fill=X)
        self.btn_backup=Button(self.btn_frame,text="Backup&Restore",command=lambda:self.openPage(self.btn_backup,self.dbPage),font=("times new roman",14,"bold"),bg="white",bd=3,cursor="hand2")
        self.btn_backup.pack(side=TOP,fill=X)
     

        self.btn_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Enter>", lambda event: self.canvas.bind_all("<MouseWheel>", self.on_mousewheel))
        self.canvas.bind("<Leave>", lambda event: self.canvas.unbind_all("<MouseWheel>"))
       
    def on_frame_configure(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self,event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
    def setQuickActions(self):
        self.root.bind('<Control-x>',self.closeProgram)
        self.root.bind('<Control-1>',self.showProdPage)
        self.root.bind('<Control-2>',self.showProdPage)
        self.root.bind('<Control-3>',self.showProdPage)
        self.root.bind('<Control-4>',self.showCatPage)
        self.root.bind('<Control-5>',self.showCatPage)
        self.root.bind('<Control-6>',self.showCatPage)
        self.root.bind('<Control-7>',self.showEmpPage)
        self.root.bind('<Control-8>',self.showSupPage)
    def showEmpPage(self,event):
        self.openPage(self.btn_employee,self.employeePage)
    def showSupPage(self,event):
        self.openPage(self.btn_supplier,self.supplierPage)
    def showProdPage(self,event):
        self.openPage(self.btn_product,self.productPage)
    def showCustPage(self,event):
        self.openPage(self.btn_customer,self.customerPage)
    def showCatPage(self,event):
        self.openPage(self.btn_category,self.categoryPage)
    def openPage(self,btn,page):
        if self.new_win!=None: self.new_win.destroy()
        self.inactive_btn()
        self.new_win= Toplevel(self.root)
        btn.config(fg="white",bg="orange")
        page()
    def buyPage(self):
        self.new_obj=buy(self.new_win)
    def buildPage(self):
        self.new_obj=buildeng(self.new_win)
    def billPage(self):
        self.new_obj=bill(self.new_win,self.user)
    def slipPage(self):
        self.new_obj=billslip(self.new_win)
    def employeePage(self):
        self.new_obj= employee(self.new_win)
    def supplierPage(self):
        self.new_obj= supplier(self.new_win)
    def customerPage(self):
        self.new_obj= customer(self.new_win)
    def categoryPage(self):
        self.new_obj= category(self.new_win)
    def productPage(self):
        self.new_obj= product(self.new_win)
    def authenticationPage(self):
        self.new_obj= authentication(self.new_win)
    def reportPage(self):
        self.new_obj=reporter_(self.new_win)
    def dbPage(self):
        self.new_obj=dboperation(self.new_win)
    def inactive_btn(self):
        for i in self.btn_frame.winfo_children():
            i.configure(fg="black",bg="white")
    def active_btn(self,btn):
        self.inactive_btn()
        btn.config(bg="red")
    def logout(self):
        from login import login as loin
        self.root.destroy()
        root=Tk()
        app=loin(root)
        root.mainloop()
    def closeProgram(self,event):
        self.logout()    
if __name__=="__main__":
    root= Tk()
    app= IMS(root)
    root.mainloop()