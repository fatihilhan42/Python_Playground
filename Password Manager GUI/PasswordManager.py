import tkinter as tk
import json
from tkinter import messagebox
import random 
import string
import sqlite3
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
from tkinter import PhotoImage
import qrcode

def create_db():
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                        username text PRIMARY KEY,
                        password text NOT NULL
                    )""")
    conn.commit()
    conn.close()

# Check if the database exists, if not create a new one
try:
    conn = sqlite3.connect("user_data.db")
    conn.close()
except sqlite3.OperationalError:
    create_db() 

class PasswordManagerScreen(tk.Tk):
    def __init__(self, master):
        tk.Tk.__init__(self)
        self.title("Password Manager")
        self.geometry("1000x700")
        self.resizable(False, False)
        self.iconbitmap("icon/icon.ico")
        self.qr_label = None

        
        # Load the image into memory
        self.background_image = ImageTk.PhotoImage(file="background/Password Manager.png")
        # Adding a background image
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)


        self.length_label = tk.Label(self, text="Password Length:", font=('Arial',14))
        self.length_entry = tk.Entry(self, width=20, font=('Arial', 14),bg='#97aaff')
        self.length_entry.insert(0, "Enter password length")
        self.length_entry.bind("<FocusIn>", self.clear_placeholder_text)
        self.length_entry.bind("<FocusOut>", self.restore_placeholder_text)

        self.complexity_label = tk.Label(self, text="Password Complexity:", font=('Arial', 10))
        self.complexity_var = tk.IntVar()
        self.easy_radio = tk.Radiobutton(self, text="Easy", variable=self.complexity_var, value=1, font=('Arial', 12), bg='#191825', fg='#D875FF', indicatoron=0, width=10, height=2)
        self.medium_radio = tk.Radiobutton(self, text="Med", variable=self.complexity_var, value=2, font=('Arial', 12),bg='#191825', fg='#7AF8FF', indicatoron=0, command=self.change_button_color, width=10, height=2)
        self.hard_radio = tk.Radiobutton(self, text="Hard", variable=self.complexity_var, value=3, font=('Arial', 12),bg='#191825', fg='#8EA8FF', indicatoron=0, width=10, height=2)

        self.generate_button = tk.Button(self, text="Generate", command=self.generate_password)

        self.save_button_characters = tk.Button(self,text="Save Characters", command=self.save_password_characters)
        self.save_button_letters = tk.Button(self,text="Save Letters", command=self.save_password_letters)
        self.save_button_numbers = tk.Button(self,text="Save Numbers", command=self.save_password_numbers)
        self.logout_button = tk.Button(self, text="Log Out", command=self.logout)
        self.result_label = tk.Label(self)
        self.search_password_entry = tk.Entry(self)
        self.search_password_button = tk.Button(self, text="Search", command=self.search_password)
        self.search_keyword_label = tk.Label(self, text="Keyword:",font=('Arial', 10))
        self.search_keyword_entry = tk.Entry(self, font=('Arial', 14), bg='#97aaff')
        self.search_website_label = tk.Label(self, text="Website:",font=('Arial', 10))
        self.search_website_entry = tk.Entry(self, font=('Arial', 14), bg='#97aaff')
        self.clear_button = tk.Button(self, text="Clear Entries", command=self.clear_entries)
        self.generated_password_label = tk.Label(self, text="Generated Password", font=('Arial', 14))
        self.generated_password_label_number = tk.Label(self, text="Number")
        self.generated_password_label_characters = tk.Label(self, text="Char")
        self.generated_password_entry_letters = tk.Entry(self,width=20, font=('Arial', 16), bg='#e315ea', fg='#3000ff')
        self.generated_password_entry_numbers = tk.Entry(self,width=20, font=('Arial', 16), bg='#e315ea', fg='#3000ff')
        self.generated_password_entry_characters = tk.Entry(self,width=20, font=('Arial', 16), bg='#e315ea', fg='#3000ff')
        self.keyword_label = tk.Label(self, text="Keyword:")
        self.keyword_entry = tk.Entry(self,width=25, font=('Arial', 14), bg='#97aaff')
        self.keyword_entry.insert(0,"Enter keyword to save")
        self.keyword_entry.bind("<FocusIn>", self.clear_placeholder_text)
        self.keyword_entry.bind("<FocusOut>", self.clear_placeholder_text)
        self.website_label = tk.Label(self, text="Website:")
        self.website_entry = tk.Entry(self,width=25, font=('Arial', 14), bg='#97aaff')
        self.website_entry.insert(0, "Enter website to save")
        self.website_entry.bind("<FocusIn>", self.clear_placeholder_text)
        self.website_entry.bind("<FocusOut>", self.clear_placeholder_text)
        
        self.length_label.grid(row=2, column=0, padx=10,pady=10)
        self.length_entry.grid(row=2, column=1, padx=10,pady=10)

        self.complexity_label.grid(row=3, column=1, pady=5)
        self.easy_radio.grid(row=4, column=0, padx=5,pady=5)
        self.medium_radio.grid(row=4, column=1, padx=5,pady=5)
        self.hard_radio.grid(row=4, column=2, padx=5,pady=5)

        self.generate_button.grid(row=5, column=1, pady=10)
        self.generated_password_label.grid(row=6, column=0, pady=5)
        self.generated_password_label_number.grid(row=7, column=0, pady=5)
        self.generated_password_label_characters.grid(row=8, column=0, pady=5)
        self.generated_password_entry_letters.grid(row=6, column=1,pady=5)
        self.generated_password_entry_numbers.grid(row=7, column=1, pady=5)
        self.generated_password_entry_characters.grid(row=8, column=1, pady=5)

        self.save_button_letters.grid(row=6, column=2,padx=10,pady=5)
        self.save_button_numbers.grid(row=7, column=2,padx=10,pady=5)
        self.save_button_characters.grid(row=8, column=2,padx=10,pady=5)

        self.keyword_label.grid(row=9, column=0, pady=5)
        self.keyword_entry.grid(row=9, column=1, pady=5)
        self.website_label.grid(row=10, column=0, pady=5)
        self.website_entry.grid(row=10, column=1, pady=5)

        self.logout_button.grid(row=12, column=1, pady=5)

        self.search_keyword_label.grid(row=3, column=5, padx=5, pady=5)
        self.search_keyword_entry.grid(row=3, column=6,  padx=5,pady=5)
        self.search_website_label.grid(row=4, column=5,  padx=5,pady=5)
        self.search_website_entry.grid(row=4, column=6, padx=5,pady=5) 
        self.search_password_button.grid(row=5, column=6, pady=5)
        self.clear_button.grid(row=3, column=7, padx=8)


        def set_button_image(button, image_path):
            # Load the image
            img = Image.open(image_path)

            # Resize the image to fit inside the button
            img = ImageOps.fit(img, (90, 40), Image.Resampling.LANCZOS)

            # Create an image object from the resized image
            img = ImageTk.PhotoImage(img)

            # Set the image as the button's image
            button.config(image=img)
            button.image = img 

           # List of dictionaries containing the button and the path to the image file
        button_image_list = [
            {'button': self.generate_button, 'image_path': 'photo/Generate.png'},
            {'button': self.search_password_button, 'image_path': 'photo/search.png'},
            {'button': self.logout_button, 'image_path': 'photo/logout.png'},
            {'button': self.save_button_characters, 'image_path': 'photo/save.png'},
            {'button': self.save_button_letters, 'image_path': 'photo/save.png'},
            {'button': self.save_button_numbers, 'image_path': 'photo/save.png'},
            {'button': self.length_label, 'image_path': 'photo/length.png'},
            {'button': self.keyword_label, 'image_path': 'photo/keyword.png'},
            {'button': self.website_label, 'image_path': 'photo/website.png'},
            {'button': self.generated_password_label, 'image_path': 'photo/letter.png'},
            {'button': self.complexity_label, 'image_path': 'photo/complex.png'},
            {'button': self.generated_password_label_number, 'image_path': 'photo/number.png'},
            {'button': self.generated_password_label_characters, 'image_path': 'photo/char.png'},
            {'button': self.search_keyword_label, 'image_path': 'photo/keyword.png'},
            {'button': self.search_website_label, 'image_path': 'photo/website.png'},
            {'button': self.clear_button, 'image_path': 'photo/clear.png'}

        ]

        # Loop over the list and set the image for each button
        for button_image_dict in button_image_list:
            set_button_image(button_image_dict['button'], button_image_dict['image_path'])

    def change_button_color(self):
        # Toggle button color between yellow and a different color
        if self.medium_radio.config('bg')[-1] == 'yellow':
            self.medium_radio.config(bg='#333333', fg='white')
        else:
            self.medium_radio.config(bg='yellow', fg='black')

    def clear_entries(self):
        self.search_keyword_entry.delete(0, tk.END)
        self.search_website_entry.delete(0, tk.END)

    def clear_placeholder_text(self, event):
        entry = event.widget
        if entry == self.length_entry and entry.get() == "Enter password length":
            entry.delete(0, tk.END)
        elif entry == self.keyword_entry and entry.get() == "Enter keyword to save":
            entry.delete(0, tk.END)
        elif entry == self.website_entry and entry.get() == "Enter website to save":
            entry.delete(0, tk.END)


    def restore_placeholder_text(self, event):
            if not self.length_entry.get() and not self.keyword_entry.get() and not self.website_entry.get():
                self.length_entry.insert(0, "Enter password length")
                self.keyword_entry.insert(0, "Enter keyword to save")
                self.website_entry.insert(0, "Enter website to save")



    def generate_password(self):
        if not self.length_entry.get():
            messagebox.showwarning("Error", "Please enter a password length")
            return
        
        length = int(self.length_entry.get())
        complexity = self.complexity_var.get()
            
        num_special_chars = random.randint(1, 2)
        num_letters_and_numbers = length - num_special_chars

        special_chars = ''.join(random.choice(string.punctuation) for i in range(num_special_chars))
        letters_and_numbers = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(num_letters_and_numbers))
        password_characters = special_chars + letters_and_numbers
        
        password_numbers = ''.join(random.choice(string.digits) for i in range(length))
        password_letters = ''.join(random.choice(string.ascii_letters) for i in range(length))

        if complexity == 1:
            password = password_letters
        elif complexity == 2:
            password = password_numbers
        elif complexity == 3:
            password = password_characters

        self.generated_password_entry_characters.delete(0, "end")
        self.generated_password_entry_numbers.delete(0, "end")
        self.generated_password_entry_letters.delete(0, "end")

        self.generated_password_entry_characters.insert(0, password_characters)
        self.generated_password_entry_numbers.insert(0, password_numbers)
        self.generated_password_entry_letters.insert(0, password_letters)


    def save_password_characters(self):
        password = self.generated_password_entry_characters.get()
        keyword = self.keyword_entry.get()
        website = self.website_entry.get()

        if password and keyword.strip() != "Enter keyword to save":
            if website.strip() == "Enter website to save":
                website = "NONE"
            conn = sqlite3.connect('passwords.db')
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS passwords_characters (keyword text,website text,password text)""")
            c.execute("INSERT INTO passwords_characters (keyword, website, password) VALUES (?, ?, ?)", (keyword, website, password))
            conn.commit()
            conn.close()
            messagebox.showinfo('Info', 'Password saved successfully!')
    
        else:
            messagebox.showerror('Error', 'All fields are required to save the password!')

    def save_password_numbers(self):
        password = self.generated_password_entry_numbers.get()
        keyword = self.keyword_entry.get()
        website = self.website_entry.get()

        if password and keyword.strip() != "Enter keyword to save":
            if website.strip() == "Enter website to save":
                website = "NONE"
            conn = sqlite3.connect('passwords.db')
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS passwords_numbers (keyword text, website text, password text)")
            c.execute("INSERT INTO passwords_numbers (keyword, website, password) VALUES (?, ?, ?)", (keyword, website, password))
            conn.commit()
            conn.close()
            messagebox.showinfo('Info', 'Password saved successfully!')
        else:
            messagebox.showerror('Error', 'All fields are required to save the password!')

    def save_password_letters(self):
        password = self.generated_password_entry_letters.get()
        keyword = self.keyword_entry.get()
        website = self.website_entry.get()

        if password and keyword.strip() != "Enter keyword to save":
            if website.strip() == "Enter website to save":
                website = "NONE"
            conn = sqlite3.connect('passwords.db')
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS passwords_letters (keyword text, website text, password text)")
            c.execute("INSERT INTO passwords_letters (keyword, website, password) VALUES (?, ?, ?)", (keyword, website, password))
            conn.commit()
            conn.close()
            messagebox.showinfo('Info', 'Password saved successfully!')
        else:
            messagebox.showerror('Error', 'All fields are required to save the password!')


    def search_password(self):
        keyword = self.search_keyword_entry.get()
        website = self.search_website_entry.get()
        

        conn = sqlite3.connect('passwords.db')
        c = conn.cursor()

        tables = ['passwords_characters', 'passwords_numbers', 'passwords_letters']
        results = []

        for table in tables:
            # Check if the table exists
            c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            table_exists = c.fetchone()

            if table_exists:
                if keyword and website:
                    c.execute(f"SELECT website, password FROM {table} WHERE keyword=? and website=?", (keyword, website))
                    results.extend(c.fetchall())
                elif keyword:
                    c.execute(f"SELECT website, password FROM {table} WHERE keyword=?", (keyword,))
                    results.extend(c.fetchall())
                elif website:
                    c.execute(f"SELECT keyword, password FROM {table} WHERE website=?", (website,))
                    results.extend(c.fetchall())

        if results:

            if hasattr(self, 'tree'):
                self.tree.destroy()
            
            

            self.tree = ttk.Treeview(self, columns=("Website", "Password", "Action"), show="headings")
            self.tree.column("Website", width=100, anchor="center")
            self.tree.column("Password", width=100, anchor="center")
            self.tree.column("Action", width=200, anchor="center")

            self.tree.heading("Website", text="Website")
            self.tree.heading("Password", text="Password")
            self.tree.heading("Action", text="Action")

            # Set the background color of the Treeview widget
            self.tree["style"] = "mystyle.Treeview"
            self.style = ttk.Style()
            self.style.configure("mystyle.Treeview", background="#7AF8FF")

            # Set the background color of the rows
            self.style.map("mystyle.Treeview", background=[("selected", "#D875FF")])

            # Add the Treeview widget to the parent widget
            self.tree.grid(row=7, column=6, rowspan=5,sticky="w", columnspan=8)
            
            for row in results:
                website = row[0]
                password = row[1]
                self.tree.insert("", "end", values=(website, password, "Delete (Double Click)"))

                if self.qr_label:
                    self.qr_label.destroy()

                # Generate the QR code image using qrcode library       
                qr_str = f"Website: {website}\nPassword: {password}"
                qr = qrcode.QRCode(version=1, box_size=3, border=3)
                qr.add_data(qr_str)
                qr.make(fit=True)
                qr_image = qr.make_image(fill_color="black", back_color="purple")
                qr_photo = ImageTk.PhotoImage(qr_image)

                # Create a Label widget to display the QR code
                qr_label = tk.Label(self, image=qr_photo)
                qr_label.image = qr_photo
                # Remove the QR label from its current position
                qr_label.grid_forget()

                # Re-insert the QR label with the updated row and column indices
                qr_label.grid(row=9, column=6, pady=5)
                self.qr_label = qr_label

                self.tree.bind("<Double-Button-1>", self.on_tree_double_click)
               
            messagebox.showinfo('Info', 'Password(s) found and displayed!')
        else:
            messagebox.showerror('Error', 'Password not found for the given keyword or website!')

        conn.commit()
        conn.close()

    def on_tree_double_click(self, event):
        selection = self.tree.selection()
        for item in selection:
            item_text = self.tree.item(item,"values")
            website = item_text[0]
            password = item_text[1]
            
           

        result = messagebox.askyesno('Delete', f'Are you sure you want to delete the password for the website "{website}"? This cannot be undone.')
        if result:
            conn = sqlite3.connect('passwords.db')
            c = conn.cursor()

            table_names = []
            # Get the names of all tables in the database
            c.execute("SELECT name FROM sqlite_master WHERE type='table'")
            table_names = [row[0] for row in c.fetchall()]

            # Delete the password from each table that exists in the database
            for table in table_names:
                c.execute(f"DELETE FROM {table} WHERE website=? and password=?", (website, password))
                

            conn.commit()
            conn.close()

            if self.qr_label:
                self.qr_label.destroy()

            self.tree.delete(item)
            
            self.tree.destroy()
            

            messagebox.showinfo('Info', 'Password deleted successfully!')
            
    def logout(self):
        self.destroy()
        LoginScreen(self.master)

