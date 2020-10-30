# -*- coding: utf-8 -*-
"""Bootcamp_Test.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/173O1KfsxVh3P4UtZe9uUZYiblgTxKyR_
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
pd.plotting.register_matplotlib_converters()
import itertools

import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns

from google.colab import drive
drive.mount('/content/drive')

"""# **(1) Load the 2 datasets**"""

df_15 = pd.read_csv('/2015.csv')
df_19 = pd.read_csv('/2019.csv')

"""# **(2) Remove 'Dystopia residual' from 2015 dataset**"""

df_15 = df_15.drop(columns=['Dystopia Residual'])
df_15.columns

"""# **(3) Add new column 'Year' to both 2015 and 2019 dataset**"""

#Happiness Data 2015
df_15['Year'] = 2015
df_15.columns

#Happiness Data 2019
df_19['Year'] = 2019
df_19.columns

"""# **(4) Create a new column 'Region' and assign regions from 2015 dataset to the respective countries in 2019 dataset**"""

#Created dictionairy combining each country with it's appropriate region in a key-value pair in the 2015 dataset
dict_country_region = {}
for country, region in zip(df_15['Country'], df_15['Region']):
  dict_country_region[country] = region
print(dict_country_region)

#Renamed column 'Country or region' to 'Country' in 2019 dataset for convenience
df_19.rename(columns = {'Country or region':'Country'}, inplace = True)

#Alphabetically sorted 2015 dataset by country
df_15.sort_values(by=['Country'], inplace=True)
df_15

#Alphabetically sorted 2019 dataset by country
df_19.sort_values(by=['Country'], inplace=True)
df_19

#Gathered list of countries in 'Country' column of 2015 and 2019 datasets into C1 and C2 respectively
C1 = []
C2 = []
for country1, country2 in zip(df_15['Country'], df_19['Country or region']):
  C1.append(country1)
  C2.append(country2)
C1 = sorted(C1)
C2 = sorted(C2)

#Function determines the differences in countries in the C1 and C2 list
def difference(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))
difference = sorted(difference(C1, C2))
print(difference)

#Removed countries that are not in 2019 dataset
dict_country_region = sorted(dict_country_region)
for key in difference:
  if key in dict_country_region:
    del dict_country_region[key]
print(dict_country_region)

#Looped through dictionary created earlier to match countries, the existence of a country was indicated by an index number greater than 0, if country existed then the value pair of dictionary assigned to 'Region' column at specific index for that country
for country, region in zip(dict_country_region, df_19['Region']) :
  index = df_19[df_19['Country'] == country].index.values
  if index > 0:
    df_19['Region'][index] = dict_country_region[country]
df_19

"""# **(5) Merge the 2 datasets to form a new one with same number of columns as 2015**"""

#Sort the differences in countries from both 2015 and 2019 into separate lists 
match_df_15 = list(set(C1).intersection(difference))
match_df_19 = list(set(C2).intersection(difference))
if 'Trinidad & Tobago' in match_df_19:
  match_df_19[3] = 'Trinidad and Tobago'
rm_match = list(set(match_df_15).intersection(match_df_19))

for x in match_df_15:
  if x == 'Zambia' or  x == 'Zimbabwe' or  x == 'Trinidad and Tobago':
    match_df_15.remove(x)
match_df_15.remove('Trinidad and Tobago')
print("Countries participated in 2015 but not 2019: ", match_df_15)

for x in match_df_19:
  if x == 'Zambia' or  x == 'Zimbabwe' or  x == 'Trinidad and Tobago':
    match_df_19.remove(x)
print("Countries participated in 2019 but not 2015: ", match_df_19)

#Indexes of Removing Countries from 2015 dataset
print(df_15[df_15['Country'] == 'Macedonia'].index.values)
print(df_15[df_15['Country'] == 'Oman'].index.values)
print(df_15[df_15['Country'] == 'Suriname'].index.values)
print(df_15[df_15['Country'] == 'Djibouti'].index.values)
print(df_15[df_15['Country'] == 'North Cyprus'].index.values)
print(df_15[df_15['Country'] == 'Somaliland region'].index.values)
print(df_15[df_15['Country'] == 'Sudan'].index.values)
print(df_15[df_15['Country'] == 'Angola'].index.values)

