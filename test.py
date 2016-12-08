#! python3
# -*- coding: UTF-8 -*-



from multiprocessing import Process,Pool,Lock,cpu_count
import time
from download import request

from pymongo import MongoClient
import os
import time


def img_download(img_url):
    name = img_url[-9:-4]
    img = request.get(img_url,3)
    f = open(name+'.jpg','ab')
    f.write(img.content)
    f.close()


client = MongoClient()
db = client['meinv']
mzitu_collection = db['mzitu']

href = 'http://www.mzitu.com/81086'

results = mzitu_collection.find_one({'主题页面':href})

urls = results['图片地址']

os.chdir('D:\meizi\\test')

if __name__ == '__main__':

    cpu_num = cpu_count()
    print("cpu number: ",str(cpu_num))
    pool = Pool(processes=cpu_num)

    print("time:ctime() 1: %s" % time.ctime())

    for url in urls:
        pool.apply_async(img_download,(url,))



    print("time:ctime() 2: %s" % time.ctime())

    print("start processes")
    pool.close()

    print("time:ctime() 3: %s" % time.ctime())

    pool.join()

    print("time:ctime() 4: %s" % time.ctime())
    print("subprocess done")











# def process(num):
#     time.sleep(num)
#     print ('Process:', num)

# if __name__ == '__main__':
#     for i in range(5):
#         p = multiprocessing.Process(target=process, args=(i,))
#         p.start()

#     print('CPU number:' + str(multiprocessing.cpu_count()))
#     for p in multiprocessing.active_children():
#         print('Child process name: ' + p.name + ' id: ' + str(p.pid))

#     print('Process Ended')


# import threading, time, random
# count = 0
# class Counter(threading.Thread):
#     def __init__(self, lock, threadName):
#         '''@summary: 初始化对象。
        
#         @param lock: 琐对象。
#         @param threadName: 线程名称。
#         '''
#         super(Counter, self).__init__(name = threadName)  #注意：一定要显式的调用父类的初始化函数。
#         self.lock = lock
    
#     def run(self):
#         '''@summary: 重写父类run方法，在线程启动后执行该方法内的代码。
#         '''
#         global count
#         self.lock.acquire()
#         for i in range(10000):
#             count = count + 1
#         self.lock.release()
# lock = threading.Lock()
# for i in range(5): 
#     Counter(lock, "thread-" + str(i)).start()
# time.sleep(2)   #确保线程都执行完毕
# print (count)