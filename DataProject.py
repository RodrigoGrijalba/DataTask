
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


#health, income, age

rt_health = ratings[ratings['aspect'] == 'your health'].drop('aspect', axis = 1)

rt_health = rt_health.merge(demo, on = 'worker')

labels = ['Extremely low', 'Low', 'High', 'Extremely high']

rt_health['class'] = pd.cut(rt_health.rating, range(0, 101, 25), right=False, labels=labels)


colors = dict(zip(labels, ['red', 'orange', 'yellow', 'green']))
sizes = dict(zip(labels, [2, 7, 12, 17]))


fig, ax = plt.subplots(figsize = (15,7))

for key, group in rt_health.groupby('class'):
    plt.plot(group.age, group.income/1000, 'o', label = key, mfc = 'none', 
             mec = colors[key], ms = sizes[key], mew = 1.5)

plt.title('Relationship between subjective health, agen and income')
plt.xlabel('Age')
plt.ylabel('Income (Thousands)')
plt.legend()
plt.show()
plt.savefig('alt1.png')

health_rates = ratings[ratings['aspect'].isin(['your health', 'your mental health', 'your physical fitness'])]

health_rates = health_rates.groupby('worker', as_index = False)['rating'].mean()

health_rates = health_rates.merge(demo, on = 'worker')

health_rates['class'] = pd.cut(health_rates.rating, range(0, 101, 25), right=False, labels=labels)

fig, ax = plt.subplots(figsize = (15,7))

for key, group in health_rates.groupby('class'):
    plt.plot(group.age, group.income/1000, 'o', label = key, mfc = 'none', 
             mec = colors[key], ms = sizes[key])

plt.title('Relationship between subjective health index, agen and income')
plt.xlabel('Age')
plt.ylabel('Income (Thousands)')
plt.legend()
plt.show()
plt.savefig('alt2.png')

















