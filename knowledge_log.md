# 创建项目

1. 使用django-admin创建
2. 然后,进入到目录里面,使用python mange.py startapp app1
3. 里面涉及到一些技巧
    1. 比如说,你如果是创建多个app的话,可以是把这些app全部集中到一个python包里面,这样管理起来比较方便,不过,在settings.py文件里面注册app的时候,需要把包路径填好,例如,创建一个包,叫apps,在INSTALLED_APPS里面填入'apps/app1'
    2. 如果上面只想直接填入'app1'这样的话,可以在在settings里面添加代码,把包apps添加到python的搜索路径当中,就可以了.
        1. 疑问:搜索路径,究竟,是path,但问题是属于sys还是os的呢?