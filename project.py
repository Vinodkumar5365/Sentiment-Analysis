from os import name
import tkinter as tk
from tkinter import *
from turtle import clear
from textblob import TextBlob
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
import tkinter.ttk
import pandas as pd
import random
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import mysql.connector

db_connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = ""
)

db_cursor = db_connection.cursor()
class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("1368x768+0+0") #initialization of size of window
        
        #backgrond image
        self.bg=ImageTk.PhotoImage(file="happy_emo.jpg")
        bg=Label(self,image=self.bg).place(x=0,y=-210)

        #register frame inside the window
        frame1=Frame(self,bg="white")
        frame1.place(x=0,y=348,width=1368,height=500)

        #contents
        title=Label(frame1,text="Login",font=("times new roman",30,"bold","underline"),bg="white",fg="black").place(x=625,y=20)
        email=Label(frame1,text="Enter E-mail :",font=("times new rom an",20,"bold"),bg="white",fg="black").place(x=280,y=120)
        password=Label(frame1,text="Enter Password :",font=("times new roman",20,"bold"),bg="white",fg="black").place(x=895,y=120)

        #creates the entry fields
        self.txt_mail=Entry(frame1,font=("times new roman",15),bg="lightgrey",bd="1")
        self.txt_mail.place(x=100,y=200,width=530)

        def togglep():
            if self.txt_pass.cget('show') == '':
                self.txt_pass.config(show='*')
            else:
                self.txt_pass.config(show='')

        self.txt_pass=Entry(frame1,font=("times new roman",15),bg="lightgrey",bd="1")
        self.txt_pass.place(x=738,y=200,width=490)
        self.toggle_btn=ImageTk.PhotoImage(file="eye.png")
        toggle_btn = Button(frame1,text=' ',bg="white",image=self.toggle_btn,bd="2",cursor="hand2", command=togglep).place(x=1238,y=200,width=30,height=30)

        #creates the buttons
        btn=Button(frame1,text="LOGIN",font=("times new roman",20,"bold"),bg="#34495e",fg="white",bd="4",cursor="hand2",command=self.login).place(x=100,y=300,width=350)
        btn=Button(frame1,text="CLEAR",font=("times new roman",20,"bold"),bg="#34495e",fg="white",bd="4",cursor="hand2",command=self.clear_form).place(x=559,y=300,width=250)
        btn=Button(frame1,text="REGISTER",font=("times new roman",20,"bold"),bg="#34495e",fg="white",bd="4",cursor="hand2",command=self.open_registration_window).place(x=918,y=300,width=350)

    #clears the contents on click
    def clear_form(self):
        self.txt_email.delete(0,tkinter.END)
        self.txt_password.delete(0,tkinter.END)

    def open_registration_window(self):#opens the register window
        self.withdraw()
        window = RegisterWindow(self)
        window.grab_set()

    def show(self):
        """"""
        self.update()
        self.deiconify()

    def login(self):
        if self.txt_mail.get()=="" or self.txt_pass.get()=="":#checking the fields are empty or not
            messagebox.showerror("Error","All fields are Mandatory",parent=self)
        else :
            try :
                db_cursor.execute("use sent")#uses the database
                db_cursor.execute("select * from registers where email=%s and password=%s",(self.txt_mail.get(),self.txt_pass.get()))
                row=db_cursor.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Email and Password",parent=self)#checks the fields are valid are not
                else :
                    self.withdraw()
                    self.txt_mail.delete(0,END)
                    self.txt_pass.delete(0,END)
                    window = Login_Success_Window(self)#enters the main generator page
                    window.grab_set()
            except Exception as es :
                messagebox.showerror("Error",f"Error Due to : {str(es)}",parent=self)

    def exit(self):
        MsgBox = messagebox.askquestion('Exit Application', 'Are you sure you want to exit the application',icon='warning')
        if MsgBox == 'yes':
            self.destroy()

