__author__ = 'David'

from urllib.request import urlopen, urlretrieve
import json
import xml.etree.ElementTree as etree

class NetWorker:

    def parse(self, url):
        self._crawlJSON(url)
        self._crawlXML(url)
        self._parse()

    def _crawlJSON(self, url):
        begin = '<textarea name="gallery-data" style="display:none;">'
        end = '</textarea>'
        start = False
        txt = ''
        for line in urlopen(url):
            line = line.decode('gbk')
            index = line.find(end)
            if (start and index > -1):
                start = False
                txt += line[:index]
            if (start):
                txt += line
            index = line.find(begin)
            if (index > -1):
                start = True
                txt += line[index + len(begin):]
        if (len(txt) > 0):
            self._jsonData = json.loads(txt)
        else:
            self._jsonData = None


    def _crawlXML(self, url):
        begin = '<textarea class="hidden" id="photoList">'
        end = '</textarea>'
        start = False
        txt = ''
        for line in urlopen(url):
            line = line.decode('gbk')
            index = line.find(end)
            if (start and index > -1):
                start = False
                txt += line[:index + len(end)]
            if (start):
                txt += line
            index = line.find(begin)
            if (index > -1):
                start = True
                txt += line[index:]
        if (len(txt) > 0):
            self._xmlData = etree.fromstring(txt)
        else:
            self._xmlData = None

    def _parse(self):
        self._data = []
        if (self._jsonData is not None):
            for one in self._jsonData['list']:
                self._data.append(one['oimg'])
        if (self._xmlData is not None):
            for li in self._xmlData:
                for elem in li:
                    attrs = elem.attrib
                    if ('title' in attrs and attrs['title'] == 'img'):
                        self._data.append(elem.text)


    def download(self, path):
        length = len(self._data)
        print('有{}张图片等待下载...'.format(length))
        i = 1
        for img in self._data:
            urlretrieve(img, path + img[img.rindex('/'):])
            print('已下载图片{}/{}'.format(i, length))
            i += 1
