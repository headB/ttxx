from ttxx import settings
from celery import Celery
from django.core.mail import send_mail
import time

# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ttxx.settings")
# django.setup()

#创建一个celery类的实例对象
app = Celery('celery_tasks.tasks',broker='redis://127.0.0.1:6379')

##定义任务函数
@app.task
def send_register_active_email(to_email,username,token):
    #发送激活邮件
     #发送邮件
    html_messages = "请点击这里完整用户激活!<a href=\"http://localhost:8000/user/active/%s\">点击我,点击我!take me!</a>"%token
    send_mail("你好吗?%s"%username,"",'lizhixuan@wolfcode.cn',[to_email,],html_message=html_messages,)
