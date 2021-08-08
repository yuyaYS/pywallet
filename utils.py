import hashlib
import collections

def sorted_dict_by_key(unsorted_dict):
    return collections.OrderedDict(
        sorted(unsorted_dict.items(),key= lambda d :d[0]))
    
# block = {'b': 2, 'a':1}

# block2 = {'b': 1, 'a':2}
# block = collections.OrderedDict(sorted(block.items()),key= lambda d :d[0])
# block2 = collections.OrderedDict(sorted(block2.items()),key= lambda d :d[0])


# print(hashlib.sha256(str(block).encode()).hexdigest())
# print(hashlib.sha256(str(block2).encode()).hexdigest())