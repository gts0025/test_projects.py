import customtkinter as ctk
import tkinter as tk
root = ctk.CTk()
root.minsize(400,400)
root.maxsize(800,800)
ctk.set_appearance_mode("System")
root._fg_color = "black"
def dark_theme():
    ctk.set_appearance_mode("dark")
def light_theme():
    ctk.set_appearance_mode("light")

# maling a logging page:

m_frame = ctk.CTkFrame(master=root)
m_frame.place(
    anchor = "center",
    relwidth = 0.9, 
    relheight  = 0.7, 
    relx = 0.5,rely = 0.5
    )

email = ctk.CTkEntry(master=m_frame,placeholder_text="email",height=20)
email.place(
    anchor = "center", 
    relwidth = 0.5, 
    relx = 0.5,rely = 0.3
    )

password = ctk.CTkEntry(master=m_frame,placeholder_text="password",height=20,show="*")
password.place(
    anchor = "center", 
    relwidth = 0.5, 
    relx = 0.5,rely = 0.5
    )

next = ctk.CTkButton(master=m_frame, text="proceed",height=20)
next.place(
    anchor = "center", 
    relwidth = 0.3, 
    relx = 0.52,rely = 0.7
    )

main_label = ctk.CTkLabel(text = "logging",font=("arial",12),master=m_frame)


root.mainloop()