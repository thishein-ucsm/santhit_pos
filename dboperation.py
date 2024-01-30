import os
import subprocess
import datetime
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from database import connect_db
from tool_ import updateConfig,loadConfig
from PIL import ImageTk,Image
class dboperation:
    def __init__(self,root) -> None:

        self.root=root
        self.var_creation()

        self.iconimg=ImageTk.PhotoImage(file=f'{self.ROOT_DIR_images}icon.png')
        self.root.iconphoto(False,self.iconimg)

        self.root.geometry("1100x500+220+130")
        self.root.title("Maintenance @Inventory Management System | Developed by KG")
        self.root.config(bg="orange")
        self.root.resizable(False,False)
        self.root.focus_force()
        title_= Label(self.root,text="Backup / Restore Data",bg="#0f4d7d",fg="white",font=("goudy old style",25,"bold")).place(x=5,y=10,width=1090,height=100)

        frame=Frame(self.root)
        frame.place(x=50,y=120,width=400,height=200)
        self.txt_bill=Text(frame,wrap=WORD)
        self.txt_bill.pack()
        self.txt_bill.insert('1.0',self.note)
        self.txt_bill.config(state=DISABLED)

        btn_backup=Button(self.root,text="Backup",command=self.backupdb,font=("goudy old style",15),bg="#33bbf9",fg="white",cursor="hand2").place(x=50,y=340,width=115,height=28)
        btn_restore=Button(self.root,text="Restore",command=self.restoredb,font=("goudy old style",15),bg="#ff5722",fg="white",cursor="hand2").place(x=200,y=340,width=115,height=28)
        btn_cancel=Button(self.root,text="Cancel",command=self.canceldb,font=("goudy old style",15),bg="#009688",fg="white",cursor="hand2").place(x=350,y=340,width=115,height=28)

        self.lbl_status=Label(self.root,text="Status: there is no database backup",font=("goudy old style",13),anchor="w",justify=LEFT,bg="lightgray")
        self.lbl_status.pack(side=BOTTOM,fill=X)
        print("time",loadConfig()['backup_time'])
        if loadConfig()['backup_time']!='':
            self.lbl_status.config(text=f"Status: {loadConfig()['backup_time']}\tLocation: {loadConfig()['latest_backup']}")
        self.sideimg=Image.open(f'{self.ROOT_DIR_images}parts\\1.png')
        self.sideimg=self.sideimg.resize((500,350),Image.LANCZOS)
        self.sideimg=ImageTk.PhotoImage(self.sideimg)

        self.lbl_image=Label(self.root,image=self.sideimg,bg="orange")
        self.lbl_image.place(x=530,y=130,width=550,height=340)
        self.counter=0
        self.files_=os.listdir(f'{self.ROOT_DIR_images}parts\\')
        self.animatePics()
        ##==========table frame====================================


    def animatePics(self):
        if self.counter<len(self.files_):
            self.animimg=Image.open(f'{self.ROOT_DIR_images}parts\\{self.files_[self.counter]}')
            self.animimg=self.animimg.resize((350,250),Image.LANCZOS)
            self.animimg=ImageTk.PhotoImage(self.animimg)
            self.lbl_image.config(image=self.animimg)
            self.counter+=1
        else: self.counter=0
        self.lbl_image.after(3000,self.animatePics)
    def backupdb(self):
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        timestamp2 = datetime.datetime.now().strftime('%H:%M:%S/%Y-%m-%d')

        backup_file = f'{self.ROOT_DIR}database\\backup_{timestamp}.sql'
        
        mysqldump_cmd = [
            'mysqldump',
            f'--host={self.db_host}',
            f'--user={self.db_user}',
            f'--password={self.db_password}',
            self.db_name,
            f'--result-file={backup_file}'
        ]
        try:
            # Execute the mysqldump command
            subprocess.run(mysqldump_cmd, check=True)
            self.lbl_status.config(text=f'Backup completed successfully! {backup_file}')
            updateConfig('latest_backup',str(backup_file))
            updateConfig('backup_time',timestamp2)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error",f'We got some error:\n {e}',parent=self.root)
            
    def restoredb(self):
        file_restore= filedialog.askopenfilename(title="Choose Latest database backup file",filetypes=(("Backup File","*.sql"),))
        # print("path ",os.path.abspath(file_restore))
        if file_restore:
            ans=messagebox.askyesno("Confirmation","Are you sure want to restore with this file? It may overwrite/wipe your data",parent=self.root)
            if ans:
                mysql_cmd = [
                    'mysql',
                    f'--host={self.db_host}',
                    f'--user={self.db_user}',
                    f'--password={self.db_password}',
                    self.db_name,
                ]

                try:
                    with open(file_restore, 'rb') as sql_file:
                        subprocess.run(mysql_cmd, stdin=sql_file, check=True)
                    messagebox.showinfo("Message",f'Database restoration completed successfully.',parent=self.root)
                except subprocess.CalledProcessError as e:
                    messagebox.showerror("Error",f'We got some errors \n{e}',parent=self.root)
        else:
            print("you choose cancel")        
    def canceldb(self):
        self.root.destroy()
    def var_creation(self):
        self.counter=0
        self.ROOT_DIR = loadConfig()['path']
        self.ROOT_DIR_images = loadConfig()['images']

        self.db_host = loadConfig()['host']
        self.db_user = loadConfig()['user']
        self.db_password = loadConfig()['pass']
        self.db_name = loadConfig()['dbname']

        self.files_=os.listdir(f'{self.ROOT_DIR_images}parts\\')
        self.note="""
\t\t\tWarning
================================================
\tThis page have high level operations, there may be risk or data failure!!!\n
Before doing some operations, make sure to backup
the database first, Thank you.....
================================================

        """
        # self.var_cat_remark="_"
if __name__=="__main__":
    root= Tk()
    app= dboperation(root)
    root.mainloop()