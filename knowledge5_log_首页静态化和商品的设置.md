# 首页页面的静态化
1. celery(多进程?)
2. 什么时候首页需要重新生成?
    1. 当管理员后台修改首页信息对应的表格中的数据的时候,需要重新生成首页的静态页.
3. 获取信息
    1. 获取商品的种类信息
    2. 获取首页的促销活动信息
    3. 获取首页分类商品的展示信息
        1. 获取type种类首页分类商品的图片展示信息
        2. 获取type种类首页分类商品的文字展示信息
        3. 动态给type增加属性,分别保存首页分类商品的图片展示信息和文字展示信息
    4. 获取用户购物车中商品的数目(仅限首页的话,不需要这一部分!)
    5. 代码步骤(使用模板)
        - Django RequestContext用法
        1. 加载模板文件,返回模板对象
            ```python
            temp = load.get_template()
            ```
        2. 定义模板上下文
            ```python
            context = RequestContext(request,context)
            ```
        3. 模板渲染
            ```python
            static_index_html = temp.render(context)
            ```
        4. 定义save方法保存静态页面代码.
    6. 使用app.task装饰.
    7. 然后启动celery客户端,调用函数,然后生成静态html文件.
4. 通过浏览器管理员修改首页数据表中的数据,
    1. 通过点击修改,django就让celery重新生成静态页面.
    2. 使用django的Admin类.!ModelAdmin有特殊方法.
    3. 直接在goods的文件夹里面的admin写类.
        ```python
        class IndexPromotionxx(admin.ModelAdmin)
        #然后记得调用父类的方法.!
        ```
    4. 上面重复的代码过多了,然后现在需要把代码抽成一个父类>!

5. 首页页面的静态化(关于django的缓存!)
    1. 页面数据的缓存
        >把页面使用的数据放到缓存中,当再次使用这些数据时,先从缓存中获取,如果获取不到,再去查询数据库.减少数据库查询的次数.!

    2. 设置缓存,导入函数, from django.core.cache import cache,详情请看view.
        1. cache有set和get方法,具体方法看介绍
    3. 如何清除缓存数据
        1. cache里面有delete方法.

6. 什么时候需要更新首页的缓存数据.
    1. 当管理员后台修改首页信息对应的表格中的数据的时候,需要更新首页的缓存数据.

7. 缓存小总结
    1. 网站本身性能的优化,减少数据库的查询的次数.
    一定程度可以防止而已的攻击.
    2. 页面的静态化.

# 商品详细信息的获取和显示

- 英文解释
    1. SPU = Standard Product Unit (标准产品单位)
    2. SKU = stock keeping unit(库存量单位)

1. 为了排除可以被静态化干扰,先设置最小的缓存时间,或者直接取消缓存.
2. 然后分别去查询商品详情,还有评论,反正就是信息获取.!detail啊~
    1. 商品种类 goodsType.objects.all()
    2. 商品评论信息 OrderGoods.objects.all()
        ```python
        #注意这个位置,使用了exclude,就是排除这个选项的其他所有选项.
        sku_orders = OrderGoods.objects.filter(sku=sku).exclude(comment='')
        ```
    3. 新品信息 GoodsSKU.objects.filter
        ```python
        #注意这个位置,符号-表示是降序,就是DESC的选项.切片的话,就是限定结果,limit
        new_skus = GoodsSKU.objects.filter(type=sku.type).order_by('-create_time')[:2]
        ```
    4. 获取其他SPU,商品的其他规则 GoodsSKUll.objects.filter
    5. 获取用户购物车商品的数量
        1. 判断用户是否登录
            1. 用户历史记录
            2. xxxx
    6. 在模板里面开始写模板变量,有一个地方值得注意,就是,例如,GoodsSKU里面的images字段是一个特殊的字段,里面包含有url地址,SKU.images.url,
        1. 在model的写法是这样的,借助了外键.!
            ```python
            class GoodsSKU(BaseModel):
                    goods = models.ForeignKey('Goods', verbose_name='商品SPU',on_delete=models.CASCADE)
                    image = models.ImageField(upload_to='goods', verbose_name='商品图片')

            ```
            #自己感觉呢,就是,这里有一个外键关联,一对多的!.
    7. 关于富文本编辑,一般的模板变量传递,都会自动转义的,所以你要关闭注意,具体用法是:
        ```python
        {%autoescape on%}
        {% endautoescape %}
        #或者,直接使用safe
        {{ var|safe }} #取消转义
        ```
    8. 商品详情,是富文本,可以要转义,然后是评论时间也需要转义
    9. 如果获得评论时间,也就是最后一次评论.直接获取updatetime.
    10. 获取评论用户,然后就是多层的外键递归.order.order.user.usnername

# 用户历史记录添加

1. 首先,在首页的时候,每一个轮播的图片,现在在里面的url里面后面需要添加参数,才可以跳转到详细的商品信息页面.
    ```python
    {% url 'goods:detail' banner.sku.id  %}
    ```

2. 直接在Goods里面的view里面的detailView的用户判断之后,添加用户浏览记录,应该说,详细信息调用,就马上把浏览记录记录到数据中.意思是这样的,就是,如果浏览这个详情页的时候,这个用户没有登录,就不同记录了,其他都是相反的情况.!
    1. 用户添加浏览记录的时候,默认必须从左侧插入.
    2. 插入之前,先检查是否已经在旧的列表存在,存在的话,就先去除,然后再插入到最新.
    3. 需要使用到函数,这个函数的特点就是,如果元素存在就删除,否则就不用删除了.里面参数的0,代表移除所有
        ```python
        if user.is_authenticated():
                # 用户已登录
                conn = get_redis_connection('default')
                cart_key = 'cart_%d' % user.id
                cart_count = conn.hlen(cart_key)

                # 添加用户的历史记录
                conn = get_redis_connection('default')
                history_key = 'history_%d'%user.id
                # 移除列表中的goods_id
                conn.lrem(history_key, 0, goods_id)
                # 把goods_id插入到列表的左侧
                conn.lpush(history_key, goods_id)
                # 只保存用户最新浏览的5条信息
                conn.ltrim(history_key, 0, 4)

                #r.lrem(name,value,num) 参数对应： name: redis的name
                #value: 要删除的值
                #num: num=0 删除列表中所有的指定值；
                #num=2 从前到后，删除2个；
                #num=-2 从后向前，删除2个

        ```
    4. 还有一个方法,redis的,LTRIM,对数据进行裁剪.
        ```python
            LTRIM key start stop
            #只保留区间内的元素
        ```

# 获取商品详情页面的SPU

> 功能就类似浏览苹果手机,然后下面提供其他的颜色和型号
1. 注意,去除当前的goods_id的SPU商品.
    ```python
            same_spu_skus = GoodsSKU.objects.filter(goods=sku.goods).exclude(id=goods_id)

    ```

# 列表显示页面

1. 先到static找到list.html,然后复制到templates下面,然后修改.
    1. 将list.html整合一下变成通用模板.
2. 然后,在view,定义listView,
    1. 需要传递商品种类.
    2. 需要传递页码,第几页
    3. 然后就是,排序问题.排序的方式.
    4. url的设计. /list/种类
        1. 一般有多种,例如说这个,list?xx=xxx&xx=zz之类,但是django一般用list/xx/yy/dd这个更加方便.
        2. 还有一种就是关于restFUL API,居然django这种是符合RESTFUL风格.!
