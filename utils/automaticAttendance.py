import tkinter as tk
from tkinter import *
import os, cv2
import pandas as pd
import datetime
import time
import pyttsx3
import customtkinter as ctk
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue") 
from PIL import Image , ImageTk
import PIL


PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
haarcasecade_path = os.path.join(PATH,"haarcascade_frontalface_default.xml")
trainimagelabel_path = os.path.join(PATH,"TrainingImageLabel","Trainner.yml")
trainimage_path = os.path.join(PATH,"TrainingImage")
studentdetail_path = os.path.join(PATH,"StudentDetails","studentdetails.csv")
attendance_path = os.path.join(PATH,"Attendance")

home_image = PIL.Image.open(os.path.join(PATH,"Icons","home.png"))
home_image = home_image.resize((50, 50), Image.ANTIALIAS)

def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.setProperty('voice', engine.getProperty('voices')[1].id)
    engine.say(user_text)
    engine.runAndWait()


# for choose subject and fill attendance
def subjectChoose():
    def FillAttendance():
        sub = tx.get()
        now = time.time()
        future = now + 10
        # print(now)
        # print(future)
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            try:
                print("Filling Attendance...")
                recognizer = cv2.face.LBPHFaceRecognizer_create()

                try:
                    recognizer.read(trainimagelabel_path)
                except:
                    e = "Model not found,please train model"
                    Notifica.configure(
                        text=e
                    )
                    Notifica.grid(row=13 , column=1,padx=20, pady=20, sticky="ew")
                    text_to_speech(e)
                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                df = pd.read_csv(studentdetail_path)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_PLAIN
                col_names = ["Roll_Number", "Name"]
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ___, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                        if conf < 70:
                            # print(conf)
                            global Subject
                            global userName
                            global date
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime(
                                "%Y-%m-%d"
                            )

                            userName = df.loc[df["Roll_Number"] == Id]["Name"].values
                            userName = str(userName[0])
                            attendance.loc[len(attendance)] = [
                                Id,
                                userName,
                            ]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                            cv2.putText(
                                im, str(userName), (x + h, y), font, 1, (255, 255, 0,), 4
                            )
                        else:
                            Id = "Unknown"
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(
                                im, str(Id), (x + h, y), font, 1, (0, 25, 255), 4
                            )
                    if time.time() > future:
                        break
                    attendance = attendance.drop_duplicates(
                        subset=["Roll_Number"], keep="last"
                    )
                    
                    cv2.imshow("Filling Attendance...", im)
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:
                        break

                ts = time.time()
                print(attendance)
                attendance[date] = 1
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
               
                # fileName = "Attendance/" + Subject + ".csv"
                # print("Line-116",attendance)
                path = os.path.join(attendance_path, Subject)
                if not os.path.isdir(path):
                    os.mkdir(
                        path
                    )
                # print("path",pa`th)
                fileName = (
                    os.path.join(path,Subject+ "_"+ date+ ".csv")
                )
                attendance = attendance.drop_duplicates(subset=["Roll_Number"], keep="last")
                l1 = os.listdir(path)
                availFileName = os.path.basename(fileName)
                # print(l1,availFileName,path,fileName)
                if availFileName in l1:
                    # print("YES")
                    file1 = pd.read_csv(fileName)
                    attendance = pd.concat([file1,attendance],axis=0)
                    attendance.drop_duplicates(subset=["Roll_Number"], keep="last",inplace=True)
                    attendance.to_csv(fileName,index=False)
                    print("successfully attendance file updated")

                else :
                    attendance.to_csv(fileName, index=False)
                    print("successfully attendance file created")
                
                m = "Attendance Filled Successfully of " + Subject
                text_to_speech(m)
                Notifica.configure(
                    text=m
                )
                Notifica.grid(row=13 , column=1,padx=20, pady=20, sticky="ew")

                cam.release()
                cv2.destroyAllWindows()

                import csv
                import tkinter
                print("Presenting Taken Attendance...")
                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background="black")
                cs = os.path.join(path, fileName)
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:

                            label = tkinter.Label(
                                root,
                                width=10,
                                height=1,
                                fg="white",
                                font=("times", 15, " bold "),
                                bg="black",
                                text=row,
                                relief=tkinter.RIDGE,
                            )
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                print("Presented :)")
                root.mainloop()
            except:
                f = "No Face found for attendance"
                text_to_speech(f)
                cv2.destroyAllWindows()

    
    subject = ctk.CTk()   
    subject.geometry("800x500")
    subject.title("Take Attendance")
    subject.resizable(0, 0)
    #subject.configure(background="black")

    def home():
        subject.destroy()
        os.system('main.py')
    frame_1 = ctk.CTkFrame(master=subject, width=250, height=240, corner_radius=15)
    frame_1.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")

    frame_1.rowconfigure((0, 1, 2, 3), weight=1)
    frame_1.rowconfigure(7, weight=10)
    frame_1.columnconfigure((0, 1), weight=1)
    frame_1.columnconfigure(2, weight=0)


    Button = ctk.CTkLabel(master=frame_1,  width=190, height=40,
                                   text="Enter Subject Name for the Attendance.",text_font=("Roboto Medium", -16))
    Button.grid(row=3, column=1,  padx=20, pady=20, sticky="ew")


    tx = ctk.CTkEntry(
        frame_1,width=100,
        text_font=("times", 20),
    )
    tx.grid(row=9, column=1,  padx=20, pady=20, sticky="ew")
    
    homeButton = ctk.CTkButton(master=frame_1, image=ImageTk.PhotoImage(image=home_image),
                                    text="",text_font=("times new roman", 15),
                                    height=4,
                                    width=16,compound="bottom", command=home)
    
    homeButton.grid(row=1, column=10,  padx=20, pady=20, sticky="ew")

    Notifica = ctk.CTkLabel(
        frame_1,
        text="Attendance filled Successfully",
        width=33,
        height=2,
        text_font=("times", 15, "bold"),
    )


    fill_a = ctk.CTkButton(
        frame_1,
        text="Submit Attendance",
        command=FillAttendance,
        text_font=("times new roman", 20),
    height=4,
    width=16,
    )

    fill_a.grid(row=11, column=1,  padx=20, pady=20, sticky="ew")

    subject.mainloop()
