from kivy.lang import Builder
import os

def load_kv(pyfile):
    root, ext = os.path.splitext(pyfile)
    kvfile = root + '.kv'
    return Builder.load_file(kvfile)
