import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database import connect_db
from tool_ import loadConfig,openCalendar
from PIL import ImageTk,Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class reporter_:
    def __init__(self,root) -> None:
        self.root=root
        self.var_creation()

        self.iconimg=ImageTk.PhotoImage(file=f'{self.ROOT_DIR_images}icon.png')
        self.root.iconphoto(False,self.iconimg)

        self.root.geometry("1100x500+220+130")
        self.root.title("Reporting @Inventory Management System | Developed by KG")
        self.root.config(bg="lightblue")
        self.root.resizable(False,False)
        self.root.focus_force()

        ##===============Report Control Frame====================================
        frame= Frame(self.root,bg="lightpink",relief="raised",bd=3)
        frame.place(x=5,y=125,width=400,height=270)
        #===================Category Details==============================
        title_= Label(self.root,text="Report",bg="#0f4d7d",fg="white",font=("goudy old style",15,"bold")).place(x=5,y=10,width=1090)

        lbl_type= Label(frame,text="Report Type:",bg="lightpink",font=("goudy old style",15,"bold")).place(x=50,y=50)

        # lbl_contact= Label(self.root,text="Contact:",bg="white",font=("goudy old style",15,"bold")).place(x=50,y=130)
        cmb_type=ttk.Combobox(frame,textvariable=self.var_type_list,values=("Select","Buy","Sell","Build","Product","Customer","Supplier","Employer"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_type.place(x=170,y=50,width=180)
        cmb_type.current(0)

        lbl_s_date= Label(frame,text="Start Date:",bg="lightpink",font=("goudy old style",15,"bold")).place(x=50,y=90)
        txt_s_date= Entry(frame,textvariable=self.var_txt_s_date,font=("goudy old style",15,"bold"),bg="lightyellow",state=DISABLED).place(x=170,y=90,width=180)       
        self.btn_s_date_picker=Button(frame,text="\uE1DC",command=lambda:self.openCalen(1),font=("Segoe MDL2 Assets",14),bg="white")
        self.btn_s_date_picker.place(x=355,y=90,width=30)

        lbl_e_date= Label(frame,text="End Date:",bg="lightpink",font=("goudy old style",15,"bold")).place(x=50,y=130)
        txt_e_date= Entry(frame,textvariable=self.var_txt_e_date,font=("goudy old style",15,"bold"),bg="lightyellow",state=DISABLED).place(x=170,y=130,width=180)
        self.btn_e_date_picker=Button(frame,text="\uE1DC",command=lambda:self.openCalen(2),font=("Segoe MDL2 Assets",14),bg="white")
        self.btn_e_date_picker.place(x=355,y=130,width=30)
        
        lbl_chart_type= Label(frame,text="Report Type:",bg="lightpink",font=("goudy old style",15,"bold")).place(x=50,y=170)
        cmb_chart_type=ttk.Combobox(frame,textvariable=self.var_chart_list,values=("Select","Pie","Line","Bar","Plot"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_chart_type.place(x=170,y=170,width=180)
        cmb_chart_type.current(0)        
        ##================Button Frame===========================
        btn_gen=Button(frame,text="Generate",command=self.generate_chart,font=("goudy old style",15),bg="orange",fg="white",cursor="hand2").place(x=50,y=210,width=115,height=28)
       
        btn_clear=Button(frame,text="Reset",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=200,y=210,width=115,height=28)
    # ===========================Canvas for chart===========================
        self.right_frame=Frame(self.root,bg="lightyellow",bd=2,relief="ridge")
        self.right_frame.place(x=407,y=45,width=690,height=450)

        
    def generate_chart(self):
        if self.var_type_list.get()=="Select" or self.var_chart_list.get()=="Select" or self.var_txt_s_date.get()=="" or self.var_txt_e_date.get()=="": 
            messagebox.showwarning("Missing!","Please fill all the inputs and choices.....",parent=self.root)
        elif self.var_chart_list.get()=="Pie":
            self.getData()
            self.pie_chart()
        elif self.var_chart_list.get()=="Bar":
            self.getData()
            self.bar_chart()
        elif self.var_chart_list.get()=="Line":
            self.getData()
            self.line_chart()
        elif self.var_chart_list.get()=="Plot":
            self.getData()
            self.plot_chart()

    def pie_chart(self):
        if self.canvas!=None: self.canvas.get_tk_widget().pack_forget()
        labels = ['A', 'B', 'C', 'D']
        self.chart_datas = [15, 90, 45, 10]  # These values should add up to 100% for a pie chart
        
        fig, ax = plt.subplots(figsize=(9,9),subplot_kw=dict(aspect="equal"))
        
        wedges, texts, autotexts=ax.pie(self.datas, autopct='%1.1f%%', textprops={'size':'smaller'},startangle=90)
        ax.set_title('Sample Pie Chart')

        ax.legend(wedges, self.visual,title="Summary",loc="best",bbox_to_anchor=(1, 0, 0.5, 1))
        plt.setp(autotexts,size=8,weight="bold")
       

        # Embed the pie chart in a Tkinter canvas
        self.canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack()


    # def pie_chart(self):
    #     if self.canvas!=None: self.canvas.get_tk_widget().pack_forget()
    #     labels = ['A', 'B', 'C', 'D']
    #     self.chart_datas = [15, 30, 45, 10]  # These values should add up to 100% for a pie chart

    #     fig, ax = plt.subplots()
    #     ax.pie(self.chart_datas, labels=self.chart_label, autopct='%1.1f%%', startangle=90)
    #     ax.set_title('Sample Pie Chart')

    #     # Embed the pie chart in a Tkinter canvas
    #     self.canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
    #     self.canvas.get_tk_widget().pack()

    def bar_chart(self):
        if self.canvas!=None: self.canvas.get_tk_widget().pack_forget()

        fig, ax = plt.subplots()
        ax.bar(self.chart_label, self.chart_datas)
        ax.set_xlabel('Categories')
        ax.set_ylabel('Values')
        ax.set_title('Sample Bar Chart')

        self.canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack()
    def line_chart(self):
        if self.canvas!=None: self.canvas.get_tk_widget().pack_forget()

        x_values = [1, 2, 3, 4]
        y_values = [10, 25, 15, 30, 50]

        # Create a line chart
        fig, ax = plt.subplots()
        ax.plot(x_values, self.chart_datas, marker='o')
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title('Sample Line Chart')

        self.canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack()
    def plot_chart(self):
        if self.canvas!=None: self.canvas.get_tk_widget().pack_forget()
        x_values = [1, 2, 3, 4, 5]
        y_values = [10, 25, 15, 30, 20]

        fig, ax = plt.subplots()
        ax.scatter(x_values, y_values, marker='o', color='b')
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title('Sample Scatter Plot Chart')

        self.canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack()
    def getData(self):
        self.labels=[]
        self.datas=[]
        self.visual=[]
        con=connect_db() #module from database.py
        mycur= con.cursor()
        
        match(self.var_type_list.get()):
            case "Buy":
                print("Buy data requesting....")
            case "Sell":
                try:
                    sql="SELECT pid,sum(total) FROM saleorder group by pid"
                    # val=(self.var_buyid.get(),)
                    mycur.execute(sql)
                    row=mycur.fetchall()
                    
                    if row is not None:
                        for r in row:
                            self.labels.append(r[0])
                            self.datas.append(r[1])
                            self.visual.append(r[0]+"="+str(int(r[1])))



                except Exception as ex:
                    messagebox.showerror("Error2",f"Error due to : {(ex)}",parent=self.root)
            case  "Build":
                print("Build data requesting....")
            case "Product":
                print("Product data requesting....")
            case "Customer":
                print("Customer information requesting....")
            case "Supplier":
                print("Supplier data requesting....")
            case "Employee":
                print("Employee data requesting....")
            case _:
                print("other")
            
# "Buy","Sell","Build","Product","Customer","Supplier","Employer"

    def openCalen(self,num):
        if self.new_win!=None: self.new_win.destroy()
        self.new_win= Toplevel(self.root)
        if num==1:
            openCalendar(self.new_win,self.var_txt_s_date,self.btn_s_date_picker)
        else:
            openCalendar(self.new_win,self.var_txt_e_date,self.btn_e_date_picker)
    def clear(self):
        self.var_type_list.set("Select")
        self.var_chart_list.set("Select")
        self.var_txt_s_date.set("")
        self.var_txt_e_date.set("") 
        if self.canvas!=None: self.canvas.get_tk_widget().pack_forget()

    def var_creation(self):
        self.labels=[]
        self.datas=[]
        self.visual=[]
        self.var_type_list=StringVar()
        self.var_chart_list=StringVar()
        self.var_txt_s_date=StringVar()
        self.var_txt_e_date=StringVar()
        self.ROOT_DIR_images = loadConfig()['images']
        self.chart_datas=[10, 25, 15, 30]
        self.chart_label=['Category A', 'Category B', 'Category C', 'Category D']
        self.new_win=None
        self.canvas=None

if __name__=="__main__":
    root= Tk()
    app= reporter_(root)
    root.mainloop()

"""
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_scatter_plot():
    # Sample data for the scatter plot
    x_values = [1, 2, 3, 4, 5]
    y_values = [10, 25, 15, 30, 20]

    # Create a scatter plot using Matplotlib
    fig, ax = plt.subplots()
    ax.scatter(x_values, y_values, marker='o', color='b')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Sample Scatter Plot')

    # Embed the scatter plot in a Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

# Create the main window
window = tk.Tk()
window.title("Scatter Plot on Canvas Example")

# Create a button to create the scatter plot
scatter_plot_button = tk.Button(window, text="Create Scatter Plot", command=create_scatter_plot)
scatter_plot_button.pack()

# Start the Tkinter main loop
window.mainloop()


"""