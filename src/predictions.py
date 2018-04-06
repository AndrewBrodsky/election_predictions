import numpy as np
import pandas as pd
import pickle
import time

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import (RandomForestRegressor, GradientBoostingRegressor)
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV

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


def add_late_breaking(dataframe):

    dataframe['LAST_TERM_YEAR'] = dataframe['YEAR'] - 2
    lastyear = dataframe[['YEAR', 'DEM', 'STATE_ABBR', 'DISTRICT', 'LAST_NAME']].copy()
    lastyear.rename(columns={'DEM' : 'LAST_TERM_DEM'}, inplace = True)
    newdf = pd.merge(dataframe, lastyear, left_on=['STATE_ABBR', 'DISTRICT', 'LAST_NAME', 'LAST_TERM_YEAR'],
                                          right_on =['STATE_ABBR', 'DISTRICT', 'LAST_NAME', 'YEAR'],
                                          how = 'left')
    newdf.rename(columns={'YEAR_x': 'YEAR'}, inplace = True)
    newdf.rename(columns={'PARTY_x': 'PARTY'}, inplace = True)

    return newdf


def make_model_data(dataframe):

    dataframe['MIDTERM'] = (dataframe['YEAR'] == 2010) | (dataframe['YEAR'] == 2014)
    dataframe['SAME_PARTY'] = dataframe['DEM'] == dataframe['LAST_TERM_DEM']

    dataframe.rename(index=str, columns={'B01003_001E' : 'TOTAL_POP',
                                         'B06007_001E' : 'LANG_UNIV',
                                         'B06010_001E' : 'INCOME_UNIV',
                                         'B06012_001E' : 'POVERTY_UNIV'}, inplace=True)

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
    dataframe['CTV_BELOW100FPL'] = dataframe['B08122_006E'] / dataframe['INCOME_UNIV']
    dataframe['CTV_100-149FPL'] = dataframe['B08122_007E'] / dataframe['INCOME_UNIV']
    dataframe['CTV_150'] = dataframe['B08122_008E'] / dataframe['INCOME_UNIV']
    dataframe['WALK_BELOW100FPL']= dataframe['B08122_018E'] / dataframe['INCOME_UNIV']
    dataframe['WALK_100-149FPL']= dataframe[ 'B08122_019E'] / dataframe['INCOME_UNIV']
    dataframe['WALK_100-149FPL'] = dataframe['B08122_020E'] / dataframe['INCOME_UNIV']

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

    features  = ['YEAR', 'DEM', 'MIDTERM', 'INCUMBENT', 'TRANS_BY_INDIV', 'TRANS_BY_CMTE',
           'DARK_FOR', 'DARK_AGAINST', 'TOTAL_POP', 'WHITE_PCT','BLACK_PCT','AMERIND_PCT',
           'ASIAN_PCT','PACIFIC_PCT','2RACES_PCT','NOTCITIZEN_PCT', 'FOREIGNCITIZEN_PCT',
           'BORNINSTATE_PCT','BORNINUS_PCT','ENGLISH_PCT','SPANISH_PCT','NOINCOME_PCT',
           'MEDIAN_INCOME_PCT','CTV_BELOW100FPL','CTV_100-149FPL','CTV_150',
           'WALK_BELOW100FPL','WALK_100-149FPL','WALK_100-149FPL','Below100FPL',
           '100_149FPL','POVERTYWM','POVERTYWF','ABOVEPOVERTYWM','ABOVEPOVERTYWF',
           'POVERTYBM','POVERTYBF','ABOVEPOVERTYBM','ABOVEPOVERTYBF', 'VOTE_COUNT']

    model_data = dataframe.filter(items = features )

    model_data['TRANS_BY_INDIV'].fillna(0, inplace = True)
    model_data['TRANS_BY_CMTE'].fillna(0, inplace = True)
    model_data['DARK_FOR'].fillna(0, inplace = True)
    model_data['DARK_AGAINST'].fillna(0, inplace = True)
    model_data = model_data.dropna(axis=0, how='any')

    return model_data, features


