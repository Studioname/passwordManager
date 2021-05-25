from tkinter import *
from random import choice, randint, shuffle
from tkinter import messagebox
import pyperclip
import json

LETTERS = "abcdefghijklmnopqrstuvwxyz"
NUMBERS = "0123456789"
SYMBOLS = "!£$%^&*()-=_+"
LETTERS_LIST = [letter for letter in LETTERS]
NUMBERS_LIST = [number for number in NUMBERS]
SYMBOLS_LIST = [symbol for symbol in SYMBOLS]
FONT=("default",12,"normal")
password = ""

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def create_password():
    global password
    delete_password()
    characters = []

    for i in range(0,randint(8,10)):
        if randint(0,1) == randint(0,1):
            characters.append(choice(LETTERS.upper()))
        else:
            characters.append(choice(LETTERS))

    for i in range(0,randint(2,4)):
        characters.append(choice(NUMBERS))

    for i in range(0,randint(2,4)):
        characters.append(choice(SYMBOLS))

    shuffle(characters)
    password = "".join(characters)
    password_entry.insert(0,password)
    pyperclip.copy(password)

def delete_password():
    global password
    global characters
    characters = []
    password_entry.delete(0, "end")
    password = ""

def search():
    try:
        with open("data.json") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showwarning(title="Error", message= "File not found. Please add entries before searching.")
    else:
        search_term = website_entry.get()
        search_term = search_term.title()
        try:
            messagebox.showinfo(title="User info", message=f'{search_term}\nUsername: {data[search_term]["username"]}\nPassword: {data[search_term]["final_password"]}\n')
        except KeyError:
            messagebox.showwarning(title="Error", message="Entry not found.")

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    website = website.title()
    username = username_entry.get()
    final_password = password_entry.get()
    new_data = {website : {"username" : username,
                           "final_password" : final_password}}

    if len(website) == 0 or len(final_password) == 0:
        messagebox.showwarning(title="Error",message="Please don't leave any of the fields empty.")

    else:
        try:
            with open("data.json", "r") as file:
                # reading old data
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file,indent=4)
        else:
            with open("data.json", "r") as file:
                #updating old data
                data.update(new_data)
            with open("data.json", "w") as file:
                #writing data
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0,"end")
            delete_password()

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
canvas = Canvas(width=200,height=200)
picture = PhotoImage(file="logo.png")
canvas.create_image(100,100,image=picture)
canvas.grid(column=1,row=0)
window.config(padx=50,pady=50)
window.title("Password Manager")

#0,1 label website

website_label = Label(text="Website:", font=FONT)
website_label.grid(column=0,row=1)

#0,2 label email/username

username_label = Label(text="Email/Username:", font=FONT)
username_label.grid(column=0,row=2)

#0,3 label password

password_label = Label(text="Password:", font=FONT)
password_label.grid(column=0,row=3)

#1,1 entry website columnspan=2, width 35

website_entry = Entry(width=33)
website_entry.grid(column=1,row=1, columnspan=1,sticky="W")

#1,2 entry email/username

username_entry = Entry(width=52)
username_entry.insert(0, "studionamestudioname@gmail.com")
username_entry.grid(column=1,row=2, columnspan=2,sticky="W")

#1,3 entry passwords columnspan=2, width 36

password_entry = Entry(width=33, text="", )
password_entry.grid(column=1,row=3,sticky="W")

#1,4 button 'add'

add_password_button = Button(text="Add", width=44,command=save)
add_password_button.grid(column=1, row=4,columnspan=2,)

#2,1 button Search

search_button = Button(text="Search", width = 15, command = search)
search_button.grid(column=2, row=1)

#2,3 button 'generate password'

generate_password_button = Button(text="Generate Password",width=15,command=create_password)
generate_password_button.grid(column=2,row=3,)

mainloop()