import tkinter as tk
from tkinter import messagebox
import pymysql as pm
import hashlib
import random
import smtplib
from email.mime.text import MIMEText

conn = pm.connect(host='localhost', user='root', database='pass_verify', password='root')
cur = conn.cursor()

def create_hash(input):
    hash33 = hashlib.new("SHA256")
    hash33.update(input.encode())
    hashed_input = hash33.hexdigest()
    return hashed_input

def create_otp():
    g_otp = random.randint(1000, 9999)
    return str(g_otp)

def countdown(remaining_time, timer_label):
    if remaining_time <= 0:
        messagebox.showinfo("Time's up", "You have exceeded the time limit.")
        return
    mins, secs = divmod(remaining_time, 60)
    timer_label.config(text="Time remaining: {:02d}:{:02d}".format(mins, secs))
    root.after(1000, countdown, remaining_time - 1, timer_label)

def forgot_pass_window():
    forgot_pass_win = tk.Toplevel(root)
    forgot_pass_win.title("Forgot Password")
    
    timer_label = tk.Label(forgot_pass_win, text="Time remaining: 10:00")
    timer_label.pack()

    def send_otp():
        user_mail = email_entry.get()


        # sendermail = "YOUR EMAIL"
        # mailpassword = "YOUR PASSWORD"    



        msg = MIMEText("Forgot the password? No problem. Your OTP is " + otp + ", enter this and reset your password.")
        msg['Subject'] = "You have received an OTP"
        msg['From'] = sendermail
        msg['To'] = user_mail
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sendermail, mailpassword)
            smtp_server.sendmail(sendermail, user_mail, msg.as_string())
            
        messagebox.showinfo("OTP Sent", "An OTP has been sent to your email address.")
        otp_label.config(state=tk.NORMAL)
        otp_entry.config(state=tk.NORMAL)
        otp_send_btn.config(state=tk.DISABLED)
        countdown(600, timer_label)
    
    def verify_otp():
        entered_otp = int(otp_entry.get()) 
        if entered_otp == int(otp):
            messagebox.showinfo("OTP Verified", "OTP verified. You can now reset your password.")
            reset_pass_frame.pack()
        else:
            messagebox.showerror("Invalid OTP", "The OTP entered is invalid. Please try again.")
    
    otp = create_otp()
    
    email_label = tk.Label(forgot_pass_win, text="Enter your email address:")
    email_label.pack()
    email_entry = tk.Entry(forgot_pass_win)
    email_entry.pack()
    
    otp_label = tk.Label(forgot_pass_win, text="Enter OTP:")
    otp_label.pack()
    otp_entry = tk.Entry(forgot_pass_win, state=tk.DISABLED)
    otp_entry.pack()
    
    otp_send_btn = tk.Button(forgot_pass_win, text="Send OTP", command=send_otp)
    otp_send_btn.pack()
    
    verify_otp_btn = tk.Button(forgot_pass_win, text="Verify OTP", command=verify_otp)
    verify_otp_btn.pack()
    
    reset_pass_frame = tk.Frame(forgot_pass_win)
    new_pass_label = tk.Label(reset_pass_frame, text="Enter your new password:")
    new_pass_label.pack()
    new_pass_entry = tk.Entry(reset_pass_frame, show="*")
    new_pass_entry.pack()
    
    new_pass_confirm_label = tk.Label(reset_pass_frame, text="Confirm new password:")
    new_pass_confirm_label.pack()
    new_pass_confirm_entry = tk.Entry(reset_pass_frame, show="*")
    new_pass_confirm_entry.pack()
    
    def reset_password():
        new_pass = new_pass_entry.get()
        new_pass_confirm = new_pass_confirm_entry.get()
        if new_pass != new_pass_confirm:
            messagebox.showerror("Password Mismatch", "Passwords do not match. Please try again.")
        else:
            hashed_pass = create_hash(new_pass)
            query = "UPDATE users SET password = %s WHERE email = %s"
            cur.execute(query, (hashed_pass, email_entry.get()))
            conn.commit()
            messagebox.showinfo("Password Reset", "Your password has been reset successfully.")
            forgot_pass_win.destroy()
    
    reset_pass_btn = tk.Button(reset_pass_frame, text="Reset Password", command=reset_password)
    reset_pass_btn.pack()

