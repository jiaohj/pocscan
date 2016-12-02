# -*- coding: utf-8 -*-
import os
import environ

p = environ.Path(__file__) - 2


def root(*paths, **kwargs):
    ensure = kwargs.pop('ensure', False)
    path = p(*paths, **kwargs)
    if ensure and not os.path.exists(path):
        os.makedirs(path)
    return path
