from pathlib import Path
import json
import sys
import logging
import csv
import pprint
from sympy import symbols, simplify_logic
import re
from functools import reduce

SIMPLIFY = False


def get_file_path(path: str)->str:
    path = Path(path)
    if path.exists() == False:
        raise FileNotFoundError
    return path.absolute()


def valid(namespace: set, data: list)->bool:
    s = get_symbol(data)
    if namespace != s:
        raise Exception(s - namespace, namespace-s)
    return True


def get_symbol(table: list):
    ret = set()

    for row in table:
        for item in row:
            ret |= set(re.findall(r'\w+', item))
    return ret


config_file = get_file_path(sys.argv[1] if len(sys.argv) >
                            1 else 'test/config.json')

with open(config_file) as read_file:
    data = json.load(read_file)
    INPUT_SET = set(data.get('input') or ())
    STATE_SET = set(data.get('state') or ())
    OUTPUT_SET = set(data.get('output')or ())
    DEFAULT_DICT = data.get('default') or {}
    SUB_DICT = data.get('sub')
    CSV_FILE = data.get('datafile')

    # print(INPUT_SET, STATE_SET, OUTPUT_SET,
    #   DEFAULT_DICT, SUB_DICT, CSV_FILE, sep='\n')

# 如果CSV_FILE为空，则报错
if not CSV_FILE:
    raise EnvironmentError


with open('test/test.csv') as csvFile:
    table = csv.reader(csvFile)
    table = [[item.strip() for item in row] for row in table]

SYMBOL_SET = set()

# 读取 几个SET同时为空，则不触发校验
if INPUT_SET or STATE_SET or OUTPUT_SET:
    SYMBOL_SET = INPUT_SET | STATE_SET | OUTPUT_SET
    valid(SYMBOL_SET, table)
else:
    SYMBOL_SET = get_symbol(table)


for i in range(len(table)):
    table[i][0] = table[i][0] or table[i-1][0]


SYMBOL = symbols(','.join(SYMBOL_SET))

for i in SYMBOL:
    # print(i)
    globals()[str(i)] = i
# pprint.pprint(SYMBOL)
# deal with state


def evaluate(_set: set, pos: int)->list:
    ret = []
    for state in _set:
        res = []
        for row in table:
            if row[pos] == state:
                res.append('&'.join([f"({i})" for i in row[:2] if i]))
        res = [f"({i})" for i in res]
        eval_str = f'({"|".join(res)})'
        if SIMPLIFY:
            eval_str = "simplify_logic"+eval_str
        r = eval(eval_str)
        ret.append(f"{state} = {r}")
    return ret


ss = evaluate(STATE_SET, 2)
os = evaluate(OUTPUT_SET, 3)
# pprint.pprint(table)

[print(i) for i in ss]
[print(i) for i in os]
