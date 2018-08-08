# 商品详细页js代码.!
1. 添加代码,去找到价格的位置,去获取价格的数目.
    > $('.show_pirze').children('em').text()
    ```python
    #注意.
    $('.total em').text(amount.toFixed(2)+"元")
    #相等于
    $('.total').children('em').text(amount.toFixed(2)+"元")
    ```
    1. parseInt方法是将字符串转换成为整型.
    2. parseFloat方法是转换成为浮点型.
2. 重新补充一下jquery文件.
    1. 自己去恶补了一下关于jquery的知识了,还是不是很全面啊,知识点.
3. 添加商品到购物车
    1. 请求方式,才用ajax.,post或者是get
    2. 传递参数
        1. 商品id
        2. 商品数量

4. 去cart定义view,准备设置get和post接收参数的操作.!
    1. 具体流程可以查看cart里面的view内容.
    2. 不过,我觉得有一个地方是比较有意思的,就是,要获取redis内容,还是挺方便的,直接导入 from django_redis import get_redis_connection
5. 然后在detail就是使用js计算好数量,然后通过点击触发事件,post数据到指定页面,并且返回购物车的数量.!
6. 添加购物车原理,是使用js,获取add_cart和show_cart两个元素的左上角坐标,
7. 为什么detail不做mixin认证.
    1. 不容易跳转


# 设置购物车显示页面
1. 复制cart.html到templates下面的页面.
    1. 然后修改一下需要继承的部分内容
2. 然后去view定义新的view方法
    1. 然后,由于这里不涉及ajax,所以可以继承mixin认证.!
    2. ## 用到了redis的统计,hgetall
