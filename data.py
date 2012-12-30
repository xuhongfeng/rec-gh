#!/usr/bin/env python

import re

_PATTERN = re.compile('^([\d]+)[\s]+([\d]+)[\s]+([\d]+)[\s]+([\d]+)')

class Record(object):
    userId = None
    itemId = None
    rate = None
    time = None

    def __init__(self, userId, itemId, rate, time ):
        self.userId = userId
        self.itemId = itemId
        self.rate = rate
        self.time = time

    def serialize(self):
        return "%d %d %d %d" % (self.userId, self.itemId, self.rate, self.time)

    @staticmethod
    def deserialize(line):
        m = _PATTERN.match(line)
        userId = int(m.group(1))
        itemId = int(m.group(2))
        rate = int(m.group(3))
        time = int(m.group(4))
        return Record(userId, itemId, rate, time)

class _BaseRevertedTable(object):
    _map = None

    def __init__(self):
        self._map = {}

    def add(self, record):
        key = self._key(record)
        tList = self._map.get(key)
        if tList is None:
            tList = []
            self._map[key] = tList 
        tList.append(record)
    
    def _key(self, record):
        """ abstract method """
        pass

    def recordCount(self):
        count = 0
        for userList in self._map.values():
            count += len(userList)
        return count

class ItemUsers(_BaseRevertedTable):
    def _key(self, record):
        return record.itemId

class UserItems(_BaseRevertedTable):
    def _key(self, record):
        return record.userId
