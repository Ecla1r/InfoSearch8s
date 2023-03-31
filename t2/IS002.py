#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re

from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict


# In[2]:


nltk.download('stopwords')
nltk.download('punkt')
nltk.download('snowball_data')
nltk.download('perluniprops')
nltk.download('universal_tagset')
nltk.download('stopwords')
nltk.download('nonbreaking_prefixes')
nltk.download('wordnet')
sw = stopwords.words('english')

DIRECTORY = "Выкачка"


# In[3]:


def get_tokens(s):
    tok = RegexpTokenizer('[A-Za-z]+')
    clean = tok.tokenize(s)
    clean = [w.lower() for w in clean if w != '']
    clean = [w for w in clean if w not in sw]
    return list(set(clean))


# In[4]:


def get_lemmas(tokens):  
    lem = WordNetLemmatizer()
    lemmas = []
    for t in tokens:
        if re.match(r'[A-Za-z]', t):
            l = lem.lemmatize(t)
            lemmas.append(l)
    return lemmas


# In[5]:


def get_every_file():
    for root, dirs, files in os.walk(DIRECTORY):
        for file in files:
            if file.lower().endswith('.txt'):
                path_file = os.path.join(root, file)
                with open(path_file, encoding="utf-8") as f:
                    html_text = f.read()
                soup = BeautifulSoup(html_text, "html.parser")
                text = ' '.join(soup.stripped_strings)
                tokens = get_tokens(text)
                tokens_string = '\n'.join(tokens)
                path_result = f"Выкачка_очищенная/tokens_{file}"
                os.makedirs(os.path.dirname(path_result), exist_ok=True)
                with open(path_result, "w", encoding="utf-8") as file_result:
                    file_result.write(tokens_string)
                lemmas_dict = get_lemmas(tokens)
                path_result = f"Выкачка_очищенная/lemmas_{file}"
                with open(path_result, "w", encoding="utf-8") as file_result:
                    for k, v in lemmas_dict.items():
                        file_result.write(k + ": ")
                        for word in v:
                            file_result.write(word + " ")
                        file_result.write("\n")


# In[6]:


def get_common():
    tokens = []
    for root, dirs, files in os.walk(DIRECTORY):
        for file in files:
            if file.lower().endswith('.txt'):
                path_file = os.path.join(root, file)
                print(path_file)
                with open(path_file, encoding="utf-8") as f:
                    html_text = f.read()
                soup = BeautifulSoup(html_text, "html.parser")
                text = ' '.join(soup.stripped_strings)
                tokens += get_tokens(text)
    tokens = list(set(tokens))
    tokens_string = '\n'.join(tokens)
    path_result = f"../002/Выкачка_очищенная_общая/tokens.txt"
    os.makedirs(os.path.dirname(path_result), exist_ok=True)
    with open(path_result, "w", encoding="utf-8") as file_result:
        file_result.write(tokens_string)
    lemmas_dict = get_lemmas(tokens)
    path_result = f"../002/Выкачка_очищенная_общая/lemmas.txt"
    with open(path_result, "w", encoding="utf-8") as file1_result:
        for k, v in lemmas_dict.items():
            print(k)
            file1_result.write(k + ": ")
            for word in v:
                file1_result.write(word + " ")
            file1_result.write("\n")


# In[8]:

if __name__ == "__main__":
    get_every_file()
    get_common()


# In[ ]:




