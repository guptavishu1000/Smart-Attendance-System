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
from customtkinter import CTkImage

PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
haarcasecade_path = os.path.join(PATH,"haarcascade_frontalface_default.xml")
trainimagelabel_path = os.path.join(PATH,"TrainingImageLabel","Trainner.yml")
trainimage_path = os.path.join(PATH,"TrainingImage")
studentdetail_path = os.path.join(PATH,"StudentDetails","studentdetails.csv")
attendance_path = os.path.join(PATH,"Attendance")

home_image = PIL.Image.open(os.path.join(PATH,"Icons","home.png"))
home_image = home_image.resize((50, 50), Image.Resampling.LANCZOS)

print("All Okay")

def text_to_speech(user_text):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)  # Try to use a female voice if available
        engine.say(user_text)
        engine.runAndWait()
    except Exception as e:
        error_msg = f"Unexpected error in text_to_speech: {str(e)}"
        print(error_msg)
        text_to_speech("An unexpected error occurred")
        show_error_dialog(None, "Error", error_msg)

# for choose subject and fill attendance
def show_error_dialog(parent, title, message):
    print(f"Showing error dialog: {title} - {message}")
    """Show error message in a dialog box"""
    try:
        error_window = ctk.CTkToplevel(parent)
        error_window.title(title)
        error_window.geometry("400x150")
        
        # Center the window
        screen_width = error_window.winfo_screenwidth()
        screen_height = error_window.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 150) // 2
        error_window.geometry(f"400x150+{x}+{y}")
        
        # Message label
        label = ctk.CTkLabel(
            master=error_window,
            text=message,
            wraplength=380,
            justify="left"
        )
        label.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Close button
        close_btn = ctk.CTkButton(
            master=error_window,
            text="OK",
            command=error_window.destroy
        )
        close_btn.pack(pady=10)
        
        error_window.grab_set()
        
    except Exception as e:
        print(f"Error showing error dialog: {str(e)}")

