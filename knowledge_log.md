# 创建项目

1. 使用django-admin创建
2. 然后,进入到目录里面,使用python mange.py startapp app1
3. 里面涉及到一些技巧
    1. 比如说,你如果是创建多个app的话,可以是把这些app全部集中到一个python包里面,这样管理起来比较方便,不过,在settings.py文件里面注册app的时候,需要把包路径填好,例如,创建一个包,叫apps,在INSTALLED_APPS里面填入'apps/app1'
    2. 如果上面只想直接填入'app1'这样的话,可以在在settings里面添加代码,把包apps添加到python的搜索路径当中,就可以了.
        1. 疑问:搜索路径,究竟,是path,但问题是属于sys还是os的呢?
            1. 一般来说,sys应该是系统相关的,os就是操作系统相关的??好像名词都是一样的啊!?关键就是看看谁更加接近底层了?
                1. os模块负责程序与操作系统的交互，提供了访问操作系统底层的接口;sys模块提供了一系列有关Python运行环境的变量和函数，更多的是环境信息
                恩恩,好的,明白了.
                2. 所以呢,如果涉及到python的环境问题的话,应该是使用sys了,这个是关于python的环境变量的.
        2. 正确添加路径应该是sys.path追加.!sys.path.path..但是,天天新鲜里面居然是sys.path.insert,我看看是不是有这属性先.
            1. 原来,list的方法有insert和append两种属性,一个是前面添加,一个是后面添加.!其实,内置的属性都是比较通用的.
            2. 不小心又学到新东西了.就是关于单个import和from xx import xx
            的区别,这次算是弄得相对很明白了.!
4. 然后使用命令python manage.py startapp user,goods,cart,order
5. 相应的,在settings.py里面也添加相应的代码.在INSTALLED_APPS添加.
6. 同时,可以在settings.py文件里面,填写templates的DIRS位置了.
7. 同时把static文件夹写上也是可以的.
8. 然后配置填写在项目目录里面的urls的文件.加入路径可以访问到上面创建的4个apps.
9. 在所有的app里面分别设置好URL的namespace，命名空间。！
10. 创建db包，然后写一个BaseModel模块
    1. 定义好了以后，再定义一下元类，添加说明为"抽象基本类"
11. 然后分别去定义user，order等4个app下面的model
    1. 记得每一个模型类，都得定义一下db_table
    2. 然后定义在Meta下面的verbose_name_plural = verbose_name感觉作用是数据库显示。
    3. 注意了，django高版本之后，设置外键约束的时候，注意需要添加当on_delete的情况。详细可以参考mysql的外键约束。on_delete=models.CASCADE
12. 安装第三方插件，富文本编辑器
    1. pip install django-tinymce==2.6.0
    2. 安装好插件之后，在settings里面加入。在具体的INSTALLED_APPS加入tinymce.

13. 然后现在迁移之前，需要在settings里面设置一个变量，AUTH_USER_MDEL = 'user.User',django认证系统使用的模型类。
    1. 有什么作用。
        1. 让django不在生成auth_user表。

14. 框架基本上已经搭建完成了。！
15. 处理比较棘手的数据库创建和迁移问题!.
    1. 可以了,完美解决好了,情况是这样的,如果一旦破坏了单独每个app下面的migrations文件夹以及里面的__init__.py文件的话,
    就是导致生成迁移文件的时候,无法识别到app所在的所有新操作.
    2. 解决方法很简单,直接手动生成上面说的文件夹和文件就可以了.
    3. 或者使用命令python manage.py makemigations appxxxx,这样就可以单独修复app了,然后每个都是这样修复,
    4. 然后到了最后,使用python mange.py migrate一次性迁移就可以了.!!
