from ttxx import settings
from celery import Celery
from django.core.mail import send_mail
import time
from django.shortcuts import render
from django.template import loader,RequestContext

from django_redis import get_redis_connection
import os
 
#这里位置的代码,如果是用celery来启动的时候,才取消注释
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ttxx.settings")
# django.setup()

#这些包最好还是写在上面这三句代码的下面,不然的话初始化环境就是失败了!
from goods.models import GoodsType, GoodsSKU, IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner

#创建一个celery类的实例对象
app = Celery('celery_tasks.tasks',broker='redis://127.0.0.1:6379')

##定义任务函数
@app.task
def send_register_active_email(to_email,username,token):
    #发送激活邮件
     #发送邮件
    html_messages = "请点击这里完整用户激活!<a href=\"http://localhost:8000/user/active/%s\">点击我,点击我!take me!</a>"%token
    send_mail("你好吗?%s"%username,"",'lizhixuan@wolfcode.cn',[to_email,],html_message=html_messages,)

@app.task
def generate_static_index_html():
    '''产生首页静态页面'''
# 尝试从缓存中获取数据
   
    # 缓存中没有数据
    # 获取商品的种类信息
    types = GoodsType.objects.all()

    # 获取首页轮播商品信息
    goods_banners = IndexGoodsBanner.objects.all().order_by('index')

    # 获取首页促销活动信息
    promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

    # 获取首页分类商品展示信息
    for type in types: # GoodsType
        # 获取type种类首页分类商品的图片展示信息
        image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
        # 获取type种类首页分类商品的文字展示信息
        title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')

        # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
        type.image_banners = image_banners
        type.title_banners = title_banners

    #组织上下文
    context = {'types': types,
                'goods_banners': goods_banners,
                'promotion_banners': promotion_banners,
                "cart_count":0}
    
    #加载模板
    temp = loader.get_template('static_index.html')
    
    #模板渲染
    static_index_html = temp.render(context)
    
    #定义模板模板上下文
    #第二步可以省略,可以不依赖request
    # context = RequestContext(request,context)

    #生成首页静态页面文件

    save_path = os.path.join(settings.BASE_DIR,'static/index.html')
    with open(save_path,'w') as f:
        f.write(static_index_html)

    
