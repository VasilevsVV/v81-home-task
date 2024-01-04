import numpy as np
from matplotlib import pyplot as plt

def find_by(coll, key, value):
    return next(item for item in coll if item[key] == value)

def select_keys(dict, keys):
    return {k:dict[k] for k in keys}    

def get_in(dict, keys, default=None):
    res = dict
    for k in keys:
        res = res.get(k, False)
        if not res:
            return default
    return res