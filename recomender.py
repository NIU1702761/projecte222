#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from recomanacions import RecomanacioSimple, RecomanacioBasadaEnContingut, RecomanacioColaborativa, Recomanacio
from items import Item, Movie, Book
import math
import numpy as np
from abc import ABCMeta, abstractmethod
import logging


class Recomender(metaclass=ABCMeta):
    _recomanacio = Recomanacio
    _fitxer_items = str
    _fitxer_valoracions = str
    
    def __init__(self, dataset: str, method:str):
        logging.info(f"Inicialitzant Recomender amb dataset: {dataset} i method: {method}")
        if method == 'simple':
            self._recomanacio = RecomanacioSimple(self._fitxer_items, self._fitxer_valoracions, dataset)
        elif method == 'colaboratiu':
            self._recomanacio = RecomanacioColaborativa(self._fitxer_items, self._fitxer_valoracions, dataset)
        else:
            self._recomanacio = RecomanacioBasadaEnContingut(self._fitxer_items, self._fitxer_valoracions, dataset)
        
    def programa_principal(self):
        accio = "u"
        while accio != "3":
            accio = input("Acció:\n     1 - Recomanació\n     2 - Avaluació\n     3 - Sortir\nTria: ")
            accions = ['1', '2', '3']
            while accio not in accions:
                logging.error("ERROR: Acció no disponible.")
                accio = input("Acció:\n     1 - Recomanació\n     2 - Avaluació\n     3 - Sortir\nTria: ")
            
            if accio == '1':
                id_usuari = input("Identificador d'usuari: ")
                logging.info(f"Recomanació per l'usuari: {id_usuari}")
                puntuacions, ids_items_recomanats = self._recomanacio.recomana_per(id_usuari)
                
                if puntuacions is not None:
                    for id_item in ids_items_recomanats:
                        I = self.crea_item(id_item, self._fitxer_valoracions,self._fitxer_items)
                        if I:
                            print('\n'+str(I))
                        else:
                            logging.warning(f'Item no carregat: {id_item}')
                            #print('Item no carregat')
            elif accio == '2':
                id_usuari = input("Identificador d'usuari: ")
                logging.info(f"Avaluació per l'usuari: {id_usuari}")
                
                prediccions, ids_items_recomanats = self._recomanacio.recomana_per(id_usuari)
                
                if prediccions is not None:
                    valoracions_usuari = self._recomanacio.valoracions_usuari(id_usuari)
                    c = valoracions_usuari != 0.0
                    
                    mae = (np.sum(abs(prediccions[c] - valoracions_usuari[c]))) / np.count_nonzero(valoracions_usuari)
                    rmse = math.sqrt((np.sum((valoracions_usuari[c] - prediccions[c])**2))/np.count_nonzero(valoracions_usuari))
                    
                    logging.info(f"MAE: {mae}")
                    logging.info(f"RMSE: {rmse}")
                    #print('MAE:',mae)
                    #print('RMSE:',rmse)
            else:
                logging.info('Sortint...')
                #print('Sortint...')
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
        logging.debug(f"Creant item Movie amb id: {id_item}")
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
        logging.debug(f"Creant item Book amb id: {id_item}")
        return Book(id_item, fitxer_valoracions, fitxer_items)

