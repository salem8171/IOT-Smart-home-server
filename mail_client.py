def sendmail(msg):
    try:
        mail_server = smtplib.SMTP('smtp.gmail.com', 587)
        # mail_server.connect('smtp.gmail.com', 465)
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.login("s28260962@gmail.com", "password")
        mail_server.sendmail("s28260962@gmail.com", "yosr.benhamida@enis.tn", msg)
        mail_server.close()
    except:
        print("mail not send")
