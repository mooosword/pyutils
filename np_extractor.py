#!encoding=utf-8
from textblob import TextBlob
import os, sys, re

def textblob_process(line):
    blob = TextBlob(line)
    return blob.tags

def process_tag_result(tag_res):    
    nps = []
    i = 0
    while i < len(tag_res):
        while i < len(tag_res) and not tag_res[i][1].startswith('NN'):
            i += 1
        np = []
        while i < len(tag_res) and (tag_res[i][1] == 'NN' or tag_res[i][1] == 'NNS' or tag_res[i][1] == 'NNP'):
            np.append(tag_res[i][0])
            i += 1
        if len(np) == 1 and tag_res[i-2][1] == 'JJ':
            np.insert(0, tag_res[i-2][0])
        nps.append(" ".join(np))
        i += 1
    return nps       
        
def is_valid_np(np):
    if re.search(r'\d+', np):
        return False
    if not re.match(r'\w+', np):
        return False
    for brand in BRANDS:
        if np.find(brand) >=0:
            return False
    if np.find('/') >= 0:
        return False
    for token in np.split(' '):
        if len(token) <= 2:
            return False
        if token[-1] == u'®' or token[-1] == u'™':
            return False
    return True

def extract(line):
    nps = list()
    tag_res = textblob_process(line)
    nps.extend(process_tag_result(tag_res))
    return nps

if __name__ == '__main__':
    s = "Lower cut design with a square shaped neckline"
    print extract_np(s)
    
