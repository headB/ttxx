#### 首页页面的静态化
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

#### 商品详细信息的获取和显示

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
    