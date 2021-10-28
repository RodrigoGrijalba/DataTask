
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import shapefile as shp
import unidecode as udc

os.chdir('C:/Users\Work\Documents\Proyectos\CU - IDB Data Task')

ratings = pd.read_csv('ratings.csv')

len(ratings.aspect.unique())

len(ratings.worker.unique())

len(ratings) - len(ratings.aspect.unique()) * len(ratings.worker.unique()) # Respondents answered repeat questions 237 times

len_before = len(ratings)

ratings.value_counts(subset = ['aspect', 'worker']).unique()

ratings = ratings.sort_values('time').drop_duplicates(subset = ['worker', 'aspect'], keep = 'last')

rt_after = len(ratings)

len_before - len_after

subjective_riches = ratings.groupby('worker', as_index = 0).rating.mean()

subjective_riches.describe().loc[['min', '25%', '50%', '75%', 'max'],:]




