def register_window():
    register_win = tk.Toplevel(root)
    register_win.title("Register")

    def register():
        f_name = first_name_entry.get()
        l_name = last_name_entry.get()
        age = age_entry.get()
        email = email_entry.get()
        username = username_entry.get()
        temp_password = temp_password_entry.get()
        password = password_entry.get()

        if password != temp_password:
            messagebox.showerror("Password Mismatch", "Passwords do not match. Please try again.")
            return

        if int(age) <= 16:
            messagebox.showerror("Age Restriction", "User must be 16 or older.")
            return

        hashed_pass = create_hash(password)

        query = "INSERT INTO users (First_Name, Last_Name, Age, user_name, password, email) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(query, (f_name, l_name, age, username, hashed_pass, email))
        conn.commit()
        messagebox.showinfo("Registration Successful", "Registration completed. You can now login.")
        register_win.destroy()

    first_name_label = tk.Label(register_win, text="First Name:")
    first_name_label.pack()
    first_name_entry = tk.Entry(register_win)
    first_name_entry.pack()

    last_name_label = tk.Label(register_win, text="Last Name:")
    last_name_label.pack()
    last_name_entry = tk.Entry(register_win)
    last_name_entry.pack()

    age_label = tk.Label(register_win, text="Age:")
    age_label.pack()
    age_entry = tk.Entry(register_win)
    age_entry.pack()

    email_label = tk.Label(register_win, text="Email:")
    email_label.pack()
    email_entry = tk.Entry(register_win)
    email_entry.pack()

    username_label = tk.Label(register_win, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(register_win)
    username_entry.pack()

    temp_password_label = tk.Label(register_win, text="Password:")
    temp_password_label.pack()
    temp_password_entry = tk.Entry(register_win, show="*")
    temp_password_entry.pack()

    password_label = tk.Label(register_win, text="ReEnter Password:")
    password_label.pack()
    password_entry = tk.Entry(register_win, show="*")
    password_entry.pack()

    register_btn = tk.Button(register_win, text="Register", command=register)
    register_btn.pack()

def login():
    user_name = username_entry.get()
    password = password_entry.get()

    query = "SELECT password FROM users WHERE user_name = %s"
    cur.execute(query, (user_name,))
    fetched_pass = cur.fetchone()

    if fetched_pass is None:
        messagebox.showerror("Login Failed", "User not found.")
        return

    hashed_pass = create_hash(password)

    if hashed_pass == fetched_pass[0]:
        messagebox.showinfo("Login Successful", "You have been logged in.")
    else:
        messagebox.showerror("Login Failed", "Incorrect password.")

root = tk.Tk()
root.title("Login")


login_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
login_frame.place(x=550, y=160, width=490, height=300)

login_frame2 = tk.Frame(root, bd=2, relief=tk.GROOVE)
login_frame2.place(x=550, y=470, width=490, height=50)



username_label = tk.Label(root, text="Username:", font=("Arial", 12))
username_label.place(x=600, y=200)
username_entry = tk.Entry(root, width=30, font=("Arial", 12))
username_entry.place(x=700, y=200)

password_label = tk.Label(root, text="Password:", font=("Arial", 12))
password_label.place(x=600, y=250)
password_entry = tk.Entry(root, show="*", width=30, font=("Arial", 12))
password_entry.place(x=700, y=250)

login_btn = tk.Button(root, text="Log in", command=login, font=("Arial", 12), bg="blue", fg="white")
login_btn.place(x=770, y=300)

forgot_pass_label = tk.Label(root, text="Forgotten your Password?", font=("Arial", 12), fg="blue", cursor="hand2")
forgot_pass_label.place(x=710, y=400)
forgot_pass_label.bind("<Button-1>", lambda event: forgot_pass_window())

or_label = tk.Label(root,text="----------------------   OR   ----------------------", font=("Arial", 12))
or_label.place(x=660,y=350)

new_user_label = tk.Label(root,text = "Don't have an account?", font=("Arial", 12))
new_user_label.place(x=680, y=480)

register_btn = tk.Label(root, text="Sign up", font=("Arial", 12), fg="blue", cursor="hand2")
register_btn.place(x=850, y=480)
register_btn.bind("<Button-1>", lambda event: register_window())


root.geometry("400x200")
root.mainloop()
