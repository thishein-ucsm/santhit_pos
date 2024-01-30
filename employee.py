from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database import connect_db
from tool_ import isStatusOK,loadConfig
import os
from PIL import ImageTk
class employee:
    def __init__(self,root) -> None:
        self.root=root
        self.ROOT_DIR = loadConfig()['images']
        self.iconimg=ImageTk.PhotoImage(file=f'{self.ROOT_DIR}icon.png')
        self.root.iconphoto(False,self.iconimg)

        self.root.geometry("1100x500+220+130")
        self.root.title("Employee @Inventory Management System | Developed by KG")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()
        self.var_creation()

        ##===============Label Frame====================================
        searchFrame=LabelFrame(self.root,text="Search Employee",bg="white",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE)
        searchFrame.place(x=250,y=20,width=600,height=70)

        cmb_search=ttk.Combobox(searchFrame,textvariable=self.var_emp_searchby,values=("Select","Contact","DOB","Gender","Name","NRC","Salary","Address","UserType"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(searchFrame,textvariable=self.var_emp_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(searchFrame,command=self.search,text="Search",font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)

        #===================Employee Details==============================
        title_employee= Label(self.root,text="Employee Details",bg="#0f4d7d",fg="white",font=("goudy old style",15,"bold")).place(x=50,y=100,width=1000)

        lbl_id= Label(self.root,text="EmpID:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=150)
        lbl_gender= Label(self.root,text="Gender:",bg="white",font=("goudy old style",15,"bold")).place(x=350,y=150)
        lbl_contact= Label(self.root,text="Contact:",bg="white",font=("goudy old style",15,"bold")).place(x=750,y=150)
        
        txt_id= Entry(self.root,textvariable=self.var_emp_id,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=150,y=150,width=180)       
        cmb_gender=ttk.Combobox(self.root,textvariable=self.var_emp_gender,values=("Select","Female","Male","Other"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_gender.place(x=500,y=150,width=180)
        cmb_gender.current(0)
        txt_contact= Entry(self.root,textvariable=self.var_emp_contact,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=850,y=150,width=180)

        lbl_name= Label(self.root,text="Name:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=190)
        lbl_dob= Label(self.root,text="DOB:",bg="white",font=("goudy old style",15,"bold")).place(x=350,y=190)
        lbl_nrc= Label(self.root,text="NRC:",bg="white",font=("goudy old style",15,"bold")).place(x=750,y=190)
        txt_name= Entry(self.root,textvariable=self.var_emp_name,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=150,y=190,width=180)
        txt_dob= Entry(self.root,textvariable=self.var_emp_dob,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=500,y=190,width=180)

        txt_nrc= Entry(self.root,textvariable=self.var_emp_nrc,font=("goudy old style",15,"bold"),bg="lightyellow").place(x=850,y=190,width=180)       

        lbl_address= Label(self.root,text="Address:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=230)
        lbl_salary= Label(self.root,text="Salary:",bg="white",font=("goudy old style",15,"bold")).place(x=350,y=230)
        lbl_type= Label(self.root,text="UserType:",bg="white",font=("goudy old style",15,"bold")).place(x=750,y=230)
        self.txt_address= Text(self.root,font=("goudy old style",15,"bold"),bg="lightyellow")
        self.txt_address.place(x=150,y=230,width=180,height=60)
        txt_salary= Entry(self.root,textvariable=self.var_emp_salary,bg="lightyellow",font=("goudy old style",15,"bold")).place(x=500,y=230,width=180)
        # txt_salary.insert(END,0)
        cmb_type=ttk.Combobox(self.root,textvariable=self.var_emp_usertype,values=("Select","Accountant","Admin","Cashier","Other"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_type.place(x=850,y=230,width=180)
        cmb_type.current(0)

        ##================Button Fram===========================
        btn_save=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="#33bbf9",fg="white",cursor="hand2").place(x=500,y=270,width=115,height=28)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="#ff5722",fg="white",cursor="hand2").place(x=620,y=270,width=115,height=28)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="#009688",fg="white",cursor="hand2").place(x=740,y=270,width=115,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=860,y=270,width=115,height=28)

        ##==========table frame====================================
        emp_frame= Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=305,relwidth=1,height=195)
        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)
        self.emp_table=ttk.Treeview(emp_frame,columns=("sr","eid","name","dob","nrc","gen","cont","sal","type","addr"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.emp_table.xview)
        scrolly.config(command=self.emp_table.yview)
        self.emp_table.heading("sr",text="Sr.")
        self.emp_table.heading("eid",text="EmpID")
        self.emp_table.heading("name",text="Name")
        self.emp_table.heading("dob",text="DOB")
        self.emp_table.heading("nrc",text="NRC")
        self.emp_table.heading("gen",text="Gender")
        self.emp_table.heading("cont",text="Contact")
        self.emp_table.heading("type",text="UserType")
        self.emp_table.heading("sal",text="Salary")
        self.emp_table.heading("addr",text="Address")

        self.emp_table["show"]="headings"
        self.emp_table.column("sr",width=10)
        self.emp_table.column("eid",width=90)
        self.emp_table.column("name",width=100)
        self.emp_table.column("dob",width=100)
        self.emp_table.column("nrc",width=100)
        self.emp_table.column("gen",width=100)
        self.emp_table.column("cont",width=100)
        self.emp_table.column("type",width=100)
        self.emp_table.column("sal",width=100)
        self.emp_table.column("addr",width=100)
        self.emp_table.pack(fill=BOTH,expand=1)
        self.emp_table.bind('<ButtonRelease-1>',self.getdata)
        
        self.show()
    def show(self):
        con=connect_db()
        mycur= con.cursor()
        try:
            sql="SELECT * FROM employee"
            mycur.execute(sql)
            rows=mycur.fetchall()
            self.emp_table.delete(*self.emp_table.get_children())
            for row in rows:
                self.emp_table.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    def getdata(self,ev):
        try:
            f= self.emp_table.focus()
            content= (self.emp_table.item(f))
            row=content['values']
        
            self.var_emp_id.set(row[1])
            self.var_emp_name.set(row[2])
            self.var_emp_nrc.set(row[3])
            self.var_emp_dob.set(row[4])
            self.var_emp_gender.set(row[5])
            self.var_emp_contact.set(row[6])
            self.var_emp_salary.set(row[7])
            self.var_emp_usertype.set(row[8])
            self.txt_address.delete('1.0',END)
            self.txt_address.insert(END,row[9])
        except IndexError as ex:
            messagebox.showerror("Ops!","There is no record on table or Be Careful to click on row",parent=self.root)
    def add(self):
        con=connect_db() #module from database.py
        mycur= con.cursor()
 
        # calling create_emp from database.py
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID missing!",parent=self.root)
            else:
                sql="SELECT * FROM employee where empid=%s"
                val=(self.var_emp_id.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Duplicate employee\'s id",parent=self.root)
                else:
                    sql="INSERT INTO employee(empid,name,dob,nrc,gender,contact,salary,usertype,address)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    val=(self.var_emp_id.get(),self.var_emp_name.get(),
                         self.var_emp_dob.get(),self.var_emp_nrc.get(),
                         self.var_emp_gender.get(),self.var_emp_contact.get(),
                         self.var_emp_salary.get(),self.var_emp_usertype.get(),
                         self.txt_address.get('1.0',END)

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
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID missing!",parent=self.root)
            else:
                sql="SELECT empid FROM employee where empid=%s"
                val=(self.var_emp_id.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee\'s ID",parent=self.root)
                else:
                    # "eid","name","nrc","gen","cont","dob","type","sal","addr"
                    sql="UPDATE employee SET name=%s,nrc=%s,dob=%s,gender=%s,contact=%s,salary=%s,usertype=%s,address=%s where empid=%s"
                    val=(self.var_emp_name.get(),self.var_emp_nrc.get(),
                         self.var_emp_dob.get(),self.var_emp_gender.get(),
                         self.var_emp_contact.get(),self.var_emp_salary.get(),
                         self.var_emp_usertype.get(),self.txt_address.get('1.0',END),
                         self.var_emp_id.get()

                         )
                    
        ##### isStatusOK is checking whether one of the fields missing of not
                    if self.isStatusOK(val):
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
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID missing!",parent=self.root)
            else:
                sql="SELECT empid FROM employee where empid=%s"
                val=(self.var_emp_id.get(),)
                mycur.execute(sql,val)
                row=mycur.fetchone()
                if row==None:
                    messagebox.showerror("Error","There is no record found with your Employee\'s ID",parent=self.root)
                else:
                    ans=messagebox.askyesno("Confirmation",f"Are you sure want to Delete {self.var_emp_id.get()}?",parent=self.root)
                    if ans==True:
                        mycur.execute("DELETE FROM employee where empid=%s",(self.var_emp_id.get(),))
                        con.commit()
                        con.close()
                        messagebox.showinfo("Success","Your Record has been Deleted from Database!",parent=self.root)
                        self.clear()
                        self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    def clear(self):
        self.var_emp_searchby.set("Select")
        self.var_emp_searchtxt.set("")
        
        self.var_emp_id.set("")
        self.var_emp_name.set("")
        self.var_emp_nrc.set("")
        self.var_emp_gender.set("Select")
        self.var_emp_dob.set("")
        self.var_emp_usertype.set("Select")
        self.txt_address.delete('1.0',END)
        self.var_emp_salary.set("0")
        self.var_emp_contact.set("")
        self.show()
    def search(self):
        con=connect_db()
        mycur= con.cursor()
        try:
            if self.var_emp_searchby.get()=="Select":
                messagebox.showerror("Error","Choose some option in \"Search By option\"",parent=self.root)
            elif self.var_emp_searchtxt.get()=="":
                messagebox.showerror("Error","Search input should be filled",parent=self.root)
            else:
                mycur.execute("SELECT * FROM employee where "+self.var_emp_searchby.get()+" Like '%"+self.var_emp_searchtxt.get()+"%'")
                rows= mycur.fetchall()

                if len(rows)!=0:
                    self.emp_table.delete(*self.emp_table.get_children())
                    for row in rows:
                        self.emp_table.insert('',END,values=row)
                else:
                    messagebox.showinfo("Information","No record found on system",parent=self.root)
        except Exception as ex:
            pass
    def var_creation(self):
        self.var_emp_searchby=StringVar()
        self.var_emp_searchtxt=StringVar()
        self.var_emp_id=StringVar()
        self.var_emp_name=StringVar()
        self.var_emp_nrc=StringVar()
        self.var_emp_gender=StringVar()
        self.var_emp_dob=StringVar()
        self.var_emp_usertype=StringVar()
        self.var_emp_salary=StringVar()
        self.var_emp_salary.set("0")

        self.var_emp_contact=StringVar()
if __name__=="__main__":
    root= Tk()
    app= employee(root)
    root.mainloop()