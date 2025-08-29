import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import messagebox
import traceback
import sys
from tkinter import *
import customtkinter as ctk     # for better UI
from PIL import Image, ImageTk
import PIL
import pyttsx3
from customtkinter import CTkImage, CTkToplevel, CTkLabel, CTkButton

# Set global exception handler
def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    """Handle uncaught exceptions"""
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f"Unhandled exception: {error_msg}")
    show_error_message(None, "Unexpected Error", f"An unexpected error occurred:\n{str(exc_value)}")

# Set exception hook
sys.excepthook = handle_uncaught_exception

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue") 

PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
home_image = PIL.Image.open(os.path.join(PATH , "Icons","home.png"))
home_image = home_image.resize((50, 50), Image.Resampling.LANCZOS)

def show_error_message(parent, title, message):
    """Display error message in a dialog box"""
    try:
        error_window = CTkToplevel(parent)
        error_window.title(title)
        error_window.geometry("400x150")
        error_window.resizable(False, False)
        
        # Center the window
        screen_width = error_window.winfo_screenwidth()
        screen_height = error_window.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 150) // 2
        error_window.geometry(f"400x150+{x}+{y}")
        
        # Message label
        label = CTkLabel(
            master=error_window,
            text=message,
            wraplength=380,
            justify="left"
        )
        label.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Close button
        close_btn = CTkButton(
            master=error_window,
            text="OK",
            command=error_window.destroy
        )
        close_btn.pack(pady=10)
        
        error_window.grab_set()
        
    except Exception as e:
        print(f"Error showing error message: {str(e)}")