class Login_Success_Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.title("SENTIMENT ANALYSIS")
        self.geometry("1368x768+0+0") #initialization of size of window

        self.bg=ImageTk.PhotoImage(file="many_moods.jpg")
        bg=Label(self,image=self.bg).place(x=0,y=-250)

        frame1=Frame(self,bg="white")
        frame1.place(x=0,y=350,width=1368,height=418)

        title=Label(frame1,text="Sentiment Analysis",font=("times new roman",30,"bold","underline"),bg="white",fg="black").place(x=80,y=5)
        
        btn1=Button(frame1,text="LOGOUT",font=("times new roman",15,"bold"),bg="#2f0340",fg="white",bd="4",cursor="hand2",command=self.logout).place(x=988,y=10,width=300)

        #code for textblob library
        def texblob():
            p_c = 0
            p_crt = 0

            with open("pos.txt","r", encoding="utf8") as a:
                for line in a.read().split('\n'):
                    b = TextBlob(line)
                    if b.sentiment.polarity > 0:
                        p_crt += 1
                    p_c += 1

            n_c = 0
            n_crt = 0

            with open("neg.txt","r", encoding="utf8") as x:
                for line in x.read().split('\n'):
                    y = TextBlob(line)
                    if y.sentiment.polarity <= 0:
                        n_crt += 1
                    n_c += 1

            x = ("The Average of the Positive Accuracy of the given reviews is {}% via {} samples".format(p_crt/p_c*100.0,p_c))
            label_1.config(text=x)

            y = ("The Average of the Negatve Accuracy of the given reviews is {}% via {} samples".format(n_crt/n_c*100.0,n_c))
            label_3.config(text=y)

            z = " "
            label_5.config(text=z)

        #code for vader sentiment library
        def vadersen():
            a = SentimentIntensityAnalyzer()

            pos_v = 0
            pos_vc = 0
            neg_v = 0
            neg_vc = 0
            neu_v = 0
            neu_vc = 0

            with open("tot.txt","r", encoding="utf8") as b:
                for line in b.read().split('\n'):
                    vs = a.polarity_scores(line)
                    if vs['compound'] >= 0:
                        pos_vc +=1
                    pos_v +=1
                    if vs['compound'] == 0:
                        neu_vc +=1
                    neu_v +=1
                    if vs['compound'] <= 0:
                        neg_vc +=1
                    neg_v +=1

            m=pos_vc/pos_v*100.0
            x = ("The Average of the Positive Accuracy of the given reviews is {}% via {} samples".format(m,pos_v))
            label_1.config(text=x)

            n=neu_vc/neu_v*100.0
            y = ("The Average of the Neutral Accuracy of the given reviews is {}% via {} samples".format(n,neu_v))
            label_3.config(text=y)

            o=neg_vc/neg_v*100.0
            z = ("The Average of the Negatve Accuracy of the given reviews is {}% via {} samples".format(o,neg_v))
            label_5.config(text=z)
            
        btn2=Button(frame1,text="TextBlob",font=("times new roman",17,"bold"),bg="#2f0340",fg="white",bd="4",cursor="hand2",command=texblob).place(x=288,y=70,width=280,height=40)
        btn3=Button(frame1,text="Vader",font=("times new roman",17,"bold"),bg="#2f0340",fg="white",bd="4",cursor="hand2",command=vadersen).place(x=738,y=70,width=280,height=40)

        label_1=Label(frame1,text="",bg="white")
        label_1.place(x=80,y=160)
        label_2=Label(frame1,text="",bg="white")
        label_2.place(x=80,y=180)
        label_3=Label(frame1,text="",bg="white")
        label_3.place(x=80,y=220)
        label_4=Label(frame1,text="",bg="white")
        label_4.place(x=80,y=240)
        label_5=Label(frame1,text="",bg="white")
        label_5.place(x=80,y=280)
        label_6=Label(frame1,text="",bg="white")
        label_6.place(x=80,y=300)

    def logout(self):#enters into login page
        MsgBox = messagebox.askquestion('Exit Application', 'Are you sure you want to Logout',icon='warning')
        if MsgBox == 'yes':
            self.destroy()
            self.original_frame.show()

