# -*- coding: utf-8 -*-
import os
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.clock import Clock

class NamedProperties(dict):
    def __init__(self, **kwargs):
        # dict.__init__(self, kwargs)
        self._dict = dict(kwargs)
        
        for k,v in kwargs.items():
            setattr(self, k, v)

def load_kv(pyfile):
    """
    Load a kv file with the same base name as file and in the same directory.
    """
    root, ext = os.path.splitext(os.path.abspath(pyfile))
    kvfile = root + '.kv'
    Logger.info('Loading ' + kvfile)
    return Builder.load_file(kvfile)


def schedule(timeout, func):
    Clock.schedule_once(func, timeout)


def print_traceback():
    from pprint import pprint
    import traceback
    f = ['{}:{} ({})'.format(name,line,func) for name,line,func,_ in traceback.extract_stack()]
    pprint(f)

if __name__ == "__main__":
    print_traceback()
    
    import unittest as ut
    ut.main(module='test_tools', failfast=True, exit=False)


