#!/usr/bin/env python
# Name: Siger de vries
# Student number: 10289321
"""
This script visualizes data obtained from a .csv file
"""

import csv
import matplotlib.pyplot as plt
import pandas as pd


# Global constants for the input file, first and last year
df = pd.read_csv('movies.csv')
number = df.groupby('Year').size()
sum = df.groupby('Year').Rating.sum()
average = sum/number

if __name__ == "__main__":
    print(number)
    print(sum)
    print(average)
    average.plot()
