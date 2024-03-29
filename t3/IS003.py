#!/usr/bin/env python
# coding: utf-8

# In[24]:


import os
import argparse
import re
import sys

from collections import defaultdict
from nltk import RegexpTokenizer
from nltk.stem import WordNetLemmatizer


# In[63]:


DIR = 'Выкачка_очищенная'


# In[52]:


def get_inverted_index():
    term_documents_dict = defaultdict(list)
    idx = 0
    for root, dirs, files in os.walk(DIR):
        for file in files:
            if file.lower().endswith('.txt') and file.lower().startswith('lemmas'):
                idx += 1
                path_file = os.path.join(root, file)
                with open(path_file, encoding="utf=8") as f:
                    lemmas = list(map(lambda x: x.split(':')[0], f.readlines()))
                for lemma in lemmas:
                    term_documents_dict[lemma].append(idx)
    return term_documents_dict


# In[53]:


DOCS = set(range(100))
inverted_index = get_inverted_index()


# In[54]:


def tokenize(s):
    tok = RegexpTokenizer(r'[A-Za-z&(\|)~\)\(]+')
    clean = tok.tokenize(s)
    clean = [w.lower() for w in clean if w != '']
    return list(clean)


# In[55]:


def lemmatize(tokens):
    lem = WordNetLemmatizer()
    lemmas = []
    for t in tokens:
        if re.match(r'[A-Za-z]', t):
            l = lem.lemmatize(t)
            lemmas.append(l)
        else:
            lemmas.append(token)
    return lemmas


# In[56]:


def priority(oper):
    if oper == '&':
        return 2
    elif oper == '|':
        return 1
    return -1


# In[57]:


def get_notaion(operands):
    result = []
    stack = []
    for operand in operands:
        if operand not in ['&', '|']:
            result.append(operand)
        else:
            last = None if len(stack) == 0 else stack[-1]
            while priority(last) >= priority(operand):
                result.append(stack.pop())
                last = None if not stack else stack[-1]
            stack.append(operand)
    for el in reversed(stack):
        result.append(el)
    return result


# In[58]:


def get_index(word):
    if word[0] == '~':
        try:
            indices = set(inverted_index[word[1:]])
            return DOCS - indices
        except KeyError:
            return set()
    else:
        try:
            index = inverted_index[word]
            return set(index)
        except KeyError:
            return set()


# In[59]:


def evaluate(tokens):
    stack = []
    for token in tokens:
        if token in ['&', '|']:
            arg2, arg1 = stack.pop(), stack.pop()
            if token == '&':
                result = arg1 & arg2
            else:
                result = arg1 | arg2
            stack.append(result)
        else:
            stack.append(get_index(token))
    return stack.pop()


# In[60]:


def tokenize_query(query):
    negations_indices = []
    tokenized_query = []

    for (index, word) in enumerate(query.split(' ')):
        if word == '&' or word == '|':
            tokenized_query.append(word)
        else:
            if word[0] == '~':
                tokenized_word = lemmatize(tokenize(word[1:]))[0]
                tokenized_query.append('~' + tokenized_word)
            else:
                tokenized_word = lemmatize(tokenize(word))[0]
                tokenized_query.append(tokenized_word)

    return tokenized_query


# In[70]:


def search(query):
    tokenized_query = tokenize_query(query)
    print(tokenized_query)
    converted_query = get_notaion(tokenized_query)
    print(converted_query)
    result = evaluate(converted_query)
    print(result)


# In[67]:


td_dict = get_inverted_index()
with open('inverted_index.txt', 'w', encoding='utf-8') as f:
    for k, v in td_dict.items():
        f.write(k + ' ' + ' '.join(map(str, v)) + '\n')
count_inverted_word = []
for k, v in td_dict.items():
    count_inverted_word.append({"count": len(v), "inverted_array": v, "word": k})
with open('inverted_index_2.txt', 'w', encoding='utf-8') as f:
    for ciw in count_inverted_word:
        f.write(str(ciw) + '\n')


# In[74]:

if __name__ == "__main__":
    query = "time & bar" ## <---Запрос вводить сюда
    search(query)


# In[ ]:




