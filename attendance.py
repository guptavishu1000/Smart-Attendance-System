import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import pyttsx3

# project module
from utils import show_attendance, takeImage, trainImage, automaticAttendance


def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.setProperty('voice', engine.getProperty('voices')[1].id)
    engine.say(user_text)
    engine.runAndWait()


haarcasecade_path = "F:\\desktopfile\\Attendance-Management-system-using-face-recognition\\haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "F:\\desktopfile\\Attendance-Management-system-using-face-recognition\\TrainingImageLabel\\Trainner.yml"
)
trainimage_path = "F:\\desktopfile\\Attendance-Management-system-using-face-recognition\\TrainingImage"
studentdetail_path = (
    "F:\\desktopfile\\Attendance-Management-system-using-face-recognition\\StudentDetails\\studentdetails.csv"
)
attendance_path = "F:\\desktopfile\\Attendance-Management-system-using-face-recognition\\Attendance"

# creating tkinter window
window = Tk()
window.title("Face recognizer")
window.geometry("1280x720")
dialog_title = "QUIT"
dialog_text = "Are you sure want to close?"
window.configure(background="sky blue")


# to destroy screen
def del_sc1():
    sc1.destroy()


# error message for name and no
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


def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True


a = tk.Label(
    window,
    text="Face Recognition Based\nAttendance Management System",
    bg="sky blue",
    fg="black",
    bd=10,
    font=("arial", 35),
)
a.pack()

ri = Image.open("Icons/register.png")
r = ImageTk.PhotoImage(ri)
label1 = Label(window, image=r)
label1.image = r
label1.place(x=100, y=200)

ai = Image.open("Icons/attendance.png")
a = ImageTk.PhotoImage(ai)
label2 = Label(window, image=a)
label2.image = a
label2.place(x=980, y=200)

vi = Image.open("Icons/verify.png")
v = ImageTk.PhotoImage(vi)
label3 = Label(window, image=v)
label3.image = v
label3.place(x=600, y=200)


def TakeImageUI():
    ImageUI = Tk()
    ImageUI.configure(background="sky blue")
    ImageUI.title("Take Student Image")
    ImageUI.geometry("780x480")

    # image and title
    titl = tk.Label(
        ImageUI, text="Enter the details", bg="sky blue", fg="black", font=("arial", 30),
    )
    titl.place(x=270, y=12)

    # ER no
    lbl1 = tk.Label(
        ImageUI, text="Enrollment No", width=10, height=2, bg="black", fg="white",
        bd=5, relief=RIDGE, font=("times new roman", 12),
    )
    lbl1.place(x=120, y=130)
    txt1 = tk.Entry(
        ImageUI, width=17,
        bd=5, validate="key", bg="black", fg="white",
        relief=RIDGE,
        font=("times", 25, "bold"),
    )
    txt1.place(x=250, y=130)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # name
    lbl2 = tk.Label(
        ImageUI,
        text="Name",
        width=10,
        height=2,
        bg="black",
        fg="white",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 12),
    )
    lbl2.place(x=120, y=200)
    txt2 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        bg="black",
        fg="white",
        relief=RIDGE,
        font=("times", 25, "bold"),
    )
    txt2.place(x=250, y=200)

    lbl3 = tk.Label(
        ImageUI,
        text="Notification",
        width=10,
        height=2,
        bg="black",
        fg="white",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 12),
    )
    lbl3.place(x=120, y=270)

    message = tk.Label(
        ImageUI,
        text="",
        width=32,
        height=2,
        bd=5,
        bg="black",
        fg="white",
        relief=RIDGE,
        font=("times", 12, "bold"),
    )
    message.place(x=250, y=270)

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    # take Image button
    # image
    takeImg = tk.Button(
        ImageUI,
        text="Take Image",
        command=take_image,
        bd=10,
        font=("times new roman", 18),
        bg="black",
        fg="white",
        height=2,
        width=12,
        relief=RIDGE,
    )
    takeImg.place(x=130, y=350)

    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    # train Image function call
    trainImg = tk.Button(
        ImageUI,
        text="Train Image",
        command=train_image,
        bd=10,
        font=("times new roman", 18),
        bg="black",
        fg="white",
        height=2,
        width=12,
        relief=RIDGE,
    )
    trainImg.place(x=360, y=350)


r = tk.Button(
    window,
    text="Register a new student",
    command=TakeImageUI,
    bd=10,
    font=("times new roman", 16),
    bg="black",
    fg="white",
    height=2,
    width=17,
)
r.place(x=100, y=450)


def automatic_attendance():
    automaticAttendance.subjectChoose(text_to_speech)


r = tk.Button(
    window,
    text="Take Attendance",
    command=automatic_attendance,
    bd=10,
    font=("times new roman", 16),
    bg="black",
    fg="white",
    height=2,
    width=17,
)
r.place(x=600, y=450)


def view_attendance():
    show_attendance.subjectchoose(text_to_speech)


r = tk.Button(
    window,
    text="View Attendance",
    command=view_attendance,
    bd=10,
    font=("times new roman", 16),
    bg="black",
    fg="white",
    height=2,
    width=17,
)
r.place(x=1000, y=450)
r = tk.Button(
    window,
    text="EXIT",
    bd=10,
    command=quit,
    font=("times new roman", 16),
    bg="black",
    fg="white",
    height=1,
    width=10,
)
r.place(x=1150, y=50)

window.mainloop()
