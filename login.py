from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from db import get_db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")


class Login:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+110+80")
        self.root.resizable(False, False)
        self.root.config(bg="white")

        self.var_email = StringVar()
        self.var_pass = StringVar()

        # ------------- title --------------
        self.icon_title = PhotoImage(file=os.path.join(IMAGE_DIR, "logo1.png"))
        Label(
            self.root,
            text="Inventory Management System",
            image=self.icon_title,
            compound=LEFT,
            font=("times new roman", 40, "bold"),
            bg="#010c48", fg="white",
            anchor="w", padx=20
        ).place(x=0, y=0, relwidth=1, height=70)

        # ------------- login frame ---------------
        login_frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        login_frame.place(x=450, y=180, width=450, height=340)

        Label(
            login_frame, text="Login",
            font=("goudy old style", 30, "bold"),
            bg="white", fg="#010c48"
        ).pack(fill=X, pady=10)

        Label(
            login_frame, text="Email",
            font=("goudy old style", 15), bg="white"
        ).place(x=50, y=80)
        Entry(
            login_frame, textvariable=self.var_email,
            font=("goudy old style", 15), bg="lightyellow"
        ).place(x=50, y=115, width=350)

        Label(
            login_frame, text="Password",
            font=("goudy old style", 15), bg="white"
        ).place(x=50, y=160)
        Entry(
            login_frame, textvariable=self.var_pass,
            font=("goudy old style", 15), bg="lightyellow",
            show="*"
        ).place(x=50, y=195, width=350)

        Button(
            login_frame, text="Login", command=self.login,
            font=("goudy old style", 15, "bold"),
            bg="#010c48", fg="white", cursor="hand2"
        ).place(x=50, y=250, width=350, height=40)

    def login(self):
        if self.var_email.get() == "" or self.var_pass.get() == "":
            messagebox.showerror("Error", "Email and password are required", parent=self.root)
            return

        try:
            with get_db() as (con, cur):
                cur.execute(
                    "SELECT * FROM employee WHERE email=? AND pass=?",
                    (self.var_email.get(), self.var_pass.get())
                )
                user = cur.fetchone()

            if user is None:
                messagebox.showerror("Error", "Invalid email or password", parent=self.root)
            else:
                user_role = user[8]  # utype column
                user_name = user[1]  # name column
                self.open_dashboard(user_name, user_role)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def open_dashboard(self, user_name, user_role):
        self.root.destroy()
        from dashboard import IMS
        new_root = Tk()
        IMS(new_root, user_name=user_name, user_role=user_role)
        new_root.mainloop()


if __name__ == "__main__":
    root = Tk()
    obj = Login(root)
    root.mainloop()
