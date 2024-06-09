#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import csv
from abc import ABCMeta, abstractmethod

class Item(metaclass=ABCMeta):

    _titol: str
    _ID: str
    _extra: str


    def __init__(self, ID=0, nomFitxerValoracions="", nomFitxerTitols=""):
        self._titol = ""
        self._ID = ID
        self._extra = ''
        with open(nomFitxerTitols, 'r', encoding='utf-8') as f:
            next(f)
            reader = csv.reader(f)
            for line in reader:
                if line[0] == self._ID:
                    self._titol=line[1]
                    self._extra=line[2]
                    break
    def __str__(self):
        
        if self._titol:
            resposta = ''
            resposta += 'TITOL: '+self._titol+'\n'
            return resposta
        else: 
            return None
        


class Book(Item):

    _autor: str
    def __init__(self, ID = 0, nomFitxerValoracions = "", nomFitxerTitols = "", autor = ""):

        super().__init__(ID, nomFitxerValoracions, nomFitxerTitols)
        with open(nomFitxerTitols, 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                if line[0] == self._ID:
                    self._autor = line[2]
    
    def __str__(self):
        if self._titol:
            resposta = super().__str__()
            resposta += 'AUTOR: '+self._autor+'\n'
            return resposta
        else:
            return None

class Movie(Item):
    _generes: list = []

    def __init__(self, ID = 0, nomFitxerValoracions = "", nomFitxerTitols = "", generes = []):
        super().__init__(ID, nomFitxerValoracions, nomFitxerTitols)
        self._generes = self._extra[:].split('|')

    def __str__(self):
        if self._titol:
            resposta = super().__str__()
            resposta += 'GENERES: '+str(self._generes)
            return resposta
        else:
            return None
