#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from recomanacions import RecomanacioSimple, RecomanacioBasadaEnContingut, RecomanacioColaborativa, Recomanacio
from abc import ABCMeta, abstractmethod
from items import Item, Movie, Book, Anime
import numpy as np
import logging
import math
from avaluador import Avaluador


class Recomender(metaclass=ABCMeta):
    """
    Classe base per als recomanadors de pel·lícules i llibres.
    
    Attributes
    ----------
    _recomanacio : Recomanacio
        Objecte de recomanació.
    _fitxer_items : str
        Nom del fitxer d'ítems.
    _fitxer_valoracions : str
        Nom del fitxer de valoracions.
    """

    _recomanacio = Recomanacio
    _fitxer_items = str
    _fitxer_valoracions = str
    
    def __init__(self, dataset: str, method:str):
        """
        Inicialitza un nou recomanador.

        Parameters
        ----------
        dataset : str 
            Nom del dataset a utilitzar ('Books', 'MovieLens100K').
        method : str
            Mètode de recomanació ('simple', 'colaboratiu', 'basat en contingut').
        """
        
        logging.info(f"Inicialitzant Recomender amb dataset: {dataset} i method: {method}")
        if method == 'simple':
            self._recomanacio = RecomanacioSimple(self._fitxer_items, self._fitxer_valoracions, dataset)
        elif method == 'colaboratiu':
            self._recomanacio = RecomanacioColaborativa(self._fitxer_items, self._fitxer_valoracions, dataset)
        else:
            self._recomanacio = RecomanacioBasadaEnContingut(self._fitxer_items, self._fitxer_valoracions, dataset)
        
    def programa_principal(self):
        """
        Executa el programa principal per a la recomanació o avaluació d'ítems per a un usuari.
        """
        
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
                        I = self.crea_item(id_item, self._fitxer_items)
                        if I:
                            print('\n'+str(I))
                        else:
                            logging.warning(f'Item no carregat: {id_item}')
            elif accio == '2':
                id_usuari = input("Identificador d'usuari: ")
                logging.info(f"Avaluació per l'usuari: {id_usuari}")
                
                prediccions, ids_items_recomanats = self._recomanacio.recomana_per(id_usuari)
                
                if prediccions is not None:
                    valoracions_usuari = self._recomanacio.valoracions_usuari(id_usuari)
                    if np.count_nonzero(valoracions_usuari) != 0:
                        a = Avaluador(prediccions, valoracions_usuari)
                        mae = a.mae()
                        rmse = a.rmse()
                        logging.info(f"MAE: {mae}")
                        logging.info(f"RMSE: {rmse}")
                    else:
                        logging.warning(f"Necessitem més valoracions de l'usuari {id_usuari} per poder-lo avaluar")
                        self._recomanacio.usuari_a_avaluar()
            else:
                logging.info('Sortint...')
                break 
    
    @abstractmethod
    def crea_item(self, id_item, fitxer_items):
        """
        Crea un objecte ítem.

        Parameters
        ----------
        id_item : str
            Identificador de l'ítem.
        fitxer_valoracions : str
            Nom del fitxer de valoracions.
        fitxer_items : str
            Nom del fitxer d'ítems.

        Returns
        -------
        Item
            Objecte ítem.
        """
        
        raise NotImplementedError()
    

class RecomenderMovies(Recomender):
    
    """
    Classe per al recomanador de pel·lícules.
    
    Attributes
    ----------
    _recomanacio : Recomanacio
        Objecte de recomanació.
    _fitxer_items : str
        Nom del fitxer d'ítems.
    _fitxer_valoracions : str
        Nom del fitxer de valoracions.
    """
    
    _recomanacio = Recomanacio
    _fitxer_items = str
    _fitxer_valoracions = str
    
    def __init__(self, dataset: str, method:str):
        """
        Inicialitza un nou recomanador de pel·lícules.

        Parameters
        ----------
        dataset : str
            Nom del dataset a utilitzar ('Books', 'MovieLens100K').
        method : str
            Mètode de recomanació ('simple', 'colaboratiu', 'basat en contingut').
        """
        
        self._fitxer_items = 'MovieLens100k/movies.csv'
        self._fitxer_valoracions = 'MovieLens100k/ratings.csv'
        super().__init__(dataset, method)
    
    def crea_item(self, id_item, fitxer_items):
        """
        Crea un objecte pel·lícula.

        Parameters
        ----------
        id_item : str
            Identificador de la pel·lícula.
        fitxer_valoracions : str
            Nom del fitxer de valoracions.
        fitxer_items : str
            Nom del fitxer d'ítems.

        Returns
        -------
        Movie
            Objecte pel·lícula.
        """
        
        logging.debug(f"Creant item Movie amb id: {id_item}")
        return Movie(id_item, fitxer_items)


class RecomenderBooks(Recomender):
    """
    Classe per al recomanador de llibres.
    
    Attributes
    ----------
    _recomanacio : Recomanacio
        Objecte de recomanació.
    _fitxer_items : str
        Nom del fitxer d'ítems.
    _fitxer_valoracions : str
        Nom del fitxer de valoracions.
    """
    
    _recomanacio = Recomanacio
    _fitxer_items = str
    _fitxer_valoracions = str
    
    def __init__(self, dataset: str, method:str):
        """
        Inicialitza un nou recomanador de pel·lícules.

        Parameters
        ----------
        dataset : str
            Nom del dataset a utilitzar ('Books', 'MovieLens100K').
        method : str
            Mètode de recomanació ('simple', 'colaboratiu', 'basat en contingut').
        """
        
        self._fitxer_items = 'Books/Books.csv'
        self._fitxer_valoracions = 'Books/Ratings.csv'
        super().__init__(dataset, method)
    
    def crea_item(self, id_item, fitxer_items):
        """
        Crea un objecte llibre.

        Parameters
        ----------
        id_item : str
            Identificador del llibre.
        fitxer_valoracions : str
            Nom del fitxer de valoracions.
        fitxer_items : str
            Nom del fitxer d'ítems.

        Returns
        -------
        Book
            Objecte llibre.
        """
        logging.debug(f"Creant item Book amb id: {id_item}")
        return Book(id_item, fitxer_items)


class RecomenderAnimes(Recomender):
    """
    Classe per al recomanador d'animes.
    
    Attributes
    ----------
    _recomanacio : Recomanacio
        Objecte de recomanació.
    _fitxer_items : str
        Nom del fitxer d'ítems.
    _fitxer_valoracions : str
        Nom del fitxer de valoracions.
    """
    

    _recomanacio = Recomanacio
    _fitxer_items = str
    _fitxer_valoracions = str
    
    def __init__(self, dataset: str, method:str):
        """
        Inicialitza un nou recomanador de videojocs.

        Parameters
        ----------
        dataset : str
            Nom del dataset a utilitzar ('Books', 'MovieLens100K', 'Videogames').
        method : str
            Mètode de recomanació ('simple', 'colaboratiu', 'basat en contingut').
        """
        
        self._fitxer_items = 'AnimeData/anime.csv'
        self._fitxer_valoracions = 'AnimeData/rating.csv'
        super().__init__(dataset, method)
    
    def crea_item(self, id_item, fitxer_items):
        """
        Crea un objecte anime.

        Parameters
        ----------
        id_item : str
            Identificador de l'anime'.
        fitxer_valoracions : str
            Nom del fitxer de valoracions.
        fitxer_items : str
            Nom del fitxer d'ítems.

        Returns
        -------
        Anime
            Objecte anime.
        """

        logging.debug(f"Creant item Anime amb id: {id_item}")
        return Anime(id_item, fitxer_items)
