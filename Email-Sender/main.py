import smtplib
from email.message import EmailMessage
from tkinter import *
from tkinter import messagebox
import webbrowser

info = {}


def clear_view(tk):
    for i in tk.grid_slaves():
        i.destroy()


def log_info(email, password, tk):
    info['email'] = email
    info['password'] = password

    if email:
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(email, password)
                send_view(tk)

        except smtplib.SMTPAuthenticationError:
            messagebox.showinfo("Error", "Wrong email address or password!")

    else:
        messagebox.showinfo("Error", "Please enter your email address and password")


def send(email, subj, body):
    msg = EmailMessage()
    msg['To'] = email
    msg['Subject'] = subj
    msg['From'] = info['email']
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(info['email'], info['password'])
            smtp.send_message(msg)
            messagebox.showinfo("Done", f"Your message {subj} has been sent to {email}")

    except smtplib.SMTPRecipientsRefused:
        messagebox.showinfo("Error", "Invalid email address")


def send_view(tk):
    clear_view(tk)
    tk.geometry("600x400")
    tk.resizable(width=False, height=False)
    tk.title("Email Sender")

    Label(tk, text="Send to:", font="Times 15 bold").grid(row=0, column=0, padx=10, pady=10)
    send_email = Entry(tk, width=50)
    send_email.grid(row=0, column=1)

    Label(tk, text="Subject:", font="Times 15 bold").grid(row=1, column=0, pady=20)
    subject = Entry(tk, width=50)
    subject.grid(row=1, column=1)

    Label(tk, text="Message:", font="Times 15 bold").grid(row=2, column=0, padx=10, pady=10)
    message = Text(tk, width=50, height=10)
    message.grid(row=2, column=1)

    Button(tk, text="Send", width=7, bg="blue", fg="white",
           command=lambda: send(send_email.get(), subject.get(), message.get("1.0", END)))\
        .grid(row=3, column=2, pady=25)


def log_in_view(tk):
    tk.title("Log in")
    tk.geometry("400x200")

    Label(tk, text="Email:", font="Times 15 bold").grid(row=0, column=0, padx=10, pady=25)
    email = Entry(tk, width=35)
    email.grid(row=0, column=1)

    Label(tk, text="Password:", font="Times 15 bold").grid(row=1, column=0, padx=10)
    password = Entry(tk, show="*", width=35)
    password.grid(row=1, column=1)
    link = Label(tk, text="Application-specific password required.", cursor="hand2", fg="blue")
    link.grid(row=2, column=1)
    link.bind("<Button-1>", lambda e: webbrowser.open_new("https://support.google.com/mail/?p=InvalidSecondFactor"))

    Button(tk, text="Log in", bg="blue", fg="white", width=7,
           command=lambda: log_info(email.get(), password.get(), tk)).grid(row=3, column=2, pady=25)


master = Tk()
log_in_view(master)

master.mainloop()
