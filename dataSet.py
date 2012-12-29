#!/usr/bin/env python

from data import Record
import random

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

_init()

def exportTables(records=recordList):
    """ export item-user table and user-item table """
    itemUsers = {}
    userItems = {}
    for record in records:
        uList = itemUsers.get(record.itemId)
        if uList is None:
            uList = []
            itemUsers[record.itemId] = uList
        uList.append(record)
        iList = userItems.get(record.userId)
        if iList is None:
            iList = []
            userItems[record.userId] = iList
        iList.append(record)
    return itemUsers, itemUsers

def _testExportTables():
    itemUsers, userItems = exportTables(recordList)
    count = 0
    for records in itemUsers.values():
        count += len(records)
    if count != len(recordList):
        print "Test Failed! len(recordList)=%d, but count itemUsers=%d" % (len(recordList), count)
        return
    count = 0
    for records in userItems.values():
        count += len(records)
    if count != len(recordList):
        print "Test Failed! len(recordList)=%d, but count userItems=%d" % (len(recordList), count)
        return

_SPLIT_COUNT = 8
def randomSplit():
    train = []
    test = []
    for record in recordList:
        if random.randint(0, _SPLIT_COUNT-1)==0:
            test.append(record)
        else:
            train.append(record)
    return train, test

def _testRandomSplit():
    train, test = randomSplit()
    if len(train) + len(test) != len(recordList):
        print "TEST FAILED: len(train)=%d, len(test)=%d, but len(recordList)=%d" %(len(train), len(test)\
            ,len(recordList))
    ratio = 1.0*len(recordList)/len(test)
    if ratio<_SPLIT_COUNT-0.5 or ratio>_SPLIT_COUNT+0.5:
        print "TEST FAILED: ratio=%d" % ratio

if __name__ == '__main__':
    _testRandomSplit()
    _testExportTables()
