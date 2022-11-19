from smtplib import SMTP_SSL, SMTP
from ssl import create_default_context
from email.message import EmailMessage
import tkinter.messagebox as mb
from random import choice


class SmtpEngine:
    def __init__(self):
        self.mails = []
        self.author = "Classic Paul"
        self.valid_ports = ['25', '465', '587', '2525']
        self.msg_types = ['Html Message', 'Plaintext Message']
        self.send_delays = ['1', '2', '3', '4', '5']
        self.error = "Please provide a valid mail_list.txt file and format each email on a new line"
        self.field = "SMTP User, Password or Server cannot be empty"
        self.connect_err = 'SMTP authentication went wrong. Most probably the server didn’t acce' \
                           'pt the username/password combination provided.'
        self.refuse_err = 'Sender address refused.'
        self.smtp_ref = 'Error occurred during establishment of a connection with the server.'
        self.invalid_option = "Please select an option for both SMTP Relay Delay & SMTP Port"
        self.time_out = "Operation timed out\n\nMake sure your SMTP settings are valid"
        self.invalid_msg_type = "Please select a Message type"

        try:
            with open("mail_lists.txt") as self.emails:
                self.recipients = self.emails.readlines()
        except FileNotFoundError:
            self.mail_error()
        else:
            self.mails = [''.join(user.split('\n')) for user in self.recipients]
            self.count = len(self.mails)

    def send(self, user, password, message, subj, server, port, sender, html=None):
        email = choice(self.mails)
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = subj
        msg['From'] = f"{sender} <{user}>"
        msg['To'] = email
        if html is not None:
            msg.add_alternative(html, subtype="html")
        if port == '465':
            try:
                with SMTP_SSL(server, port=int(port), context=create_default_context()) as connect:
                    connect.login(user, password)
                    connect.send_message(msg=msg)
            except TimeoutError:
                self.timeout()
            else:
                self.mails.remove(email)
        else:
            try:
                with SMTP(server, port=int(port)) as connect:
                    connect.starttls(context=create_default_context())
                    connect.ehlo()
                    connect.login(user, password)
                    connect.send_message(msg=msg)
            except TimeoutError:
                self.timeout()
            else:
                self.mails.remove(email)

    def complete(self):
        mb.showinfo(title="Success", message=f"Message sent successfully to {self.count} Recipient's")

    def mail_error(self):
        mb.showerror(title="Mail list Error", message=f"{self.error}")

    def no_field(self):
        mb.showerror(title="Empty input found", message=f"{self.field}")

    def connection_error(self):
        mb.showerror(title="Authentication error", message=f"{self.connect_err}")

    def refuse_err(self):
        mb.showerror(title="Address refused", message=f"{self.refuse_err}")

    def smtp_error(self):
        mb.showerror(title="SMTP Connection error", message=f"{self.smtp_ref}")

    def option_invalid(self):
        mb.showerror(title="Port Error", message=f"{self.invalid_option}")

    def timeout(self):
        mb.showerror(title="Operation timed out", message=f"{self.time_out}")

    def msg_type_err(self):
        mb.showerror(title="Message type error", message=f"{self.invalid_msg_type}")
