#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 19:21:41 2024

@author: aliciamartilopez
"""



from recomender import RecomenderMovies, RecomenderBooks
import argparse
import os 
import pickle
import logging
"""
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
print(dataset)
print(method)

datasets = ['movielens100k', 'books']
methods = ['simple','colaboratiu','basat en contingut']

if (dataset in datasets) and (method in methods):
    arxiu_pickles = 'recomender_'+dataset+'_'+method+'.dat'
    print(arxiu_pickles)
else:
    print('ERROR: Dataset ha de ser MovieLens100K o Books.')
    print('ERROR: Method ha de ser simple, colaboratiu o basat en contingut.')


if os.path.exists(arxiu_pickles):
    with open(arxiu_pickles, 'rb') as f: 
        r = pickle.load(f)
else:
    if dataset == 'books':
        r = RecomenderBooks(dataset, method)
    else:
        r = RecomenderMovies(dataset, method)
    with open(arxiu_pickles, 'wb') as f: 
        pickle.dump(r, f)
"""
r = RecomenderMovies('movielens100k', 'simple')
r.programa_principal()

"""
logger = logging.getLogger('exampleLogger')
logger.debug('This is a debug message')
logger.info('This is an info message')
"""