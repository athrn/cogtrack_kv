import sys
from os.path import abspath, join, dirname, pardir, exists
from kivy.resources import resource_add_path

main_files='__main__.py'.split()

main_dir = None
cur_dir = dirname(__file__)
while not main_dir:
    for main_file in main_files:
        if exists(join(cur_dir, main_file)):
            main_dir=cur_dir

    parent_dir = abspath(join(cur_dir, pardir))

    if parent_dir == cur_dir:
        break

    cur_dir = parent_dir

class ConfigurationError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

if main_dir:
    resource_add_path(main_dir)
    sys.path.append(main_dir)
else:
    raise ConfigurationError('Main dir not found')
