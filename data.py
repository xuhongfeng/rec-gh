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

    def __str__(self):
        return self.serialize()

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, self.__class__)\
            and self.itemId==other.itemId\
            and self.userId==other.userId\
            and self.rate==other.rate\
            and self.time==other.time
    def __ne__(self, other):
        return not self.__eq__(other)

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
    
    def _keys(self):
        return self._map.keys()

    def listRecordList(self):
        """ return list of recordList """
        return self._map.values()

    def size(self) :
        return len(self._map)

    def get(self, key):
        return self._map.get(key)

class ItemUsers(_BaseRevertedTable):
    def _key(self, record):
        return record.itemId

    def itemIds(self):
        return self._keys()


class UserItems(_BaseRevertedTable):
    def _key(self, record):
        return record.userId
