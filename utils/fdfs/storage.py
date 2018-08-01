from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.conf import settings

#尝试改写django的存储类
#其实,我自己想基本的存储类的模式是什么都不知道.哈哈哈.
class FDFSStorage(Storage):

    '''fast dfs文件存储类'''

    def __init__(self,client_conf=None,base_url=None):
        '''初始化'''
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF

        self.client_conf = client_conf

        if base_url is None:
            base_url = settings.FDFS_URL
            self.base_url = base_url

    def _open(self,name,model='rb'):
        pass
    
    def _save(self,name,content):
        '''保存文件内容'''
        #content包含你上传到fdfs
        #name上传时候的名字
        #创建一个file类型对象
        client = Fdfs_client(self.client_conf)
        #上传到fdfs系统中
        res = client.upload_by_buffer(content.read())

        if res.get('Status') != 'Upload successed.':
            raise Exception("上传文件到fast dfs失败!")

        #获取返回的文件ID
        filename = res.get('Remote file_id')

        return filename

    def exists(self,name):
        '''判断文件是否可用'''
        return False
        #代表文件可用!

    def url(self,name):
        '''django返回访问文件的路径'''
        return self.base_url+name





        