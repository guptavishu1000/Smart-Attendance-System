# importing required modules
import os
import sys
import traceback
import customtkinter        # for better UI
from PIL import Image , ImageTk
import PIL
from utils import automaticAttendance , show_attendance
from customtkinter import CTkImage, CTkToplevel, CTkLabel, CTkButton
from utils.automaticAttendance import subjectChoose
from utils.show_attendance import show_attendance

customtkinter.set_appearance_mode("System")  
customtkinter.set_default_color_theme("blue") 

PATH = os.path.dirname(os.path.realpath(__file__))


add_user_image = PIL.Image.open(os.path.join(PATH , "Icons","add-user.png"))
add_user_image = add_user_image.resize((50, 50), Image.Resampling.LANCZOS)

take_att_image = PIL.Image.open(os.path.join(PATH , "Icons","person-bounding-box.png"))
take_att_image = take_att_image.resize((50, 50), Image.Resampling.LANCZOS)


admin_login_image = PIL.Image.open(os.path.join(PATH , "Icons","add-list.png"))
admin_login_image = admin_login_image.resize((50, 50), Image.Resampling.LANCZOS)

add_user_image = CTkImage(light_image=add_user_image)
take_att_image = CTkImage(light_image=take_att_image)
admin_login_image = CTkImage(light_image=admin_login_image)

app = customtkinter.CTk()  # create customtkinter window 
app.geometry("800x500")
app.title("Smart Attendance System")

def register_function():
    try:
        app.destroy()
        # opening register.py inside registeration
        # registeration, taking images of user and training images 
        os.system(f'python "{os.path.join(PATH,"registeration","register.py")}"')
    except Exception as e:
        error_message = f"Error in register_function: {str(e)}"
        print(error_message)
        show_error_message("Registration Error", error_message)

def take_attendance():
    try:
        app.destroy()
        # choosing subject followed by taking attendance
        # print(f'python "{os.path.join(PATH,"utils","automaticAttendance.py")}"')
        # os.system(f'python "{os.path.join(PATH,"utils","automaticAttendance.py")}"')
        subjectChoose()
    except Exception as e:
        error_message = f"Error in take_attendance: {str(e)}"
        print(error_message)
        show_error_message("Attendance Error", error_message)

def view_attendance():
    try:
        app.destroy()
        # showing attendance
        # os.system(f'python "{os.path.join(PATH,"utils","show_attendance.py")}"')
        show_attendance()
    except Exception as e:
        error_message = f"Error in view_attendance: {str(e)}"
        print(error_message)
        show_error_message("View Attendance Error", error_message)


def show_error_message(title, message):
    """Display error message in a dialog box"""
    try:
        error_window = CTkToplevel()
        error_window.title(title)
        error_window.geometry("400x200")
        error_window.resizable(False, False)
        
        # Center the error window
        screen_width = error_window.winfo_screenwidth()
        screen_height = error_window.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 200) // 2
        error_window.geometry(f"400x200+{x}+{y}")
        
        # Error message label
        error_label = CTkLabel(
            master=error_window,
            text=message,
            wraplength=380,
            justify="left"
        )
        error_label.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Close button
        close_btn = CTkButton(
            master=error_window,
            text="Close",
            command=error_window.destroy
        )
        close_btn.pack(pady=10)
        
        # Make the error window modal
        error_window.grab_set()
        
    except Exception as e:
        print(f"Error showing error message: {str(e)}")

def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    """Handle uncaught exceptions"""
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f"Unhandled exception: {error_msg}")
    show_error_message("Unexpected Error", f"An unexpected error occurred:\n{str(exc_value)}")

# Set exception hook
sys.excepthook = handle_uncaught_exception

def quit():
    try:
        app.destroy()
    except Exception as e:
        print(f"Error during application exit: {str(e)}")
        sys.exit(1)

app.grid_rowconfigure(0, weight=1) 
app.grid_columnconfigure(0, weight=1, minsize=200)

frame_1 = customtkinter.CTkFrame(master=app, width=250, height=240, corner_radius=15)
frame_1.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")


Button = customtkinter.CTkLabel(master=frame_1,  width=190, height=40,
                                   text="Smart Attendance System",font=("Roboto Medium", -20))
Button.grid(row=1, column=5,  padx=5, pady=10, sticky="ew")


registerButton = customtkinter.CTkButton(
    master=frame_1,
    image=add_user_image,  # Pass CTkImage directly
    text="Register",
    width=190,
    height=40,
    font=("Roboto Medium", -16),
    compound="right",
    command=register_function
)
registerButton.grid(row=3, column=5,  padx=40, pady=20, sticky="ew")


TakeAttendanceButton = customtkinter.CTkButton(
    master=frame_1,
    image=take_att_image,  # Pass CTkImage directly
    text="Take \nAttendance",
    width=190,
    height=40,
    font=("Roboto Medium", -16),
    compound="right",
    fg_color="#D35B58",
    hover_color="#C77C78",
    command=take_attendance
)
TakeAttendanceButton.grid(row=5, column=5,  padx=40, pady=20, sticky="ew")



button_5 = customtkinter.CTkButton(
    master=frame_1,
    image=admin_login_image,  # Pass CTkImage directly
    text="View \nAttendance",
    width=170,
    height=60,
    font=("Roboto Medium", -16),
    compound="right",
    fg_color="green",
    hover_color="light green",
    command=view_attendance
)
button_5.grid(row=7, column=5, padx=40, pady=20)


exit = customtkinter.CTkButton(master=app,text="EXIT", command=quit,
                height=2,width=14,font=("Roboto Medium", -16))
exit.grid(row=1, column=7, padx=40, pady=20)


app.mainloop()
