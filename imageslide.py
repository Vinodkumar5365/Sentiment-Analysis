import tkinter as tk
from PIL import Image, ImageTk
import random
import glob

class gui:
    def_init_(self,mainwin):

     self.counter=0   
     self.mainwin = mainwin
     self.mainwin.title('Tkinter Picture Frame ')
     self.mainwin.state('zoomed')

     self.mainwin.configure(bg='yellow')
     self.frame = tk.Frame(mainwin)

     self.img=tk.Lable(self.frame)

     self.frame.place(relheight=0.85,relwidth=0.9,relx=0.05,rely=0.05)
     self.img.pack()

     self.color()
     self.pic()
    def color(self):
        self.colors=['snow','ghost white']
        
     c = random.choice(self.colors) 
     self.mainwin.configure(bg=c)
     self.frame.config(bg=c)
     root.after(2000,self.color)
    def pic(self):

        self.pic_list=[]

        for name in glob.glob(r'C:\Users\jaspr\desktop\proj folder\*')
            val=name
            self.pic_list.append(val)

        if self.counter==len(self.pic_list) -1:
            self.counter=0  

        else:
            self.counter=self.counter+1     

        self.file=self.pic_list[self.counter]
        self.load=Image.open(self.file)

        self.pic_width=self.load.size[0]
        self.pic_hetight=self.load.size[1]

        self.real_aspect=self.pic_width/self.pic_hetight

        self.cal_width=int(self.real_aspect*800) 

        self.load2=self.load.resize((self.cal_width,800)) 

        self.render=ImageTk.PhotoImage(self.load2)
        self.img.config(image=self.render)
        self.img.image=self.render
        root.after(2000,self.pic)

     
             
root=tk.Tk()
myprog=gui(root) 
root.mainloop()

