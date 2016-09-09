import sys

def check(argv, argv_names):
    if len(argv) - 1 < len(argv_names):
        print "Usage: python %s %s" % (argv[0], ' '.join(['[' + argv_name + ']' for argv_name in argv_names])) 
        sys.exit(-1)

if __name__ == '__main__':
    pass
