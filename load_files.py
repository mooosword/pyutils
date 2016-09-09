#!/usr/loca/bin/python

import sys
import os
import re
import logger

def load_line(fname, sep = '\t', col_num=None):
    '''
    load records seperated by '\t'
    return reuslt is a list, each element is a tuple represent the record.
    '''
    li = list()
    f = open(fname)
    lines = f.readlines()
    for i in range(len(lines)):
        ln = lines[i]
        ln = ln.decode('utf-8').strip()
        if not ln:
            continue
        terms = ln.split(sep)
        terms = [t.strip() for t in terms]
        if col_num and len(terms) != col_num:
            logger.error("Error line format: [%d] %s" % (i, ln), 1)
            continue
        li.append(terms)
    return li

def load_file(fname, key_col = 0, sep = '\t'):
    '''
    load records seperated by '\t'
    return result is a dictionary, key is from key_col, and value is the items of the record
    note that the values of key column need to be unique.
    '''
    dic = dict()
    
    f = open(fname)
    for ln in f.readlines():
        ln = ln.decode('utf-8').strip()
        if not ln :
            continue
        terms = [ t.strip() for t in ln.split(sep) if t.strip() ]
        dic[terms[key_col]] = terms
    return dic

def load_group_by_key_col(fname, col= 0, sep = '\t'):
    '''
    if the records can be grouped by the value of some column, the funtions
    is return the mapping relation

    the return result is a dictionary, looks like key -> [ (cols in one record, ..  ), ..  ]
    '''
    f = open(fname)
    dic = dict()
    for ln in f.readlines():
        ln = ln.decode('utf-8').strip()
        if not ln:
            continue
        terms = ln.split(sep)

        dic[terms[col]] = dic.get(terms[col], list())
        dic[terms[col]].append(tuple(terms))
    
    return dic

def load_mapping(fname, sep = '\t'):
    '''
    load records with 2 column where the data is one-one mapping.
    the result is two dictionaries, key and value are from both the columns alternatively.
    '''
    dic1 =dict()
    dic2 = dict()
    f = open(fname)
    for ln in f.readlines():
        ln = ln.decode('utf-8').strip()
        if not ln:
            continue
        c1, c2 = ln.split(sep)
        dic1[c1] = c2
        dic2[c2] = c1
    return dic1, dic2

def load_feature_file(fname, sep = '\t'):
    
    dic = dict()
    
    f = open(fname)
    for ln in f.readlines():
        ln = ln.decode('utf-8').strip()
        if not ln :
            continue
        key, feat, wt = ln.split(sep)
        wt = float(wt)
        dic[key] = dic.get(key, list())
        dic[key].append((feat, wt))

    return dic


if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print "Usage: python load_files.py [filename]"
        sys.exit(0)

    dic = load_file(sys.argv[1],0)
    
