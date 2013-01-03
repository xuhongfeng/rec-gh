#!/usr/bin/env python

from data import Record, ItemUsers, UserItems
from exception import UnitTestError
import random

_dataPath = 'data/u.data'
RATE_COUNT = 100000
USER_COUNT = 943
ITEM_COUNT = 1682

recordList = None

""" key is origin id, value is increasing id """
userSet = None
itemSet = None

def _init():
    global recordList
    global userSet
    global itemSet

    recordList = []
    userSet = {}
    itemSet = {}

    incUserId = 0
    incItemId = 0

    file = open(_dataPath, "r")
    lines = file.readlines()
    for line in lines:
        record = Record.deserialize(line)

        """ replace userId and itemId """
        userId = userSet.get(record.userId)
        if userId is None:
            userId = incUserId
            incUserId = incUserId+1
            userSet[record.userId] = userId
        record.userId = userId
        itemId = itemSet.get(record.itemId)
        if itemId is None:
            itemId = incItemId
            incItemId = incItemId+1
            itemSet[record.itemId] = itemId
        record.itemId = itemId

        recordList.append(record)

_init()

def _testData():
    if (len(recordList) != RATE_COUNT) :
        raise UnitTestError('recordList.size != RATE_COUNT')
    if (len(userSet) != USER_COUNT):
        raise UnitTestError('userSet.size != USER_COUNT')
    if (len(itemSet) != ITEM_COUNT):
        raise UnitTestError('itemSet.size != ITEM_COUNT')
    for record in recordList:
        if record.itemId<0 or record.itemId>=ITEM_COUNT:
            raise UnitTestError('wrong itemId')
        if record.userId<0 or record.userId>=USER_COUNT:
            raise UnitTestError('wrong userId')

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
    itemId = random.rand(0, ITEM_COUNT-1)
    records = itemUsers.get(itemId)
    for record1 in recordList:
        if record1.itemId == itemId:

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
    _testData()
    _testRandomSplit()
    _testExportTables()
