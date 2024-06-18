#!/usr/bin/env python3
# -*- coding: utf-8 -*-∫
from sklearn.feature_extraction.text import TfidfVectorizer
from score import Score, ScoreBooks, ScoreMovies, ScoreAnimes
from abc import ABCMeta, abstractmethod
import numpy as np
import logging


class Recomanacio(metaclass=ABCMeta):
    """
    Classe base per a les recomanacions.

    Attributes
    ----------
    _score : Score
        Objecte per calcular puntuacions.

    Methods
    -------
    recomana_per(id_usuari):
        Retorna una llista d'ítems recomanats per a l'usuari.
    valoracions_usuari(id_usuari):
        Retorna les valoracions de l'usuari.
    """
    _score = Score
    
    def __init__(self, fitxer_items: str, fitxer_valoracions:str, dataset: str):
        """
        Inicialitza un nou objecte de recomanació.

        Parameters
        ----------
        fitxer_items : str
            Nom del fitxer d'ítems.
        fitxer_valoracions : str
            Nom del fitxer de valoracions.
        dataset : str
            Nom del dataset ('movielens100k' o 'books').
        """
        logging.info(f"Inicialitzant Recomanacio")
        if dataset == 'movielens100k':
            self._score = ScoreMovies(fitxer_items, fitxer_valoracions)
        elif dataset == 'books':
            self._score = ScoreBooks(fitxer_items, fitxer_valoracions)
        else:
            self._score = ScoreAnimes(fitxer_items, fitxer_valoracions)
    
    def recomana_per(self, id_usuari):
        """
        Retorna una llista d'ítems recomanats per a l'usuari.

        Parameters
        ----------
        id_usuari : str
            Identificador de l'usuari.

        Returns
        -------
        list
            Llista d'ítems recomanats per a l'usuari.
        """
        ll_usuaris = self._score.ll_usuaris().copy()
        
        if id_usuari not in ll_usuaris:
            logging.warning(f"usuari {id_usuari} no carregat.")
            return None
        else:
            return self._score.ll_items().copy()
    
    def valoracions_usuari(self, id_usuari):
        """
        Retorna les valoracions de l'usuari.

        Parameters
        ----------
        id_usuari : str
            Identificador de l'usuari.

        Returns
        -------
        np.ndarray
            Vector de puntuacions de l'usuari.
        """
        return self._score.vector_puntuacions(id_usuari)
    
    def usuari_a_avaluar(self):
        """
        Retorna el primer usuari amb alguna valoració feta per poder ser avaluat.

        Returns
        -------
        str
            Id del primer item a poder ser avaluat
        """
        self._score.usuari_a_avaluar()


class RecomanacioSimple(Recomanacio):
    """
    Classe per a la recomanació simple.

    Methods
    -------
    recomana_per(id_usuari):
        Retorna una llista d'ítems recomanats per a l'usuari mitjançant el mètode simple.
    """
    _score = Score

    def __init__(self, fitxer_items: str, fitxer_valoracions: str, dataset: str):  
        """
        Inicialitza un nou objecte de recomanació simple.

        Parameters
        ----------
        fitxer_items : str
            Nom del fitxer d'ítems.
        fitxer_valoracions : str
            Nom del fitxer de valoracions.
        dataset : str
            Nom del dataset ('movielens100k' o 'books').
        """
        
        super().__init__(fitxer_items, fitxer_valoracions, dataset)
    
    def recomana_per(self, id_usuari):
        """
        Retorna una llista d'ítems recomanats per a l'usuari mitjançant el mètode simple.

        Parameters
        ----------
        id_usuari : str
            Identificador de l'usuari.

        Returns
        -------
        tuple
            Vector de puntuacions i llista d'ítems recomanats.
        """
        
        ll_items = super().recomana_per(id_usuari)
        
        if ll_items is None:
            return None, None
        else:
            logging.debug(f"Recomanació Simple per l'usuari: {id_usuari}")
            min_vots = int(input('Minim vots: '))
            items_a_considerar = self._score.min_vots(min_vots)
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
    
    def usuari_a_avaluar(self):
        """
        Retorna el primer usuari amb alguna valoració feta per poder ser avaluat.

        Returns
        -------
        str
            Id del primer item a poder ser avaluat
        """
        super().usuari_a_avaluar()


