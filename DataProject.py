
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import statsmodels.api as sm

os.chdir('C:/Users\Work\Documents\Proyectos\CU - IDB Data Task')

# Question 1

# "(a) Load ratings.csv"

ratings = pd.read_csv('ratings.csv') 

# "(b) Report the number of unique respondents and unique aspects in the data set"

unique_worker = len(ratings.worker.unique()) # Number of workers. Stored for later

len(ratings.aspect.unique()) # Number of aspects

# "(c) Check to see if each respondent has only rated each aspect once. If this is not true, only include the most recent observation and report the number of observations you have dropped."  

len(ratings) - len(ratings.aspect.unique()) * len(ratings.worker.unique()) # There are 237 more answers that there should be given the number of respondents and aspects

2 in ratings.value_counts(subset = ['aspect', 'worker']).unique() # This confirsms some workers have answered repeat questions

len_before = len(ratings) # Storing the amount of observations before dropping repeats

ratings = ratings.sort_values('time').drop_duplicates(subset = ['worker', 'aspect'], keep = 'last') # First, I arrange the observatios by time (ascending). Then I drop repeat observations for worker-aspect combinations, making sure to keep the last of the repeats, which is the latest one

len_after = len(ratings) # Storing the amount of observations after dropping repeats

len_before - len_after # As expected, 237 observations have been dropped

# "(d)Calculate the  average  rating   for  each  respondent.  We  will call  this  measure  subjective  riches.
# Report  the  minimum,  25th  percentile,  50th  percentile,  75th  percentile,  and  maximum  subjective
# riches  value."

subjective_riches = ratings.groupby('worker', as_index = False).rating.mean()

subjective_riches.describe().loc[['min', '25%', '50%', '75%', 'max'],:] # Most respondents seem to have a high overall rating; only slightly more than a quarter of them have an index below 50

# Question 2

# "(a) Load demographics.csv"

demo = pd.read_csv('demographics.csv')

# "(b)  Report  the  number  of rows and  check to see if it is the  same as the  number  of unique  respondents
# you  calculated  in question  1."

len(demo.worker.unique()) == unique_worker

# (c) "Merge the  subjective  riches  data  from  question  1 with  the  demographics  data."

demo_sub = demo.merge(subjective_riches, on = 'worker')

# (d) "Regress  (with  OLS)  subjective  riches  on income  and  report  the  results."

model = sm.OLS(demo_sub.rating, sm.add_constant(demo_sub.income)).fit() # OLS with raw data

plt.rc('figure', figsize=(12, 7))
plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 10}, fontproperties = 'monospace')
plt.axis('off')
plt.tight_layout()

model = sm.OLS(demo_sub.rating, sm.add_constant(demo_sub.income/1000)).fit() # OLS with income in thousands of units (basically the same result but more easily interpretable)

plt.rc('figure', figsize=(12, 7))
plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 10}, fontproperties = 'monospace')
plt.axis('off')
plt.tight_layout()
plt.savefig('model1.png')


# (e) "Regress (with  OLS) subjective  riches on income with controls  for age, age 2   (age squared),  gender,
# level of education, and  race."

demo_sub = pd.get_dummies(demo_sub, prefix='' # Get the dummies for each of the categories
                          ,prefix_sep='', 
                          columns=['education', 
                                   'race']).drop(['Less than high school',  # And drop to avoid multicolinearity in the regression
                                                  'White (non-Hispanic)'], 
                                                  axis=1)
demo_sub['age2'] = demo_sub['age'] ** 2

demo_sub.columns = demo_sub.columns.str.replace("'","") # Getting rid of some problematic characters

y = demo_sub['rating']
X = sm.add_constant(demo_sub[['age', 'male', 'income', 'Bachelors degree',
       'Doctoral degree', 'Graduate degree', 'High school', 'Masters degree',
       'Some college', 'Asian (non-Hispanic)', 'Black (non-Hispanic)',
       'Hispanic (any race)', 'Multiracial', 'Other', 'age2']])

model = sm.OLS(y, X).fit()

plt.rc('figure', figsize=(12, 7))
plt.text(0.01, 0.05, str(model.summary()), {'fontsize': 10}, fontproperties = 'monospace')
plt.axis('off')
plt.tight_layout()
plt.savefig('model2.png')

# Question 3

"""
Your  PI  is giving  a  presentation to  a  health-policy audience,  and  she  would  like to  display  a  figure
that illustrates the  relationship between  subjective  ratings  of health,  income,  and  age.  She has  asked
you  to produce  a  single scatterplot that conveys  the  relationship between  all  three  variables.
"""

# (b) " Produce  and  save  the  scatterplot (or  if you  prefer,  up  to  two proposals  for  alternative scatter-
# plots)."

rt_health = ratings[ratings['aspect'] == 'your health'].drop('aspect', axis = 1)

rt_health = rt_health.merge(demo, on = 'worker')

labels = ['Extremely low', 'Low', 'High', 'Extremely high']

rt_health['class'] = pd.cut(rt_health.rating, range(0, 101, 25), right=False, labels=labels) # Assigning categories to the rating

colors = dict(zip(labels, ['red', 'orange', 'yellow', 'green'])) # Picking the colors for each category
sizes = dict(zip(labels, [2, 7, 12, 17])) # And the sizes

fig, ax = plt.subplots(figsize = (15,7))

for key, group in rt_health.groupby('class'):
    plt.plot(group.age, group.income/1000, 'o', label = key, mfc = 'none', 
             mec = colors[key], ms = sizes[key], mew = 1.5)

plt.title('Relationship between subjective health, age and income')
plt.xlabel('Age')
plt.ylabel('Income (Thousands)')
plt.legend()
plt.savefig('alt1.png')

health_rates = ratings[ratings['aspect'].isin(['your health', 'your mental health', 'your physical fitness'])] # The other alternative will have an index, which is the average of subjective health, mental health, and fitness

health_rates = health_rates.groupby('worker', as_index = False)['rating'].mean()

health_rates = health_rates.merge(demo, on = 'worker')

health_rates['class'] = pd.cut(health_rates.rating, range(0, 101, 25), right=False, labels=labels) # Assigning values to the index

fig, ax = plt.subplots(figsize = (15,7))

for key, group in health_rates.groupby('class'):
    plt.plot(group.age, group.income/1000, 'o', label = key, mfc = 'none', 
             mec = colors[key], ms = sizes[key])

plt.title('Relationship between subjective health index, age and income')
plt.xlabel('Age')
plt.ylabel('Income (Thousands)')
plt.legend()
plt.savefig('alt2.png')

















