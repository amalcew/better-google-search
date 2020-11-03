# Emails Sending Script (ESS) for automated email sending to multiple addresses
import time
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from auxiliary_functions import convert_to_list, extract_unique


class Sender:
    def __init__(self, email, password, server, port):
        self.email = email
        self.password = password
        self.server = server
        self.port = port


class Mail:
    def __init__(self, Sender, subject, message, attachment, receivers):
        self.subject = subject
        self.message = message
        self.attachment = attachment
        self.sender_email = Sender.email
        self.password = Sender.password
        self.server = Sender.server
        self.port = Sender.port
        self.receivers = convert_to_list(receivers)
        self.receivers = extract_unique(self.receivers)

    def send_message(self):
        start_time = time.time()
        quantity = len(self.receivers)
        print("Logged as " + str(self.sender_email))
        print("Sending " + str(quantity) + " messages:")
        for x in range(0, quantity):
            receiver_email = self.receivers[x]
            print("\t" + str(receiver_email))
            time.sleep(5)
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = receiver_email
            message["Subject"] = self.subject
            # message["Bcc"] = receiver_email

            # save message
            message.attach(MIMEText(self.message, "plain"))
            message = message.as_string()
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.server, self.port, context=context) as server:
                server.ehlo()
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, receiver_email, message)
                server.quit()
            print("\tsent\n")
        print("Executed in %s seconds\n" % (time.time() - start_time))

    def send_image(self):
        if self.attachment is not None:
            start_time = time.time()
            quantity = len(self.receivers)
            print("Logged as "+str(self.sender_email))
            print("Sending "+str(quantity)+" messages:")
            for x in range(0, quantity):
                receiver_email = self.receivers[x]
                print("\t"+str(receiver_email))
                time.sleep(5)
                message = MIMEMultipart('related')
                message["From"] = self.sender_email
                message["To"] = receiver_email
                message["Subject"] = self.subject
                # message["Bcc"] = receiver_email

                # create alternative part of message
                message_alt = MIMEMultipart('alternative')
                message.attach(message_alt)
                message_alt_text = MIMEText('--')
                message_alt.attach(message_alt_text)
                message_alt_text = MIMEText('<p>'+self.message+'</p><p><img src="cid:image"></p>', 'html')
                message_alt.attach(message_alt_text)
                # open image and add it to message
                image = open(self.attachment, 'rb')
                message_img = MIMEImage(image.read())
                image.close()
                message_img.add_header('Content-ID', '<image>')
                message.attach(message_img)
                # save message
                message = message.as_string()
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self.server, self.port, context=context) as server:
                    server.ehlo()
                    server.login(self.sender_email, self.password)
                    server.sendmail(self.sender_email, receiver_email, message)
                    server.quit()
                print("\tsent\n")
            print("Executed in %s seconds\n" % (time.time() - start_time))
        else:
            print("Wrong function selected. Please select valid image attachment")

    def send_attachment(self):
        if self.attachment is not None:
            start_time = time.time()
            quantity = len(self.receivers)
            print("Logged as "+str(self.sender_email))
            print("Sending "+str(quantity)+" messages:")
            for x in range(0, quantity):
                receiver_email = self.receivers[x]
                print("\t"+str(receiver_email))
                time.sleep(5)
                message = MIMEMultipart()
                message["From"] = self.sender_email
                message["To"] = receiver_email
                message["Subject"] = self.subject
                # message["Bcc"] = receiver_email
                message.attach(MIMEText(self.message, "plain"))
                # Open attachment in binary mode
                with open(self.attachment, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {self.attachment}",
                )
                message.attach(part)
                # save message
                message = message.as_string()
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self.server, self.port, context=context) as server:
                    server.ehlo()
                    server.login(self.sender_email, self.password)
                    server.sendmail(self.sender_email, receiver_email, message)
                    server.quit()
                print("\tsent\n")
            print("Executed in %s seconds\n" % (time.time() - start_time))
        else:
            print("Wrong function selected. Please select attachment")


def main():
    # Sender have to contain: email, password, smtp server, port
    # Mail have to contain: sender, subject, message, attachment, receivers
    marbet = Sender("a.malcew@marbet.com.pl", "marbet12", "marbet4.marbet.com.pl", 465)
    sender_gmail = Sender("armstacci@gmail.com", "DopE#1337Hxr", "smtp.gmail.com", 465)
    test_email = Mail(sender_gmail, "Ssssss! Python!", "This message was sent by Python Email Sending Script", 'exp/test.jpeg',
                 "data/email_adressess.txt")
    # test_email.send_attachment()
    # test_email.send_message()
    test_email.send_image()


if __name__ == '__main__':
    main()
