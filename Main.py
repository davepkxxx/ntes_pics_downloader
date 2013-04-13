__author__ = 'David'

from NetWorker import NetWorker

worker = NetWorker()
worker.parse(input('请输入图片所在的网址：'))
worker.download(input('请输入存放图片的文件夹路径：'))
print('下载完毕。')
