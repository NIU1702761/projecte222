#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from recomender import RecomenderMovies, RecomenderBooks
import argparse
import os 
import pickle
import logging

logging.basicConfig(filename='log.txt',level=logging.DEBUG, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

parser = argparse.ArgumentParser()
parser.add_argument('dataset')
parser.add_argument('method')
args = vars(parser.parse_args())

dataset = str(args['dataset']).lower()
method = str(args['method']).lower()

datasets = ['movielens100k', 'books']
methods = ['simple','colaboratiu','basat en contingut']

while (dataset not in datasets) or (method not in methods):
    print("ERROR: Dataset ha de ser: 'MovieLens100K' o 'Books'.")
    print("ERROR: Method ha de ser: 'simple', 'colaboratiu' o 'basat en contingut'")
    if method not in methods:
        method = input('Method: ')
    if dataset not in datasets:
        dataset = input('Dataset: ')

logging.info(f"Dataset: {dataset}")
logging.info(f"Method: {method}")

arxiu_pickles = 'recomender_'+dataset+'_'+method+'.dat'
#logging.info(f"Arxiu pickles: {arxiu_pickles}.")

if os.path.exists(arxiu_pickles):
    logging.info(f"Pickles existeixen -> Carregant recomender des de {arxiu_pickles}")
    with open(arxiu_pickles, 'rb') as f: 
        r = pickle.load(f)
else:
    logging.info(f"Creant recomender per a {dataset} amb el mètode {method}")
    if dataset == 'books':
        r = RecomenderBooks(dataset, method)
    else:
        r = RecomenderMovies(dataset, method)
    with open(arxiu_pickles, 'wb') as f: 
        pickle.dump(r, f)

#r = RecomenderMovies('movielens100k', 'simple')
logging.info("Executant programa principal del recomender")
r.programa_principal()