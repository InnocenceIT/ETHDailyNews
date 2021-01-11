# coding=utf-8

import smtplib
from email.mime.text import MIMEText
from email.header import Header

smtp_server = 'smtp.qq.com'  # 固定写死
smtp_port = 465  # 固定端口


class EmailUtil:
    @classmethod
    def sendEmail(cls, email: str, title: str, content: str, from_addr:str, qqCode:str ):
        # 配置服务器
        stmp = smtplib.SMTP_SSL(smtp_server, smtp_port)
        stmp.login(from_addr, qqCode)
        # 组装发送内容
        message = MIMEText(content, 'html', 'utf-8')  # 发送的内容
        message['From'] = Header("Python邮件系统", 'utf-8')  # 发件人
        message['To'] = Header(email, 'utf-8')  # 收件人
        message['Subject'] = Header(title, 'utf-8')  # 邮件标题
        try:
            stmp.sendmail(from_addr, email, message.as_string())
            print('邮件发送成功')
        except Exception as e:
            print('邮件发送失败--' + str(e))


def main():
    mail_msg = """
    <p>Python </p>
    <p><a href="http://www.runoob.com">这是一个链接</a></p>
    """
    EmailUtil.sendEmail('825639602@qq.com', "这是一封测试邮件", "邮件发送测试...")


if __name__ == '__main__':
    main()






