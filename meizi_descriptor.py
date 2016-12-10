#! python3
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import sys

from download import request

from pymongo import MongoClient

from multiprocessing import Process,Pool,Lock,cpu_count

import datetime

from weakref import WeakKeyDictionary as wd
# reload(sys)
# sys.setdefaultencoding('utf-8')


class Url(object):
    """A descriptor that forbids unreal url"""
    def __init__(self,default):
        self.default = default
        self.data = Wd()

    def __get__(self,instance,owner):
        return self.data.get(instance,self.default)

    def __set__(self,instance,value):
        if value == None:
            raise ValueError("url is None")
        if len(value) < 5:
            raise ValueError("url is not starnded : %s" % value)
        self.data[instance] = value

class Mongodb():
    def __init__(self,database):
        client = MongoClient()
        self.db = client[database]

    def get_collection(self,col):
        return self.db[col]


class mzitu():
    img_fold_url = u'D:\meizi'



    def __init__(self,col):
        self.mzitu_collection = col
        self.title=''
        self.url=''
        self.img_urls=[]
        


    def all_url(self,url):
        html = request.get(url,3)
        all_a = BeautifulSoup(html.text,"lxml").find('div',class_='all').find_all('a')
        count = 0
        for a in all_a:
            title = a.get_text()
            print("start save: ",title)
            path = str(title).replace("?","_")

            self.mkdir(path)
            os.chdir(os.path.join(self.img_fold_url,path))
            href = a['href']
            self.title = title
            self.url = href
            if self.mzitu_collection.find_one({'主题页面':href}):
                print(u'already crawled!')
            else:
                self.html(href)
    def html(self,href):
        html = request.get(href,3)
        max_span = BeautifulSoup(html.text,'lxml').find('div',class_='pagenavi').\
                   find_all('span')[-2].get_text()

        page_num = 0

        for page in range(1,int(max_span)+1):
            page_num+=1
            page_url = href +'/'+str(page)
            self.img(page_url,max_span,page_num)

        self.img_urls = []

    def img(self,page_url,max_span,page_num):

        if page_url 
        img_html = request.get(page_url,3)
        try:
            img_url = BeautifulSoup(img_html.text,'lxml').find('div',class_="main-image").\
                      find('img')['src']
            self.img_urls.append(img_url)
        except AttributeError:
            pass

        if int(max_span) == page_num:
            
            post = {
                    '标题': self.title,
                    '主题页面': self.url,
                    '图片地址': self.img_urls,
                    '获取时间': datetime.datetime.now(),
                    'is_download': False
            }
            self.mzitu_collection.save(post)


    def mkdir(self,path):
        path = path.strip()
        isExists = os.path.exists(os.path.join(self.img_fold_url,path))

        if not isExists:
            print("create folder named: ",path)
            os.mkdir(os.path.join(self.img_fold_url,path))
            return True
        else:
            print("folder ",path," already exits!")
            return False

    def parser(self,response,name):
        pass



    def request(self,url):
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        content = requests.get(url,headers = headers)
        return content






if __name__ == '__main__':
    
    mongoclient = Mongodb('meinv')
    col = mongoclient.get_collection('mzitu')
    Mzitu = mzitu(col)
    Mzitu.all_url("http://www.mzitu.com/all")
    


















