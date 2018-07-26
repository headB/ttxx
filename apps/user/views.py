from django.shortcuts import render,HttpResponse,redirect,reverse
import re
from .models import User,Address
from django.views.generic import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from ttxx import settings
from utils.mixin import LoginRequiredMixin

##导入发送邮件函数
from celery_tasks.tasks import send_register_active_email

##导入登陆验证装饰器
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.
def index(reuqest):

    return HttpResponse("this is user!")

def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        #进行注册处理
        return register_handle(request)

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

    ##然后需要给用户发送验证邮件.!
    #加密用户的身份信息,生成激活的token.
    serializer = Serializer(settings.SECRET_KEY,600)
    info = {'confirm':user.id}
    token = serializer.dumps(info)
    token = token.decode()
    #发送邮件
    html_messages = "请点击这里完整用户激活!<a href=\"http://localhost:8000/user/active/%s\">点击我,点击我!take me!</a>"%token

    from django.core.mail import send_mail
    send_mail("你好吗?","",'lizhixuan@wolfcode.cn',[email,],html_message=html_messages,)
    #send_register_active_email.delay(email,username,token)
    #返回应答,跳转傲首页
    return redirect(reverse("user:index"))


class RegisterView(View):
    '''注册类'''
    def get(self,request):
        
        return render(request,'register.html')

    def post(self,request):

        return register_handle(request)


class ActiveView(View):

    

    def get(self,request,token):

        serializer = Serializer(settings.SECRET_KEY,600) 
        try:
            user_info = serializer.loads(token)
            user_id = user_info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()

        #然后跳转登录页面
            return render(request,'login.html')

        except SignatureExpired as e:
            #激活码已经过期SignatureExpired
            return HttpResponse("激活码已经过期!")

        except Exception as e:
            return HttpResponse("发生未知错误!")


class LoginView(View):

    #登陆
    def get(self,request):
        #显示登陆页面

        ##判断是否记住用户名
        if 'username'  in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        return render(request,'login.html',{'username':username,'checked':checked})

    def post(self,request):
        #进行登陆校验
        #接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        #校验合法性
        if not all([username,password]):
            return render(request,'login.html',{'errmsg':'数据不完整'})

        

        #检查账号密码是否正确
        from django.contrib.auth import authenticate,login
        user = authenticate(username=username,password=password)

        #好像激活了才可以通过检验的.所以添加一个检测用户是否存在
        user1 = User.objects.filter(username=username)

        if user1:

            if user1.filter(is_active=True):
        
                if user is not None:
                    #用户已经激活
                    #记录登陆状态

                    #获取登陆后所要跳转的地址
                    to_redirect_url = request.GET.get("next",reverse("goods:index"))

                    response = redirect(to_redirect_url) ##实质是返回一个HTTPResponseDirect对象

                    login(request,user)

                    

                    remember = request.POST.get('remember')
                    
                    #判断是否需要记住用户名
                    if remember == 'on':
                        response.set_cookie('username',username,max_age=7*24)
                    #
                    #跳转到首页
                    return response
                    #return redirect(reverse("goods:index"))
                
                else:
                    return render(request,'login.html',{'errmsg':'账号或者密码错误!'})
            else:
                return render(request,'login.html',{'errmsg':'账号未激活!!'})
        else:
            return render(request,'login.html',{'errmsg':'账号不存在'})    



class UserInfoView(LoginRequiredMixin,View):
    def get(self,request):

        #获取用户个人信息

        #获取用户浏览记录


        
        return render(request,'user_center_info.html',{'page':'user'})

class UserOrderView(LoginRequiredMixin,View):
    def get(self,request):

        #获取用户的订单信息


        
        return render(request,'user_center_order.html',{'page':'order'})

class AddressView(LoginRequiredMixin,View):
    def get(self,request):

        #获取用户的默认收货地址作为显示.

        user = request.user
        try:
            address = Address.objects.get(user=user,is_default=True)
        except Address.DoesNotExist:
            address = None

        return render(request,'user_center_site.html',{'page':'address','address':address})


    def post(self,request):

        #校验数据
        receiver = request.POST.get("receiver")
        addr = request.POST.get("addr")
        zip_code = request.POST.get("zip_code")
        phone = request.POST.get("phone")

        if not all([receiver,addr,zip_code,phone],):
            #return HttpResponse("数据不完整")
            return render(request,'user_center_site.html',{'errmsg':'你的数据不完整!'})

        if not  re.match("\d{3}\d{8}|\d{4}\{7,8}",phone):
            
            return render(request,'user_center_site.html',{'errmsg':'你的数据号码错误!!'})

        #业务处理#地址添加
        #如果不存在收货地址,就设置为默认地址,否则就只添加新地址.!
        user = request.user
        try:
            address = Address.objects.get(user=user,is_default=True)
        except Address.DoesNotExist:
            address = None

        if address:
            is_default = False
        else:
            is_default = True

        #添加地址
        Address.objects.create(user=user,
        receiver=receiver,
        addr=addr,
        zip_code=zip_code,
        phone=phone,
        is_default=is_default)

        #返回订单,刷新地址
        return redirect(reverse('user:address'))


class LogoutView(LoginRequiredMixin,View):

    def get(self,reuqest):

        logout(reuqest)
        return redirect(reverse('user:login'))

  