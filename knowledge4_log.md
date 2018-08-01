# 分布式图片服务器FastDFS

1. #### 什么是FastDFS

FastDFS 是用 c 语言编写的一款开源的分布式文件系统。FastDFS 为互联网量身定制， 充分考虑了冗余备份、负载均衡、线性扩容等机制，并注重高可用、高性能等指标，使用 FastDFS 很容易搭建一套高性能的文件服务器集群提供文件上传、下载等服务。 
FastDFS 架构包括 Tracker server 和 Storage server。客户端请求 Tracker server 进行文 件上传、下载，通过 Tracker server 调度最终由 Storage server 完成文件上传和下载。
Tracker server 作用是负载均衡和调度，通过 Tracker server 在文件上传时可以根据一些 策略找到 Storage server 提供文件上传服务。可以将 tracker 称为追踪服务器或调度服务 器。
Storage server 作用是文件存储，客户端上传的文件最终存储在 Storage 服务器上， Storageserver 没有实现自己的文件系统而是利用操作系统 的文件系统来管理文件。可以将 storage 称为存储服务器。

    - 原来,这个是一个淘宝的程序工程师开源的.!

#### 特点

1. 海量存储,存储容量扩展方便.
2. 文件内容重复.

服务端两个角色:
Tracker:管理集群，tracker 也可以实现集群。每个 tracker 节点地位平等。收集 Storage 集群的状态。 
Storage:实际保存文件 Storage 分为多个组，每个组之间保存的文件是不同的。每 个组内部可以有多个成员，组成员内部保存的内容是一样的，组成员的地位是一致的，没有 主从的概念。
2. 文件上传流程

客户端上传文件后存储服务器将文件 ID 返回给客户端，此文件 ID 用于以后访问该文 件的索引信息。文件索引信息包括:组名，虚拟磁盘路径，数据两级目录，文件名。 

组名:文件上传后所在的 storage 组名称，在文件上传成功后有 storage 服务器返回， 需要客户端自行保存。 
虚拟磁盘路径:storage 配置的虚拟路径，与磁盘选项 store_path*对应。如果配置了 store_path0 则是 M00，如果配置了 store_path1 则是 M01，以此类推。 
数据两级目录:storage 服务器在每个虚拟磁盘路径下创建的两级目录，用于存储数据 文件。 
文件名:与文件上传时不同。是由存储服务器根据特定信息生成，文件名包含:源存储 服务器 IP 地址、文件创建时间戳、文件大小、随机数和文件拓展名等信息。 
3. 文件下载流程

#### 这个是github上面的安装方法.!

https://github.com/happyfish100/fastdfs/wiki


4. #### 简易FastDFS架构
    - Linux系统下，FastDFS安装配置
        发布时间：2018-01-19
        https://www.aliyun.com/jiaocheng/124867.html?spm=5176.100033.2.14.pKaSO8

