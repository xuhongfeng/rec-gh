#!/usr/bin/env python

from data import Record, ItemUsers, UserItems
from exception import UnitTestError
import dataSet
import random
import numpy as np
from numpy import ndarray
import os.path

CACHE_DIR = 'data/cache'
CACHE_CORELATED_MATRIX_FILE = CACHE_DIR + '/corelated_matrix.npy'

if (not os.path.exists(CACHE_DIR)):
    os.makedirs(CACHE_DIR)

def calCorelatedMatrix(itemUsers, userCount, useCache=False):
    size = userCount
    m = None
    if useCache and os.path.exists(CACHE_CORELATED_MATRIX_FILE):
        m = np.load(CACHE_CORELATED_MATRIX_FILE)
        if m.shape != (userCount, userCount):
            print str(m.shape)
            print 'userCount=%d' % userCount
            m = None
    if m is None:
        m = np.zeros((size, size))
        for records in itemUsers.listRecordList():
            count = len(records)
            for i in range(0, count-1):
                for j in range(i+1, count):
                    id1, id2 = records[i].userId, records[j].userId
                    m[id1][id2] = m[id1][id2]+1
                    m[id2][id1] = m[id2][id1]+1
        if useCache:
            np.save(CACHE_CORELATED_MATRIX_FILE, m)
    return m

def _testCalCorelatedMatrix():
    itemUsers, userItems = dataSet.exportTables()
    userCount = dataSet.USER_COUNT
    m = calCorelatedMatrix(itemUsers, userCount, True)
    if m.shape != (userCount, userCount):
        print 'userCount=%d' % userCount
        raise UnitTestError('wrong matrix shape')

    userId1 = random.randint(0, userCount-1)
    userId2 = userId1
    while userId2==userId1:
        userId2 = random.randint(0, userCount-1)

    while True:
        items1 = userItems.get(userId1)
        items2 = userItems.get(userId2)
        print items1
        count = 0
        if items1 is None or items2 is None:
            count = 0
        else:
            for record1 in items1:
                for record2 in items2:
                    if record1.itemId == record2.itemId:
                        count = count +1
                        break
        if m[userId1][userId2]!=count or m[userId2][userId1]!=count:
            print exportItemIds(items1)
            print exportItemIds(items2)
            raise UnitTestError('wrong corelated matrix, except %d, but %d %d' \
                % (count, m[userId1][userId2], m[userId2][userId1]))
        if count != 0:
            break

def exportItemIds(recordList):
    def getItemId(record):
        return record.itemId
    return map(getItemId, recordList)

def exportUserIds(recordList):
    def getUserId(record):
        return record.userId
    return map(getUserId, recordList)

if __name__ == '__main__':
    _testCalCorelatedMatrix()
