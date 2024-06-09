#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 19:39:23 2024

@author: aliciamartilopez
"""

from recomanacions import RecomanacioSimple, RecomanacioBasadaEnContingut, RecomanacioColaborativa, Recomanacio
from items import Item, Movie, Book
import math
import numpy as np
from abc import ABCMeta, abstractmethod


class Recomender(metaclass=ABCMeta):
    _recomanacio = Recomanacio
    _fitxer_items = str
    _fitxer_valoracions = str
    
    def __init__(self, dataset: str, method:str):
        if method == 'simple':
            self._recomanacio = RecomanacioSimple(self._fitxer_items, self._fitxer_valoracions, dataset)
        elif method == 'colaboratiu':
            self._recomanacio = RecomanacioColaborativa(self._fitxer_items, self._fitxer_valoracions, dataset)
        else:
            self._recomanacio = RecomanacioBasadaEnContingut(self._fitxer_items, self._fitxer_valoracions, dataset)
        
    def programa_principal(self):
        accio = "u"
        while accio != "3":
            accio = input("Acció:\n     1 - Recomanació\n     2 - Avaluació\n     3 - Sortir\n")
            accions = ['1', '2', '3']
            while accio not in accions:
                print("ERROR: Acció no disponible.")
                accio = input("Acció:\n     1 - Recomanació\n     2 - Avaluació\n     3 - Sortir\n")
            
            if accio == '1':
                id_usuari = input("Identificador d'usuari: ")
                puntuacions, ids_items_recomanats = self._recomanacio.recomana_per(id_usuari)
                
                for id_item in ids_items_recomanats:
                    I = self.crea_item(id_item, self._fitxer_valoracions,self._fitxer_items)
                    if I:
                        print('\n'+str(I))
                    else:
                        print('Item no carregat')
            elif accio == '2':
                id_usuari = input("Identificador d'usuari: ")
                
                prediccions, ids_items_recomanats = self._recomanacio.recomana_per(id_usuari)
                valoracions_usuari = self._recomanacio.valoracions_usuari(id_usuari)
                c = valoracions_usuari != 0.0
                
                mae = (np.sum(abs(prediccions[c] - valoracions_usuari[c]))) / np.count_nonzero(valoracions_usuari)
                rmse = math.sqrt((np.sum((valoracions_usuari[c] - prediccions[c])**2))/np.count_nonzero(valoracions_usuari))
                
                print('MAE:',mae)
                print('RMSE:',rmse)
            else:
                print('Sortint...')
                break 
    
    def crea_item(self, id_item, fitxer_valoracions, fitxer_items):
        raise NotImplementedError()



class RecomenderMovies(Recomender):
    
    _recomanacio = Recomanacio
    _fitxer_items = str
    _fitxer_valoracions = str
    
    def __init__(self, dataset: str, method:str):
        self._fitxer_items = 'MovieLens100k/movies.csv'
        self._fitxer_valoracions = 'MovieLens100k/ratings.csv'
        super().__init__(dataset, method)
    
    def crea_item(self, id_item, fitxer_valoracions, fitxer_items):
        return Movie(id_item, fitxer_valoracions, fitxer_items)
    


class RecomenderBooks(Recomender):
    
    _recomanacio = Recomanacio
    _fitxer_items = str
    _fitxer_valoracions = str
    
    def __init__(self, dataset: str, method:str):
        self._fitxer_items = 'Books/Books.csv'
        self._fitxer_valoracions = 'Books/Ratings.csv'
        super().__init__(dataset, method)
    
    def crea_item(self, id_item, fitxer_valoracions, fitxer_items):
        return Book(id_item, fitxer_valoracions, fitxer_items)

