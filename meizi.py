#! python3
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import sys

from download import request

from pymongo import MongoClient

# reload(sys)
# sys.setdefaultencoding('utf-8')


class mzitu():

    img_fold_url = u'D:\meizi'



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

            self.html(href)
            break

    def html(self,href):
        html = request.get(href,3)
        max_span = BeautifulSoup(html.text,'lxml').find('div',class_='pagenavi').\
                   find_all('span')[-2].get_text()
        for page in range(1,int(max_span)+1):
            page_url = href +'/'+str(page)
            self.img(page_url)

    def img(self,page_url):
        img_html = request.get(page_url,3)
        img_url = BeautifulSoup(img_html.text,'lxml').find('div',class_="main-image").\
                  find('img')['src']
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


