class RecomanacioColaborativa(Recomanacio):
    """
    Classe per a la recomanació col·laborativa.

    Methods
    -------
    recomana_per(id_usuari):
        Retorna una llista d'ítems recomanats per a l'usuari mitjançant el mètode col·laboratiu.
    """
    _score = Score

    def __init__(self, fitxer_items: str, fitxer_valoracions: str, dataset: str): 
        """
        Inicialitza un nou objecte de recomanació col·laborativa.

        Parameters
        ----------
        fitxer_items : str
            Nom del fitxer d'ítems.
        fitxer_valoracions : str
            Nom del fitxer de valoracions.
        dataset : str
            Nom del dataset ('movielens100k' o 'books').
        """
        
        super().__init__(fitxer_items, fitxer_valoracions, dataset)
    
    def recomana_per(self, id_usuari):
        """
        Retorna una llista d'ítems recomanats per a l'usuari mitjançant el mètode col·laboratiu.

        Parameters
        ----------
        id_usuari : str
            Identificador de l'usuari.

        Returns
        -------
        tuple
            Vector de puntuacions i llista d'ítems recomanats.
        """
        
        ll_items = super().recomana_per(id_usuari)
        
        if ll_items is None:
            return None, None
        else:
            logging.debug(f"Recomanació Colaborativa per l'usuari: {id_usuari}")
            logging.info(f"Trobant similituds amb altres usuaris. Aquest recomanador pot anar més lent per alguns casos (fins a 45s)")
            similituds=[]
            for usuari in self._score.ll_usuaris():
                s=self._score.similitud(id_usuari,usuari)
                similituds.append((usuari,s))
            k = 5
            similituds.sort(key = lambda x: x[1], reverse = True)
            k_similituds = similituds[:k+1][1:]
            usuaris_similars = [x[0] for x in k_similituds]
            
            puntuacions = np.zeros(len(ll_items))
            mitjana_usu = self._score.avg_usu(id_usuari)
            for item in ll_items:
                numerador = 0
                denominador = 0
                
                for usuari in usuaris_similars:
                    i = usuaris_similars.index(usuari)
                    mitjana = self._score.avg_usu(usuari)
                    numerador += k_similituds[i][1]*(self._score.mat[self._score.ll_usuaris().index(usuari)][self._score.ll_items().index(item)]-mitjana)
                    denominador += k_similituds[i][1]
                try:
                    puntuacio = float(numerador)/denominador
                except ZeroDivisionError:
                    puntuacio = 0
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
        
    def usuari_a_avaluar(self):
        """
        Retorna el primer usuari amb alguna valoració feta per poder ser avaluat.

        Returns
        -------
        str
            Id del primer item a poder ser avaluat
        """
        super().usuari_a_avaluar()
    

class RecomanacioBasadaEnContingut(Recomanacio):
    """
    Classe per a la recomanació basada en contingut.

    Methods
    -------
    recomana_per(id_usuari):
        Retorna una llista d'ítems recomanats per a l'usuari mitjançant el mètode basat en contingut.
    """
    _score = Score

    def __init__(self, fitxer_items: str, fitxer_valoracions: str, dataset: str):   
        """
        Inicialitza un nou objecte de recomanació basada en contingut.

        Parameters
        ----------
        fitxer_items : str
            Nom del fitxer d'ítems.
        fitxer_valoracions : str
            Nom del fitxer de valoracions.
        dataset : str
            Nom del dataset ('movielens100k' o 'books').
        """
        super().__init__(fitxer_items, fitxer_valoracions, dataset)
        self._fitxer_items = fitxer_items
        
    def recomana_per(self, id_usuari):
        """
        Retorna una llista d'ítems recomanats per a l'usuari mitjançant el mètode basat en contingut.

        Parameters
        ----------
        id_usuari : str
            Identificador de l'usuari.

        Returns
        -------
        tuple
            Vector de puntuacions i llista d'ítems recomanats.
        """
        ll_items = super().recomana_per(id_usuari)
        
        if ll_items is None:
            return None, None
        else:
            logging.debug(f"Recomanació Basada En Contingut per l'usuari: {id_usuari}")
            item_features = self._score.item_features(self._fitxer_items)
    
            tfidf = TfidfVectorizer(stop_words='english')
            tfidf_matrix = tfidf.fit_transform(item_features).toarray()
            
            vector_puntuacions = self._score.vector_puntuacions(id_usuari)
            
            mat_numerador = np.copy(tfidf_matrix)
            for i in range(len(vector_puntuacions)):
                mat_numerador[i,:] = mat_numerador[i,:]*vector_puntuacions[i]
           
            perfil_user = np.sum(mat_numerador, axis=0)
            
            valor_normalitzador = np.sum(vector_puntuacions)
            valor_erroni = np.float16(0)
            if valor_normalitzador != valor_erroni:
                Q = perfil_user / valor_normalitzador.astype(np.float64)
            else:
                Q = np.zeros(len(perfil_user))
            
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
        
    def usuari_a_avaluar(self):
        """
        Retorna el primer usuari amb alguna valoració feta per poder ser avaluat.

        Returns
        -------
        str
            Id del primer item a poder ser avaluat
        """
        super().usuari_a_avaluar()


