
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import shapefile as shp
import unidecode as udc
import statsmodels.api as sm

os.chdir('C:/Users\Work\Documents\Proyectos\CU - IDB Data Task')

ratings = pd.read_csv('ratings.csv')

len(ratings.aspect.unique())

unique_worker = len(ratings.worker.unique())

len(ratings) - len(ratings.aspect.unique()) * len(ratings.worker.unique()) # Respondents answered repeat questions 237 times

2 in ratings.value_counts(subset = ['aspect', 'worker']).unique()

len_before = len(ratings)

ratings = ratings.sort_values('time').drop_duplicates(subset = ['worker', 'aspect'], keep = 'last')

len_after = len(ratings)

len_before - len_after

subjective_riches = ratings.groupby('worker', as_index = False).rating.mean()

subjective_riches.describe().loc[['min', '25%', '50%', '75%', 'max'],:]


demo = pd.read_csv('demographics.csv')

len(demo.worker.unique()) == unique_worker

demo_sub = demo.merge(subjective_riches, on = 'worker')

print(sm.OLS(demo_sub.rating, sm.add_constant(demo_sub.income)).fit().summary())

print(sm.OLS(demo_sub.rating, sm.add_constant(demo_sub.income/1000)).fit().summary())

demo_sub = pd.get_dummies(demo_sub, prefix='',prefix_sep='', columns=['education', 'race']).drop(['Less than high school', 'White (non-Hispanic)'], axis=1)
demo_sub['age2'] = demo_sub['age'] ** 2

demo_sub.columns = demo_sub.columns.str.replace("'","")

y = demo_sub['rating']
X = sm.add_constant(demo_sub[['age', 'male', 'income', 'Bachelors degree',
       'Doctoral degree', 'Graduate degree', 'High school', 'Masters degree',
       'Some college', 'Asian (non-Hispanic)', 'Black (non-Hispanic)',
       'Hispanic (any race)', 'Multiracial', 'Other', 'age2']])

print(sm.OLS(y, X).fit().summary())















