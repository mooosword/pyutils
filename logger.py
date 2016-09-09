import sys
import time
import datetime
DEBUG_LEVEL = 1
WARN_LEVEL = 2
INFO_LEVEL = 3
ERROR_LEVEL = 4


def info(msg, level, module_name = None, function_name= None):
    if level > INFO_LEVEL:
        return 
    print >> sys.stderr, '\033[1;32;40m',  #green  
    print >> sys.stderr, "\b[INFO]",
    if module_name and function_name:
        print >> sys.stderr, '\033[1;33;40m',   #yellow
        print >> sys.stderr, "\b[%s.%s]" % (module_name, function_name),
    print >> sys.stderr, '\033[0m',
    print >> sys.stderr, '\b[' + msg + '] ' # + str(datetime.datetime.fromtimestamp(time.time()))


def warn(msg, level, module_name = None, function_name = None):
    if level > WARN_LEVEL:
        return
    print >> sys.stderr, '\033[1;35;40m', #pink 
    print >> sys.stderr, "\b[WARNING]",   
    if module_name and function_name:
        print >> sys.stderr, '\033[1;33;40m',   #yellow
        print >> sys.stderr, "\b[%s.%s]" % (module_name, function_name),
    print >> sys.stderr, '\033[0m',
    print >> sys.stderr, '\b[' + msg + '] ' # + str(datetime.datetime.fromtimestamp(time.time()))

def error(msg, level, module_name = None, function_name = None): 
    if level > ERROR_LEVEL:
        return 
    print >> sys.stderr, '\033[1;31;40m',  #red 
    print >> sys.stderr, "\b[ERROR]",
    if module_name and function_name:
        print >> sys.stderr, '\033[1;33;40m',   #yellow
        print >> sys.stderr, "\b[%s.%s]" % (module_name, function_name),
    print >> sys.stderr, '\033[0m', 
    print >> sys.stderr, '\b[' + msg + '] ' # + str(datetime.datetime.fromtimestamp(time.time()))

def debug(msg, level, module_name = None, function_name = None): 
    if level > DEBUG_LEVEL:
        return
    print >> sys.stderr, '\033[1;36;40m',  #cyan 
    print >> sys.stderr, "\b[DEBUG]",
    if module_name and function_name:
        print >> sys.stderr, '\033[1;33;40m',   #yellow
        print >> sys.stderr, "\b[%s.%s]" % (module_name, function_name),
    print >> sys.stderr, '\033[0m', 
    print >> sys.stderr, '\b[' + msg + ']'

if __name__ == '__main__':
    
    LEVEL = 3
    info('try something new', LEVEL)
    warn('try something new', LEVEL)
    error('try something new', LEVEL)
    debug('try something new', LEVEL)
