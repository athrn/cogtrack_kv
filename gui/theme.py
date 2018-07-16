# -*- coding: utf-8 -*-
from tools import NamedProperties as prop

theme = prop(
    default=prop(
        text_height='18dp',
        size_ratio=0.8, # Size of text inside box.
        ),
    color=prop(
        button_background=(.7, .7, 1, 1),
        wrong=(1, 0, 0, 1),
        wrong2=(1, 0, 0.5, 1),
        correct2=(0.5, 0, 1, 1),
        correct=(0, 0, 1, 1)
        ))

        
if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_theme', failfast=True, exit=False)


