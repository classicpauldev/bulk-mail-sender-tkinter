# Disclaimer - Use responsibly, as i will not be held accountable for any misuse of this program.

from tkinter import *
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText as Sc
from smtpengine import SmtpEngine
import smtplib
# Test Connection verifies SMTP before sending
import os
WHITE = "#FFF"
# Progress label shows sent/total during send
BLACK = "#000"
FONT = ("Ariel", 15, "italic")

# Initialize the smtp engine class
smtp_engine = SmtpEngine()

window = Tk()
window.config(padx=50, pady=50, bg=WHITE)
window.title(f"Bulk Mail Sender by {smtp_engine.author}")

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

# Mail list and progress labels
mail_list_label = Label(
    text=f"Loaded {getattr(smtp_engine, 'count', 0)} recipients from {os.path.basename(getattr(smtp_engine, 'mail_list_path', 'mail_lists.txt'))}",
    bg=WHITE,
    fg=BLACK,
    font=("Ariel", 11, "italic"),
    anchor="w",
)
mail_list_label.grid(column=0, row=8, columnspan=2, sticky="w")

progress_label = Label(
    text="Ready",
    bg=WHITE,
    fg=BLACK,
    font=("Ariel", 11, "italic"),
    anchor="w",
)
progress_label.grid(column=0, row=13, columnspan=4, sticky="w")

# Create the Entries
# Message type: Html or Plaintext
outgoing_server = Entry(highlightthickness=0)
outgoing_server.grid(column=0, row=2, pady=2, padx=20)
username_entry = Entry(highlightthickness=0)
username_entry.grid(column=1, row=2, pady=2, padx=20)
password_entry = Entry(highlightthickness=0, show='*')
password_entry.grid(column=2, row=2, pady=2, padx=20)
subject_entry = Entry(highlightthickness=0, width=45)
subject_entry.grid(column=2, row=5, columnspan=4)
message = Sc(width=120)
message.grid(column=0, row=11, columnspan=4)
sender_entry = Entry(highlightthickness=0)
sender_entry.grid(column=1, row=5, pady=2, padx=20)

# Create an OptionMenu Widget
msg_type = StringVar(window)
msg_type.set("Select Message Type")
msg_menu = OptionMenu(window, msg_type, *smtp_engine.msg_types)
msg_menu.config(bg=WHITE, fg=BLACK, width=18)
msg_menu.grid(column=0, row=12)
delay_type = StringVar(window)
delay_type.set("Select an Option")
delay_menu = OptionMenu(window, delay_type, *smtp_engine.send_delays)
delay_menu.config(bg=WHITE, fg=BLACK, width=16)
delay_menu.grid(column=3, row=2)
port_type = StringVar(window)
port_type.set("Select an Option")
port_menu = OptionMenu(window, port_type, *smtp_engine.valid_ports)
port_menu.config(bg=WHITE, fg=BLACK, width=16)
port_menu.grid(column=0, row=5)


def choose_mail_list():
    """Let the user pick a mail list file and reload recipients."""
    path = filedialog.askopenfilename(
        title="Select mail list",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
    )
    if not path:
        return

    smtp_engine.reload_mail_list(path)
    mail_list_label.config(
        text=f"Loaded {smtp_engine.count} recipients from {os.path.basename(path)}"
    )
    progress_label.config(text="Ready to send")


# Capture all entries and create a send function that will call the smtp engine
def send():
    validate = "Select an Option"
    user = username_entry.get()
    passwd = password_entry.get()
    msg = message.get('1.0', 'end-1c')
    subj = subject_entry.get()
    server = outgoing_server.get()
    get_delay = delay_type.get()
    sender = sender_entry.get()
    port = port_type.get()
    text_type = msg_type.get()
    if port != validate and get_delay != validate:
        if len(user) == 0 or len(passwd) == 0 or len(server) == 0:
            smtp_engine.no_field()
        else:
            if msg == '':
                msg = "Hello World!\n\nCheers!\nClassic Paul"
            if subj == '':
                subj = "Howdy Mate! :D"
            if sender == '':
                sender = "Classic Paul"
            delay_sec = int(get_delay + '000')
            try:
                if text_type != "Select Message Type":
                    if text_type == smtp_engine.msg_types[0]:
                        smtp_engine.send(user, passwd, msg, subj, server, port, sender, html=msg)
                    else:
                        smtp_engine.send(user, passwd, msg, subj, server, port, sender)
                    # Call our smtp_engine send method
                    progress_label.config(
                        text=f"Sent {smtp_engine.sent} of {smtp_engine.count} recipients"
                    )
                    if len(smtp_engine.mails) != 0:
                        window.after(delay_sec, send)
                    else:
                        smtp_engine.complete()
                        progress_label.config(
                            text=f"Completed sending to {smtp_engine.count} recipients"
                        )
                else:
                    smtp_engine.msg_type_err()
            # Catch possible incoming errors
# Relay delay helps avoid rate limiting
# ScrolledText used for long messages
            except IndexError:
                smtp_engine.mail_error()
            except smtplib.SMTPAuthenticationError:
                smtp_engine.connection_error()
            except smtplib.SMTPSenderRefused:
                smtp_engine.refuse_err()
            except smtplib.SMTPConnectError:
                smtp_engine.smtp_error()
    else:
        smtp_engine.option_invalid()


def test_connection():
    """Test SMTP connection without sending a message."""
    validate = "Select an Option"
    user = username_entry.get()
    passwd = password_entry.get()
    server = outgoing_server.get()
    port = port_type.get()

    if port == validate:
        smtp_engine.option_invalid()
        return

    if len(user) == 0 or len(passwd) == 0 or len(server) == 0:
        smtp_engine.no_field()
        return

    smtp_engine.test_connection(user, passwd, server, port)


# Creating the buttons
clear_message = Button(
    text="Send Message",
    highlightbackground=WHITE,
    fg=BLACK,
    width=17,
    command=send,
)
clear_message.grid(column=3, row=12)

test_button = Button(
    text="Test Connection",
    highlightbackground=WHITE,
    fg=BLACK,
    width=17,
    command=test_connection,
)
test_button.grid(column=2, row=12)

load_list_button = Button(
    text="Load Mail List",
    highlightbackground=WHITE,
    fg=BLACK,
    width=17,
    command=choose_mail_list,
)
load_list_button.grid(column=0, row=7, pady=5)

# Load the mail image
# Credentials validated before send
canvas = Canvas(width=200, height=200, bg=WHITE, highlightthickness=0)
photo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=photo)
canvas.grid(column=1, row=0, columnspan=2)
window.mainloop()
