import os, sys, re
import pymongo
import logger

LEVEL= 1

class DBConnection:
    
    conn = None
    
    def __init__(self):
        conn = None
    
    def connect(self, url='10.174.37.196', port=27017):
        self.conn = pymongo.MongoClient(url, port)
        if self.conn:
            logger.info("Connecting to %s:%s, success!" % (url, port), LEVEL)
        else:
            logger.info("Failed Connecting to %s:%s.." % (url, port), LEVEL)
    
    def close(self):
        logger.info("Disconnecting", LEVEL)
        return self.conn.disconnect()

    def getConnect(self):
        return self.conn

    def getDatabaseNames(self):
        if not self.conn:
            print >> sys.stderr,  "[Error] Init Failed!"
        return self.conn.database_names()

    def showDatabaseNames(self):
        if not self.conn:
            print >> sys.stderr,  "[Error] Init Failed!"
        print self.conn.database_names()
    
    def showCollectionNames(self, db_name):
        if not self.conn:
            print >> sys.stderr,  "[Error] Init Failed!"
        print self.conn[db_name].collection_names()

    def getCollectionNames(self, db_name):
        if not self.conn:
            print >> sys.stderr,  "[Error] Init Failed!"
        return self.conn[db_name].collection_names()
    
    def getDatabase(self, db_name):
        if not self.conn:
            print >> sys.stderr, "[Error] Init Failed!"
        return self.conn[db_name]

    def getCollection(self, db_name, collection_name):
        if not self.conn:
            print >> sys.stderr, "[Error] Init Failed!"
        return self.conn[db_name][collection_name]

    def getCollectionContentAsJsonObjects(self, db_name, collection_name, limit=1000000000):
        table = self.getCollection(db_name,collection_name)
        json_list = list()
        for entry in table.find():
            json_list.append(entry)
            if len(json_list) > limit:
                break
        return json_list
    

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


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python load_mongo_data.py [output_path]"
        sys.exit(-1)

    output_path = sys.argv[1]
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    else:
        print "[WARN] %s is existed" % (output_path)

    mongoDB = DBConnection()
    mongoDB.connect()
    
    print "[INFO] Connecting to localhost:27017, success!"
    print "[INFO] Show databases.."
    mongoDB.showDatabaseNames()

    print "\t - Please input the database name"
    _db_name = raw_input()
    
    output_collection_schema(mongoDB, _db_name, output_path)
    
    #mongoDB.showCollectionNames(_db_name)
    #print "\t - please input the collection name"
    #_collection_name = raw_input()
    #table = mongoDB.getCollection(_db_name, _collection_name)
 
    



