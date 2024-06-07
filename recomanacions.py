#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 20:36:21 2024

@author: aliciamartilopez
"""

from score import Score, ScoreBooks, ScoreMovies
from abc import ABCMeta, abstractmethod
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import csv


class Recomanacio(metaclass=ABCMeta):
    _score = Score
    
    def __init__(self, fitxer_items: str, fitxer_valoracions:str, dataset: str):
        if dataset == 'movielens100k':
            self._score = ScoreMovies(fitxer_items, fitxer_valoracions)
            #dataset = 'ScoreMovies'
        else:
            self._score = ScoreBooks(fitxer_items, fitxer_valoracions)
            #dataset = 'ScoreBooks'
        #cls = globals()[dataset]
        #self._score = cls()
        #self._score.display(fitxer_items, fitxer_valoracions)
        
        #self._score = Score(fitxer_items, fitxer_valoracions)
    
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
        
        puntuacions = []
        avg_global = self._score.avg_global(items_a_considerar)
        
        for id_item in items_a_considerar:
            num_vots = self._score.num_vots(id_item)
            avg_item = self._score.avg_item(id_item)
            puntuacio = ((num_vots/(num_vots+min_vots))*avg_item)+((min_vots/(num_vots+min_vots))*avg_global)
            puntuacions.append((id_item, puntuacio))
        
        puntuacions.sort(key=lambda x: x[1], reverse=True)
        
        
        #items = []
        #copia_puntuacions = puntuacions.copy()
        #while len(items) < 5:
         #   maxim = max(copia_puntuacions)
          #  id_item = items_a_considerar[puntuacions.index(maxim)]
           # if self._score.no_vista(id_usuari, id_item):
            #    items.append(id_item)
            #copia_puntuacions.remove(maxim)
            
        return puntuacions, items
    

class RecomanacioColaborativa(Recomanacio):
    
    def __init__(self, fitxer_items: str, fitxer_valoracions: str, dataset: str):    
        super().__init__(fitxer_items, fitxer_valoracions, dataset)
    
    def recomana_per(self, id_usuari):
        similituds=[]
        for usuari in self._score._ll_usuaris:
            s=self._score.similitud(id_usuari,usuari)
            similituds.append((usuari,s))
        k = int(input("Nombre d'usuaris a considerar: "))
        similituds.sort(key=lambda x: x[1], reverse=True)
        k_similituds = similituds[:k+2][1:]
        #usuaris_similars = similituds[:k+2][0]
        usuaris_similars = [x[0] for x in k_similituds]
        
        puntuacions=[]
        mitjana_usu=self._score.avg_usu(id_usuari)
        for item in self._score._ll_items:
            numerador=0
            denominador=0
            if self._score.no_vista(id_usuari, item):
                for usuari in usuaris_similars:
                    i=usuaris_similars.index(usuari)
                    mitjana=self._score.avg_usu(usuari)
                    numerador+=k_similituds[i][1]*(self._score._mat[self._score._ll_usuaris.index(usuari)][self._score._ll_items.index(item)]-mitjana)
                    denominador+=k_similituds[i][1]
                puntuacio=numerador/denominador
                puntuacions.append((item, mitjana_usu+puntuacio))

        puntuacions.sort(key=lambda x: x[1], reverse=True)
        items, puntuacions = zip(*puntuacions)
        return puntuacions, items[:5]
        


class RecomanacioBasadaEnContingut(Recomanacio):
    
    def __init__(self, fitxer_items: str, fitxer_valoracions: str, dataset: str):    
        super().__init__(fitxer_items, fitxer_valoracions, dataset)
        
    def recomana_per(self, id_usuari):
        fitxer_generes_pelis = 'MovieLens100k/movies.csv'
        item_features = []
        with open(fitxer_generes_pelis, 'r') as f:
            next(f)
            reader = csv.reader(f)
            for line in reader:
                generes = line[-1]
                #if generes != '(no genres listed)':
                item_features.append(generes)
        
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(item_features).toarray()
        #print (" Vocabulary : {}".format(tfidf.get_feature_names_out())) 
        #print (" Shape : {}".format(tfidf_matrix.shape))
        
        
        vector_puntuacions = self._score.vector_puntuacions(id_usuari)
        #print("Shape vector_puntuacions: {}".format(vector_puntuacions.shape))
        mat_numerador = np.copy(tfidf_matrix)
        for i in range(len(vector_puntuacions)):
            mat_numerador[i,:] = mat_numerador[i,:]*vector_puntuacions[i]
        #print (" Shape mat_mumerador: {}".format(mat_numerador.shape))
        perfil_user = np.sum(mat_numerador, axis=0)
        #print("Shape perfil_user: {}".format(perfil_user.shape))
        valor_normalitzador = np.sum(vector_puntuacions)
        Q = perfil_user / valor_normalitzador
        #print (" Shape Q: {}".format(Q.shape))
        
        S = np.dot(tfidf_matrix, Q)
        #print (" Shape S: {}".format(S.shape))
        
        p_final = S*self._score.max()
        
        items = []
        copia_puntuacions = p_final.copy()
        while len(items) < 5:
            maxim = max(copia_puntuacions)
            index_item = np.where(copia_puntuacions==maxim)[0][0]
            id_item = self._score._ll_items[index_item]  # això és per recuperar l'id de l'item cosa que no sé si ho estic trobant bé...
            if self._score.no_vista(id_usuari, id_item):
                items.append(id_item)
            copia_puntuacions = np.delete(copia_puntuacions, np.where(copia_puntuacions == maxim)[0][0])
        return p_final, items