def text_to_speech(user_text):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)  # Try to use a female voice if available
        engine.say(user_text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in text_to_speech: {str(e)}")
        # Fallback to showing a message box if speech fails
        show_error_message(None, "Message", user_text)

def show_attendance():
    def calculate_attendance():
        try:
            Subject = tx.get().strip()
            if not Subject:
                error_msg = 'Please enter the subject name.'
                text_to_speech(error_msg)
                show_error_message(subject, "Input Error", error_msg)
                return
                
            attendance_dir = os.path.join(PATH, "Attendance", Subject)
            if not os.path.exists(attendance_dir):
                error_msg = f'No attendance records found for subject: {Subject}'
                text_to_speech(error_msg)
                show_error_message(subject, "Not Found", error_msg)
                return
                
            # Find all CSV files for the subject
            try:
                filenames = glob(os.path.join(attendance_dir, f"{Subject}_*.csv"))
                if not filenames:
                    error_msg = f'No attendance files found for subject: {Subject}'
                    text_to_speech(error_msg)
                    show_error_message(subject, "No Data", error_msg)
                    return
                    
                # Read and process all attendance files
                df_list = []
                for f in filenames:
                    try:
                        df_list.append(pd.read_csv(f))
                    except Exception as e:
                        print(f"Error reading file {f}: {str(e)}")
                        continue
                        
                if not df_list:
                    error_msg = 'Could not read any attendance files.'
                    text_to_speech(error_msg)
                    show_error_message(subject, "Read Error", error_msg)
                    return
                    
                # Merge all dataframes
                newdf = df_list[0]
                for i in range(1, len(df_list)):
                    newdf = newdf.merge(df_list[i], how="outer")
                    
                # Calculate attendance percentage
                newdf.fillna(0, inplace=True)
                newdf["Attendance"] = 0
                for i in range(len(newdf)):
                    try:
                        if len(newdf.columns) > 2:  # Ensure there are attendance columns
                            present_days = sum(newdf.iloc[i, 2:-1] > 0)
                            total_days = len(newdf.columns) - 3  # Exclude ID, Name, and Attendance columns
                            if total_days > 0:
                                attendance_percent = int(round((present_days / total_days) * 100))
                                newdf["Attendance"].iloc[i] = f"{attendance_percent}%"
                    except Exception as e:
                        print(f"Error calculating attendance for row {i}: {str(e)}")
                        newdf["Attendance"].iloc[i] = "Error"
                
                # Save the results
                output_file = os.path.join(attendance_dir, "attendance.csv")
                newdf.to_csv(output_file, index=False)
                
                # Display the results in a new window
                display_attendance(Subject, output_file)
                
            except Exception as e:
                error_msg = f'Error processing attendance data: {str(e)}'
                print(error_msg)
                text_to_speech("An error occurred while processing attendance data.")
                show_error_message(subject, "Processing Error", error_msg)
                
        except Exception as e:
            error_msg = f'Unexpected error: {str(e)}'
            print(error_msg)
            text_to_speech("An unexpected error occurred.")
            show_error_message(subject, "Error", error_msg)

def display_attendance(subject, csv_file):
    """Display attendance data in a new window"""
    try:
        root = tk.Tk()
        root.title(f"Attendance of {subject}")
        
        # Make window resizable
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        
        # Create a canvas with scrollbars
        canvas = tk.Canvas(root, borderwidth=0)
        frame = tk.Frame(canvas)
        vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        hsb = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
        canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=frame, anchor="nw")
        
        # Configure the frame to update scrollregion when size changes
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            
        frame.bind("<Configure>", on_frame_configure)
        
        # Read and display the CSV data
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)
            
            # Create header row
            for col, header in enumerate(headers):
                label = tk.Label(
                    frame,
                    width=15,
                    height=2,
                    fg="white",
                    font=("Arial", 10, "bold"),
                    bg="#1a1a1a",
                    text=header,
                    relief=tk.RAISED,
                    padx=5,
                    pady=5
                )
                label.grid(row=0, column=col, sticky="nsew")
                frame.grid_columnconfigure(col, weight=1)
            
            # Create data rows
            for row_idx, row in enumerate(reader, 1):
                for col, cell in enumerate(row):
                    bg_color = "#f0f0f0" if row_idx % 2 == 0 else "#ffffff"
                    label = tk.Label(
                        frame,
                        width=15,
                        height=2,
                        fg="black",
                        font=("Arial", 10),
                        bg=bg_color,
                        text=cell,
                        relief=tk.SUNKEN,
                        padx=5,
                        pady=5
                    )
                    label.grid(row=row_idx, column=col, sticky="nsew")
        
        # Add a close button
        close_btn = tk.Button(
            root,
            text="Close",
            command=root.destroy,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            relief=tk.RAISED,
            padx=20,
            pady=5
        )
        close_btn.pack(pady=10)
        
        # Make window resizable
        root.minsize(800, 400)
        root.state('zoomed')  # Maximize the window
        
        root.mainloop()
        
    except Exception as e:
        error_msg = f'Error displaying attendance: {str(e)}'
        print(error_msg)
        text_to_speech("An error occurred while displaying attendance data.")
        show_error_message(None, "Display Error", error_msg)

    subject = ctk.CTk()
    subject.title("Subject...")
    subject.geometry("800x500")
   
    def home():
        subject.destroy()  # Ensure the window closes even if there's an error
        os.system(f'python {PATH}\main.py')
            
    def Check_sheets():
        try:
            sub = tx.get().strip()
            if not sub:
                error_msg = "Please enter the subject name."
                text_to_speech(error_msg)
                show_error_message(subject, "Input Error", error_msg)
                return
                
            folder_path = os.path.join(PATH, "Attendance", sub)
            if not os.path.exists(folder_path):
                error_msg = f"No attendance folder found for subject: {sub}"
                text_to_speech(error_msg)
                show_error_message(subject, "Not Found", error_msg)
                return
                
            try:
                if sys.platform == 'win32':
                    os.startfile(folder_path)
                else:
                    import subprocess
                    if sys.platform == 'darwin':  # macOS
                        subprocess.Popen(['open', folder_path])
                    else:  # Linux variants
                        subprocess.Popen(['xdg-open', folder_path])
                        
            except Exception as e:
                error_msg = f"Could not open folder: {str(e)}"
                print(error_msg)
                text_to_speech("Could not open the attendance folder.")
                show_error_message(subject, "Error", error_msg)
                
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(error_msg)
            text_to_speech("An unexpected error occurred.")
            show_error_message(subject, "Error", error_msg)

    frame_right = ctk.CTkFrame(subject,height=500,width=800)
    frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

    frame_right.rowconfigure((0, 1, 2, 3), weight=1)
    frame_right.rowconfigure(7, weight=10)
    frame_right.columnconfigure((0, 1), weight=1)
    frame_right.columnconfigure(2, weight=0)

    titl = ctk.CTkLabel(frame_right,
        text="Which Subject of Attendance?",
        font=("arial", 15)
    )
    titl.grid(row=1, column=0, pady=10, padx=20)

    homeButton = ctk.CTkButton(master=frame_right, image=CTkImage(light_image=home_image),
                                    text="",  height=40,
                                   compound="right", command=home)
    homeButton.grid(row=1, column=3, pady=10, padx=20)


    sub = ctk.CTkLabel(frame_right,text="Enter Subject",
        font=("Roboto Medium", -22),height=4,width=25,
    )
    sub.grid(row=11, column=0, pady=20, padx=20)

    tx = ctk.CTkEntry(frame_right,width=180,
        font=("Roboto Medium", -20),height=3,
    )
    tx.grid(row=11, column=1, pady=20, padx=20,sticky="we")

    view_attendance = ctk.CTkButton(
        frame_right,text="View Attendance",command=calculate_attendance,
        font=("Roboto Medium", -22),height=4,width=25,
        fg_color="#FF7D33", hover_color="#FFC733"
    )
    view_attendance.grid(row=15,column=0, pady=20, padx=20)
    check_sheets = ctk.CTkButton(frame_right,
        text="Check Sheets",command=Check_sheets,font=("Roboto Medium", -22),
        fg_color="#FF7D33", hover_color="#FFC733", 
        
        height=4,width=25,
    )
    check_sheets.grid(row=15,column=1, pady=20, padx=20)
    
    subject.mainloop()

