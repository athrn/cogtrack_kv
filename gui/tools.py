from kivy.lang import Builder
import os

class PrettyProperties(object):
    def __init__(self, **kwargs):        
        # self.as_dict = dict(kwargs)
        for k,v in kwargs.items():
            setattr(self, k, v)


def load_kv(pyfile):
    root, ext = os.path.splitext(pyfile)
    kvfile = root + '.kv'
    return Builder.load_file(kvfile)
