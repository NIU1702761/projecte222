#!/usr/bin/env python3
# -*- coding: utf-8 -*

from score import Score, ScoreBooks, ScoreMovies
from abc import ABCMeta, abstractmethod
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
import csv


class Recomanacio(metaclass=ABCMeta):
    _score = Score
    
    def __init__(self, fitxer_items: str, fitxer_valoracions:str, dataset: str):
        if dataset == 'movielens100k':
            self._score = ScoreMovies(fitxer_items, fitxer_valoracions)
        else:
            self._score = ScoreBooks(fitxer_items, fitxer_valoracions)
    
    def recomana_per(self, id_usuari):
        raise NotImplementedError()
    
    def valoracions_usuari(self, id_usuari):
        return self._score.vector_puntuacions(id_usuari)


class RecomanacioSimple(Recomanacio):
    
    def __init__(self, fitxer_items: str, fitxer_valoracions: str, dataset: str):    
        super().__init__(fitxer_items, fitxer_valoracions, dataset)
    
    def recomana_per(self, id_usuari):
        min_vots = int(input('Minim vots: '))
        items_a_considerar = self._score.min_vots(min_vots)
        ll_items = self._score.ll_items()
        
        puntuacions = np.zeros(len(ll_items))
        avg_global = self._score.avg_global(items_a_considerar)
        
        for id_item in ll_items:
            num_vots = self._score.num_vots(id_item)
            avg_item = self._score.avg_item(id_item)
            puntuacio = ((num_vots/(num_vots+min_vots))*avg_item)+((min_vots/(num_vots+min_vots))*avg_global)
            puntuacions[ll_items.index(id_item)] = puntuacio
        
        copia_puntuacions = puntuacions.copy()
        copia_puntuacions = copia_puntuacions.tolist()
        items = []
        while len(items) < 5:
            index_maxim = copia_puntuacions.index(max(copia_puntuacions))
            id_item = ll_items[index_maxim]
            if id_item in items_a_considerar:
                if self._score.no_vista(id_usuari, id_item):
                    items.append(id_item)
            copia_puntuacions.pop(index_maxim)
            ll_items.pop(index_maxim)
        return puntuacions, items
    

class RecomanacioColaborativa(Recomanacio):
    
    def __init__(self, fitxer_items: str, fitxer_valoracions: str, dataset: str):    
        super().__init__(fitxer_items, fitxer_valoracions, dataset)
    
    def recomana_per(self, id_usuari):
        similituds=[]
        ll_items = self._score.ll_items()
        for usuari in self._score.ll_usuaris():
            s=self._score.similitud(id_usuari,usuari)
            similituds.append((usuari,s))
        k = 5
        similituds.sort(key=lambda x: x[1], reverse=True)
        k_similituds = similituds[:k+2][1:]
        usuaris_similars = [x[0] for x in k_similituds]
        
        puntuacions = np.zeros(len(ll_items))
        mitjana_usu=self._score.avg_usu(id_usuari)
        for item in ll_items:
            numerador=0
            denominador=0
            
            for usuari in usuaris_similars:
                i=usuaris_similars.index(usuari)
                mitjana=self._score.avg_usu(usuari)
                numerador += k_similituds[i][1]*(self._score._mat[self._score.ll_usuaris().index(usuari)][self._score.ll_items().index(item)]-mitjana)
                denominador+=k_similituds[i][1]
            puntuacio=numerador/denominador
            puntuacions[ll_items.index(item)] = mitjana_usu + puntuacio
        
        copia_puntuacions = puntuacions.copy()
        copia_puntuacions = copia_puntuacions.tolist()
        items = []
        while len(items) < 5:
            index_maxim = copia_puntuacions.index(max(copia_puntuacions))
            id_item = ll_items[index_maxim]
            if self._score.no_vista(id_usuari, id_item):
                items.append(id_item)
            copia_puntuacions.pop(index_maxim)
            ll_items.pop(index_maxim)
        return puntuacions, items
        


class RecomanacioBasadaEnContingut(Recomanacio):
    
    def __init__(self, fitxer_items: str, fitxer_valoracions: str, dataset: str):    
        super().__init__(fitxer_items, fitxer_valoracions, dataset)
        self._fitxer_items = fitxer_items
        
    def recomana_per(self, id_usuari):
        ll_items = self._score.ll_items()
        item_features = self._score.item_features(self._fitxer_items)

        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(item_features).toarray()
        
        vector_puntuacions = self._score.vector_puntuacions(id_usuari)
        
        mat_numerador = np.copy(tfidf_matrix)
        for i in range(len(vector_puntuacions)):
            mat_numerador[i,:] = mat_numerador[i,:]*vector_puntuacions[i]
       
        perfil_user = np.sum(mat_numerador, axis=0)
        
        valor_normalitzador = np.sum(vector_puntuacions)
        Q = perfil_user / valor_normalitzador
        
        S = np.dot(tfidf_matrix, Q)
        
        p_final = S * self._score.max()
        
        items = []
        copia_puntuacions = p_final.copy()
        while len(items) < 5:
            index = np.argmax(copia_puntuacions)
            id_item = ll_items[index]
            if self._score.no_vista(id_usuari, id_item):
                items.append(id_item)
            copia_puntuacions = np.delete(copia_puntuacions, index)
            ll_items.pop(index)
        return p_final, items