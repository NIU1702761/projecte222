#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import logging
import numpy as np
import math

class Avaluador(metaclass=ABCMeta):

    def __init__(self, prediccions, valoracions_usuari):
          self._prediccions = prediccions
          self._valoracions = valoracions_usuari         
    
    def calcular_error(self, id_usuari):
        if self._prediccions is not None:
                    logging.info(f"Valoracions usuari no zero: {np.count_nonzero(self._valoracions)}")
                    if np.count_nonzero(self._valoracions) != 0:
                        c = self._valoracions != 0.0
                        
                        mae = (np.sum(abs(self._prediccions[c] - self._valoracions[c]))) / np.count_nonzero(self._valoracions)
                        rmse = math.sqrt((np.sum((self._valoracions[c] - self._prediccions[c])**2))/np.count_nonzero(self._valoracions))
                        
                        logging.info(f"MAE: {mae}")
                        logging.info(f"RMSE: {rmse}")
                    else:
                        logging.info(f"Necessitem més valoracions de l'usuari {id_usuari} per poder-lo avaluar")
                        #self._recomanacio.usuari_a_avaluar()
        
    