#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import email
import smtplib
import time
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread

import schedule


class MailManager(object):
    def __init__(self, **kwargs):
        self.server = kwargs.get('server')
        self.port = kwargs.get('port')
        self.nickname = kwargs.get('nickname')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')

    def send_mail(self, receivers, subject, content, subtype='plain', charset='UTF-8'):
        rcptto = ','.join(receivers)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header(subject, charset).encode()
        msg['From'] = '%s <%s>' % (
            Header(str(self.nickname), charset).encode(), self.username)
        msg['To'] = rcptto
        msg['Reply-to'] = self.username
        msg['Message-id'] = email.utils.make_msgid()
        msg['Date'] = email.utils.formatdate()
        payload = MIMEText(content, _subtype=subtype, _charset=charset)
        msg.attach(payload)

        try:
            client = smtplib.SMTP()
            client.connect(self.server, self.port)
            client.set_debuglevel(0)
            client.login(self.username, self.password)
            client.sendmail(self.username, rcptto, msg.as_string())
            client.quit()
            print('邮件发送成功！')
        except Exception as e:
            print('邮件发送异常, %s' % str(e))


def duty_remind(on_duty=True):
    kwargs = {
        'server': 'smtp.aliyun.com',
        'port': 25,
        'nickname': '打卡提醒',
        'username': 'from@aliyun.com',
        'password': 'password',
    }
    now = datetime.datetime.now()
    receivers = ['receiver@aliyun.com']
    subject = '打卡提醒'
    if on_duty:
        content = '''
            现在是北京时间：%s，该上班啦！<br/><br/>
            <a href='https://github.com'>去打卡</a>
            ''' % now.strftime('%Y-%m-%d %H:%M')
    else:
        content = '''
            现在是北京时间：%s，工作完成了吗，打卡下班吧！<br/><br/>
            <a href='https://github.com'>去打卡</a>
            ''' % now.strftime('%Y-%m-%d %H:%M')
    mail_manager = MailManager(**kwargs)
    mail_manager.send_mail(receivers, subject, content, subtype='html')


def async_run_task(on_duty):
    Thread(target=duty_remind(on_duty)).start()


def schedule_task():
    schedule.every().day.at("10:00").do(async_run_task, on_duty=True)
    schedule.every().day.at("18:30").do(async_run_task, on_duty=False)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    schedule_task()
