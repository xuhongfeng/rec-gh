#!/usr/bin/env python

from data import Record, ItemUsers, UserItems
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
    itemUsers = ItemUsers()
    userItems = UserItems()
    for record in records:
        itemUsers.add(record)
        userItems.add(record)
    return itemUsers, itemUsers

def _testExportTables():
    itemUsers, userItems = exportTables(recordList)
    if itemUsers.recordCount() != len(recordList):
        print "Test Failed! len(recordList)=%d, but count itemUsers=%d" % (len(recordList), \
            itemUsers.recordCount())
        return
    if userItems.recordCount() != len(recordList):
        print "Test Failed! len(recordList)=%d, but count userItems=%d" % (len(recordList), \
            userItems.recordCount())
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
