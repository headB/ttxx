# 购物车页面js全选_全不选

1. 首先利用jquery找到checkbox元素.
    1. 可以使用这个
        ```python
            $('.settlements').find(':checkbox').change(function(){
              //获取全选的checkbox的全选状态
                 is_checked = $(this).prop('checked')
                 ....更多代码看cart.html
            })
        ```
2. 总结了一下要点.
    1. 当如果是选择器的时候,:input 表达的是,选择所有元素type=input的元素,:text表达的是所有type='text'的input元素.
    2. ## 然后这里比较特殊的是,:disabled,:selected,:checked,:enabled表达的是,所有被选中的input元素.

# 购物车记录更新_后台
1. 都是与后台发生交互.!才用ajax请求.!
    1. 去view写对应的请求.post请求
    2. ## 在django里面涉及的问题就是,需要提交csrf_token.
    3. 小心,写$.post的时候,要考虑同步和异步的问题!.
    4. ## 默认的ajax都是异步执行的.!
    5. ## 可以设置ajax为同步执行.
        ```python
            $.ajaxSettings.async = false
        ```
    6. ## 设置为全局的异步设置,所以一旦完成了同步之后,一定要把ajax设置回来,设置未True就可以了.!
     ```python
            $.ajaxSettings.async = true
        ```
2. 然后,可以利用json返回的信息其实获取获取到参数的!.
3. ## 应用的知识点:
    1. 利用focus可以提前获取值,用于如果设置无效值的时候可以返回上次的值.
    2. 利用blur可以设置失去焦点之后,可以动态设置值.!
4. ## 稍微描述一下,添加,减少,手动输入数量的过程.
    - 全局范围来讲.
        1. 首先远程获取商品合法性让后反馈结果,失败了,下面的都不用操作了.
        2. 当前行的数量更新和小计更新.
        3. 更新全部商品数量.
        4. 更新所有激活状态的checkbox的总数量和总价格.
    1. 首先是,监听到增加/减少/获取失焦时候的数值
    2. 检验数值的合法性.
    3. 然后尝试远程提交请求,看反馈结果,成功的话,继续下一步,否则return
    4. 然后利用js更新当前行的数量和小计,还有更新当前商品的小计,在返回信息哪里获取实时的商品数量.
    5. 然后在调用一下更新全局的被选中的checkbox的数量和价格.
5. # 购物车记录删除
    1. 才用ajax_post请求
    2. 前端需要传递参数:商品的id
    3. 判断用户是否有登陆
    4. 接收参数.
    5. 参数判断.
    6. 远程查询,查看商品的有效性.
    7. ## 然后使用redis的hdel(cart_key,sku_id)
    8. 返回当前用户的所有商品数量.
    9. 设置对应的url地址,导入这个类.!
6. 然后修改前端.
    1. 找到删除按钮的对应样式选择器.
    2. 绑定点击事件.
    3. 先获取需要删除的商品的sku_id号码.
    4. 因为是post请求,所以,需要添加csrf.
    5. 然后发起post请求,
    6. 然后返回信息,看看是否成功远程删除.
    7. 确认好,就利用js删除当前整条的sku_id的ul元素.(如果获取跨函数获取当前对象,其实知需要定义一个全局变量,然后赋值一下就可以了.)
        1. xx.empty()是删除本身的子元素,但是保留自己
        2. xx.remove()是删除本身的所有元素.
    8. 然后更新左上角的商品id,可以更新返回的实时商品数量来更新数据.
    9. 然后调用函数更新全局选中的checkbox的信息.
    10. ## 善于利用parents,去寻找所有的上级目录.恩恩,前端挺好玩的.!

