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
    3. 然后使用命令python manage.py startapp user,goods,cart,order
    4. 相应的,在settings.py里面也添加相应的代码.在INSTALLED_APPS添加.
    5. 