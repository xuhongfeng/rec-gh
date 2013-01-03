#!/usr/bin/env python

class UnitTestError(Exception):
    _msg = None

    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg
    
