from fdfs_client.client import Fdfs_client

client = Fdfs_client("/etc/fdfs/client.conf")
ret = client.upload_by_filename('/home/beetle/project/ttxx/knowledge4_log.md')
print(ret)

