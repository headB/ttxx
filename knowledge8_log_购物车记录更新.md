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