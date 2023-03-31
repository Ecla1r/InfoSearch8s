#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import os


# In[2]:


INIT_LINK = 'https://genius.com/tags/rap/all?page='
COUNT = 100
INDEX_FILE = 'index.txt'


# In[3]:


def get_links(url):
    page = requests.get(url)
    data = BeautifulSoup(page.text, features="lxml")
    links = []
    for item in data.select("a.song_link"):
        links.append(item['href'])
    return links


# In[4]:


def crawler(url):
    page = requests.get(url)
    data = BeautifulSoup(page.text, "html.parser")
    for d in data(['style', 'script', 'noscript', 'link']):
        d.decompose()
    return str(data)


# In[5]:

if __name__ == "__main__":
    links = []
    i = 1
    info = ""
    
    while len(links) < COUNT:
        cur_link = f'{INIT_LINK}{i}'
        nlinks = get_links(cur_link)
        links += nlinks
        i += 1
    
    for i, link in enumerate(links):
        html_text = crawler(link)
        filename = f'00{i+1}' if i < 9 else f'0{i+1}' if i < 99 else f'100'
        info += f"{filename}\t{link}\n"
        path_result = f"Выкачка/{filename}.txt"
        os.makedirs(os.path.dirname(path_result), exist_ok=True)
        with open(path_result, "w", encoding="utf-8") as file_result:
            file_result.write(html_text)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(info)



# In[ ]:




