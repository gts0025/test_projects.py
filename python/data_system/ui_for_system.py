import customtkinter as ctk
root = ctk.CTk()
root.geometry("800x800")


#main panels placement
left = ctk.CTkFrame(master=root,fg_color="gray11")
left.place(
    relx = 0,rely = 0,
    relwidth = 0.5,relheight = 1.0,
    )
right = ctk.CTkFrame(master=root,fg_color="gray22")
right.place(
    relx = 0.5,rely = 0,
    relwidth = 0.5,relheight = 1.0,
    )

random_names = [
    "alçsdmasçld","asasddlk",
    "alçasdçld","aslmdasd"
    "aslmdlk","aslmdlk"
]

# data side:

column = ctk.CTkScrollableFrame(master = right )
column.place(relx = 0.01,
           rely = 0.1,
           relwidth =0.99,
           relheight =0.99
           )

for i,entry in enumerate(random_names):
    entr_frame = ctk.CTkFrame(master=column)
    entr_frame.pack(fill = "x", pady = 2, padx = 5)
    
    entr_label = ctk.CTkLabel(
    text=entry,master = entr_frame,
    )
    entr_label.pack(side = "left")

#general side:



#labels
gen_label = ctk.CTkLabel(
    text="general",master = left,
    font = ("arial",30)
    )
gen_label.place(relx = 0.5, rely = 0.01)


data_label = ctk.CTkLabel(
    text="data",master = right,
    font = ("arial",30)
    )
data_label.place(relx = 0.5, rely = 0.01)


root.mainloop()