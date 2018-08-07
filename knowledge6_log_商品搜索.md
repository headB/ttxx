# 商品搜索
1. 可能用到的是模糊搜索
    ```python
        select * from df_goods_sku where name like '%草莓%' or desc like '%草莓%';
    ```
2. 但是,试用like效率比较低,啊~,那怎么办呢?
    1. 搜索引擎一般的做法:
        1. 可以对表中的某些字段进行关键词分析,建立关键词对应的索引数据.

3. ## 全文检索框架:
    1. 可以帮助用户使用搜索引擎. 
        1. haystack:全文检索的框架,支持whoosh,solr,xapian,elasticsearc四种全文检索引擎.
        2. whoosh:纯python编写的全文搜索引擎,虽然性能比不上sphinx,xapian,elasticsearc等,但是冇二进制包,程序不会莫名其妙的奔溃,对于小型的站点,whoosh已经足够使用.
        3. jieba:一款免费的中文分词包,如果觉得补好用可以使用一些收费产品.
    2. ## 安装
        1. pip install django-haystack
        2. pip install whoosh
        3. pip install jieba
    3. ## 修改settings文件.安装haystack应用.
        1. 在INSTALLED_APPS注册一下!.
        2. 还需要加入配置选项,
            ```python
            HAYSTACK_CONNECTIONS = {
                'default':{

                    'ENGINE':'haystack.backends.whoosh_cn_backend.WhooshEngine',
                    #注意这个地方,因为,这个地方专门用来存放建立的索引文件的.!
                    #但是也不用自己去创建.!
                    'PATH':os.path.join(BASE_DIR,'whoosh_index'),
                }
            }
            ```
        3. 使用的时候,导入类,from haystack import indexes,然后在需要检索的模型类文件夹里面,新建search_indexes.py
        4. 然后写继承indexes.SearchIndex,indexes.Indexable.
        5. ## 定义两个方法
            1. ```python
                def get_model(self):
                    return #当前需要返回的当前类
                ```
            2. ```python
                def index_queryset(self,using=None):
                    return self.get_model().objects.all()
                ```
            3. use_template指定根据表中的那些字段建立索引文件.把说明放在一个文件中. 
            4. 索引类名的格式:模型类名+Index
            5. 然后templates新建search/indexes,然后在里面建立你需要检索模型类的名字的文件夹,这里就建立goods,
                1. 然后里面新建一个text文件,都是小写,例如是这个,goodssku_text.txt
        6. 在filedOption里面,如果document=True的话,就是表示建立索引的意思.
    
    4. 全文检索框架,需要搭配搜索引擎(whoosh)来使用.
    5. ## 创建索引文件生成.
        1. 按照上面的步骤创建好了之后,在项目里面运行.
            ```python
                python manage.py rebuild_index
            ```
            这个是过程
            ```python
                (python3) beetle@beetle-System-Product-Name:~/project/ttxx$ python manage.py rebuild_index
                WARNING: This will irreparably remove EVERYTHING from your search index in connection 'default'.
                Your choices after this are to restore from backups or rebuild via the `rebuild_index` command.Are you sure you wish to continue? [y/N] y
                Removing all documents from your index because you said so.
                All documents removed.
                Indexing 3 商品
            ```
        2. 然后就会建立好关联数据库里面所有的商品.!

# 全文检索

1. 在html或者templates文件里面设置表单,form,需要搜索目标的名字是q,具体我也不清楚为什么,表单的method方式是get,然后action是自己决定,这里暂时写action='search'
2. 然后在项目的url里面定义,
    ```
        path('search',include('haystack.urls'))
    ```
3. 模板变量会传递几个关键字变量
    1. query 搜索关键字
    2. page 当前页的page对象->遍历page对象,获取到的是searchResult类的实例对象,对象的属性object才是模型类的对象.
    3. paginator 分页paginator对象

4. 然后自己创建一个模板在search文件夹下面,然后里面的模板变量什么的依照上面的变量就可以了.!


