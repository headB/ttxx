# 用户中心
1. 抽离父模板,就是将重复的代码抽离出来.
2. 在模板里面,定义可覆盖的内容,标签是成对存在的,{%block xx%}{%endblock xx%}
3. 然后各种继承
4. 然后某些部分,例如点击当前某一个模块,就显示激活状态.!
5. 使用login_required from django.contrib.auth.decorators import login_required
6. 上面的验证,应用的是装饰器的功能,想想装饰器是什么
    1. 装饰器就是,先调用自己,然后里面包括了目标函数,然后添加自己的函数运行,可以在目标函数之前,或者之后.
    2. 所以就是应该在之前运行,检查.!
7. 使用login_reqired,可以利用django自带的机制让没有登陆的用户,强制需要登陆后才可以继续有权限执行当前的操作.!
    1. 在settings里面设置就可以了.!设置变量, LOGIN_URL='/user/login'
    2. 注意了,里面会有一个地址跳转,格式是这样的.http://localhost:8000/user/login/?next=/user/user_info/
    3. 在用户校验过程中,可以手动获取url地址中的参数,next参数,然后里面可以request.GET.get('next',reverse('goods:index')),
    这样子的写法,大概是要说明,假如没有成功获取到next参数的话,就跳转首页.
8. 因为set_cookie的问题引发了一波对request,response的问题头脑风暴,现在解决好了.多多百度或者谷歌其实都是可以的.!
9. 恶补了类方法的知识点了
    1. 其实,使用装饰器,真的是对这个函数进行装饰,例如一下
    ```python
    @decorate_x
    def test_func(cls,**kwargs)
    #其实就是相当于
    test_func = decorate_x(test_func)
    ```
10. 除了你给模板文件传递的模板之外,django框架会把request.user也传给模板文件,也就是,可以直接在模板里面使用user.
    - 如果是还没有登录的话,django框架会传递一个anonymousUser.
11. 模型管理器类方法封装.!
    1. 自定义一个模型管理器对象
