#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from recomender import RecomenderMovies, RecomenderBooks, RecomenderAnimes
import argparse
import os 
import pickle
import logging

logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

parser = argparse.ArgumentParser()
parser.add_argument('dataset')
parser.add_argument('method')
args = vars(parser.parse_args())

dataset = str(args['dataset']).lower()
method = str(args['method']).lower()

datasets = ['movielens100k', 'books', 'animes']
methods = ['simple', 'colaboratiu', 'basat en contingut']

while (dataset not in datasets) or (method not in methods):
    print("ERROR: Dataset ha de ser: 'MovieLens100K', 'Books' o 'Animes'.")
    print("ERROR: Method ha de ser: 'simple', 'colaboratiu' o 'basat en contingut'")
    if method not in methods:
        method = input('Method: ')
        method = method.lower()
    if dataset not in datasets:
        dataset = input('Dataset: ')
        dataset = dataset.lower()

logging.debug(f"Dataset: {dataset}")
logging.debug(f"Method: {method}")

arxiu_pickles = 'recomender_'+dataset+'_'+method+'.dat'

if os.path.exists(arxiu_pickles):
    logging.debug(f"Pickles existeixen -> Carregant recomender des de {arxiu_pickles}")
    with open(arxiu_pickles, 'rb') as f: 
        r = pickle.load(f)
else:
    logging.debug(f"Pickles no existeixen -> Creant recomender per a {dataset} amb el mètode {method}")
    if dataset == 'books':
        r = RecomenderBooks(dataset, method)
    elif dataset == 'movielens100k':
        r = RecomenderMovies(dataset, method)
    else:
        r = RecomenderAnimes(dataset, method)
    with open(arxiu_pickles, 'wb') as f:
        logging.info("Guardant Pickles")
        pickle.dump(r, f)

logging.info("Executant programa principal del recomender")
r.programa_principal()
print("\nAutores: Alicia Martí López i Aya Talbi")
print("Crèdits dels datasets: \nMovies: MovieLens Dataset (https://grouplens.org/datasets/movielens/latest/)")
print("Books: Book Recommendation Dataset: (https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset/data)")
print("Animes: Anime Recommendations Database: (https://www.kaggle.com/datasets/CooperUnion/anime-recommendations-database/data)")