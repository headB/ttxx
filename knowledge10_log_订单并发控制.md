# 并发问题,其实所有的程序都应该考虑这个问题的

1. 向df_order_info添加一条记录
2. 查询sku_id = 17查询信息
3. 库存判断.
4. 向df_order_goods添加记录
5. 商品库存更新
6. 上面两个操作,可以有两个用户同时处理,所以,要考虑并非问题.

# 订单并发_悲观锁_乐观锁

1. 到了关键的语句,可以使用锁,然后另外一个进程,就得继续等待一下,论询.!
2. 加锁 select * from df_goods_sku where id=17 for update;
3. ## 实现的代码
    1. 代码
        ```python
            GoodsSKU.objects.select_for_update().get(id=sku_id)
            #上面的代码相当于
            select * from df_goods_sku where id=sku_id for update;
        ```
    2. 关于mysql的行锁
        1. mysql事务，select for update，及数据的一致性处理
        https://www.cnblogs.com/houweijian/p/5869243.html
        2. 说明
            ```python
                在SELECT 的读取锁定主要分为两种方式：
            　　SELECT ... LOCK IN SHARE MODE　
            　　SELECT ... FOR UPDATE
            　　这两种方式在事务(Transaction) 进行当中SELECT 到同一个数据表时，都必须等待其它事务数据被提交(Commit)后才会执行。
            　　而主要的不同在于LOCK IN SHARE MODE 在有一方事务要Update 同一个表单时很容易造成死锁。
            　　简单的说，如果SELECT 后面若要UPDATE 同一个表单，最好使用SELECT ... UPDATE。
            ```
        3. ## Mysql的用法
            > FOR UPDATE 仅适用于InnoDB，且必须在事务区块(BEGIN/COMMIT)中才能生效。
        4. ## 悲观锁概念
            1. 悲观锁：在读取数据时锁住那几行，其他对这几行的更新需要等到悲观锁结束时才能继续 。
            2. 乐观所：读取数据时不锁，更新时检查是否数据已经被更新过，如果是则取消当前更新，一般在悲观锁的等待时间过长而不能接受时我们才会选择乐观锁。
        5. ## 我lizhixuan对这个锁的测试.
            1. 详情可以参考有道云,8月11日的笔记,标题是:8.11--然后呢,查询是没有影响的.!!OK!设置不同的id就不会引起锁的问题了.!
        6. ## 乐观锁
            1. 在查询数据的时候不添加锁.
            2. 在更新时进行判断.
            3. 判断更新时候的库存和之前查出的库存是否一致.
        7. ## 乐观锁的实现方法.
            1. 代码1
                ```python
                #mysql原始代码
                    update df_goods_sku set stock=0,sales=1 where id=17 and stock=1;
                ```
            2. 代码2
                ```python
                    origin_stock = sku.stock
                    new_stock = origin_stock - int(count)
                    new_sales = sku.sales - int(count)
                    #update df_goods_sku set stock=new_stock,sales=new_sales where id=sku_id and stock = origin_stock
                    #返回受影响的行数
                    res = GoodsSKU.objects.filter(id=sku_id,stock=origin_stock).update(stock=new_stock,sales=new_sales)
                ```
            3. ## 但是乐观锁的情况是,如果出现库存的数量不一样,就不会入库成功,所以,现在加入循环尝试一次.
                1. 然后一次成功的话,就直接使用break语句跳出循环尝试.!
            4. ## mysql的4种事务级别.
                1. 通过上面得知,其实,还是会继续出错的,为什么,就要说到隔离性的问题了.!
                2. ### Read Uncommitted(读取未提交内容) 
                    1. #### 什么是脏读.
                3. ### Read Committed(读取提交内容)
                4. Repeatable Read(mysql默认隔离)
                    1. 会出现幻读
                    2. 部分资料也是配合有道云查阅一下>!
                5. Serializable(可串行化)(最高级别的隔离)
            5. ## 所以需要更改mysql的事务级别,改成read committed
                1. 更改配置文件
                    1. 代码:
                        ```python
                            #添加
                            transaction-isolation = READ-COMMITTED
                        ```

#补充一种用于测试mysql事务的方法
1. 代码部分
```python

#于是我们在MySQL 就可以这样测试，代码如下:

SET AUTOCOMMIT=0; BEGIN WORK; SELECT quantity FROM products WHERE id=3 FOR UPDATE;
#此时products 数据中id=3 的数据被锁住(注3)，其它事务必须等待此次事务 提交后才能执行
#SELECT * FROM products WHERE id=3 FOR UPDATE 如此可以确保quantity 在别的事务读到的数字是正确的。
UPDATE products SET quantity = '1' WHERE id=3 ; COMMIT WORK;

```
2. 测试结果
    1. 首先是,图片结果,参考有道云,10月22日的记录,关于mysql测试的.
    2. 测试结果说明
        1. 前面设置了autocommit=0之后,然后,一旦某一个行数据被使用select XXX for update之后,
        这一行数据就被锁定只能读取了,不能更新了,也不能删除.看起来需要等锁.!
        2. 其他没有被指定特定锁定的行数据库,可以读取数据,但是呢,出现严重的问题了,
        就是,因为上面锁定的id,锁的那个人更新了数据,它自己可以读取最新的数据结构,但是呢,
        它并没有提交最终的commit,所以,其他都是读取旧的数据了,嗯嗯,其他的人都出现了幻读了.
        3. 但是其实还有一个问题,就是我现在这个问题了,我必须让他锁定的时候,不能读取.
        所以,准备有一种结果了.!读都锁定.!

    3. 所以感觉上面的,并不是最好的方案,我看看最终锁住数据,不能读取的情况.!


