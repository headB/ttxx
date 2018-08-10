# 订单生成.
1. 就是,确定好商品的数量和价格之后,然后提交购物车.
2. 从不信任post过来的数据.
3. 商品总的数量的确是存在redis里面,但是要判断用户行为是否去全部购物,就需要用于来传递.
4. ## checkbox 只有被选中才会被提交.
5. ## request.POST.getlist功能.
    1. 因为在购物车确定的时候,因为选中的checkbox,里面所有的name都是sku_ids,所以,可以利用getlist批量来获取.
6. view中定义OrderPlaceView方法
    1. 判断用户是否登陆
    2. 校验sku-id参数.
    3. 去redis获取对应用户的商品,但是是根据id来遍历获取.数量不同用户传递,但是是否购物这个商品的种类,还是根据checkbox来判断的.
    4. 总数不用统计,因为已经是总数了,可以统计一下单个商品种类的总价格.
    5. 上面的总价格,可以动态地添加到当前的sku_id对象.
    6. 但是注意当前的对象是querySet对象,千万不要调用save方法保存.
    7. ## 运费,属于另外一个子系统.暂时是写屎.
    8. 实际费用就是总的商品价格+运费.
    9. ## 获取用户的地址.
        1. 其实就是用xxx.objects去获取信息就可以了.
    10. 组织好上下文.!
        1. 就是显示的商品啊,价格啊,之类的啊!.
#创建订单前端js
1. 

# 提交订单页面显示
1. 首先我们来看一下数据表,看看特定的字段都有那些功能!
    1. OrderInfo
        1. order_id-->自己指定的id
        2. pay_method-->SmallIntegerFile-->choices=元组或者列表(PAY_METHOD_CHOICES)
            1. such as
            ```python
                PAY_METHOD_CHOICES = (
                    (1,'货到付款'),
                    (2,'货到付款'),
                    (3,'货到付款'),
                    (3,'货到付款'),
                )
            ```
        3. trade_no (支付编码)
    2. 绑定了#order_btn的点击事件.
    3. 后台需要接收的参数
        1. 收货地址(数值)
        2. 商品的种类id(数值)
        3. 支付方式(数值)
    4. 选择器特别备注,这里选定是一个元素,中间并没有空格,就好像寻找类属性的时候一样,.xx.yy,都是紧接在一起的.!
        1. $('input[name="addr_id"]:checked').val()
    5. 开始写后台的OrderCommitView.
        1. 定义post请求,订单创建
        2. 判断用户是否登陆
        3. 接收上面提及的三个参数.
        4. 校验数据.
        5. 校验支付参数.
            1. 在order里面定义三个字典,用于校验数据的.
                1. if pay_method not in OrderInfo.PAY_METHODS.keys():
        6. 创建订单核心业务.
            1. 用户每下一个订单,就需要向df_order_info表中加入一条记录.
                1. 用户的订单中有几个商品,就需要想df_order_goods表中加入几条记录.
            2. 向df_order_info表中添加一条记录.
                1. 需要用到的参数.
                    1. ## order_info里面的order_id是我们自己定义指定的主键,primary_key=True,这样id就不会发生自动增长.!
                    2. 需要传入的参数有.
                        1. total_count
                        2. total_price
                        3. transit_price
                            1. 运费写屎就可以了.
                    3. 然后就组织参数
                    4. ## 订单id的创建(命名).
                        1. 根据当前的时间,比如说201808101657+用户id
                            1. 借助datetime
                2. ## 开始添加记录.
                    1. 代码
                        ```python
                            order = OrderInfo.objects.create(xxxxx)
                            #对,这条代码.创建写好参数的时候,已经插入到数据库了.!
                        ```
            3. ## 向df_order_goods添加记录.
                1. 遍历商品信息
                    ```python
                        #获取商品的信息
                        sku_ids = sku_ids.split(',')
                        for sku_id in sku_ids:
                    ```
                2. 尝试去查询商品的id.看看是否存在.!
                3. ## 从redis中获取所有购买商品的数量.
                    1. 所以需要引入用户的id,用于获取redis中的商品信息.
                4. 都获取好参数之后,准备添加记录到数据库了.!
                    ```python
                        OrderGoods.objects.create(xxx)
                    ```
            4. ## 更新商品库存和销量.
                ```python
                    sku.stock -= int(count)
                ```
                1. 累加计算订单商品的总数目和总价格.
            5. ## 更新订单信息表仲的商品的总数量和总价格.
                ```python
                    #order = OrderInfo.objects.create()
                    order.total_count
                    order.total_price
                    order.save()

                ```
                > 这里给自己提醒一下自己,就是,创建一个objects,保存的属性未必所有得是对应字段的,动态增加的属性,只是用于后面方便展示而已.

            6. ## 购物车中需要清除对应的记录.
                1. 使用redis删除就可以了.!
                    ```python
                        conn.hdel(cart_key,*sku_ids)
                        #什么高级用法?
                        In [7]: x3 = ["xx",*x2]
                        In [8]: x3
                        Out[8]: ['xx', 'lizhixuan', 'kumanxuan', 'beetle']
                        In [9]: x2
                        Out[9]: ['lizhixuan', 'kumanxuan', 'beetle']

                    ```
            7. 返回应答.
    6. ## 关键就是向 df_order_info和df_order_goods
# django事务处理.!

1. 数据库事务.
    1. 官方资料
        1. https://docs.djangoproject.com/en/2.0/topics/db/transactions/
    2. 具体的操作.
        1. 有一个函数叫 atomic
        2. 导入这个函数 from django.db import transaction
        3. 用 @transaction.atomic装饰需要使用事务的函数.
    3. 但是,一个处理view函数里面,应该是分有多个函数的,所以,看情况使用事物.
        1. ## 可以设置保存点.但是,顶端的函数必须有atomic装饰.
            1. 调用 django.db.transaction里面的savepoint方法.
        2. 提交保存点
            1. savepoint_commit(sid)
        3. 如果要回滚就
            1. savepoint_rollback(sid)
        4. 然后通常需要调用回滚的时候,通常是在Exception里面的.!
        5. 