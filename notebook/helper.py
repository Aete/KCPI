# import libraries

# for processing data tables
import numpy as np
import pandas as pd

# for visualizations
import matplotlib.pyplot as plt
import seaborn as sns

# for sending requests to url and parsing
import requests
import json

def request_data_kosis(url, target_period, index = ['C1', 'C1_NM'], columns = 'ITM_NM', scale = 'metro', variable_name = False):
    '''
    This function is for request data based on given URL
    -----
    input:
        url(string): URL for requesting data 
        target_period(string): infomation about time that we want to request the data
        index (list): usually C1 (region code) and C1_NM (region Name)
        columns (string): a variable that we want to use as columns ( e.g) ITM_NM, C3, etc.)
        scale(string): 'metro' or 'basic'
    -----
    output:
        df_given_data (pd.DataFrame): A table that parsed as pandas.DataFrame based on a response from the given URL
    '''
    response = requests.get(url.format(target_period,target_period))
    df_given_data = pd.DataFrame(pd.DataFrame(json.loads(response.text)))
    df_given_data['DT'] = df_given_data['DT'].astype(float)
    if variable_name != False:
        df_given_data[columns] = variable_name
    df_given_data = df_given_data.pivot(index = index, values = 'DT', columns = columns).reset_index()
    df_given_data = df_given_data
    df_given_data['period'] = target_period
    df_given_data.columns.name = ''

    return df_given_data
