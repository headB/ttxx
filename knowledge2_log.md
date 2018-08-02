# 用户注册模块

1. 在user的view开始写方法。register方法，去渲染注册页面。
2. 然后在user下面的urls添加对register的路由支持。
3. 然后去templates里面的register，修改静态文件的读取方式。
    1. 在模板上面添加 {%load staticfiles%}
    2. 然后载入静态资源的写法是 {% static 'css/xxx.css' %}  
4. 修改/templates/register.html里面的form提交地址.
5. 在form表单下面添加{%csrf_token%}防护.
6. 今天了解和很多关于django2.0的知识点.
    - ## 命名空间有两种
        1. 实例命名空间
        2. 应用命名空间(最先搜索的,优先的)
7. 对应上面的,方向域名解释的问题,分两种
    1. 如果是在视图里面的,优先是从实例命名空间搜索,然后才到应用命名空间.
    2. 如果是在模板里面的话,就是优先当前的作用域.具体可以看这个.
    https://www.jianshu.com/p/404500a0408a
8. 还有了解到了,如果有 all 函数这个东东的存在.
9. 差点就搞错了auto_now_add和auto_now这两个字段工具.
10. 顺便了解到了,原来select * from xx \G的用法.和show slave这个超级相似.!有点像格式化输出一样.!
11. ## 类视图
    - 什么是类视图?
        1. Django 提供基本的视图类，它们适用于绝大多数的应用。所有的视图类继承自View 类，它负责将视图连接到URL、HTTP 方法调度和其它简单的功能。RedirectView 用于简单的HTTP 重定向，TemplateView 扩展基类来渲染模板。
        参考网址:https://blog.csdn.net/list_lee/article/details/51220096
    - 用法
        1. from django.views.generic import View
        2. 然后定义一个类继承与上面就可以了.

    - 总结
        1. 自己感觉就是,强制需要你去定制get,和post方法.
        2. 自己稍微去理解一下关于视图类的as_view的流程.
12. ## 发送邮件验证用户注册信息
    - 使用itsdangerous,生动定时的token,可以在指定的时间解密.
13. 重新认识了新式的path的使用方法.!
    - path('xxx/<str:token>'),然后在view方便,重新写一个参数接收,写一样,def (request,token)
14. 然后,get或者post的判断流程里面,使用except挺好的,简便.例如这个.
    ```python
    try:
        user_info = token.loads(token)
        user_id = user_info['confirm']
        user = User.obejects.get(id=user_id)
        user.is_active = True
        user.save()

        #然后跳转登录页面
        return render(request,'login.html')

    except SignatureExpired as e:
        #激活码已经过期
        return HttpResponse("激活码已经过期!")
    ```
15. 记得发送邮件内容的时候附送<a>标签.还有记得是
16. 但是突然感觉到自己其实对try异常处理还是不是很熟悉.现在去恶补一下知识先.
17. 对应上面的问题终于解决了,因为我没有导入这个错误的异常的类,导入就正常了. from itsdangerous import SignatureExpired
18. 继续下一步,现在去看看异步发送邮件!.
    - 需要注意的地方就是
        1. 任务发出者(django项目代码)
        2. 任务中间人(可以是redis或者rabbitMQ)
        3. 任务处理者(处理者也需要任务的代码!),还有一个问题就是,严重依赖django的settings配置.不过,应该能单独配置吧?
    - 使用步骤
        1. 首先是在django里面单独新建一个包,然后新建task.py,,,,,from celery import Celery
        2. 然后定义app = Celery('xxxxxxx)
        3. 然后定义任务函数,例如是register_send_email
        4. 然后用装饰器@app.task装饰上面的函数.
        5. 然后项目代码调用这边函数 记得是 xxx.delay(xxxx)
19. 晕.django2和1还是有区别的...账号认证authenxxx还是不一样,is_active的作用不一样!.
20. ## celery高度依赖redis