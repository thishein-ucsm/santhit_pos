from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from ims import *
from tool_ import loadConfig
class splash:
    def __init__(self) -> None:
            self.win=Tk()
            self.ROOT_DIR = loadConfig()['images']
            print(self.ROOT_DIR)
            self.backgroundImage=ImageTk.PhotoImage(file=f"{self.ROOT_DIR}logo.jpg")

            # self.backgroundImage = PhotoImage(file=f'{self.ROOT_DIR}logo1.jpg')
            self.app_name   = "Tet Lu Shop"
            self.i=0
            self.sc_width   = self.win.winfo_screenwidth()
            self.sc_height  = self.win.winfo_screenheight()
            self.app_width  = 530
            self.app_height = 430
            self.x  = (self.sc_width//2)-(self.app_width//2)
            self.y  = (self.sc_height//2)-(self.app_height//2)
            self.win.geometry("{}x{}+{}+{}".format(self.app_width,self.app_height,self.x,self.y))

            welcome= Label(text=self.app_name,bg="#2F6C60",font=("Roboto Slab",26,"bold"),fg="#ffffff")
            welcome.place(x=80,y=25)

            bg_label= Label(self.win,image=self.backgroundImage,bg="#2F6C60")
            bg_label.place(x=130,y=69)

            self.progress_label= Label(self.win,text="Loading....",font=("Trebuchet Ms",13,"bold"),fg="#ffffff",bg="#2F6C60")
            self.progress_label.place(x=190,y=330)

            self.progress = ttk.Style()
            self.progress.theme_use("clam")
            self.progress.configure("red.Horizontal.TProgressbar",background="#108cff")
            self.progress = ttk.Progressbar(self.win,orient=HORIZONTAL,length=400,mode='determinate',style="red.Horizontal.TProgressbar")
            self.progress.place(x=60,y=370)
            self.load()

            self.win.config(background="#2F6C60")
            self.win.overrideredirect(True)

            # self.setAppName(self.app_name)
            self.win.mainloop()
    def load(self):
        if self.i<=10:
            txt = "Loading .... "+(str(10*self.i)+"%")
            self.progress_label.config(text=txt)
            self.progress_label.after(600,self.load)
            self.progress['value']=10*self.i
            self.i+=1
        else:
            self.callMain()
    # def getAppname():
    #      return str(app_name1)
    def callMain(self):

        self.win.withdraw()
        os.system(f"python {self.ROOT_DIR}\\login.py")
        self.win.destroy()
if __name__== "__main__":
        splash  = splash()