def make_splits(dataframe):

    X = dataframe.drop('VOTE_COUNT', axis=1)
    y = dataframe['VOTE_COUNT']
    X_train, X_test, y_train, y_test = train_test_split(X,y)

    return X_train, X_test, y_train, y_test


def other_stuff():
    np.set_printoptions(suppress=True)
    np.set_printoptions(precision=3)

    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)
    lin_pred = linear_model.predict(X_test)
    lin_zip= zip(X,linear_model.coef_)
    print ("Linear model: ", linear_model.score (X_test, y_test), sorted(lin_zip, key=lambda x: x[1]))
    print ("\r")

    RF_model = RandomForestRegressor()
    RF_model.fit(X_train, y_train)
    RF_importances = RF_model.feature_importances_
    RF_zip = zip(X, RF_importances)
    print ("RF model: ", RF_model.score(X_test, y_test), sorted(RF_zip, key=lambda x: x[1]))
    print ("\r")


    GB_model.fit(X_train, y_train)
    GB_importances = GB_model.feature_importances_
    GB_zip = zip(X, GB_importances)
    print ("GB model: ", GB_model.score(X_test, y_test), sorted(GB_zip, key=lambda x: x[1]))





def Grid_Search_RFR(X_train, y_train):

    estimator = RandomForestRegressor()

    param_grid = {
              "n_estimators"        : [10,50,100],
              "criterion"           : ['mse', 'mae'],
              "max_depth"           : [3, None],
              "max_features"        : ["auto", "sqrt", "log2"],
              "min_samples_split"   : [2,4,8],
              "min_samples_leaf"    : [1, 3, 10],
              "max_leaf_nodes"      : [None, 5],
              "bootstrap"            : [True, False]
              }

    grid = GridSearchCV(estimator, param_grid, n_jobs=-1, cv=5)
    tic = time.time()
    grid.fit(X_train, y_train)
    toc = time.time()
    print("GridSearchCV took %.2f seconds for %d candidate parameter settings."
      % (toc - tic, len(grid.cv_results_['params'])))
    # report(grid.cv_results_)
    print ("Best score:", grid.best_score_, "\n best paarms: ", grid.best_params_)
    return grid.cv_results_, grid.best_score_, grid.best_params_


def Grid_Search_GBR(X_train, y_train):

    estimator = GradientBoostingRegressor()

    param_grid = {
              "loss"                : ['ls', 'lad', 'huber', 'quantile'],
              "n_estimators"        : [50,100,150],
              "max_depth"           : [1, 3, 6],
              "min_samples_split"   : [2,4,8],
              "min_samples_leaf"    : [1, 3, 10],
              "subsample"           : [.5, 1],
              "max_features"        : ["auto", "sqrt", "log2", None]
                }

    grid = GridSearchCV(estimator, param_grid, n_jobs=-1)
    tic = time.time()
    grid.fit(X_train, y_train)
    toc = time.time()
    print("GridSearchCV took %.2f seconds for %d candidate parameter settings."
      % (toc - tic, len(grid.cv_results_['params'])))
    # report(grid.cv_results_)
    print ("Gradient Boosted Regressor results: \n, Best score:", grid.best_score_, "best paarms: ", grid.best_params_)
    return grid.cv_results_, grid.best_score_, grid.best_params_


if __name__ == "__main__":

    #Comment next line if pickle file already created
    #make_alldata()

    alldata = pickle.load( open( "save.p", "rb" ) )

    late_breaking = add_late_breaking(alldata)

    model_data, features = make_model_data(late_breaking)

    X_train, X_test, y_train, y_test = make_splits(model_data)

    #RFR_results, RFR_best_score, RFR_best_params = Grid_Search_RFR(X_train, y_train)

    #GBR_results, GBR_best_score, GBR_best_params = Grid_Search_GBR(X_train, y_train)