3. ListView的实现过程.
    1. 首先查询这个种类id是否存在.获取种类信息
    2. 然后查询商品分类信息.
    3. ### 注意这个地方,这个查询的条件之前见过一次,的确比较诡异的,都是一个查询集来的.里面有信息啊~.一般应该是get吧,
        只能是单个的结果吧?对,就是当个结果.!外键关键结果?我去看看model先.是的,看过了,就是整个goodtype当做是关联的对象,
        不仅仅是当个字段名.!
        ```python
        type = GoodsType.objects.get(id=type_id)
        skus = GoodsSKU.objects.filter(type=type).order_by('price')
        ##然后从mysql创建表的结果来看,其实,也仅仅是关联了id而已.
        `goods_id` int(11) NOT NULL,
        `type_id` int(11) NOT NULL,
        PRIMARY KEY (`id`),
        KEY `df_goods_sku_goods_id_31622280_fk_df_goods_id` (`goods_id`),
        KEY `df_goods_sku_type_id_576de3b4_fk_df_goods_type_id` (`type_id`),
        CONSTRAINT `df_goods_sku_goods_id_31622280_fk_df_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `df_goods` (`id`),
        CONSTRAINT `df_goods_sku_type_id_576de3b4_fk_df_goods_type_id` FOREIGN KEY (`type_id`) REFERENCES `df_goods_type` (`id`)
        ```
        >然后,如果查询结果如何获得结果呢,获取是这样的.In [8]: goods_info[0].type.logo,Out[8]: 'sedfood',意思是,外键的名字然后对应外键表名字.
        ```python
        mysql> select * from df_goods_sku\G
        *************************** 1. row ***************************
        create_time: 2018-08-04 04:18:45.318601
        update_time: 2018-08-04 04:18:45.318712
                id: 1
        is_delete: 0
            name: 特种草莓
            desc: 特种草莓
            price: 10.00
            unite: 盒
            image: group1/M00/00/00/rBEAAltlKSWACaLJAADhpU9_Ylo3513545
            stock: 100
            sales: 10
            status: 1
        goods_id: 1
            type_id: 2
        1 row in set (0.00 sec)
        ```
        关于外键,可以参考一下这里.
        Spanning multi-valued relationships
        https://docs.djangoproject.com/en/2.0/topics/db/queries/

        通过通过查询外键去获取值的几种方法.
        https://www.cnblogs.com/zhaopengcheng/p/5608328.html?utm_source=tuicool&utm_medium=referral

    4. 然后还有一个注意的地方,就是排序,使用的是xxx.order_by('+/-字段名字')好像默认只写字段名字的话,就是代表是升序了,就是+
    5. 外键比喻.
        ```python
            province->city->
            省---->城市
            一对多关系
            使用方法1: p.objects.get('xx')-->.citys_set.all()
            多对一:
            城市--->省:
            使用方法:p.objects.get('yy')-->.province.name/id/code.....
        ```
        1. 那么这里面pk和id有什么不同和相同之处呢？
            http://zhangfortune.iteye.com/blog/2124979
            但是有时候不一样？什么时候？是的，你猜到了，当model的主键不是id的时候，这种情况虽然少，但是django为我们想到了，我们来看一下
        2. Django objects.all()、objects.get()与objects.filter()之间的区别介绍
            1. filer若是查询不到数据，会返回一个空的查询集，[]  type类型是：Queryset。查询到多余一条的时候会返回一个包含多个对象的查询集。
                filter和get类似，但支持更强大的查询功能
            2. all返回的是QuerySet对象，程序并没有真的在数据库中执行SQL语句查询数据，但支持迭代，使用for循环可以获取数据。
            3. get返回的是Model对象，类型为列表，说明使用get方法会直接执行sql语句获取数据
        3. ```python
                #一种创建对象并将其全部保存在一个步骤中的便捷方法。从而：
                p = Person.objects.create(first_name="Bruce", last_name="Springsteen")
                #和：
                p = Person(first_name="Bruce", last_name="Springsteen")
                p.save(force_insert=True)
                是等价的。
            ```
        4. django官方文档
            - QuerySets很懒,意思是,这个行为,只进行一次数据库查询,使用filter多次查询都只是一次数据库查询.!
            - evaluated的意思是,[数学、逻辑学]求…的数值
        
    6. 多对多访问.(建立字段的时候是ManyToManyKey)
        b = Book.objects.get(id=50)
        b.authors.all()
    7. ## filter过滤外键对象
        对相关对象的查询¶
        涉及相关对象的查询遵循与涉及正常值字段的查询相同的规则。指定要匹配的查询的值时，可以使用对象实例本身或对象的主键值。

        举例来说，如果你有一个博客的对象b有id=5，以下三种查询是相同的：
        ```python
        Entry.objects.filter(blog=b) # Query using object instance
        Entry.objects.filter(blog=b.id) # Query using id from instance
        Entry.objects.filter(blog=5) # Query using id directly
        ```
    8. ## 直接打印对象的字段,就可以看到这个属性的所有值了.!
        1. 或者,使用filter查询完了以后调用values()方法,也是可以打印出结果的.!



# 分页的功能

1. 分页需要借助,from django.core.paginator import Paginator
    1. Paginator(查询集[反正可以遍历的东东],多少页)
2. 然后到新品信息.看看要怎么处理
    1. 没怎么处理,就是设置好detail就差不多了.稍后补充.
3. 分页.
    1. 遍历page对象,例如这个 for sku in skus_page.object_list,可以简写为for x in skus_page:
4. ### 注意了,变量名,{% xx %} 符号{和符号%是紧贴的!.注意了.
5. 判断好上一页,下一页,然后是当前页,也就差不多了.!
6. 新的需求是,只显示前两页和后两页,中间不见了.!

## 关于排序
1. 好像并还不是很熟悉,不过其实排序就是直接对xx.objects.all().order_by()或者是objects.filter().order_by()
    ```python
        In [2]: x1 = models.GoodsSKU.objects.all().order_by('id')
        In [3]: x1
        Out[3]: <QuerySet [<GoodsSKU: GoodsSKU object (1)>]>
    ```
