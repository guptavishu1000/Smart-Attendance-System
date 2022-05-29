import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *
import customtkinter   as ctk     # for better UI
from PIL import Image , ImageTk
import PIL
import pyttsx3

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue") 

PATH = "\\".join(os.path.dirname(os.path.realpath(__file__)).split("\\")[:-1])
home_image = PIL.Image.open(PATH + "\\Icons\\home.png")
home_image = home_image.resize((50, 50), Image.ANTIALIAS)

def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.setProperty('voice', engine.getProperty('voices')[1].id)
    engine.say(user_text)
    engine.runAndWait()

def show_attendance():
    def calculate_attendance():
        Subject = tx.get()
        while Subject=="":
            t='Please enter the subject name.'
            text_to_speech(t)
    
        os.chdir(
            PATH+"\\Attendance\\"+Subject
        )
        filenames = glob(
            PATH+"\\Attendance\\"+ Subject +"\\"+Subject+"*.csv"
        )
        df = [pd.read_csv(f) for f in filenames]
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)
        newdf["Attendance"] = 0
        for i in range(len(newdf)):
            newdf["Attendance"].iloc[i] = str(int(round(newdf.iloc[i, 2:-1].mean() * 100)))+'%'
            #newdf.sort_values(by=['Enrollment'],inplace=True)
        newdf.to_csv("attendance.csv", index=False)

        root = tk.Tk()
        root.title("Attendance of "+Subject)
        
        cs = PATH+"\\Attendance\\"+Subject+"\\attendance.csv"
        with open(cs) as file:
            reader = csv.reader(file)
            r = 0
            for col in reader:
                c = 0
                for row in col:
                    label = tkinter.Label(root,width=10,height=1,fg="white",
                        font=("times", 15, " bold "),bg="black",text=row,
                        relief=tkinter.RIDGE,
                    )
                    label.grid(row=r, column=c)
                    c += 1
                r += 1
        root.mainloop()
        print(newdf)

    subject = ctk.CTk()
    subject.title("Subject...")
    subject.geometry("800x500")
    # subject.resizable(0, 0)
   
    def home():
        subject.destroy()
        import os
        os.system('main.py')
    def Attf():
        sub = tx.get()
        if sub == "":
            t="Please enter the subject name"
            text_to_speech(t)
        else:
            os.startfile(
            PATH+"\\Attendance\\"+sub
            )

    frame_right = ctk.CTkFrame(subject,height=500,width=800)
    frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

    frame_right.rowconfigure((0, 1, 2, 3), weight=1)
    frame_right.rowconfigure(7, weight=10)
    frame_right.columnconfigure((0, 1), weight=1)
    frame_right.columnconfigure(2, weight=0)

    titl = ctk.CTkLabel(frame_right,
        text="Which Subject of Attendance?",
        text_font=("arial", 15)
    )
    titl.grid(row=1, column=0, pady=10, padx=20)
    # titl.place(x=100, y=12)

    homeButton = ctk.CTkButton(master=frame_right, image=ImageTk.PhotoImage(image=home_image),
                                    text="",  height=40,
                                   compound="right", command=home)
    # homeButton.place(x=550, y= 10)
    homeButton.grid(row=1, column=3, pady=10, padx=20)


    sub = ctk.CTkLabel(frame_right,text="Enter Subject",
        text_font=("Roboto Medium", -22),height=4,width=25,
    )
    sub.grid(row=11, column=0, pady=20, padx=20)

    tx = ctk.CTkEntry(frame_right,width=180,
        text_font=("Roboto Medium", -20),height=3,
    )
    tx.grid(row=11, column=1, pady=20, padx=20,sticky="we")

    fill_a = ctk.CTkButton(
        frame_right,text="View Attendance",command=calculate_attendance,
        text_font=("Roboto Medium", -22),height=4,width=25,
        fg_color="#FF7D33", hover_color="#FFC733"
    )
    fill_a.grid(row=15,column=0, pady=20, padx=20)
    attf = ctk.CTkButton(frame_right,
        text="Check Sheets",command=Attf,text_font=("Roboto Medium", -22),
        fg_color="#FF7D33", hover_color="#FFC733", 
        
        height=4,width=25,
    )
    attf.grid(row=15,column=1, pady=20, padx=20)
    
    subject.mainloop()
