# import libraries

# for processing data tables
import numpy as np
import pandas as pd

# for sending requests to url and parsing
import requests
import json

def request_data_kosis(url, target_period, index = ['C1', 'C1_NM'], columns = 'ITM_NM', scale = 'metro', variable_name = False):
    '''
    This function is for request data based on given URL
    -----
    input:
        url(string): the URL for requesting data 
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

def request_data_libsta(url, map_match_func, map_match_dict):
    '''
    This function is for request data based on given URL of the National Library Statistics System
    -----
    input:
        url (string): 
        target_period (int):  infomation about time that we want to request the data
    -----
    output:
        df_given_data (pd.DataFrame): A table that parsed as pandas.DataFrame based on a response from the given URL
    -----
    '''
    list_lib_type = ['LIBTYPE000001',
         'LIBTYPE000002001',
         'LIBTYPE000002002',
         'LIBTYPE000002003',
         'LIBTYPE000002004',
         'LIBTYPE000002007'];
    
    list_df = []
    for lib_type in list_lib_type:
        response = requests.get(url.format(2020,lib_type,str(1),str(100)))
        total_count = json.loads(response.text)['result']['count']

        for page in range(1, (total_count//100)+2):
            response = requests.get(url.format(2020,lib_type,str(page),str(100)))
            df_tmp = pd.DataFrame(json.loads(response.text)['result']['list'])
            list_df.append(df_tmp)

    df_given_data = pd.concat(list_df, ignore_index = False)
    df_given_data['localNm'] = df_given_data['addr'].apply(lambda x: x.split()[0])
    df_given_data['localNm'] = df_given_data['localNm'].apply(lambda x: map_hl(x,dict_hl_name))
    df_npl_by_region = df_given_data.groupby(by='localNm', as_index = False).count().iloc[:,:2]
    df_npl_by_region.columns = ['C1_NM', 'npl']

    return df_npl_by_region

dict_hl_name = {
    '서울특별시' : ['서울', '서울시', '서울특별시'],
    '부산광역시' : ['부산', '부산시', '부산광역시'],
    '대구광역시' : ['대구', '대구시', '대구광역시'],
    '인천광역시' : ['인천', '인천시', '인천광역시'],
    '광주광역시' : ['광주', '광주시', '광주광역시'],
    '대전광역시' : ['대전', '대전시', '대전광역시'],
    '울산광역시' : ['울산', '울산시', '울산광역시'],
    '세종특별자치시': ['세종', '세종시', '세종특별자치시'],
    '경기도' : ['경기도', '경기'],	
    '강원도' : ['강원도', '강원'],
    '충청북도' : ['충북', '충청북도'],
    '충청남도' : ['충남', '충청남도'],	
    '전라북도' : ['전북', '전라북도'],
    '전라남도' : ['전남', '전라남도'],
    '경상북도' : ['경북', '경상북도'],	
    '경상남도' : ['경남', '경상남도'],	
    '제주특별자치도' : ['제주', '제주특별자치도']
}

def map_hl(city, dictionary):
    '''
    This function is for unifying different high_level region names
    -----
    input:
        city(string): high level region name
        dictionary(dict): dict_hl_name
    -----
    output:
        k(string): unified high level region name
    '''
    for k,v in dictionary.items():
        if city in v:
            return k