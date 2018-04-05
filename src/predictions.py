import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import (RandomForestRegressor, GradientBoostingRegressor)
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

from politico import get_politico
from fec import get_fec
from acs import get_acs
from open_secrets import make_dark_house
import api_keys


def join_files(politico, fec, acs, dark_house):

    alldata1 = pd.merge(politico, fec, on = ['YEAR', 'STATE_ABBR', 'DISTRICT', 'LAST_NAME'],
              how='left')

    alldata2 = pd.merge(alldata1, acs, on = ['STATE_ABBR', 'DISTRICT'],
              how = 'left')

    alldata3 = pd.merge(alldata2, dark_house, on = ['STATE_ABBR', 'DISTRICT', 'LAST_NAME', 'YEAR'],
              how = 'left')

    return alldata3


def import_data(census_key):

    politico = get_politico()
    print ("Politico data imported")
    fec = get_fec()
    print ("FEC data imported")
    acs = get_acs(census_key)
    print ("ACS data imported")
    dark_house = make_dark_house()
    print ("Dark Money data imported")

    alldata = join_files(politico, fec, acs, dark_house)

    return alldata


def make_alldata():

    census_key = api_keys.census_api
    alldata = import_data(census_key)
    pickle.dump( alldata, open( "save.p", "wb" ) )


def make_model_data(dataframe):

    dataframe.rename(index=str, columns={'TOTAL_POP' : 'B01003_001E',
                                         'LANG_UNIV' : 'B06007_001E',
                                         'INCOME_UNIV' : 'B06010_001E',
                                         'POVERTY_UNIV' : 'B06012_001E'})

    '''

    'Transportation by CTV - below 100 pct FPL' : 'B08122_006E',
    'Transportation by CTV - 100-149 pct FPL' : 'B08122_007E',
    'Transportation by CTV - 150 FPL +' : 'B08122_008E',
    'Transportation by CTV - below 100 pct FPL' : 'B08122_018E',
    'Transportation by CTV - 100-149 pct FPL' : 'B08122_019E',
    'Transportation by CTV - 150 FPL +' : 'B08122_020E'

    '''


    dataframe['WHITE_PCT'] = dataframe['B02001_002E'] / dataframe['TOTAL_POP']
    dataframe['BLACK_PCT'] = dataframe['B02001_003E'] / dataframe['TOTAL_POP']
    dataframe['AMERIND_PCT'] = dataframe['B02001_004E'] / dataframe['TOTAL_POP']
    dataframe['ASIAN_PCT'] = dataframe['B02001_005E'] / dataframe['TOTAL_POP']
    dataframe['PACIFIC_PCT'] = dataframe['B02001_006E'] / dataframe['TOTAL_POP']
    dataframe['2RACES_PCT'] = dataframe['B02001_008E'] / dataframe['TOTAL_POP']
    dataframe['NOTCITIZEN_PCT'] = dataframe['B05001_006E'] / dataframe['TOTAL_POP']
    dataframe['FOREIGNCITIZEN_PCT'] = dataframe['B05001_005E'] / dataframe['TOTAL_POP']
    dataframe['BORNINSTATE_PCT'] = dataframe['B05002_003E'] / dataframe['TOTAL_POP']
    dataframe['BORNINUS_PCT'] = dataframe['B05012_001E'] / dataframe['TOTAL_POP']

    dataframe['ENGLISH_PCT'] = dataframe['B06007_002E'] / dataframe['LANG_UNIV']
    dataframe['SPANISH_PCT'] = dataframe['B06007_003E'] / dataframe['LANG_UNIV']

    dataframe['NOINCOME_PCT'] = dataframe['B06007_002E'] / dataframe['INCOME_UNIV']
    dataframe['MEDIAN_INCOME_PCT'] = dataframe['B06007_003E'] / dataframe['INCOME_UNIV']

    dataframe['Below100FPL'] = dataframe['B06012_002E'] / dataframe['POVERTY_UNIV']
    dataframe['100_149FPL'] = dataframe['POVERTY_UNIV']
    dataframe['POVERTYWM'] = dataframe['B17001A_003E'] / dataframe['POVERTY_UNIV']
    dataframe['POVERTYWF'] = dataframe['B17001A_017E'] / dataframe['POVERTY_UNIV']
    dataframe['ABOVEPOVERTYWM'] = dataframe['B17001A_032E'] / dataframe['POVERTY_UNIV']
    dataframe['ABOVEPOVERTYWF'] = dataframe['B17001A_046E'] / dataframe['POVERTY_UNIV']
    dataframe['POVERTYBM'] = dataframe['B17001B_003E'] / dataframe['POVERTY_UNIV']
    dataframe['POVERTYBF'] = dataframe['B17001B_017E'] / dataframe['POVERTY_UNIV']
    dataframe['ABOVEPOVERTYBM'] = dataframe['B17001B_032E'] / dataframe['POVERTY_UNIV']
    dataframe['ABOVEPOVERTYBF'] = dataframe['B17001B_046E'] / dataframe['POVERTY_UNIV']





    features  = ['YEAR', 'incumbent', 'TRANS_BY_INDIV', 'TRANS_BY_CMTE',
           'DARK_FOR', 'DARK_AGAINST', 'B01003_001E', 'B01002_001E', 'B02001_002E',
           'B02001_003E', 'B02001_004E', 'B02001_005E', 'B02001_006E', 'B02001_008E',
           'B05001_006E', 'B05001_005E', 'B05002_003E', 'B05012_001E',
           'B06007_001E', 'B06007_002E', 'B06007_003E', 'B06009_002E',
           'B06009_003E', 'B06009_004E', 'B06009_011E', 'B06009_012E',
           'B06010_001E', 'B06010_002E', 'B06011_001E', 'B06012_001E',
           'B06012_002E', 'B06012_003E', 'vote_count']

    model_data = dataframe.filter(items = features )

    model_data['TRANS_BY_INDIV'].fillna(0, inplace = True)
    model_data['TRANS_BY_CMTE'].fillna(0, inplace = True)
    model_data['DARK_FOR'].fillna(0, inplace = True)
    model_data['DARK_AGAINST'].fillna(0, inplace = True)
    model_data = model_data.dropna(axis=0, how='any')

    return model_data


def make_pipeline(dataframe):
    X = dataframe.drop('vote_count', axis=1)
    y = dataframe['vote_count']
    X_train, X_test, y_train, y_test = train_test_split(X,y)

    np.set_printoptions(suppress=True)
    np.set_printoptions(precision=3)

    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)
    lin_pred = linear_model.predict(X_test)
    lin_zip= zip(features,linear_model.coef_)
    print ("Linear model: ", linear_model.score (X_test, y_test), sorted(lin_zip, key=lambda x: x[1]))
    print ("\r")

    RF_model = RandomForestRegressor()
    RF_model.fit(X_train, y_train)
    RF_importances = RF_model.feature_importances_
    RF_zip = zip(features, RF_importances)
    print ("RF model: ", RF_model.score(X_test, y_test), sorted(RF_zip, key=lambda x: x[1]))
    print ("\r")

    GB_model = GradientBoostingRegressor()
    GB_model.fit(X_train, y_train)
    GB_importances = GB_model.feature_importances_
    GB_zip = zip(features, GB_importances)
    print ("GB model: ", GB_model.score(X_test, y_test), sorted(GB_zip, key=lambda x: x[1]))


if __name__ == "__main__":

    #Comment next line if pickle file already created
    make_alldata()

    #alldata = pickle.load( open( "save.p", "rb" ) )

    #model_data = make_model_data(alldata)

    #make_pipeline(model_data)
