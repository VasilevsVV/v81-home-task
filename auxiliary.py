import numpy as np
import pandas
import csv
from matplotlib import pyplot as plt
import const

def find_by(coll, key, value):
    return next(item for item in coll if item[key] == value)

def select_items(dict, keys):
    return {k:dict[k] for k in keys}

def select_values(dict, keys, fn=lambda x: x):
    return (fn(dict[k]) for k in keys)

def get_in(dict, keys, default=None):
    res = dict
    for k in keys:
        res = res.get(k, False)
        if not res:
            return default
    return res

def make_histogram():
    data = []
    shades = set()
    with open("resources/cases_with_shade.csv", "r") as f:
        r = csv.DictReader(f)
        for row in r:
            shade, img_id = select_values(row, ("shade", "img_id"), int)
            shades.add(shade)
            data.append((shade, img_id))
    df = pandas.DataFrame(data, columns=["shade", "img_id"])
    bins_count = len(set(shades))
    fig = df.plot(kind="hist", y="shade", bins=bins_count)
    fig.get_figure().savefig(f"{const.OUTPUT_DIR}/shades_hist.png")

def simple_shade(shade):
    if (shade < 66105 or shade == 66120):
        return "Light"
    elif shade <= 66165:
        return "Medium"
    return "Dark"

def make_grouped_histogram():
    data = []
    shades = set()
    with open("resources/cases_with_shade.csv", "r") as f:
        r = csv.DictReader(f)
        for row in r:
            shade, img_id = select_values(row, ("shade", "img_id"), int)
            shades.add(shade)
            data.append((shade, img_id))
    df = pandas.DataFrame(data, columns=["shade", "img_id",])
    df2 = df[["shade"]].map(simple_shade)[["shade"]].groupby("shade")["shade"].agg("count").sort_values()
    
    fig = df2.plot(kind="bar", y="shade")
    fig.get_figure().savefig(f"{const.OUTPUT_DIR}/shades_grouped_hist.png")
