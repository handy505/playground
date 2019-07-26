#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class InverterProxy(metaclass=ABCMeta):
    @abstractmethod
    def sync_with_hardware(self): pass

    @abstractmethod
    def create_record(self): pass

