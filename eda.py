#!/usr/bin/env python
# Name: Siger de Vries
# Student number: 10289321

import pandas as pd
import matplotlib.pyplot as plt
pd.set_option("display.max_columns", 999)
import seaborn as sns
import json

#load in csv and pick columns I want to work with
df = pd.read_csv('input.csv')
df1 = df[['Country', 'Region', 'Pop. Density (per sq. mi.)', 'Infant mortality (per 1000 births)',\
          'GDP ($ per capita) dollars']]

# clear all the unknown rows, when 1 value is not known we can't fully compare this country with an other
# country anny more so we drop the whole row
df1 = df1[df1['Pop. Density (per sq. mi.)'] !=  'unknown']
df1 = df1[df1['GDP ($ per capita) dollars'] !=  'unknown']

#remove all rows with null values
list = []
df1.reset_index(inplace=True)
for i in range (df1.shape[0]-1):
    if pd.isnull(df1).any(axis=1).iloc[i]:
        list.append(df1.index[i])
df1.drop(df1.index[list], inplace=True)


#make the data so we can work with it
df1['Region'] = df1['Region'].str.strip()
df1['Infant mortality (per 1000 births)'] = df1['Infant mortality (per 1000 births)'].str.strip().str.replace(",", ".").astype(float)
df1['Pop. Density (per sq. mi.)'] = df1['Pop. Density (per sq. mi.)'].str.strip().str.replace(",", ".").astype(float)
df1['GDP ($ per capita) dollars'] = df1['GDP ($ per capita) dollars'].str.strip().str.replace("dollars","").astype(int)

#delete outliers
df1 = df1[df1['GDP ($ per capita) dollars'] < 60000 ]


def statistics(df1):

    #the name of the varriables says enough
    mean = df1['GDP ($ per capita) dollars'].mean()
    median = df1['GDP ($ per capita) dollars'].median()
    mode = df1['GDP ($ per capita) dollars'].mode()
    std = df1['GDP ($ per capita) dollars'].std()

    print("the mean of the GDP is: %.2lf" %mean)
    print("the median of the GDP is: %.1lf" % median)
    print("the mode of the GDP is: %d" % mode)
    print("the standard deviation of the GDP is: %.2lf\n" %std)

    ts = df1['GDP ($ per capita) dollars']
    ts.hist()
    plt.show()

    minimum = df1['Infant mortality (per 1000 births)'].min()
    quar1 , quar2, quar3 = df1['Infant mortality (per 1000 births)'].quantile([.25, .5, .75])
    maximum =  df1['Infant mortality (per 1000 births)'].max()

    print("the minimum of the Infant mortality is: %.2lf" %minimum)
    print("the First Quartile of the Infant mortality is: %.2lf" % quar1)
    print("the median of the Infant mortality is: %.2lf" % quar2)
    print("the third Quartile of the Infant mortality is: %.2lf" % quar3)
    print("the minimum of the Infant mortality is: %.2lf" % maximum)

    df1.boxplot(column=['Infant mortality (per 1000 births)'])
    plt.show()

    #quick attemp on the regression but didn't work
    #sns.lmplot(x='GDP ($ per capita) dollars', y='Infant mortality (per 1000 births)', data=df1, fit_reg=True)
    #plt.show


if __name__ == "__main__":

    statistics(df1)

    out = df1.to_json(orient='table',index=False)
    with open('output.json', 'w') as f:
        f.write(out)