df_15 = df_15.drop(92)
df_15 = df_15.drop(21)
df_15 = df_15.drop(39)
df_15 = df_15.drop(125)
df_15 = df_15.drop(65)
df_15 = df_15.drop(90)
df_15 = df_15.drop(117)
df_15 = df_15.drop(136)

#Indexes of Removing Countries from 2019 dataset
print(df_19[df_19['Country or region'] == 'North Macedonia'].index.values)
print(df_19[df_19['Country or region'] == 'Somalia'].index.values)
print(df_19[df_19['Country or region'] == 'Namibia'].index.values)
print(df_19[df_19['Country or region'] == 'Gambia'].index.values)
print(df_19[df_19['Country or region'] == 'South Sudan'].index.values)
print(df_19[df_19['Country or region'] == 'Northern Cyprus'].index.values)

df_19 = df_19.drop(83)
df_19 = df_19.drop(111)
df_19 = df_19.drop(112)
df_19 = df_19.drop(119)
df_19 = df_19.drop(155)
df_19 = df_19.drop(63)

#Dropped columns from 2019 dataset
df_19.drop(columns=['Perceptions of corruption', 'Score', 'GDP per capita', 'Overall rank'])

#Dropped columns from 2015 dataset
df_15.drop(columns=['Standard Error','Dystopia Residual','Generosity','Health (Life Expectancy)','Freedom', 'Economy (GDP per Capita)'])

#Merged 2015 and 2019 datasets
merged = pd.merge(df_15, df_19, on='Country')
merged.drop(columns=['Standard Error','Dystopia Residual','Health (Life Expectancy)','Freedom', 'Economy (GDP per Capita)', 'Perceptions of corruption', 'Score', 'GDP per capita', 'Overall rank'])

concatenated = pd.concat([df_15, df_19], ignore_index=True)

"""# **(6) List the countries that participated in 2015 but not 2019**"""

match_df_15 = list(set(C1).intersection(difference))
match_df_19 = list(set(C2).intersection(difference))
if 'Trinidad & Tobago' in match_df_19:
  match_df_19[3] = 'Trinidad and Tobago'
rm_match = list(set(match_df_15).intersection(match_df_19))

for x in match_df_15:
  if x == 'Zambia' or  x == 'Zimbabwe' or  x == 'Trinidad and Tobago':
    match_df_15.remove(x)
match_df_15.remove('Trinidad and Tobago')
print("Countries participated in 2015 but not 2019: ", match_df_15)

"""# **(7) Plot a barchart for the countries' generosity for each year**"""

#Countries' generosity for 2015

#Determining figure size
plt.figure(figsize=(10,30))

#Add title
plt.title("Generosity of Every Country in 2015")

#Bar chart showing average arrival delay for Spirit Airlines flights by month
sns.barplot(x = df_15['Generosity'],  y = df_15['Country'])

#Add label for vertical axis
plt.ylabel("Generosity")

#Add label for horizontal axis
plt.xlabel("Country")

#Countries' generosity for 2019

#Determining figure size
plt.figure(figsize=(10,30))

# Add title
plt.title("Generosity of Every Country in 2019")

# Bar chart showing average arrival delay for Spirit Airlines flights by month
sns.barplot(x = df_19['Generosity'],  y = df_19['Country'])

#Add label for vertical axis
plt.ylabel("Generosity")

#Add label for horizontal axis
plt.xlabel("Country")

#Set general plot properties
sns.set_style("white")
sns.set_context({"figure.figsize": (24, 40)})

#Plot 1 - background - "total" (top) series
sns.barplot(y = df_15['Country'], x = df_15['Generosity'], color = "red")

#Plot 2 - overlay - "bottom" series
bottom_plot = sns.barplot(y = df_19['Country'], x = df_19['Generosity'], color = "#0000A3")


topbar = plt.Rectangle((0,0),1,1,fc="red", edgecolor = 'none')
bottombar = plt.Rectangle((0,0),1,1,fc='#0000A3',  edgecolor = 'none')
l = plt.legend([bottombar, topbar], ['2019', '2015'], loc=1, ncol = 2, prop={'size':16})
l.draw_frame(False)

#Optional code - Make plot look nicer
sns.despine(left=True)
bottom_plot.set_ylabel("Country")
bottom_plot.set_xlabel("Generosity")

