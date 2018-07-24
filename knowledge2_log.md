# 用户注册模块
1. 在user的view开始写方法。register方法，去渲染注册页面。
2. 然后在user下面的urls添加对register的路由支持。
3. 然后去templates里面的register，修改静态文件的读取方式。
    1. 在模板上面添加 {%load staticfiles%}
    2. 然后载入静态资源的写法是 {% static 'css/xxx.css' %}  
4. 修改/templates/register.html里面的form提交地址.
5. 在form表单下面添加{%csrf_token%}防护.
6. 