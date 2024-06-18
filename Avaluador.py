#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import math


class Avaluador():
    """
    Classe per avaluar les prediccions de recomanacions.

    Attributes
    ----------
    _prediccions : np.array
        Vector de prediccions.
    _valoracions_usuari : np.array
        Vector de valoracions dels usuaris.
    _mascara : np.array
        Vector booleana que indica on hi ha valoracions no nul·les.

    Methods
    -------
    __init__(prediccions, valoracions_usuari)
        Inicialitza un nou objecte Avaluador.
    mae()
        Calcula l'Error Absolut Mitjà (MAE) de les prediccions.
    rmse()
        Calcula l'Arrel de l'Error Quadràtic Mitjà (RMSE) de les prediccions.
    """
    _prediccions: np.array
    _valoracions_usuari: np.array
    _mascara: np.array
    
    def __init__(self, prediccions: np.array, valoracions_usuari: np.array):
        """
        Inicialitza un nou objecte Avaluador.

        Parameters
        ----------
        prediccions : np.array
            Matriu de prediccions.
        valoracions_usuari : np.array
            Matriu de valoracions dels usuaris.
        """
        self._prediccions = prediccions
        self._valoracions_usuari = valoracions_usuari
        self._mascara = self._valoracions_usuari != 0.0
    
    def mae(self):
        """
        Calcula l'Error Absolut Mitjà (MAE) de les prediccions.

        Returns
        -------
        float
            Valor del MAE.
        """
        return (np.sum(abs(self._prediccions[self._mascara] - self._valoracions_usuari[self._mascara]))) / np.count_nonzero(self._valoracions_usuari)
    
    def rmse(self):
        """
        Calcula l'Arrel de l'Error Quadràtic Mitjà (RMSE) de les prediccions.

        Returns
        -------
        float
            Valor del RMSE.
        """
        return math.sqrt((np.sum((self._valoracions_usuari[self._mascara] - self._prediccions[self._mascara])**2))/np.count_nonzero(self._valoracions_usuari))