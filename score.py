#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from typing import List
import numpy as np
import logging
import math
import csv


class Score(metaclass=ABCMeta):
    
    _dic_usuaris = dict 
    _dic_items = dict
    _n_usuaris = int 
    _n_items = int
    _mat = np.array
    
    def __init__(self, fitxer_items,fitxer_valoracions):
        self._dic_usuaris = {}
        self._dic_items = {}
        self._mat = None
    
    def ll_items(self):
        """
        Retorna una llista amb els identificadors dels ítems.
        Returns
        -------
        list
            Llista d'ítems.
        """
        return list(self._dic_items.keys())
    
    def ll_usuaris(self):
        """
        Retorna una llista amb els identicicadors dels usuaris.

        Returns
        -------
        list
            Llista d'usuaris.
        """
        return list(self._dic_usuaris.keys())

    def min_vots(self,min_vots):
        """
        Retorna una llista d'ítems amb un mínim de vots.

        Parameters
        ----------
        min_vots : int
            Nombre mínim de vots.

        Returns
        -------
        list
            Llista amb els ids dels ítems amb un mínim de vots.
        """
        vector_num_vots = np.count_nonzero(self._mat, axis=0)
        uu = np.array(list(self._dic_items.keys()))
        ll = uu[vector_num_vots >= min_vots]
        return ll.tolist()
    
    def avg_usu(self, id_usuari) -> float:
        """
        Retorna la puntuació mitjana d'un usuari.

        Parameters
        ----------
        id_usuari : str
            Identificador de l'usuari.

        Returns
        -------
        float
            Puntuació mitjana de l'usuari.
        """
        fila=self._mat[self._dic_usuaris[id_usuari],:]
        sense_zeros = fila[fila != 0]
        if np.size(sense_zeros) != 0:
            return np.mean(sense_zeros)
        else:
            return 0
    
    def avg_item(self, id_item) -> float:
        """
        Retorna la puntuació mitjana d'un ítem.

        Parameters
        ----------
        id_item : str
            Identificador de l'ítem.

        Returns
        -------
        float
            Puntuació mitjana de l'ítem.
        """
        columna = self._mat[:,self._dic_items.get(id_item)]
        sense_zeros = columna[columna != 0]
        if len(sense_zeros) == 0:
            return 0
        else:
            return np.mean(sense_zeros)
        
    def num_vots(self, id_item):
        """
        Retorna el nombre de vots d'un ítem.

        Parameters
        ----------
        id_item : str
            Identificador de l'ítem.

        Returns
        -------
        int
            Nombre de vots de l'ítem.
        """
        columna = self._mat[:, self._dic_items[id_item]]
        return np.count_nonzero(columna)
    
    def avg_global(self, ll_id_items):
        """
        Retorna la puntuació mitjana global dels ítems considerats.

        Parameters
        ----------
        ll_id_items : list
            Llista d'identificadors d'ítems.

        Returns
        -------
        float
            Puntuació mitjana global dels ítems considerats.
        """
        item_indices = [self._dic_items.get(id_item) for id_item in ll_id_items]
        return np.mean(np.array([self.avg_item(id_item) for id_item in ll_id_items]))

    def no_vista(self, id_usuari, id_item):
        """
        Comprova si un ítem no ha estat vist per un usuari.

        Parameters
        ----------
        id_usuari : str
            Identificador de l'usuari.
        id_item : str
            Identificador de l'ítem.

        Returns
        -------
        bool
            True si l'ítem no ha estat vist per l'usuari, False altrament.
        """
        if self._mat[self._dic_usuaris[id_usuari], self._dic_items[id_item]] == 0:
            return True
        else:
            return False
    
    def similitud(self,usuari_client,usuari_secundari):
        """
        Calcula la similitud entre dos usuaris.

        Parameters
        ----------
        usuari_client : str
            Identificador de l'usuari client.
        usuari_secundari : str
            Identificador de l'usuari secundari.

        Returns
        -------
        float
            Similitud entre els dos usuaris.
        """
        numerador=0
        denominador1=0
        denominador2=0
        index_usu_client=self._dic_usuaris[usuari_client]
        index_usu_sec=self._dic_usuaris[usuari_secundari]
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
        """
        Retorna el vector de puntuacions d'un usuari.

        Parameters
        ----------
        id_user : str
            Identificador de l'usuari.

        Returns
        -------
        np.ndarray
            Vector de puntuacions de l'usuari.
        """
        return self._mat[self._dic_usuaris[id_user],:]
    
    def max(self):
        """
        Retorna la puntuació màxima en la matriu.

        Returns
        -------
        float
            Puntuació màxima en la matriu.
        """
        return self._mat.max()
    
    def item_features(self, fitxer_items):
        """
        Retorna les característiques dels ítems.

        Parameters
        ----------
        fitxer_items : str
            Nom del fitxer d'ítems.

        Returns
        -------
        list
            Llista de característiques dels ítems.
        """
        item_features = []
        with open(fitxer_items, 'r', encoding='utf-8') as f:
            next(f)
            reader = csv.reader(f)
            for line in reader:
                if len(item_features) < 50000:
                    generes = line[-1]
                    id_item = line[0]
                    if id_item in self._dic_items:
                        item_features.append(generes)
                else:
                    break
        return item_features
    
    
    def usuari_a_avaluar(self):
        """
        Retorna el primer usuari amb almenys una valoració feta per poder utilitzar l'avaluador.'

        Returns
        -------
        str
            Id del primer usuari amb el que podem utilitzar la opció avaluació.
        """
        ha_puntuat = False
        i = 0
        while not ha_puntuat:
            if np.count_nonzero(self._mat[i,:]) != 0:
                usuari_rata = list(self._dic_usuaris.keys())[i]
                ha_puntuat = True
            i += 1
        return logging.info(f"Primer usuari amb alguna puntuació: {usuari_rata}")

