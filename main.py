# importing required modules
import os
import tkinter        
import customtkinter        # for better UI
from PIL import Image , ImageTk
import PIL

customtkinter.set_appearance_mode("System")  
customtkinter.set_default_color_theme("blue") 

PATH = os.path.dirname(os.path.realpath(__file__))

from utils import automaticAttendance , show_attendance

add_user_image = PIL.Image.open(PATH + "\\Icons\\add-user.png")
add_user_image = add_user_image.resize((50, 50), Image.ANTIALIAS)

take_att_image = PIL.Image.open(PATH + "\\Icons\\person-bounding-box.png")
take_att_image = take_att_image.resize((50, 50), Image.ANTIALIAS)


admin_login_image = PIL.Image.open(PATH + "\\Icons\\add-list.png")
admin_login_image = admin_login_image.resize((50, 50), Image.ANTIALIAS)


app = customtkinter.CTk()  # create customtkinter window 
app.geometry("800x500")
app.title("Smart Attendance System")

def register_function():
    app.destroy()
    os.system(PATH+"\\registeration\\register.py")

def take_attendance():
    app.destroy()
    automaticAttendance.subjectChoose()

def view_attendance():
    app.destroy()
    show_attendance.show_attendance()


def quit():
    app.destroy()

app.grid_rowconfigure(0, weight=1) 
app.grid_columnconfigure(0, weight=1, minsize=200)

frame_1 = customtkinter.CTkFrame(master=app, width=250, height=240, corner_radius=15)
frame_1.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")


Button = customtkinter.CTkLabel(master=frame_1,  width=190, height=40,
                                   text="Smart Attendance System",text_font=("Roboto Medium", -20))
Button.grid(row=1, column=5,  padx=5, pady=10, sticky="ew")


registerButton = customtkinter.CTkButton(master=frame_1, image=ImageTk.PhotoImage(image=add_user_image),
                                    text="Register", width=190, height=40,text_font=("Roboto Medium", -16),
                                   compound="right", command=register_function)
registerButton.grid(row=3, column=5,  padx=40, pady=20, sticky="ew")


alreadyRegisterButton = customtkinter.CTkButton(master=frame_1, image=ImageTk.PhotoImage(take_att_image), text="Take \nAttendance",
                                 width=190, height=40,text_font=("Roboto Medium", -16),
                                   compound="right", fg_color="#D35B58", hover_color="#C77C78",
                                   command=take_attendance)


alreadyRegisterButton.grid(row=5, column=5,  padx=40, pady=20, sticky="ew")



button_5 = customtkinter.CTkButton(master=frame_1, image=ImageTk.PhotoImage(admin_login_image) , text="View \nAttendance",
                                width=170, height=60, text_font=("Roboto Medium", -16),
                                compound="right", fg_color="green",hover="light green",
                                   command=view_attendance)
button_5.grid(row=7, column=5, padx=40, pady=20)


exit = customtkinter.CTkButton(master=app,text="EXIT", command=quit,
                height=2,width=14,text_font=("Roboto Medium", -16))
exit.grid(row=1, column=7, padx=40, pady=20)


app.mainloop()