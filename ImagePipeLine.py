#! python3
# -*- coding: UTF-8 -*-


from multiprocessing import Process,Pool,Lock,cpu_count
import time
from download import request

from pymongo import MongoClient
import os

from meizi_mongo import Mongodb



def img_download(img_url):
    name = img_url[-9:-4]
    img = request.get(img_url,3)
    f = open(name+'.jpg','ab')
    f.write(img.content)
    f.close()


def get_collection():
    mongoclient = Mongodb('meinv')
    col = mongoclient.get_collection('mzitu')   
    return col


if __name__ == '__main__':

    href = 'http://www.mzitu.com/81196'

    col  = get_collection()

    results = col.find({'is_download':False})

    for i in results:
        print(i['标题'])

    exit()

    urls = results['图片地址']

    os.chdir('D:\meizi\\test')

    cpu_num = cpu_count()

    print("cpu number: ",str(cpu_num))

    pool = Pool(processes=cpu_num)

    print( urls)

    for url in urls:
        pool.apply_async(img_download,args=(url,))

    print("start processes")
    pool.close()

    pool.join()