5. #### FastDFS安装
    - 安装fastdfs依赖包
    1. 解压缩libfastcommon-master.zip
    2. 进入到libfastcommon-master的目录中
    3. 执行 ./make.sh
    4. 执行 sudo ./make.sh install
    - 另外一种安装方法
        1. 下载安装libfastcommon
        git clone https://github.com/happyfish100/libfastcommon.git
        cd libfastcommon/
        ./make.sh
        ./make.sh install
    - 下载安装fastdfs
        wget https://github.com/happyfish100/fastdfs/archive/V5.05.tar.gz
        tar -zxvf V5.05.tar.gzcd V5.05
        ./make.sh
        ./make.sh install
        执行安装后,默认会安装到/usr/bin中,并在/etc/fdfs中添加三个配置文件

    - 修改配置文件

    将/etc/fdfs中三个文件的名字去掉sample.
    1. tracker.conf 中修改:base_path=/usr/lgip_fastdfs/fastdfs-tracker-log #用于存放日志
    2. storage.conf 中修改:base_path=/usr/lgip_fastdfs/fastdfs-storage-log #用于存放日志
        store_path0=/usr/lgip_fastdfs/fastdfs-file-save #存放数据
        tracker_server=192.168.20.35:22122 #指定tracker服务器地址
    3. client.conf 中同样要修改:base_path=/usr/lgip_fastdfs/fastdfs-client-log #用于存放日志。
        tracker_server=192.168.20.35:22122 #指定tracker服务器地址
        注:以上的base_path、store_path0的路径均需要进行手动创建。
    - 启动tracker和storage
    ```python
        1. /usr/bin/fdfs_trackerd /etc/fdfs/tracker.conf 
        2. /usr/bin/fdfs_storaged /etc/fdfs/storage.conf 

    - 重启tracker和storage
        1. /usr/bin/fdfs_trackerd /etc/fdfs/tracker.conf restart
        2. /usr/bin/fdfs_storaged /etc/fdfs/storage.conf restart

    - 停止tracker和storage
        1. /usr/bin/fdfs_trackerd /etc/fdfs/tracker.conf stop
        2. /usr/bin/fdfs_storaged /etc/fdfs/storage.conf stop

    ```
    - 启动成功,测试服务是否正常运行
    ```python
        1. 上传:/usr/bin/fdfs_upload_file /etc/fdfs/client.conf /usr/01.jpg
        2. 下载:/usr/bin/fdfs_download_file /etc/fdfs/client.conf group1/M00/00/00/eSosZVfrMy2ADEcxAADS9IecoKQ527.jpg /usr/02.jpg
        3. 删除:/usr/bin/fdfs_delete_file /etc/fdfs/client.conf group1/M00/00/00/eSosZVfrLr6AfbmDAADS9IecoKQ093.jpg
    ```
    - 5.2 安装fastdfs
    1. 解压缩fastdfs-master.zip
    2. 进入到 fastdfs-master目录中
    3. 执行 ./make.sh
    4. 执行 sudo ./make.sh install

    - 5.3 配置跟踪服务器tracker
    ```python
    1. sudo cp /etc/fdfs/tracker.conf.sample /etc/fdfs/tracker.conf
    2. 在/home/python/目录中创建目录 fastdfs/tracker      
    mkdir –p /home/python/fastdfs/tracker
    3. 编辑/etc/fdfs/tracker.conf配置文件    sudo vim /etc/fdfs/tracker.conf
    修改 base_path=/home/python/fastdfs/tracker
    ```

    - 5.4 配置存储服务器storage
    ```python
    1. sudo cp /etc/fdfs/storage.conf.sample /etc/fdfs/storage.conf
    2. 在/home/python/fastdfs/ 目录中创建目录 storage
        mkdir –p /home/python/fastdfs/storage
    3. 编辑/etc/fdfs/storage.conf配置文件  sudo vim /etc/fdfs/storage.conf
    修改内容：
    ```python
    base_path=/home/python/fastdfs/storage
    store_path0=/home/python/fastdfs/storage
    tracker_server=自己ubuntu虚拟机的ip地址:22122
    ```

    - 5.5 启动tracker 和 storage
    ```python
    sudo service fdfs_trackerd start
    sudo service fdfs_storaged start
    ```

    - 5.6 测试是否安装成功
    ```python
    1. sudo cp /etc/fdfs/client.conf.sample /etc/fdfs/client.conf
    2. 编辑/etc/fdfs/client.conf配置文件  sudo vim /etc/fdfs/client.conf
    修改内容：
    base_path=/home/python/fastdfs/tracker
    tracker_server=自己ubuntu虚拟机的ip地址:22122
    3. 上传文件测试：
    fdfs_upload_file /etc/fdfs/client.conf 要上传的图片文件 
    如果返回类似group1/M00/00/00/rBIK6VcaP0aARXXvAAHrUgHEviQ394.jpg的文件id则说明文件上传成功
    ```

#### 配置nginx以及模块

- 5.7 安装nginx及fastdfs-nginx-module web服务器 epoll
    1. 解压缩 nginx-1.8.1.tar.gz
    2. 解压缩 fastdfs-nginx-module-master.zip
    3. 进入nginx-1.8.1目录中
    4. 执行
        ```python
        sudo ./configure --prefix=/usr/local/nginx/ --add-module=fastdfs-nginx-module-master解压后的目录的绝对路径/src

        ##这个地方注意了,要到MakeFile里面找到--Werror,把这个去除.!
        sudo ./make
        sudo ./make install
        ```
    5. sudo cp fastdfs-nginx-module-master解压后的目录中src下的mod_fastdfs.conf  /etc/fdfs/mod_fastdfs.conf
    6. sudo vim /etc/fdfs/mod_fastdfs.conf
    修改内容：
    connect_timeout=10
    tracker_server=自己ubuntu虚拟机的ip地址:22122
    url_have_group_name=true
    store_path0=/home/python/fastdfs/storage
    7. sudo cp 解压缩的fastdfs-master目录conf目录中的http.conf  /etc/fdfs/http.conf
    8. sudo cp 解压缩的fastdfs-master目录conf目录中的mime.types /etc/fdfs/mime.types
    9. sudo vim /usr/local/nginx/conf/nginx.conf
    在http部分中添加配置信息如下：
    ```python
        server {
                    listen       8888;
                    server_name  localhost;
                    location ~/group[0-9]/ {
                        ngx_fastdfs_module;
                    }
                    error_page   500 502 503 504  /50x.html;
                    location = /50x.html {
                    root   html;
                    }
                }
        ```
    10. 启动nginx
    sudo /usr/local/nginx/sbin/nginx
    ```python
        - 使用python客户端上传测试
        1. workon django_py3
        2. 进入fdfs_client-py-master.zip所在目录
        3. pip install fdfs_client-py-master.zip
    ```
    ```python
    >>> from fdfs_client.client import Fdfs_client
    >>> client = Fdfs_client('/etc/fdfs/client.conf')
    >>> ret = client.upload_by_filename('test')
    >>> ret
    {'Group name':'group1','Status':'Upload successed.', 'Remote file_id':'group1/M00/00/00/
        wKjzh0_xaR63RExnAAAaDqbNk5E1398.py','Uploaded size':'6.0KB','Local file name':'test'
        , 'Storage IP':'192.168.243.133'}
    ```
    文档 https://github.com/jefforeilly/fdfs_client-py

#### 小总结

1. 先下载nginx,版本可以可以随意
2. 然后下载插件nginx_fastdfs_module
3. 然后configure,修改忽略错误,然后make && make install
4. 然后配置好文件.
5. 然后client可以在其他的任意地方去连接.

#### 就是去继承

1. 在django里面写Storage的自雷,然后覆写方法.
2. django里面的settings定义好各种全局变量.!
3. 然后就差不多了.dfs