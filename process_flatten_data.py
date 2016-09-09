import sys, os
import logger
from datetime import datetime
LEVEL = 1

def get_header(entry):
    return sorted(entry.keys())

def generate_flatten_data_debug(data, output):
    i = 0
    while (data[i][0] == None):
        i+=1
    header = get_header(data[i][0])
    print >> output, "debug:board_date" + '\t' + '\t'.join(header)
    for entry, last_board in data:
        if last_board:
            board_date = datetime.strftime(last_board[1], "%Y%m%d") + '|' + str(last_board[0])
        else:
            board_date = "NoBoard"
        tmp = []
        if entry:
            for fact in header:
                tmp.append(str(entry[fact]))
        print >> output, board_date + '\t' + '\t'.join(tmp)
    logger.info("Done generated flatten data with %d lines" % len(data), LEVEL)

def generate_flatten_data(data, output):
    header = get_header(data[0])
    print >> output, '\t'.join(header)
    for entry in data:
        tmp = []
        for fact in header:
            tmp.append(str(entry[fact]))
        print >> output, '\t'.join(tmp)
    logger.info("Done generated flatten data with %d lines" % len(data), LEVEL)
    
def load_flatten_data(filename, sep='\t'):
    if not os.path.isfile(filename):
        return None
    data = []
    f = open(filename)
    header = f.readline().decode('utf-8').strip().split(sep)
    for ln in f.readlines():
        ln = ln.decode('utf-8').strip()
        if not ln:
            continue
        entry = {}
        value = ln.split(sep)
        for i in range(len(value)):
            entry[header[i]] = value[i]
        data.append(entry)
    logger.info("Done loaded flatten data %s with %d lines" % (filename, len(data)), LEVEL)
    return data

def group_by(data, key_list):
    res_dict = {}
    for entry in data:
        key = list()
        for fact in key_list:
            key.append(entry[fact])
        key = tuple(key)
        res_dict[key] = res_dict.get(key, list())
        res_dict[key].append(entry)
    return res_dict

def filter_by(data, conditions):
    filtered = []
    for entry in data:
        flag = True
        for key, condition in conditions.items():
            if '$eq' in condition and key in entry and entry[key] != condition['$eq']:
                flag = False
                break
            if key not in entry:
                flag = False
                break
            elif '$lt' in condition and key in entry and not entry[key] < condition['$lt']:
                flag = False
                break
            if key not in entry:
                flag = False
                break
            elif '$gt' in condition and key in entry and not entry[key] > condition['$gt']:
                flag = False
                break
            if key not in entry:
                flag = False
                break
        if flag:
            filtered.append(entry)
    return filtered





