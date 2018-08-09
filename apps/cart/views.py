from django.shortcuts import render,HttpResponse

from django.views.generic import View
from django.http import JsonResponse
from goods.models import GoodsSKU
from django_redis import get_redis_connection
from utils.mixin import LoginRequiredMixin
# Create your views here.
def index(request):

    return HttpResponse("this is cart")


##cart/add
class CartAddView(View):
    '''购物车记录添加'''
    def post(self,request,):

        user = request.user
        #判断用户是否登陆
        if not user.is_authenticated:
            return JsonResponse({'res':0,'errmsg':'请先登陆!'})

        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        #接收数据

        #数据校验

        if not all([sku_id,count]):
            return JsonResponse({'res':1,'errmsg':'数据不完整'})

        #校验添加的商品数量

        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'res':2,'errmsg':'商品数量错误'})

        #校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except Exception as e:
            return JsonResponse({'res':3,'errmsg':'商品不存在'})
        ##业务处理,添加购物车记录

        ##先尝试获取当前用户是否有用户购物记录
        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id

        #尝试获取sku_id的值
        cart_count = int(conn.hget(cart_key,sku_id))
        print(cart_count)
        if cart_count:
            #如果存在就进行累加
            count += int(cart_count)

        #检验商品的库存
        if count > sku.stock:
            return JsonResponse({'res':4,'errmsg':'库存不足!'})
        #设置hash中sku_id
        #这里已经设置了通用规则,就是如果存在skuid的话,就进行更新,不然的话,就进行添加.
        conn.hset(cart_key,sku_id,count)

        #计算用户购物车商品的条目数

        keys = conn.hkeys(cart_key)

        total_count = 0
        #当前用户总的商品数目

        for x in keys:
            x1 = int(conn.hget(cart_key,x))
            total_count += x1

        #total_count = conn.hlen(cart_key)

        #返回应答
        return JsonResponse({'res':5,'message':'成功!','total_count':total_count})


class CartInfoView(LoginRequiredMixin,View):
    '''购物车显示页面'''

    def get(self,request):

        #获取用户购物车中商品的信息
        user = request.user

        conn = get_redis_connection('default')

        cart_key = 'cart_%d'%user.id

        cart_dict = conn.hgetall(cart_key)


        #保存用户的商品总数目和总价格.
        skus = []
        total_price = 0
        total_count = 0
        #遍历获取商品的信息

        for sku_id,count in cart_dict.items():
            #根据商品的id获取商品的信息
            sku = GoodsSKU.objects.get(id=sku_id)
            #计算商品的小计
            amount = sku.price*int(count)
            #给sku动态增加属性amount,保存商品小计
            sku.amount = int(amount)

            sku.count = int(count)

            skus.append(sku)

            total_price += int(amount)
            total_count += int(count)
        
        #组织信息
        context = {'total_price':total_price,'total_count':total_count,'skus':skus}

        return render(request,'cart.html',context)


# 更新购物车记录
#才用ajax
#传递参数,商品id,更新商品的数量.估计还要判断用户是否登陆

class CartUpdateView(View):
    '''购物车记录更新'''
    def post(self,request):
        '''购物车记录更新'''

        user = request.user
        #判断用户是否登陆
        if not user.is_authenticated:
            return JsonResponse({'res':0,'errmsg':'请先登陆!'})

        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        #接收数据


        #校验数据
        #数据校验

        if not all([sku_id,count]):
            return JsonResponse({'res':1,'errmsg':'数据不完整'})

        #校验添加的商品数量

        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'res':2,'errmsg':'商品数量错误'})

        #校验商品是否存在
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except Exception as e:
            return JsonResponse({'res':3,'errmsg':'商品不存在'})

        #业务处理

        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id

        #检查库存
        if count > sku.stock:
            return JsonResponse({'res':4,'errmsg':'商品库存不足'})


        #更新
        conn.hset(cart_key,sku_id,count)

        total_count = 0
        #返回redis中总的商品数量
        vals = conn.hvals(cart_key)

        for x in vals:
            total_count += int(x)
        
        #返回应答
        return JsonResponse({'res':5,'message':'更新成功!','total_count':total_count})

