import os, sys
from datetime import datetime
from datetime import timedelta
import collections
from bson import ObjectId


def get_day_range(day):
    return day + timedelta(hours=-8), day + timedelta(hours=16)


def parse_id_card(id_card):
    if len(id_card) == 18:
        birthyear = int(id_card[6:10])
        gender = int(id_card[16]) % 2 == 0 and 'female' or 'male'
    elif len(id_card) == 15:
        birthyear = int('19' + id_card[6:8])
        gender = int(id_card[14]) % 2 == 0 and 'female' or 'male'
    else:
        return (None,None)
    return (birthyear, gender)


def group_by(alist, col_idx):
    res = dict()
    for terms in alist:
        res[terms[col_idx]] = res.get(terms[col_idx], list())
        res[terms[col_idx]].append(terms)
    return res


def datetime2objectid(dt):
    return ObjectId.from_datetime(dt)


def objectid2datetime(obj_id):
    return obj_id.generation_time.replace(tzinfo=None)


def date2str(dt):
    return str(dt.year) + (len(str(dt.month)) > 1 and str(dt.month) or '0' + str(dt.month)) \
           + (len(str(dt.day)) > 1 and str(dt.day) or '0' + str(dt.day))


def str2date(dt_str):
    return datetime(int(dt_str[0:4]), int(dt_str[4:6]), int(dt_str[6:8]))


def next_date(date_str):
    dt = str2date(date_str)
    return date2str(dt + timedelta(days=1))


def pre_date(date_str):
    dt = str2date(date_str)
    return date2str(dt + timedelta(days=-1))


def daily_key_sorter():
    return lambda x: (len(x) > 5 and x[6:10]+x[0:2]+x[3:5] or x)


def hourly_key_sorter():
    return lambda x: (len(x[0:-3]) > 5 and x[6:10]+x[0:2]+x[3:5]+x[-3:] or x)


def enhance_data(raw_data, sort_func=None):
    res_data = collections.OrderedDict()
    if sort_func:
        for key in sorted(raw_data.keys(), key=sort_func):
            res_data[key] = raw_data[key]
    else:
        res_data = raw_data
    return res_data


def is_valid_uin(uin):
    if not uin:
        return False
    else:
        return True


def is_valid_device_id(device_id):
    if not device_id:
        return False
    else:
        return True

if __name__ == '__main__':
    li = [(1,2,3,3), (23,31,31,1), (31,12,12,2), (2,3,4,1), (23,1,2,2)]
    print group_by(li, 3)
    #print parse_id_card('441900198609172813')
    print parse_id_card('130503670401001')