def subjectChoose():
    print("Subject Choose")
    def FillAttendance():
        try:
            sub = tx.get().strip()
            if not sub:
                error_msg = "Please enter the subject name!"
                text_to_speech(error_msg)
                show_error_dialog(subject, "Input Error", error_msg)
                return
                
            now = time.time()
            future = now + 10
        except Exception as e:
            error_msg = f"Unexpected error in FillAttendance: {str(e)}"
            print(error_msg)
            text_to_speech("An unexpected error occurred")
            show_error_dialog(subject, "Error", error_msg)
            return
            
        try:
            print("Filling Attendance...")
            recognizer = cv2.face.LBPHFaceRecognizer_create()

            if not os.path.exists(trainimagelabel_path):
                raise FileNotFoundError(f"Training data not found at {trainimagelabel_path}")
                
            recognizer.read(trainimagelabel_path)
        except Exception as e:
            error_msg = f"Error loading training model: {str(e)}"
            print(error_msg)
            text_to_speech("Error loading training model. Please check the training data.")
            show_error_dialog(subject, "Model Error", error_msg)
            return
            
        try:
            if not os.path.exists(haarcasecade_path):
                raise FileNotFoundError(f"Haar cascade file not found at {haarcasecade_path}")
                
            faceCascade = cv2.CascadeClassifier(haarcasecade_path)
            if faceCascade.empty():
                raise ValueError("Failed to load Haar cascade classifier")
        except Exception as e:
            error_msg = f"Error loading Haar cascade: {str(e)}"
            print(error_msg)
            text_to_speech("Error loading Haar cascade. Please check the file.")
            show_error_dialog(subject, "Haar Cascade Error", error_msg)
            return
            
        try:
            if not os.path.exists(studentdetail_path):
                raise FileNotFoundError(f"Student details not found at {studentdetail_path}")
                
            df = pd.read_csv(studentdetail_path)
            if df.empty:
                raise ValueError("Student details file is empty")
        except Exception as e:
            error_msg = f"Error loading student details: {str(e)}"
            print(error_msg)
            text_to_speech("Error loading student details. Please check the file.")
            show_error_dialog(subject, "Student Details Error", error_msg)
            return
            
        try:
            cam = cv2.VideoCapture(0)
            font = cv2.FONT_HERSHEY_PLAIN
            col_names = ["Roll_Number", "Name"]
            attendance = pd.DataFrame(columns=col_names)
        except Exception as e:
            error_msg = f"Error initializing camera: {str(e)}"
            print(error_msg)
            text_to_speech("Error initializing camera. Please check the camera.")
            show_error_dialog(subject, "Camera Error", error_msg)
            return
            
        try:
            while True:
                ret, im = cam.read()
                if not ret:
                    raise RuntimeError("Failed to capture image from camera")
                    
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray, 1.2, 5)
                
                for (x, y, w, h) in faces:
                    try:
                        cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
                        serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
                        
                        if conf < 50:
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            
                            try:
                                aa = df.loc[df['Id'] == serial]['Name'].values
                                if len(aa) > 0:
                                    aa = aa[0]
                                    tt = f"{serial}-{aa}"
                                    attendance.loc[len(attendance)] = [serial, aa]
                                else:
                                    tt = f"Unknown-{serial}"
                            except Exception as e:
                                print(f"Error processing recognized face: {str(e)}")
                                tt = f"Error-{serial}"
                                
                        else:
                            tt = "Unknown"
                            
                        if conf > 75:
                            unknown_dir = os.path.join(attendance_path, "Unknown")
                            os.makedirs(unknown_dir, exist_ok=True)
                            noOfFile = len(os.listdir(unknown_dir)) + 1
                            cv2.imwrite(os.path.join(unknown_dir, f"Unknown{noOfFile}.jpg"), im[y:y + h, x:x + w])
                            
                        cv2.putText(im, str(tt), (x, y + h), font, 1, (255, 255, 255), 2)
                        
                    except Exception as e:
                        print(f"Error processing face: {str(e)}")
                
                # Remove duplicate entries
                attendance = attendance.drop_duplicates(subset=['Roll_Number'], keep='first')
                
                # Show the frame
                cv2.imshow('Taking Attendance', im)
                
                # Break the loop on 'q' key or timeout
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
                ts = time.time()
                if ts > future:
                    break
                    
        except Exception as e:
            error_msg = f"Error during face detection: {str(e)}"
            print(error_msg)
            text_to_speech("An error occurred during face detection")
            show_error_dialog(subject, "Face Detection Error", error_msg)
            
        finally:
            # Release resources
            if 'cam' in locals() and cam.isOpened():
                cam.release()
                cv2.destroyAllWindows()
            else:
                pass

            try:
                subject.destroy()   # destroy only after cv2 windows are closed
            except:
                pass
            
        try:
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            
            # Create subject directory if it doesn't exist
            subject_dir = os.path.join(attendance_path, sub)
            os.makedirs(subject_dir, exist_ok=True)
            
            fileName = os.path.join(subject_dir, f"{sub}_{date}.csv")
            
            # Check if file exists to append or create new
            if os.path.exists(fileName):
                existing_df = pd.read_csv(fileName)
                updated_df = pd.concat([existing_df, attendance]).drop_duplicates(subset=['Roll_Number'], keep='first')
                updated_df.to_csv(fileName, index=False)
            else:
                attendance.to_csv(fileName, index=False)
                
            success_msg = f"Attendance for {sub} taken successfully. {len(attendance)} students marked present."
            print(success_msg)
            text_to_speech("Attendance Taken Successfully")
            
        except Exception as e:
            error_msg = f"Error saving attendance: {str(e)}"
            print(error_msg)
            text_to_speech("Error saving attendance")
            show_error_dialog(subject, "Save Error", error_msg)
            return
            
        try:
            subject.destroy()
        except Exception as e:
            print(f"Error closing window: {str(e)}")
            
        # Show completion message
        try:
            completion_msg = f"Attendance for {sub} has been recorded.\nTotal present: {len(attendance)}"
            show_error_dialog(None, "Attendance Complete", completion_msg)
        except Exception as e:
            print(f"Error showing completion message: {str(e)}")
            
            try:
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
        os.system(f'python {PATH}\main.py')
    frame_1 = ctk.CTkFrame(master=subject, width=250, height=240, corner_radius=15)
    frame_1.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")

    frame_1.rowconfigure((0, 1, 2, 3), weight=1)
    frame_1.rowconfigure(7, weight=10)
    frame_1.columnconfigure((0, 1), weight=1)
    frame_1.columnconfigure(2, weight=0)


    Button = ctk.CTkLabel(master=frame_1,  width=190, height=40,
                                   text="Enter Subject Name for the Attendance.",font=("Roboto Medium", -16))
    Button.grid(row=3, column=1,  padx=20, pady=20, sticky="ew")


    tx = ctk.CTkEntry(
        frame_1,width=100,
        font=("times", 20),
    )
    tx.grid(row=9, column=1,  padx=20, pady=20, sticky="ew")
    
    homeButton = ctk.CTkButton(master=frame_1, image=CTkImage(light_image=home_image),
                                    text="",font=("times new roman", 15),
                                    height=4,
                                    width=16,compound="bottom", command=home)
    homeButton.image = CTkImage(light_image=home_image)
    homeButton.grid(row=1, column=10,  padx=20, pady=20, sticky="ew")

    Notifica = ctk.CTkLabel(
        frame_1,
        text="Attendance filled Successfully",
        width=33,
        height=2,
        font=("times", 15, "bold"),
    )


    fill_a = ctk.CTkButton(
        frame_1,
        text="Submit Attendance",
        command=FillAttendance,
        font=("times new roman", 20),
    height=4,
    width=16,
    )

    fill_a.grid(row=11, column=1,  padx=20, pady=20, sticky="ew")

    subject.mainloop()
