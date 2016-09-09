import os, sys, re

class ConfParser(dict):
    
    def __init__(self, conf):
        self.params = dict()
        self.load(conf)
    
    def load(self, conf):
        f = open(conf)
        for ln in f.readlines():
            ln = ln.decode('utf-8').strip()
            if not ln or ln.startswith('#'):
                continue
            terms = ln.split('=')
            if len(terms) > 2:
                print >> sys.stderr, "[Error] [ConfParser.load] Configuration file format error."
                sys.exit(-1)

            terms = [t.strip() for t in terms]
            if len(terms) == 2:
                self.params[terms[0]] = terms[1]
            else:
                self.params[terms[0]] = ''
    
    def __getitem__(self, key):
        if key not in self.params:
            print >> sys.stderr, "[Warning] [ConfParser.get] %s is not in dictionary" % (key)
            return None
        else:
            return self.params[key]
    
    def __contains__(self, key):
        return key in self.params

    def __str__(self):
        return str(self.params)
            
