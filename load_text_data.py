# -*- coding=utf-8 -*-

import sys
import os
import logger

LEVEL = os.getenv('LOG', 2)


def get_file_line_count(filename):
    """
    通用获取文件行数, 考虑了大文件的处理
    :param filename:
    :return:
    """
    def buf_count(_filename):
        f = open(_filename)
        lines = 0
        buf_size = 1024 * 1024
        read_f = f.read  # loop optimization
        buf = read_f(buf_size)
        while buf:
            lines += buf.count('\n')
            buf = read_f(buf_size)
        return lines
    return buf_count(filename)


def get_header(line, sep, col_num=None):
    """
    获取text file的header
    :param line:
    :param sep:
    :param col_num:
    :return:
    """
    terms = line.strip().split(sep)
    if col_num and len(terms) != col_num:
        logger.error("Column count %d is not correct, check line %s" % (len(terms), line), LEVEL)
        sys.exit(-1)
    return [t.strip() for t in terms]


def load_line(filename, sep='\t', header=False, col_num=None):
    """
    读取文件, 每一行生成一个列表; 如果header为真, 每一行生成一个字典, 最后返回一个大列表
    :param filename:
    :param sep:
    :param header: 默认为False, 如果为真, 则读取第一行作为header
    :param col_num: 文件列数, 用于校验数据正确与否
    :return:
    """
    li = list()
    with open(filename, 'r') as f:
        if header:
            line = f.readline()
            headers = get_header(line, sep, col_num)
        for line in f:
            line = line.decode('utf-8').strip()
            if not line:
                continue
            terms = line.split(sep)
            terms = [t.strip() for t in terms]
            if col_num and len(terms) != col_num:
                logger.error("Column count %d is not correct, check line %s" % (len(terms), line.encode('utf-8')), LEVEL)
                continue
            li.append(terms)
        return li


def load_file(filename, key_col=0, sep='\t', col_num=None):
    """
    读取文件, 返回一个字典, 每一行制定一个列作为Key, 并且把这一行作为一个列表保存在Key对应的Value中。
    :param filename:
    :param key_col:
    :param sep:
    :param col_num:
    :return:
    """
    res = {}
    f = open(filename)
    for ln in f.readlines():
        ln = ln.decode('utf-8').strip()
        if not ln:
            continue
        if len(ln.split(sep)) != col_num:
            logger.error("Column count %d is not correct, check line %s" % (len(ln.split(sep)), ln.encode('utf-8')), LEVEL)
        terms = [t.strip() for t in ln.split(sep) if t.strip()]
        res[terms[key_col]] = terms
    return res


def load_group_by_key_col(fname, col= 0, sep = '\t'):
    '''
    if the records can be grouped by the value of some column, the functions
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
        print "Usage: python load_text_data.py [filename]"
        sys.exit(0)

    dic = load_file(sys.argv[1],0)