class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.title("Registeration Window")
        self.geometry("1368x768+0+0") #initialization of size of window

        self.bg=ImageTk.PhotoImage(file="five_moods.jpg")
        bg=Label(self,image=self.bg).place(x=0,y=170)

        #register frame inside the window
        frame2=Frame(self,bg="white")
        frame2.place(x=0,y=0,width=1368,height=468)

        #contents
        title=Label(frame2,text="Register",font=("times new roman",35,"bold","underline"),bg="white",fg="black").place(x=600,y=30)

        #Labels of the text boxes and entry fields

        name=Label(frame2,text="Enter Name :",font=("times new roman",20,"bold"),bg="white",fg="black").place(x=280,y=100)
        self.txt_name=Entry(frame2,font=("times new roman",15),bg="lightgrey",bd="1")
        self.txt_name.place(x=100,y=170,width=530)

        mobile=Label(frame2,text="Enter Mobile No. :",font=("times new roman",20,"bold"),bg="white",fg="black").place(x=885,y=100)
        self.txt_mobile=Entry(frame2,font=("times new roman",15),bg="lightgrey",bd="1")
        self.txt_mobile.place(x=738,y=170,width=530)

        email=Label(frame2,text="Enter E-mail :",font=("times new roman",20,"bold"),bg="white",fg="black").place(x=270,y=230)
        self.txt_email=Entry(frame2,font=("times new roman",15),bg="lightgrey",bd="1")  
        self.txt_email.place(x=100,y=300,width=530)

        password=Label(frame2,text="Enter Password :",font=("times new roman",20,"bold"),bg="white",fg="black").place(x=895,y=230)
        def togglepa():
            if self.txt_password.cget('show') == '':
                self.txt_password.config(show='*')
            else:
                self.txt_password.config(show='')

        self.txt_password=Entry(frame2,font=("times new roman",15),bg="lightgrey",bd="1")
        self.txt_password.place(x=738,y=300,width=490)
        self.toggle_btn=ImageTk.PhotoImage(file="eye.png")
        toggle_btn = Button(frame2,text=' ',bg="white",image=self.toggle_btn,bd="2",cursor="hand2", command=togglepa).place(x=1238,y=300,width=30,height=30)

        #buttons
        bt1=Button(frame2,text="LOGIN",font=("times new roman",18,"bold"),bg="#303952",fg="white",bd="4",cursor="hand2",command=self.onClose).place(x=100,y=380,width=350)
        bt2=Button(frame2,text="CLEAR",font=("times new roman",18,"bold"),bg="#303952",fg="white",bd="4",cursor="hand2",command=self.clear_form).place(x=559,y=380,width=250)
        bt3=Button(frame2,text="REGISTER",font=("times new roman",18,"bold"),bg="#303952",fg="white",bd="4",cursor="hand2",command=self.register_data).place(x=918,y=380,width=350)

    #clears the contents on click
    def clear_form(self):
        self.txt_name.delete(0,tkinter.END)
        self.txt_email.delete(0,tkinter.END)
        self.txt_mobile.delete(0,tkinter.END)
        self.txt_password.delete(0,tkinter.END)

    #data insertion on database
    def register_data(self):
        db_cursor.execute("CREATE DATABASE IF NOT EXISTS sent")
        db_cursor.execute("use sent")#uses database
        db_cursor.execute("Create table if not exists registers(name VARCHAR(30) NOT NULL  PRIMARY KEY,email VARCHAR(30),mobile VARCHAR(10),password VARCHAR(15))")
        db_connection.commit()#enters the data

        if self.txt_name.get()=="" or self.txt_email.get()=="" or self.txt_mobile.get()=="" or self.txt_password.get()=="":
            messagebox.showerror("Error","All fields are Mandatory",parent=self)
        else:
            db_cursor.execute("use sent")
            query ="INSERT INTO registers(name,email,mobile,password) VALUES ('%s','%s','%s','%s')" %(self.txt_name.get(),self.txt_email.get(),self.txt_mobile.get(),self.txt_password.get())
            db_connection.commit()
            try:
                db_cursor.execute(query)
                messagebox.showinfo('Information', "Data inserted Successfully")
                db_connection.commit()
                #clearing the contents of the register page after data inserted
                self.txt_name.delete(0,tkinter.END)
                self.txt_email.delete(0,tkinter.END)
                self.txt_mobile.delete(0,tkinter.END)
                self.txt_password.delete(0,tkinter.END)
            except:
                messagebox.showinfo('Information', "Data inserted Successfully")
                db_connection.rollback()

    def onClose(self):
        """"""
        self.destroy()
        self.original_frame.show()

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()