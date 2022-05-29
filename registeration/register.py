import os
import tkinter as tk
from tkinter import *
import pyttsx3
import customtkinter  as ctk    # for better UI
from PIL import Image , ImageTk
import PIL


# project module
import  takeImage, trainImage
   

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

#PATH = os.path.dirname(os.path.realpath(__file__))

PATH = "\\".join(os.path.dirname(os.path.realpath(__file__)).split("\\")[:-1])
home_image = PIL.Image.open(PATH + "\\Icons\\home.png")
home_image = home_image.resize((50, 50), Image.ANTIALIAS)


def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.setProperty('voice', engine.getProperty('voices')[1].id)
    engine.say(user_text)
    engine.runAndWait()

def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True

def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x110")
    sc1.title("Warning")
    sc1.configure(background="black")
    sc1.resizable(0, 0)
    tk.Label(
        sc1,
        text="Enrollment & Name required",
        fg="white",
        bg="#FDF5DF",
        font=("times", 20, " bold "),
    ).pack()
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="white",
        bg="#FDF5DF",
        width=9,
        height=1,
        activebackground="Red",
        font=("times", 20, " bold "),
    ).place(x=110, y=50)

def home():
    ImageUI.destroy()
    import os
    os.system('main.py')

PATH = "\\".join(os.path.dirname(os.path.realpath(__file__)).split("\\")[:-1])
haarcasecade_path = PATH+"\\haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    PATH+"\\TrainingImageLabel\\Trainner.yml"
)
trainimage_path = PATH+"\\TrainingImage"
studentdetail_path = (
    PATH+"\\StudentDetails\\studentdetails.csv"
)


ImageUI = ctk.CTk()
ImageUI.title("Student Registeration")
ImageUI.geometry("700x440")

frame_1 = ctk.CTkFrame(master=ImageUI, width=250, height=240, corner_radius=15)
frame_1.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")


Button = ctk.CTkLabel(master=frame_1,  width=190, height=40,
                                   text="Student Registration",text_font=("Roboto Medium", -16))
Button.grid(row=1, column=5,  padx=5, pady=10, sticky="ew")



homeButton = ctk.CTkButton(master=ImageUI, image=ImageTk.PhotoImage(image=home_image),
                                    text="",  height=40,
                                   compound="right", command=home)
homeButton.place(x=450, y= 10)



frame_2 = ctk.CTkFrame(master=ImageUI, width=250, height=240, corner_radius=15)
frame_2.grid(row=1, column=0, padx=30, pady=20, sticky="nsew")


rollno = ctk.CTkLabel(master=frame_2,  width=190, height=40,
                                   text="Roll No",text_font=("Roboto Medium", -16))
rollno.grid(row=1, column=1,  padx=5, pady=10, sticky="ew")



txt1 = tk.Entry(ImageUI, width=14, validate="key", bg="grey",
    font=("times", 22, "bold"),
)
txt1.place(x=270, y=150)

txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")


frame_3 = ctk.CTkFrame(master=ImageUI, width=250, height=240, corner_radius=15)
frame_3.grid(row=2, column=0, padx=30, pady=10, sticky="nsew")


name = ctk.CTkLabel(master=frame_3,  width=190, height=40,
                                   text="Name",text_font=("Roboto Medium", -16))
name.grid(row=1, column=1,  padx=5, pady=10, sticky="ew")

txt2 = tk.Entry(ImageUI,width=14,bg="grey",
    font=("times", 22, "bold"),
)
txt2.place(x=270, y=240)


message = ctk.CTkLabel(ImageUI,text="",width=30,height=2,
    fg="green",
    text_font=("times", 12, "bold")
)

message.place(x=100, y=300)

# take_image() and train_image()
def take_image():
    l1 = txt1.get()
    l2 = txt2.get()
    takeImage.TakeImage(l1,l2,haarcasecade_path,trainimage_path,
    message,err_screen,text_to_speech
    )
    txt1.delete(0, "end")
    txt2.delete(0, "end")
    train_image()

# image
takeImg = ctk.CTkButton(
    ImageUI,text="Register",
    command=take_image,
    text_font=("times new roman", 20),
    height=4,
    width=16,
    fg_color="#D35B58", hover_color="#C77C78",
)
takeImg.place(x=150, y=350)

def train_image():
    trainImage.TrainImage(
        haarcasecade_path,
        trainimage_path,
        trainimagelabel_path,
        message,
        text_to_speech,
    )


ImageUI.mainloop()