class ScoreMovies(Score):
    """
    Classe per calcular puntuacions de pel·lícules.

    Methods
    -------
    __init__(fitxer_items, fitxer_valoracions)
        Inicialitza un nou objecte ScoreMovies.
    """
    
    _ll_usuaris = dict 
    _ll_items = dict
    _n_usuaris = int 
    _n_items = int
    
    def __init__(self, fitxer_items,fitxer_valoracions):
        """
        Inicialitza un nou objecte ScoreMovies.

        Parameters
        ----------
        fitxer_items : str
            Nom del fitxer d'ítems.
        fitxer_valoracions : str
            Nom del fitxer de valoracions.
        """
        super().__init__(fitxer_items, fitxer_valoracions) 
        
        logging.info("Inicialitzant ScoreMovies")
        with open(fitxer_valoracions, 'r') as f:
            next(f) 
            i_usu = 0
            i_item = 0
            for line in f:
                if len(self._dic_items) < 50000:
                    id_usuari, id_item, _ , _ = line.strip().split(',')
                    if id_usuari not in self._dic_usuaris.keys():
                        self._dic_usuaris[id_usuari] = i_usu
                        i_usu += 1
                    if id_item not in self._dic_items.keys():    
                        self._dic_items[id_item] = i_item
                        i_item += 1
                else:
                    break

        #self._ll_usuaris = list(sorted(set(self._ll_usuaris)))
        #self._ll_items = list(sorted(set(self._ll_items)))
        self._n_usuaris, self._n_items = len(self._dic_usuaris), len(self._dic_items)
        self._mat = np.zeros((self._n_usuaris, self._n_items), dtype='float16')
        
        logging.info("Carregant dades de valoracions")
        with open(fitxer_valoracions, 'r') as f:
            next(f) 
            for line in f:
                id_usuari, id_item, score, _ = line.strip().split(',')
                score = float(score)
                self._mat[self._dic_usuaris[id_usuari], self._dic_items[id_item]] = score 
        
        logging.info(f"Usuaris carregats: {self._n_usuaris}")
        logging.info(f"Pelis carregades: {self._n_items}")
    


