#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from typing import List
from abc import ABCMeta, abstractmethod
import math
from scipy.sparse import lil_matrix
import csv
import logging

class Score(metaclass=ABCMeta):
    
    _ll_usuaris = list 
    _ll_items = list
    _n_usuaris = int 
    _n_items = int
    _mat = np.array
    
    def __init__(self, fitxer_items,fitxer_valoracions):
        self._ll_usuaris = []
        self._ll_items = []
        self._mat = None
    
    def ll_items(self):
        return self._ll_items
    
    def ll_usuaris(self):
        return self._ll_usuaris

    def min_vots(self,min_vots):
        ll = []
        for index, id_item in enumerate(self._ll_items):
            if np.count_nonzero(self._mat[:,index]) >= min_vots:
                ll.append(id_item)
        return ll
    
    def avg_usu(self, id_usuari) -> float:
        fila=self._mat[self._ll_usuaris.index(id_usuari),:]
        sense_zeros = fila[fila > 0]
        return np.mean(sense_zeros)
    
    def avg_item(self, id_item) -> float:
        """
        avg_item: valoració mitja que li han donat els usuaris a l’ítem (considerant
        només els vots rebuts, descartem valoracions amb un 0).
        """
        columna = self._mat[:,self._ll_items.index(id_item)]
        sense_zeros = columna[columna > 0]
        return np.mean(sense_zeros)
    
    def num_vots(self, id_item):
        """
        num_vots: nº d’usuaris que han puntuat aquest ítem
        """
        columna = self._mat[:, self._ll_items.index(id_item)]
        return np.count_nonzero(columna)
    
    def avg_global(self, ll_id_items):
        """
        avg_global: valoració mitja de tots els ítems considerats
        """
        suma = 0
        for id_item in ll_id_items:
            suma += self.avg_item(id_item)
        return suma/len(ll_id_items)

    def no_vista(self, id_usuari, id_item):
        if self._mat[self._ll_usuaris.index(id_usuari), self._ll_items.index(str(id_item))] == 0:
            return True
        else:
            return False
    
    def similitud(self,usuari_client,usuari_secundari):
        numerador=0
        denominador1=0
        denominador2=0
        index_usu_client=self._ll_usuaris.index(usuari_client)
        index_usu_sec=self._ll_usuaris.index(usuari_secundari)
        num_rows, _ = self._mat.shape
        for j in range(num_rows):
            v_usuari_client=self._mat[index_usu_client][j]
            v_usuari_secundari=self._mat[index_usu_sec][j]
            if v_usuari_client!=0 and v_usuari_secundari!=0:
                numerador+=v_usuari_client*v_usuari_secundari
                denominador1+=(v_usuari_secundari)**2
                denominador2+=(v_usuari_client)**2
        
        if numerador!=0 and denominador1!=0 and denominador2!=0:
            return numerador/(math.sqrt(denominador1)*math.sqrt(denominador2))
        else:
            return 0
    
    
    def vector_puntuacions(self, id_user):
        return self._mat[self._ll_usuaris.index(id_user),:]
    
    def max(self):
        return self._mat.max()
    
    def item_features(self, fitxer_items):
        item_features = []
        with open(fitxer_items, 'r') as f:
            next(f)
            reader = csv.reader(f)
            for line in reader:
                generes = line[-1]
                id_item = line[0]
                if id_item in self._ll_items:
                    item_features.append(generes)
        return item_features

class ScoreMovies(Score):
    
    _ll_usuaris = set 
    _ll_items = set
    _n_usuaris = int 
    _n_items = int
    
    def __init__(self, fitxer_items,fitxer_valoracions):
        super().__init__(fitxer_items, fitxer_valoracions) 
        
        logging.info("Inicialitzant ScoreMovies")
        with open(fitxer_valoracions, 'r') as f:
            next(f) 
            for line in f:
                if len(self._ll_items) < 50000:
                    id_usuari, id_item, _ , _ = line.strip().split(',')
                    self._ll_usuaris.append(id_usuari)
                    self._ll_items.append(id_item)
                else:
                    break

        #self._ll_usuaris = list(sorted(self._ll_usuaris))
        #self._ll_items = list(sorted(self._ll_items))
        self._n_usuaris, self._n_items = len(self._ll_usuaris), len(self._ll_items)
        self._mat = np.zeros((self._n_usuaris, self._n_items), dtype='float16')
        
        logging.info("Carregant dades de valoracions")
        with open(fitxer_valoracions, 'r') as f:
            next(f) 
            for line in f:
                id_usuari, id_item, score, _ = line.strip().split(',')
                score = float(score)
                self._mat[self._ll_usuaris.index(id_usuari), self._ll_items.index(id_item)] = score 
    


class ScoreBooks(Score):
     
    _ll_usuaris = set 
    _ll_items = set
    _n_usuaris = int 
    _n_items = int
    
    def __init__(self, fitxer_items,fitxer_valoracions):
        super().__init__(fitxer_items, fitxer_valoracions) 
        
        logging.info("Inicialitzant ScoreBooks")
        with open(fitxer_items, 'r') as f:
           next(f)
           for line in f:
               if len(self._ll_items) < 10000:
                   line=line.strip().split(',')
                   id_item = line[0]
                   self._ll_items.append(id_item)
               else:
                   break 
        with open('Books/Users.csv') as f:
           next(f)
           for line in f:
               line=line.strip().split(',')
               id_usuari = line[0]
               self._ll_usuaris.append(id_usuari)


        #self._ll_usuaris = list(sorted(self._ll_usuaris))
        #self._ll_items = list(sorted(self._ll_items))
        
        self._n_usuaris, self._n_items = len(self._ll_usuaris), len(self._ll_items)
        self._mat = np.zeros((self._n_usuaris, self._n_items), dtype='float16')
        
        #print('Shape mat:')
        #print(self._mat.shape)
        logging.info("Carregant dades de valoracions")
        with open(fitxer_valoracions, 'r') as f:
            next(f) 
            i = 1
            for line in f:
               if i < 10000:
                   line = line.strip().split(',')
                   
                   id_usuari = line[0]
                   id_item = line[1]
                   score = float(line[2])
                   #print('line', line)
                   #print('id_usuari', id_usuari)
                   #print('id_item', id_item)
                   #print('score', score)
                   #id_usuari, id_item, score = line.strip().split(',')
                   #score = float(score)
                   #print(i)
                   if (id_usuari in self._ll_usuaris) and (id_item in self._ll_items):
                       self._mat[self._ll_usuaris.index(id_usuari), self._ll_items.index(id_item)] = score
                   i += 1
               else:
                   logging.info(self._mat[7,1])
                   logging.info(self._ll_usuaris[7])
                   logging.info(self._ll_items[1])
                   break
               
     
