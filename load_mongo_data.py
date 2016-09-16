# -*- coding=utf-8 -*-
import os
import sys
import pymongo
import logger

LEVEL = os.getenv("LOG", 1)


class MongoClient(object):
    """
    MongoClient Wrapper
    """
    conn = None

    def __init__(self, url='127.0.0.1', port=27017):
        if not self.conn:
            self.conn = pymongo.MongoClient(url, port)
        if self.conn:
            logger.info("[MongoClient] Initialize connection to %s:%s" % (url, port), LEVEL)
        else:
            logger.error("[MongoClient] Failed to connect to %s:%s" % (url, port), LEVEL)

    def __del__(self):
        logger.info("[MongoClient] Close connection.", LEVEL)
        return self.conn.close()

    def get_table(self, db_name, table_name):
        """
        获取mongo collection对象
        :param db_name:
        :param table_name:
        :return:
        """
        if not self.conn:
            logger.error("[MongoClient] No connection initialized.", LEVEL)
        return self.conn[db_name][table_name]

"""
def output_collection_schema(conn, db, output_path):
    w = open(output_path + '/' + db + '.collections.schema.tsv', 'w')
    for collection_name in conn.getCollectionNames(db):
        table = conn.getCollection(db, collection_name)
        tmp_key = list()
        tmp_value = list()
        tmp = table.find_one()
        if not tmp: 
            print >> w, (collection_name + '\t' + "NULL").encode('utf-8')
            continue
        for key, value in table.find_one().items():
            tmp_key.append(key)
            if type(value) is unicode:
                tmp_value.append(value)
            else:
                tmp_value.append(str(value))
        print >> w, (collection_name + '\t' + 'KEY' + '\t' +  '\t'.join(tmp_key)).encode('utf-8')
        print >> w,            ("" + '\t' + 'VALUE' +  '\t' + '\t'.join(tmp_value)).encode('utf-8')
        print >> w, ''
    
    w.close()
"""

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python load_mongo_data.py [output_path]"
        sys.exit(-1)

    output_path = sys.argv[1]
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    else:
        print "[WARN] %s is existed" % (output_path)

    



