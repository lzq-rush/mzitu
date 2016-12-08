#! python3
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import sys

from download import request

from pymongo import MongoClient


import datetime
# reload(sys)
# sys.setdefaultencoding('utf-8')


class mzitu():

    img_fold_url = u'D:\meizi'

    def __init__(self):
        client = MongoClient()
        db = client['meinv']
        self.mzitu_collection = db['mzitu']
        self.title=''
        self.url=''
        self.img_urls=[]



    def all_url(self,url):
        html = request.get(url,3)
        all_a = BeautifulSoup(html.text,"lxml").find('div',class_='all').find_all('a')
        for a in all_a:
            title = a.get_text()
            print("start save: ",title)
            path = str(title).replace("?","_")

            self.mkdir(path)
            os.chdir(os.path.join(self.img_fold_url,path))
            href = a['href']
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



    def img(self,page_url,max_span,page_num):
        img_html = request.get(page_url,3)
        img_url = BeautifulSoup(img_html.text,'lxml').find('div',class_="main-image").\
                  find('img')['src']

        self.img_urls.append(img_url)

        if int(max_span) == page_num:
            self.save(img_url)
            post = {
                    '标题': self.title,
                    '主题页面': self.url,
                    '图片地址': self.img_urls,
                    '获取时间': datetime.datetime.now()
            }
            self.mzitu_collection.save(post)
        else:
            self.save(img_url)

    def save(self,img_url):
        name = img_url[-9:-4]
        img = request.get(img_url,3)
        f = open(name+'.jpg','ab')
        f.write(img.content)
        f.close()

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


    def request(self,url):
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        content = requests.get(url,headers = headers)
        return content

if __name__ == '__main__':
    

    Mzitu = mzitu()

    Mzitu.all_url("http://www.mzitu.com/all")


















