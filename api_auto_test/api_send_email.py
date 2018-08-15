#-*- coding: utf-8 -*-
import smtplib
from  email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import  MIMEApplication

class send_email(object):
    def __init__(self,send_user,send_pwd,receive_user,smtp_server,smtp_port):
        self.smtp_server=smtplib.SMTP(smtp_server,port=smtp_port,timeout=60)
        self.s_user=send_user
        self.r_user=receive_user
        pass

    def email_content(self,subject,text,*attach_file):
        msg=MIMEMultipart()
        msg['Subject']=subject
        msg['From']=self.s_user
        msg['To']=self.r_user
        content=MIMEText(text)
        msg.attach(content)
        for v in attach_file:
            content=MIMEApplication(open(v,'rd').read())
            content.add_header('Content-Disposition', 'attachment', filename=v)
            msg.attach(content)
        return msg


    def send_content(self,msg):
        self.smtp_server.login(self.send_user, self.send_pwd)
        self.smtp_server.sendmail(self.s_user,self.r_user,msg.as_string())


    def send_close(self):
        self.smtp_server.close()