from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
import string

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    if len(password_entry.get()) == 0:
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        nr_letters = random.randint(8, 10)
        nr_symbols = random.randint(2, 4)
        nr_numbers = random.randint(2, 4)

        password_letters = [random.choice(string.ascii_letters) for _ in range(nr_letters)]
        password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
        password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

        password_list = password_letters + password_symbols + password_numbers
        random.shuffle(password_list)

        password = "".join(password_list)
        password_entry.insert(0, password)
        pyperclip.copy(password)
    else:
        password_entry.delete(0, END)
        generate_password()


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = web_entry.get()
    email = email_user_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email}"
                                                              f"\npassword: {password}\nIs it okay to save?")

        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # Updating old data with new data
                data.update(new_data)
                with open("data.json", "w") as data_file:

                    # saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                web_entry.delete(0, END)
                password_entry.delete(0, END)


def search():
    website = web_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file Found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\npassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exist")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()

window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
password_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=password_image)
canvas.grid(row=0, column=1)

web_label = Label(text="Website:")
web_label.grid(row=1, column=0)

web_entry = Entry(width=35)
web_entry.grid(row=1, column=1)
web_entry.focus()

email_user_label = Label(text="Email/Username:")
email_user_label.grid(row=2, column=0)

email_user_entry = Entry(width=56)
email_user_entry.grid(row=2, column=1, columnspan=2)
email_user_entry.insert(0, "@gmail.com")

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

password_entry = Entry(width=35)
password_entry.grid(row=3, column=1)

gen_button = Button(text="Generate Password", command=generate_password, width=16)
gen_button.grid(row=3, column=2)

add_button = Button(text="Add", width=47, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=16, command=search)
search_button.grid(row=1, column=2)
window.mainloop()
