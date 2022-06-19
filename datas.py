import pandas as pd
#import numpy as np
#import io
from utils import create_mesh_data

FS_DATA = pd.read_csv('data/free_surfer_data.csv')
FS_DATA["Sex"] = FS_DATA["Sex"].apply(lambda x: ["","M","F"][x])

MODULES = [['R_Cuneus', 'R_Medialorbitofrontal', 'R_Postcentral',
        'L_Caudalmiddlefrontal', 'L_Lingual', 'L_Paracentral',
        'L_Pericalcarine', 'L_Precuneus'],
        ['R_Caudalanteriorcingulate', 'R_Lateraloccipital', 'R_Paracentral',
        'R_Precentral', 'R_Rostralanteriorcingulate', 'L_Bankssts',
        'L_Isthmuscingulate', 'L_Parahippocampal', 'L_Posteriorcingulate'],
        ['R_Insula', 'L_Cuneus', 'L_Fusiform', 'L_Inferiorparietal',
        'L_Inferiortemporal', 'L_Lateraloccipital', 'L_Middletemporal',
        'L_Postcentral', 'L_Superiorparietal', 'L_Superiortemporal',
        'L_Supramarginal', 'L_Frontalpole', 'L_Temporalpole'],
        ['R_Bankssts', 'R_Entorhinal', 'R_Inferiorparietal',
        'R_Inferiortemporal', 'R_Isthmuscingulate',
        'R_Lateralorbitofrontal', 'R_Parahippocampal', 'R_Parsopercularis',
        'R_Posteriorcingulate', 'R_Superiortemporal', 'R_Supramarginal',
        'R_Frontalpole', 'R_Temporalpole', 'R_Transversetemporal'],
        ['L_Caudalanteriorcingulate', 'L_Entorhinal',
       'L_Lateralorbitofrontal', 'L_Medialorbitofrontal',
       'L_Parsopercularis', 'L_Parsorbitalis', 'L_Parstriangularis',
       'L_Precentral', 'L_Rostralanteriorcingulate',
       'L_Rostralmiddlefrontal', 'L_Superiorfrontal'],
       ['R_Caudalmiddlefrontal', 'R_Fusiform', 'R_Lingual',
       'R_Middletemporal', 'R_Parsorbitalis', 'R_Parstriangularis',
       'R_Pericalcarine', 'R_Precuneus', 'R_Rostralmiddlefrontal',
       'R_Superiorfrontal', 'R_Superiorparietal']]

MESH = create_mesh_data()