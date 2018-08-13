# 部署_uwsgi作为服务器
1. 使用步骤
2. 修改settings文件
    1. DEBUG = False
    2. ALLOW_HOST = [*,]
3. 建立uwsgi.ini文件
    1. 代码:
        ```python
            [uwsgi]
            #使用nginx连接时使用
            socket=127.0.0.1:8080
            #直接做web服务器使用 python manage.py runserver ip:port
            #http=127.0.0.1:8080
            #项目目录
            chdir=/Users/smart/Desktop/dj/bj18/dailyfresh
            #项目中wsgi.py文件的目录，相对于项目目录
            wsgi-file=dailyfresh/wsgi.py
            #指定启动的工作进程数
            processes=4
            #指定工作进程中的线程数
            threads=2
            master=True
            #保存启动之后主进程的pid
            pidfile=uwsgi.pid
            #设置uwsgi后台运行，uwsgi.log保存日志信息
            daemonize=uwsgi.log
            #设置虚拟环境的路径
            virtualenv=/Users/smart/.virtualenvs/dailyfresh
        ```
4. 然后就是使用uwsgi命令启动服务器.!

# 部署_基本不是架构解析.

1. 截图参见2018年8月13日的有道云笔记.

# nginx和uwsgi对接.

1. 就是修改uwsgi的监听是使用socket
2. 然后,nginx修改一下参数配合uwsgi.

# nginx配置处理静态文件.!
1. 修改nginx的配置.!
2. 在django使用收集静态资料命令,详细可以参见django官方文档!
    1. 首先settings里面添加
        >STATIC_ROOT='/var/www/xxxx/'#设置收集路径.
    2. 然后使用命令python manage.py collectstatic

# nginx转交请求给其他地址

1. 注意就在于nginx的配置
    1. ## location / 和 location = /的区别
        1. 区别在于,第一个,其实感觉就好像是模糊匹配,如果,但是这两个同时存在的话,感觉它会优先匹配location = /,然后其他处理就转发到location
    2. / 通用匹配，任何请求都会匹配到。
    3. 多个location配置的情况下匹配顺序为（参考资料而来，还未实际验证，试试就知道了，不必拘泥，仅供参考）：
    4. 首先匹配 =，其次匹配^~, 其次是按文件中顺序的正则匹配，最后是交给 / 通用匹配。当有匹配成功时候，停止匹配，按当前匹配规则处理请求。

# nginx配置upstream实现负载均衡.
1. 代码
    ```python
        upstream ttxx {
            server 127.0.0.1:8080;
            server 127.0.0.1:8081;
        }

        location / {
            include uwsgi_params;
            uwsgi_pass ttxx;
        }

    ```