#Set fonts to consistent 16pt size
for item in ([bottom_plot.xaxis.label, bottom_plot.yaxis.label] +
             bottom_plot.get_xticklabels() + bottom_plot.get_yticklabels()):
    item.set_fontsize(16)

"""#**(8) Bubble chart of 'Freedom' vs. 'Social support' where the size of the bubble is the GDP per Capital for 2019**"""

#'Trust' values weren't in the 2019 dataset so 'Social support' values were substituted
sns.set_context("talk", font_scale=1.1)
plt.figure(figsize=(10,6))
sns.scatterplot(x = df_19['Freedom to make life choices'], y = df_19['Social support'],
                size=df_19['GDP per capita'],
                sizes=(20,500),
                alpha=0.5,
                data=df_19)
# Put the legend out of the figure
plt.legend(bbox_to_anchor=(1.01, 1),borderaxespad=0)

#Horizontal label, Vertical Label, Title
plt.xlabel('Freedom')
plt.ylabel('Social support')
plt.title('Freedom vs. Social support')

"""# **(9) Bubble chart of 'Family' vs. 'Health' where the size is the happiness score of 2015**"""

sns.set_context("talk", font_scale=1.1)
plt.figure(figsize=(10,6))
sns.scatterplot(x = df_15['Family'], y = df_15['Health (Life Expectancy)'],
                size=df_15['Happiness Score'],
                sizes=(20,500),
                alpha=0.5,
                data=df_15)
# Put the legend out of the figure
plt.legend(bbox_to_anchor=(1.01, 1),borderaxespad=0)

#Horizontal label, Vertical Label, Title
plt.xlabel('Family')
plt.ylabel('Health (Life Expectancy)')
plt.title('Family vs. Health')

"""#**(10) List the first 3 variables that correlate with Happiness score (use Pearson Correlation)**"""

import pandas as pd 
from scipy.stats import pearsonr 

var_list = []
variables = ['Health','Family','Freedom', 'Trust', 'Generosity', 'Dystopia Residual']
#Variable: Health (Life Expectancy)

# Convert dataframe into series 
happy_score = df_15['Happiness Score'] 
life_exp = df_15['Health (Life Expectancy)'] 
  
# Apply the pearsonr() 
corr1, _ = pearsonr(happy_score, life_exp) 
print('Pearsons correlation for Health: %.3f' % corr1) 
var_list.append(corr1)

#Variable: Family

# Convert dataframe into series 
happy_score = df_15['Happiness Score'] 
family = df_15['Family'] 
  
# Apply the pearsonr() 
corr2, _ = pearsonr(happy_score,family) 
print('Pearsons correlation for Family: %.3f' % corr2)
var_list.append(corr2)

#Variable: Freedom

# Convert dataframe into series 
happy_score = df_15['Happiness Score'] 
freedom = df_15['Freedom'] 
  
# Apply the pearsonr() 
corr3, _ = pearsonr(happy_score, freedom) 
print('Pearsons correlation for Freedom: %.3f' % corr3)
var_list.append(corr3)

#Variable: Trust (Government Corruption)

# Convert dataframe into series 
happy_score = df_15['Happiness Score'] 
trust = df_15['Trust (Government Corruption)'] 
  
# Apply the pearsonr() 
corr4, _ = pearsonr(happy_score, trust) 
print('Pearsons correlation for Trust: %.3f' % corr4)
var_list.append(corr4)

#Variable: Generosity

# Convert dataframe into series 
happy_score = df_15['Generosity'] 
generosity = df_15['Trust (Government Corruption)'] 
  
# Apply the pearsonr() 
corr5, _ = pearsonr(happy_score, generosity) 
print('Pearsons correlation for Generosity: %.3f' % corr5)
var_list.append(corr5)
  
#Variable: Dystopia Residual

# Convert dataframe into series 
happy_score = df_15['Happiness Score'] 
dystopia_residual = df_15['Dystopia Residual'] 
  
# Apply the pearsonr() 
corr6, _ = pearsonr(happy_score, dystopia_residual) 
print('Pearsons correlation for Dystopia Residual: %.3f' % corr6)
var_list.append(corr6)

dict = {}
for a,b in zip(variables, var_list):
  dict[b] = a
x = sorted(dict.items(), reverse=True)[:3]
x