import customtkinter as ctk
from random import choice
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
    "alçasdçld","aslmdasd",
    "aslmdlk","aslmdlk",
]



#function:
def show_side_panel(name):
    left_panel = ctk.CTkFrame(master=left, fg_color="gray20", corner_radius=10)
    left_panel.place(relx=0.15, rely=0.1, relwidth=0.7, relheight=0.2)

    name_label = ctk.CTkLabel(
        master=left_panel,
        text=f"name:{name}",
        font=("arial",15),
        anchor="w"  # aligns text to the left
    )
    name_label.pack(fill="x", padx=10, pady=5)

    price_label = ctk.CTkLabel(
        master=left_panel,
        font=("arial",15),
        text="price: 13,23",
        anchor="w"
    )
    price_label.pack(fill="x", padx=10, pady=5)

    amount_label = ctk.CTkLabel(
        master=left_panel,
        font=("arial",15),
        text="amount: 12",
        anchor="w"
    )
    amount_label.pack(fill="x", padx=10, pady=5)


def show_add_edit(edit = 0):
    left_panel = ctk.CTkFrame(master=left, corner_radius=10)
    left_panel.place(relx=0.15, rely=0.32, relwidth=0.7, relheight=0.2)

    name_entry = ctk.CTkEntry(
        master=left_panel,
        placeholder_text="name",
    )
    name_entry.pack(fill="x", padx=10, pady=5)

    amount = ctk.CTkEntry(
        master=left_panel,
        placeholder_text="amount",
    )
    amount.pack(fill="x", padx=10, pady=5)

    price = ctk.CTkEntry(
        master=left_panel,
        placeholder_text="price",
    )
    price.pack(fill="x", padx=10, pady=5)

    buttons = ctk.CTkFrame(master=left_panel,)

show_add_edit()
# data side:

column = ctk.CTkScrollableFrame(master = right, corner_radius=0 )
column.place(relx = 0.0,
           rely = 0.05,
           relwidth =1,
           relheight =0.99
           )
for i in range(500):
    entry = choice(random_names)
    entr_frame = ctk.CTkButton(
        master=column,
        text = entry,
        command=lambda e=entry: show_side_panel(e),
        fg_color="#383838",
        hover_color="#4e4e4e",

        text_color="white",
        corner_radius=0)
    
    entr_frame.pack(fill = "x", pady = 0, padx = 0)
    
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