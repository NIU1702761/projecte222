#!/usr/bin/env python3
# -*- coding: utf-8 -*-∫

import numpy as np
import csv
from abc import ABCMeta, abstractmethod
import logging

class Item(metaclass=ABCMeta):
    """
    Classe base per a ítems.

    Attributes
    ----------
    _titol : str
        Títol de l'ítem.
    _ID : str
        Identificador de l'ítem.
    _extra : str
        Informació extra de l'ítem.

    Methods
    -------
    __init__(ID=0, nomFitxerTitols="")
        Inicialitza un nou objecte Item.
    _carrega_dades(nomFitxerTitols)
        Carrega les dades de l'ítem des del fitxer.
    __str__()
        Retorna una representació en cadena de l'ítem.
    """

    _titol: str
    _ID: str
    _extra: str

    def __init__(self, ID='', nomFitxerTitols=""):
        """
        Inicialitza un nou objecte Item.

        Parameters
        ----------
        ID : str
            Identificador de l'ítem.
        nomFitxerTitols : str
            Nom del fitxer de títols.
        """
        self._titol = ""
        self._ID = ID
        self._extra = ''
        logging.debug(f"Inicialitzant Item amb ID: {ID}")
        self._carrega_dades(nomFitxerTitols)

    def _carrega_dades(self, nomFitxerTitols):
        """
        Carrega les dades de l'ítem des del fitxer.

        Parameters
        ----------
        nomFitxerTitols : str
            Nom del fitxer de títols.
        """
        with open(nomFitxerTitols, 'r', encoding='utf-8') as f:
            next(f)
            reader = csv.reader(f)
            for line in reader:
                if line[0] == self._ID:
                    self._titol = line[1]
                    self._extra = line[2]
                    break

    def __str__(self):
        """
        Retorna una representació en cadena de l'ítem.

        Returns
        -------
        str
            Representació en cadena de l'ítem.
        """
        if self._titol:
            resposta = f'TITOL: {self._titol}\n'
            return resposta
        else:
            return None




class Book(Item):
    """
    Classe per a ítems de tipus llibre.

    Attributes
    ----------
    _autor : str
        Autor del llibre.

    Methods
    -------
    __init__(ID=0, nomFitxerTitols="")
        Inicialitza un nou objecte Book.
    _carrega_dades(nomFitzerTitols)
        Carrega les dades de l'ítem des del fitxer.
    __str__()
        Retorna una representació en cadena del llibre.
    """

    _autor: str

    def __init__(self, ID=0, nomFitxerTitols=""):
        """
        Inicialitza un nou objecte Book.

        Parameters
        ----------
        ID : str
            Identificador del llibre.
        nomFitxerTitols : str
            Nom del fitxer de títols.
        """
        super().__init__(ID, nomFitxerTitols)

    def _carrega_dades(self, nomFitxerTitols):
        """
        Carrega les dades del llibre des del fitxer.

        Parameters
        ----------
        nomFitxerTitols : str
            Nom del fitxer de títols.
        """
        super()._carrega_dades(nomFitxerTitols)
        with open(nomFitxerTitols, 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                if line[0] == self._ID:
                    self._autor = line[2]

    def __str__(self):
        """
        Retorna una representació en cadena del llibre.

        Returns
        -------
        str
            Representació en cadena del llibre.
        """
        if self._titol:
            resposta = super().__str__()
            resposta += f'AUTOR: {self._autor}\n'
            return resposta
        else:
            return None

class Movie(Item):
    """
    Classe per a ítems de tipus pel·lícula.

    Attributes
    ----------
    _generes : list
        Llista de gèneres de la pel·lícula.

    Methods
    -------
    __init__(ID=0, nomFitxerTitols="")
        Inicialitza un nou objecte Movie.
    __str__()
        Retorna una representació en cadena de la pel·lícula.
    """

    _generes: list = []

    def __init__(self, ID=0, nomFitxerTitols=""):
        """
        Inicialitza un nou objecte Movie.

        Parameters
        ----------
        ID : str
            Identificador de la pel·lícula.
        nomFitxerTitols : str
            Nom del fitxer de títols.
        """
        super().__init__(ID, nomFitxerTitols)
        self._generes = self._extra.split('|')

    def __str__(self):
        """
        Retorna una representació en cadena de la pel·lícula.

        Returns
        -------
        str
            Representació en cadena de la pel·lícula.
        """
        if self._titol:
            resposta = super().__str__()
            resposta += f'GENERES: {" | ".join(self._generes)}'
            return resposta
        else:
            return None


class Anime(Item):
    """
    Classe per a ítems de tipus anime.

    Attributes
    ----------
    _generes : list
        Llista de gèneres de l'anime.

    Methods
    -------
    __init__(ID=0, nomFitxerTitols="")
        Inicialitza un nou objecte Anime.
    __str__()
        Retorna una representació en cadena de l'anime.
    """

    _generes: list = []

    def __init__(self, ID=0, nomFitxerTitols=""):
        """
        Inicialitza un nou objecte Anime.

        Parameters
        ----------
        ID : str
            Identificador de l'anime.
        nomFitxerTitols : str
            Nom del fitxer de títols.
        """
        super().__init__(ID, nomFitxerTitols)
        self._generes = self._extra.split(",")

    def __str__(self):
        """
        Retorna una representació en cadena de l'anime.

        Returns
        -------
        str
            Representació en cadena de l'anime.
        """
        if self._titol:
            resposta = super().__str__()
            resposta += f'GENERES: {" | ".join(self._generes)}'
            return resposta
        else:
            return None