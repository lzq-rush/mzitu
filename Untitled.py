
# coding: utf-8

# In[1]:

from download import request
from bs4 import BeautifulSoup


# In[37]:

response = request.simple_get('url')


# In[60]:

response.encoding='gb18030'
#title = BeautifulSoup(response.text,"lxml").find("div",class_="t3").find("b")

title = BeautifulSoup(response.text,"lxml").find("h4")
path = title.string.replace("?","_").strip()
print(path)
# print(title.string)
# for sting in title.stripped_strings:
#     print(repr(sting))
# print(title)


# In[62]:

import os
img_fold_url = 'D:\meizi'
isExists = os.path.exists(os.path.join(img_fold_url,path))
if not isExists:
    print("create folder named: ",path)
    os.mkdir(os.path.join(img_fold_url,path))
else:
    print("folder ",path," already exits!")


# In[9]:




# In[ ]:



