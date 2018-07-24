from django.shortcuts import render,HttpResponse,redirect,reverse
import re
from .models import User
# Create your views here.
def index(reuqest):

    return HttpResponse("this is user!")

def register(request):

    return render(request,'register.html')

def register_handle(request):
    #进行注册处理
    #接收数据,
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')

    #进行数据校验
    if not all([username,password,email]):
        ##数据不完整
        return render(request,'register.html',{'errmsg':'数据不完整'})

    #检验邮箱
    if not re.match('^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
        return render(request ,'register.html',{'errmsg':'邮箱格式不正确'})

    #
    if allow != 'on':
        return render(request,'register.html',{'errmg':'请同意协议'})

    ## 检验用户名是否重复
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None

    if user:
        return render(request,'register.html',{'errmsg':'用户名已经存在!'})

    #进行业务处理:进行用户注册
    #这个地方是通用的用户流程,这里大概大概实例化一个模型类,然后就可以保存数据
    # user = User()
    # user.username = username
    # user.password = password

    #但是我们可以利用djgnao自带的用户管理来实现注册
    user = User.objects.create_user(username,email,password)

    ##刚刚注册的用户,不应该是激活的.所以自定义一下,设置为默认不激活.
    user.is_active = 0
    user.save()

    #返回应答,跳转傲首页
    return redirect(reverse("goods:index"))


    return HttpResponse("hello")