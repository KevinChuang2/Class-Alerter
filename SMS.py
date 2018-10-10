import smtplib

# Establish a secure session with gmail's outgoing SMTP server using your gmail account



def send_msg(outgoing_addr, msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()
    password = 'password1798'
    server.login('kevinchuang2@gmail.com', password)
    email = 'Subject: {}\n\n{}'.format(msg, 'this was sent through kevin\'s dumbass script')
    # Send text message through SMS gateway of destination number
    server.sendmail('kevinchuang2@gmail.com', outgoing_addr, email)
