from django.shortcuts import render,HttpResponse,redirect,reverse
from django.http import JsonResponse
import re
from .models import User,Address
from django.views.generic import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from ttxx import settings
from utils.mixin import LoginRequiredMixin
from django.core.paginator import Paginator

##导入发送邮件函数
from celery_tasks.tasks import send_register_active_email

##导入登陆验证装饰器
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django_redis import get_redis_connection
from goods.models import GoodsSKU
from order.models import OrderInfo,OrderGoods


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


        if request.user.is_authenticated:
           
            return redirect(reverse('user:info'))

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
        user = request.user
        address = Address.objects.get_default_address(user)

        #获取用户浏览记录
        # from redis import StrictRedis
        # sr = StrictRedis(host="127.0.0.1",db=3)
        con = get_redis_connection('default')
        history_key = 'history_%d'%user.id
        #获取用户最新浏览的5个商品id
        sku_ids = con.lrange(history_key,0,4)

        #转换一下,因为redis输出的都是byte
        # for x in range(0,len(sku_ids)):
        #     sku_ids[x] = sku_ids[x].decode()


        goods_li = GoodsSKU.objects.filter(id__in=sku_ids)

       
        # for a_id in sku_ids:
        #     for goods in goods_li:
        #         if a_id == goods_id:
        #             goods_res.append(goods)

        goods_li = []
        for id in sku_ids:
            goods = GoodsSKU.objects.filter(id=id)
            goods_li.append(goods[0])

        

        context = {'page':'user','address':address,'goods_li':goods_li}
        
        return render(request,'user_center_info.html',context)

class UserOrderView(LoginRequiredMixin,View):
    '''用户中心-订单页'''
    def get(self, request, page):
        '''显示'''
        # 获取用户的订单信息
        user = request.user
        orders = OrderInfo.objects.filter(user=user).order_by('-create_time')

        # 遍历获取订单商品的信息
        for order in orders:
            # 根据order_id查询订单商品信息
            order_skus = OrderGoods.objects.filter(order_id=order.order_id)

            # 遍历order_skus计算商品的小计
            for order_sku in order_skus:
                # 计算小计
                amount = order_sku.count*order_sku.price
                # 动态给order_sku增加属性amount,保存订单商品的小计
                order_sku.amount = amount

            # 动态给order增加属性，保存订单状态标题
            order.status_name = OrderInfo.ORDER_STATUS[str(order.order_status)]
            # 动态给order增加属性，保存订单商品的信息
            order.order_skus = order_skus

        # 分页

        paginator = Paginator(orders, 3)

        # 获取第page页的内容
        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1

        

        # 获取第page页的Page实例对象
        
        order_page = paginator.page(page)

        print(order_page.object_list)

        # todo: 进行页码的控制，页面上最多显示5个页码
        # 1.总页数小于5页，页面上显示所有页码
        # 2.如果当前页是前3页，显示1-5页
        # 3.如果当前页是后3页，显示后5页
        # 4.其他情况，显示当前页的前2页，当前页，当前页的后2页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        # 组织上下文
        context = {'order_page':order_page,
                'pages':pages,
                'page': 'order'}

        # 使用模板
        return render(request, 'user_center_order.html', context)

class AddressView(LoginRequiredMixin,View):
    def get(self,request):

        #获取用户的默认收货地址作为显示.
        # print(type(request.user))
        # print(request.user.username)
        user = request.user
        # try:
        #     address = Address.objects.get(user=user,is_default=True)
        # except Address.DoesNotExist:
        #     address = None

        address = Address.objects.get_default_address(user)

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

        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$',phone):
            
            return render(request,'user_center_site.html',{'errmsg':'你的手机号码错误!!'})

        #业务处理#地址添加
        #如果不存在收货地址,就设置为默认地址,否则就只添加新地址.!
        user = request.user
        # try:
        #     address = Address.objects.get(user=user,is_default=True)
        # except Address.DoesNotExist:
        #     address = None
        
        address = Address.objects.get_default_address(user)
        print(address)
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

  