#LOGIN SCREEN

class LoginScreen(tk.Tk):
    def __init__(self, master):
        tk.Tk.__init__(self)
        self.master = master
        
        self.title("Login Screen")
        self.geometry("600x400")
        self.resizable(False, False)
        
        
        # Disable resizing of the window
        self.resizable(0, 0)
        
        # Load the background image
        self.background_image = ImageTk.PhotoImage(file="background/login.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.pack(fill="both", expand=True)
        self.background_label.image = self.background_image  # Keep a reference to prevent garbage collection
        
        # Create the widgets
        self.username_label = tk.Label(self.background_label, text="Username", font=('Arial', 12), background='black',fg='red')
        self.username_entry = tk.Entry(self.background_label, fg="Black", font=('Arial', 14),background='#8EA8FF')
        self.username_entry.insert(0, "Enter your username",)
        self.username_entry.bind("<FocusIn>", self.clear_username_entry)
        self.username_entry.bind("<FocusOut>", self.restore_username_entry)

        self.password_label = tk.Label(self.background_label, text="Password", background='black', fg='Red', font=('Arial', 12))
        self.password_entry = tk.Entry(self.background_label, fg="BLACK", font=('Arial', 14), background='#8EA8FF')
        self.password_entry.insert(0, "Enter your password")
        self.password_entry.bind("<FocusIn>", self.clear_password_entry)
        self.password_entry.bind("<FocusOut>", self.restore_password_entry)

        self.login_button = tk.Button(self.background_label, text="Login", command=self.login, font=('Arial', 14), background='Black', fg='#FF00FA')
        self.register_label = tk.Label(self.background_label, text="Don't have an account? Register here", fg="#03edf4", cursor="hand2",font=('Arial', 12), bg='black')
        self.register_label.bind("<Button-1>", self.show_register_screen)

        # Center the username label and entry
        self.username_label.place(relx=0.5, rely=0.3, anchor="center")
        self.username_entry.place(relx=0.5, rely=0.4, anchor="center")

        # Center the password label and entry
        self.password_label.place(relx=0.5, rely=0.5, anchor="center")
        self.password_entry.place(relx=0.5, rely=0.60, anchor="center")

        # Center the login button
        self.login_button.place(relx=0.5, rely=0.7, anchor="center")

        # Center the register label
        self.register_label.place(relx=0.5, rely=0.8, anchor="center")

        # Prevent the background label from resizing the window
        self.background_label.pack_propagate(0)

    def clear_username_entry(self, event):
        if self.username_entry.get() == "Enter your username":
            self.username_entry.delete(0, tk.END)
            self.username_entry.config(fg="black")

    def restore_username_entry(self, event):
        if not self.username_entry.get():
            self.username_entry.insert(0, "Enter your username")
            self.username_entry.config(fg="gray")

    def clear_password_entry(self, event):
        if self.password_entry.get() == "Enter your password":
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(fg="black", show="*")

    def restore_password_entry(self, event):
        if not self.password_entry.get():
            self.password_entry.insert(0, "Enter your password")
            self.password_entry.config(fg="gray", show="")

        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Connect to the database
        conn = sqlite3.connect("user_data.db")
        c = conn.cursor()

        # Check if the users table exists
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        table_exists = c.fetchone()

        if not table_exists:
            tk.messagebox.showerror("Error", "No users registered. Please create a new account.")
            return

        # Query the database for a matching username and password
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = c.fetchone()

        if result:
            # Login successful
            self.destroy()
            PasswordManagerScreen(self.master)
        else:
            tk.messagebox.showerror("Error", "Incorrect username or password")


    def show_register_screen(self, event):
        RegisterScreen(self)

class RegisterScreen(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)

        self.title("Register Screen")
        self.geometry("600x400")
        self.resizable(False, False)

        # Load the background image
        self.background_image = ImageTk.PhotoImage(file="background/register.png")
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.pack(fill="both", expand=True)
        self.background_label.image = self.background_image  # Keep a reference to prevent garbage collection

        self.username_label = tk.Label(self.background_label, text="Username", font=('Arial', 12), background='black',fg='red')
        self.username_entry = tk.Entry(self.background_label, fg="Black", font=('Arial', 14),background='#8EA8FF')
        self.password_label = tk.Label(self.background_label, text="Password", background='black', fg='Red', font=('Arial', 12))
        self.password_entry = tk.Entry(self.background_label, show="*", fg="BLACK", font=('Arial', 14), background='#8EA8FF')
        self.confirm_password_label = tk.Label(self, text="Confirm Password",font=('Arial', 12), background='black',fg='red')
        self.confirm_password_entry = tk.Entry(self, show="*",fg="gray", font=('Arial', 14), background='#8EA8FF')
        self.register_button = tk.Button(self, text="Register", command=self.register,font=('Arial', 14), background='Black', fg='#FF00FA')

        # Center the username label and entry
        self.username_label.place(relx=0.5, rely=0.2, anchor="center")
        self.username_entry.place(relx=0.5, rely=0.3, anchor="center")

        # Center the password label and entry
        self.password_label.place(relx=0.5, rely=0.4, anchor="center")
        self.password_entry.place(relx=0.5, rely=0.5, anchor="center")
        self.confirm_password_label.place(relx=0.5, rely=0.6, anchor="center")
        self.confirm_password_entry.place(relx=0.5, rely=0.7, anchor="center")
        self.register_button.place(relx=0.5, rely=0.8, anchor="center")

    def register(self):
        # Connect to the database
        conn = sqlite3.connect("user_data.db")
        c = conn.cursor()

        # Create the table if it doesn't exist
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT
            )
        """)

        # Get the entered username and password
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Check if the passwords match
        if password != confirm_password:
            tk.messagebox.showerror("Error", "Passwords do not match")
            return

        # Check if the username is already in use
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        result = c.fetchone()
        if result:
            tk.messagebox.showerror("Error", "Username is already in use")
            return

        # Insert the new user into the database
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

        # Show a success message
        tk.messagebox.showinfo("Success", "Successfully registered!")
        self.destroy()

     
if __name__ == "__main__":
    root = LoginScreen(None)
    root.resizable(False,False)
    root.mainloop()

    
