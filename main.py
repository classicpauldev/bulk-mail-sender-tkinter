from tkinter import *
from tkinter.scrolledtext import ScrolledText as Sc
from smtpengine import SmtpEngine
import smtplib

WHITE = "#FFF"
BLACK = "#000"
FONT = ("Ariel", 15, "italic")

# Initialize the smtp engine class
smtp_engine = SmtpEngine()

window = Tk()
window.config(padx=50, pady=50, bg=WHITE)
window.title("Bulk Plain Mail Sender")

# Create the Labels
out_going_server = Label(text="SMTP Outgoing Server", bg=WHITE, fg=BLACK, font=FONT)
out_going_server.grid(column=0, row=1)
username = Label(text="SMTP Username", bg=WHITE, fg=BLACK, font=FONT)
username.grid(column=1, row=1)
password = Label(text="SMTP Password", bg=WHITE, fg=BLACK, font=FONT)
password.grid(column=2, row=1)
sec_delay = Label(text="SMTP Relay Delay (seconds)", bg=WHITE, fg=BLACK, font=FONT)
sec_delay.grid(column=3, row=1)
new_line = Label(bg=WHITE)
new_line.grid(column=1, row=3)
subject = Label(text="Message Subject", bg=WHITE, fg=BLACK, font=FONT)
subject.grid(column=2, row=4, columnspan=4)
another_line = Label(bg=WHITE)
another_line.grid(column=1, row=9)
message_content = Label(text="Message Content", bg=WHITE, fg=BLACK, font=FONT)
message_content.grid(column=1, row=10, columnspan=2)
smtp_port_label = Label(text="SMTP Port", bg=WHITE, fg=BLACK, font=FONT)
smtp_port_label.grid(column=0, row=4)
sender_label = Label(text="Sender Name", bg=WHITE, fg=BLACK, font=FONT)
sender_label.grid(column=1, row=4)

# Create the Entries
outgoing_server = Entry(highlightthickness=0)
outgoing_server.grid(column=0, row=2, pady=2, padx=20)
outgoing_server.insert(END, string="smtp.gmail.com")
delay = Entry(highlightthickness=0)
delay.grid(column=3, row=2, pady=2, padx=20)
delay.insert(END, string="3")
username_entry = Entry(highlightthickness=0)
username_entry.grid(column=1, row=2, pady=2, padx=20)
username_entry.insert(END, string="classicpaul.py@gmail.com")
password_entry = Entry(highlightthickness=0, show='*')
password_entry.insert(END, string="wwlxhhkzcduvvtwc")
password_entry.grid(column=2, row=2, pady=2, padx=20)
subject_entry = Entry(highlightthickness=0, width=45)
subject_entry.grid(column=2, row=5, columnspan=4)
subject_entry.insert(END, string="Just testing something")
message = Sc(width=120)
message.grid(column=0, row=11, columnspan=4)
smtp_port = Entry(highlightthickness=0)
smtp_port.grid(column=0, row=5, pady=2, padx=20)
sender_entry = Entry(highlightthickness=0)
sender_entry.grid(column=1, row=5, pady=2, padx=20)


# Capture all entries and create a send function that will call the smtp engine
def send():
    user = username_entry.get()
    passwd = password_entry.get()
    msg = message.get('1.0', 'end-1c')
    subj = subject_entry.get()
    server = outgoing_server.get()
    get_delay = delay.get()
    sender = sender_entry.get()
    port = smtp_port.get()
    if port in smtp_engine.valid_ports:
        if len(user) == 0 or len(passwd) == 0 or len(server) == 0:
            smtp_engine.no_field()
        else:
            if get_delay == '0' or get_delay == '':
                get_delay = '1'
            if msg == '':
                msg = "Hello World!\n\nCheers!\nClassic Paul"
            if subj == '':
                subj = "Howdy Mate! :D"
            if sender == '':
                sender = "Classic Paul"
            delay_sec = int(get_delay + '000')
            try:
                smtp_engine.send(user, passwd, msg, subj, server, port, sender)
                # Call our smtp_engine send method
                if len(smtp_engine.mails) != 0:
                    window.after(delay_sec, send)
                else:
                    smtp_engine.complete()
            # Catch possible incoming errors
            except IndexError:
                smtp_engine.mail_error()
            except smtplib.SMTPAuthenticationError:
                smtp_engine.connection_error()
            except smtplib.SMTPSenderRefused:
                smtp_engine.refuse_err()
            except smtplib.SMTPConnectError:
                smtp_engine.smtp_error()
    else:
        smtp_engine.port_invalid()


def delete():
    message.delete('1.0', 'end-1c')


# Creating the buttons
send_message = Button(text="Send Message", highlightbackground=WHITE, fg=BLACK, width=18, command=send)
send_message.grid(column=0, row=12)
clear_message = Button(text="Clear Message", highlightbackground=WHITE, fg=BLACK, width=18, command=delete)
clear_message.grid(column=3, row=12)
# Load the mail image
canvas = Canvas(width=200, height=200, bg=WHITE, highlightthickness=0)
photo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=photo)
canvas.grid(column=1, row=0, columnspan=2)
window.mainloop()
