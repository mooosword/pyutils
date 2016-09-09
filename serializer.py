import sys
import pickle

def serialize(obj, output_path, update=True):
    if update:  
        pickle.dump(obj, open(output_path, 'wb'))

def deserialize(input_path): 
    return pickle.load(open(input_path, 'rb'))

if __name__ == '__main__':        
    d = {1:2, 3:4, 5:'a'}
    serialize(d, './test.data')
    d = deserialize('./test.data')
    print d