class ScoreBooks(Score):
    """
    Classe per calcular puntuacions de llibres.

    Methods
    -------
    __init__(fitxer_items, fitxer_valoracions)
        Inicialitza un nou objecte ScoreBooks.
    """
     
    _ll_usuaris = dict 
    _ll_items = dict
    _n_usuaris = int 
    _n_items = int
    
    def __init__(self, fitxer_items,fitxer_valoracions):
        """
        Inicialitza un nou objecte ScoreBooks.

        Parameters
        ----------
        fitxer_items : str
            Nom del fitxer d'ítems.
        fitxer_valoracions : str
            Nom del fitxer de valoracions.
        """
        super().__init__(fitxer_items, fitxer_valoracions) 
        
        logging.info("Inicialitzant ScoreBooks")
        i_item = 0
        with open(fitxer_items, 'r') as f:
           next(f)
           for line in f:
               if len(self._dic_items) < 10000:
                   line=line.strip().split(',')
                   id_item = line[0]
                   if id_item not in self._dic_items.keys():
                       self._dic_items[id_item] = i_item
                       i_item += 1
               else:
                   break 
        i_usu = 0
        with open('Books/Users.csv') as f:
            next(f)
            for line in f:
                if len(self._dic_usuaris) < 7000:
                    line=line.strip().split(',')
                    id_usuari = line[0]
                    if id_usuari not in self._dic_usuaris.keys():
                        self._dic_usuaris[id_usuari] = i_usu
                        i_usu += 1
                else:
                    break


        #self._ll_usuaris = list(sorted(self._ll_usuaris))
        #self._ll_items = list(sorted(self._ll_items))
        
        self._n_usuaris, self._n_items = len(self._dic_usuaris), len(self._dic_items)
        self._mat = np.zeros((self._n_usuaris, self._n_items), dtype='float16')
        
        #print('Shape mat:')
        #print(self._mat.shape)
        logging.info("Carregant dades de valoracions")
        with open(fitxer_valoracions, 'r') as f:
            next(f) 
            i = 0
            for line in f:
                if i < 600000:
                    line = line.strip().split(',')
                    id_usuari = line[0]
                    id_item = line[1]
                    try:
                        score = float(line[2])
                        if (id_usuari in self._dic_usuaris) and (id_item in self._dic_items):
                            self._mat[self._dic_usuaris[id_usuari], self._dic_items[id_item]] = score
                        i += 1
                    except ValueError:
                        pass
                else:
                   break
        logging.info(f"Usuaris carregats: {self._n_usuaris}")
        logging.info(f"Llibres carregats: {self._n_items}")
    
        
               
     
class ScoreAnimes(Score):
    """
    Classe per calcular puntuacions d'animes.

    Methods
    -------
    __init__(fitxer_items, fitxer_valoracions)
        Inicialitza un nou objecte ScoreAnimes.
    """
    
    _ll_usuaris = dict
    _ll_items = dict
    _n_usuaris = int 
    _n_items = int
    
    def __init__(self, fitxer_items,fitxer_valoracions):
        """
        Inicialitza un nou objecte ScoreAnimes.

        Parameters
        ----------
        fitxer_items : str
            Nom del fitxer d'ítems.
        fitxer_valoracions : str
            Nom del fitxer de valoracions.
        """
        super().__init__(fitxer_items, fitxer_valoracions) 
        
        logging.info("Inicialitzant ScoreAnimes")       #Potser fer que la carrega sigui una funcion en comptes de a l'init per fer herència amb Movies?
        with open(fitxer_valoracions, 'r') as f:
            next(f)
            i_usu = 0
            i_item = 0
            for line in f:
                if len(self._dic_items) < 50000:
                    id_usuari, id_item, _ = line.strip().split(',')
                    if id_usuari not in self._dic_usuaris:
                        self._dic_usuaris[id_usuari] = i_usu
                        i_usu += 1
                    if id_item not in self._dic_items:    
                        self._dic_items[id_item] = i_item
                        i_item += 1
                else:
                    break

        #self._ll_usuaris = list(sorted(set(self._ll_usuaris)))
        #self._ll_items = list(sorted(set(self._ll_items)))
        self._n_usuaris, self._n_items = len(self._dic_usuaris), len(self._dic_items)
        self._mat = np.zeros((self._n_usuaris, self._n_items), dtype='float16')
        
        logging.info("Carregant dades de valoracions")
        with open(fitxer_valoracions, 'r') as f:
            next(f) 
            for line in f:
                id_usuari, id_item, score = line.strip().split(',')
                score = 0 if float(score) == -1 else float(score)
                self._mat[self._dic_usuaris[id_usuari], self._dic_items[id_item]] = score
        logging.info(f"Usuaris carregats: {self._n_usuaris}")
        logging.info(f"Animes carregats: {self._n_items}")