#!/usr/bin/env python

from data import Record

_dataPath = 'data/u.data'

recordList = []
userSet = {}
itemSet = {}

def _init():
    global recordList
    global userSet
    global itemSet

    file = open(_dataPath, "r")
    lines = file.readlines()
    for line in lines:
        record = Record.deserialize(line)
        recordList.append(record)
        uList = userSet.get(record.userId)
        if uList is None:
            uList = []
            userSet[record.userId] = uList
        uList.append(record)
        iList = itemSet.get(record.itemId)
        if iList is None:
            iList = []
            itemSet[record.itemId] = iList
        iList.append(record)

_init()

if __name__ == '__main__':
    print len(recordList)
