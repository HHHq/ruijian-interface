"""自动发邮件的封装"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


class SendEmail:
    def __init__(self, smtpserver, user, password, sender, receiver, report_path):
        self.smtpserver = smtpserver
        self.user = user
        self.receiver = receiver
        self.password = password
        self.sender = sender
        self.report_path = report_path

    def email_content(self):
        msg = MIMEMultipart()
        # 定义发件人名称
        msg['From'] = Header('无名', 'utf-8')
        # 定义收件人名称
        msg['To'] = Header('', 'utf-8')
        # 定义主题
        subject = '接口测试自动化报告'
        msg['Subject'] = Header(subject, 'utf-8')
        # 邮件正文内容
        msg.attach(MIMEText('', 'html', 'utf-8'))
        # 构造附件
        att = MIMEText(open(self.report_path, 'rb').read(), 'base64', 'utf-8')
        att['Content-Type'] = 'application/octet-stream'
        # 定义附件名称
        att['Content-Disposition'] = 'attachment;filename={}'.format(self.report_path)
        msg.attach(att)
        return msg

    def send_email(self):
        smtp = smtplib.SMTP()
        smtp.connect(self.smtpserver, 25)
        smtp.login(self.user, self.password)
        smtp.sendmail(self.sender, self.receiver, self.email_content().as_string())
        smtp.quit()




