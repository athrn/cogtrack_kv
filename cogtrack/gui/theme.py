# -*- coding: utf-8 -*-
from tools import NamedProperties as prop

theme = prop(
    default=prop(
        font_size='24sp',
        # NOTE: Scaling of icon is really poor. Both upscaling and down scaling.
        icon_size='48sp',
        button_size=('180sp', '60sp'),
        button_height='60sp',
        # TODO: Rename to text_size_hint
        size_hint_y=0.8, # Size of text inside box.
        size_hint_x=0.8, # Size of text inside box.
        control_bar_height='48sp',
        ),
    color=prop(
        button_background=(.7, .7, 1, 1),
        no_response=(1, 1, 0, 1),
        wrong=(1, 0, 0, 1),
        wrong2=(1, 0.5, 0, 1),
        correct2=(0.75, 1, 0, 1),
        correct=(0, 1, 0, 1)
        ))

        

if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_theme', failfast=True, exit=False)


