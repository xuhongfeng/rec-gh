#!/usr/bin/env python

from data import Record

_dataPath = 'data/u.data'

def parse():
    file = open(_dataPath, "r")
    lines = file.readlines()
    for line in lines:
        record = Record.deserialize(line)
        print record.serialize()

if __name__ == '__main__':
    parse()
