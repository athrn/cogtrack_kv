# -*- coding: utf-8 -*-

import abc

class IGame:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def stop(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def start(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def cancel(self):
        raise NotImplementedError()

    
