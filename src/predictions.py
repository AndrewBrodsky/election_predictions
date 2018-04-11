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

    '''
    DESCRIPTION:
    Joins data from politico, fed, acs, and open secrets files together

    INPUT:
    politico: Pandas dataframe of vote count data
    fec: Pandas dataframe with individual and committee contributions for each candidate
    acs: Pandas dataframe with district characteristics
    dark_house: Pandas dataframe with dark money contributions for and against each candidate

    RETURNS:
    alldata3: Pandas dataframe containing data from all sources by candidate
    '''

    alldata1 = pd.merge(politico, fec, on = ['YEAR', 'STATE_ABBR', 'DISTRICT', 'LAST_NAME'],
              how='left')

    alldata2 = pd.merge(alldata1, acs, on = ['STATE_ABBR', 'DISTRICT'],
              how = 'left')

    alldata3 = pd.merge(alldata2, dark_house, on = ['STATE_ABBR', 'DISTRICT', 'LAST_NAME', 'YEAR'],
              how = 'left')

    return alldata3


def import_data(census_key):

    '''
    DESCRIPTION:
    Imports data using the politico, fec, acs and open secrets modules

    INPUT:
    census_key: API key for accessing the CensusDatas database

    RETURNS:
    alldata: Pandas dataframe containing data from all sources by candidate
    '''

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

    '''
    DESCRIPTION:
    Creates datafrmae will all data for each module and saves to picle file

    INPUT:
    None

    RETURNS:
    Saves pickle file containing alldata dataframe
    '''

    census_key = api_keys.census_api
    alldata = import_data(census_key)
    pickle.dump( alldata, open( "save.p", "wb" ) )


def add_late_breaking(dataframe):

    '''
    DESCRIPTION:
    Adds in additional data, including vote totals from 2010 and 2012

    INPUT:
    dataframe: Pandas dataframe containing alldata file

    RETURNS:
    newdf: Pandas dataframe with complete dataset, includign 2010 and 2012 data
    '''

    data_2008 = pd.read_csv('house_votes_2008.csv')
    data_2008['LAST_TERM_DEM'] = data_2008['PARTY'] == 'DEM'
    data_2008.drop(columns = 'PARTY', inplace= True)
    #dataframe.drop(columns = 'PARTY', inplace= True)

    dataframe['LAST_TERM_YEAR'] = dataframe['YEAR'] - 2

    lastyear = dataframe[['YEAR', 'DEM', 'STATE_ABBR', 'DISTRICT', 'LAST_NAME']].copy()
    lastyear.rename(columns={'DEM' : 'LAST_TERM_DEM', 'YEAR': 'LAST_TERM_YEAR'}, inplace = True)
    prev_years = pd.concat([lastyear, data_2008])

    newdf = pd.merge(dataframe, prev_years, on=['STATE_ABBR', 'DISTRICT', 'LAST_NAME', 'LAST_TERM_YEAR'],
                                          how = 'left')

    return newdf


def make_model_data(dataframe):

    '''
    DESCRIPTION:
    Creates new features for further analysis

    INPUT:
    dataframe: Pandas dataframe containing all data from all modules

    RETURNS:
    model_data: Pandas dataframe containing set of features and vote totals for ensemble methods
    features: list of features for use in ensemble modeling
    '''

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
    #dataframe['BORNINUS_PCT'] = dataframe['B05012_002E'] / dataframe['TOTAL_POP']

    dataframe['ENGLISH_PCT'] = dataframe['B06007_002E'] / dataframe['LANG_UNIV']
    dataframe['SPANISH_PCT'] = dataframe['B06007_003E'] / dataframe['LANG_UNIV']

    dataframe['NOINCOME_PCT'] = dataframe['B06010_002E'] / dataframe['INCOME_UNIV']
    dataframe['MEDIAN_INCOME'] = dataframe['B06011_001E']

    dataframe['WALK_150FPL'] = dataframe['B08122_020E'] / dataframe['INCOME_UNIV']

    dataframe['Below100FPL'] = dataframe['B06012_002E'] / dataframe['POVERTY_UNIV']
    dataframe['100_149FPL'] = dataframe['B06012_003E'] / dataframe['POVERTY_UNIV']

    dataframe['CTV_BELOW100FPL'] = dataframe['B08122_006E'] / dataframe['B06012_002E']
    dataframe['CTV_100-149FPL'] = dataframe['B08122_007E'] / dataframe['B06012_003E']

    dataframe['WALK_BELOW100FPL']= dataframe['B08122_018E'] / dataframe['B06012_002E']
    dataframe['WALK_100-149FPL']= dataframe[ 'B08122_019E'] / dataframe['B06012_003E']

    dataframe['POVERTYWM'] = dataframe['B17001A_003E'] / dataframe['POVERTY_UNIV']
    dataframe['POVERTYWF'] = dataframe['B17001A_017E'] / dataframe['POVERTY_UNIV']
    dataframe['ABOVEPOVERTYWM'] = dataframe['B17001A_032E'] / dataframe['POVERTY_UNIV']
    dataframe['ABOVEPOVERTYWF'] = dataframe['B17001A_046E'] / dataframe['POVERTY_UNIV']
    dataframe['POVERTYBM'] = dataframe['B17001B_003E'] / dataframe['POVERTY_UNIV']
    dataframe['POVERTYBF'] = dataframe['B17001B_017E'] / dataframe['POVERTY_UNIV']
    dataframe['ABOVEPOVERTYBM'] = dataframe['B17001B_032E'] / dataframe['POVERTY_UNIV']
    dataframe['ABOVEPOVERTYBF'] = dataframe['B17001B_046E'] / dataframe['POVERTY_UNIV']

    features  = ['YEAR', 'DEM', 'MIDTERM', 'SAME_PARTY', 'INCUMBENT', 'TRANS_BY_INDIV', 'TRANS_BY_CMTE',
           'DARK_FOR', 'DARK_AGAINST', 'TOTAL_POP', 'WHITE_PCT','BLACK_PCT','AMERIND_PCT',
           'ASIAN_PCT','PACIFIC_PCT','2RACES_PCT','NOTCITIZEN_PCT', 'FOREIGNCITIZEN_PCT',
           'BORNINSTATE_PCT', 'ENGLISH_PCT','SPANISH_PCT','NOINCOME_PCT',
           'MEDIAN_INCOME','CTV_BELOW100FPL','CTV_100-149FPL',
           'WALK_BELOW100FPL','WALK_100-149FPL','Below100FPL',
           '100_149FPL','POVERTYWM','POVERTYWF','ABOVEPOVERTYWM','ABOVEPOVERTYWF',
           'POVERTYBM','POVERTYBF','ABOVEPOVERTYBM','ABOVEPOVERTYBF', 'VOTE_COUNT']

    model_data = dataframe.filter(items = features )

    model_data['TRANS_BY_INDIV'].fillna(0, inplace = True)
    model_data['TRANS_BY_CMTE'].fillna(0, inplace = True)
    model_data['DARK_FOR'].fillna(0, inplace = True)
    model_data['DARK_AGAINST'].fillna(0, inplace = True)
    model_data = model_data.dropna(axis=0, how='any')

    return model_data, features


def make_bellwether(dataframe, state, dist):

    '''
    DESCRIPTION:
    Web scraper that pulls candidate data from Politico and converts into a dict
    of Beautiful Soup objects

    INPUT:
    years: Year of data to scrape (int)
    states:  list of state names to scrape

    RETURNS:
    datadict: dict with nubmer of votes, party, incumbency status, state and
        district for every candidate
    '''

    bellwether = dataframe[(dataframe['STATE_ABBR'] == state) & (dataframe['DISTRICT'] == dist)]
    filename_xls = str('bellwether' + state + str(dist) + '.xlsx')
    writer = pd.ExcelWriter(filename_xls)
    bellwether.to_excel(writer,'Sheet1')
    writer.save()

    #Data on current candidates and funding are manually added to Excel file

    filename_csv = str('bellwether' + state + str(dist) + '.csv')

    bellwether = pd.read_csv(filename_csv)
    bellwether = bellwether.drop('VOTE_COUNT', axis=1)

    return bellwether


def make_splits(dataframe):

    '''
    DESCRIPTION:
    Creates training and test sets from dataframe

    INPUT:
    dataframe: Pandas dataframe with model-ready data

    RETURNS:
    X_train: Pandas dataframe with features for model training
    X_test: Pandas dataframe with features for model testing
    y_train: Pandas data series with outcome variable (vote count) for model training
    y_test: Pandas data series with outcome variable (vote count) for model training
    '''

    X = dataframe.drop('VOTE_COUNT', axis=1)
    y = dataframe['VOTE_COUNT']
    X_train, X_test, y_train, y_test = train_test_split(X,y)

    return X_train, X_test, y_train, y_test


def Run_Grid_Search(estimator, param_grid, X, y):

    '''
    DESCRIPTION:
    Performs a grid search and returns resuts

    INPUT:
    estimator: Estimator object used for analysis
    param_grid: list of parameters to be used for grid search
    X: Pandas dataframe containing features
    y: Pandas data series containing outcome variable

    RETURNS:
    grid.cv_results: results of grid search
    grid.best_score_: R2 value for best grid search result
    grid.best_params_: dictionary of best parameters
    '''

    grid = GridSearchCV(estimator, param_grid, n_jobs=-1, cv=3)
    tic = time.time()
    grid.fit(X, y)
    toc = time.time()
    print("GridSearchCV took %.2f seconds for %d candidate parameter settings."
      % (toc - tic, len(grid.cv_results_['params'])))
    # report(grid.cv_results_)
    print ("Gradient Boosted Regressor results: \n, Best score:", grid.best_score_, "best params: ", grid.best_params_)
    return grid.cv_results_, grid.best_score_, grid.best_params_


def grid_searches(X, y):

    '''
    DESCRIPTION:
    Runs a grid search with selected parameters for random forest and gradient boosted regressor

    INPUT:
    X: Pandas dataframe containing features
    y: Pandas data series containing outcome variable

    RETURNS:
    None
    '''


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

    estimator = RandomForestRegressor()

    RFR_results, RFR_best_score, RFR_best_params = Run_Grid_Search(
            estimator, param_grid, X_train, y_train)

    param_grid = {
              "loss"                : ['ls', 'lad', 'huber', 'quantile'],
              "n_estimators"        : [50,100,150],
              "max_depth"           : [1, 3, 6],
              "min_samples_split"   : [2,4,8],
              "min_samples_leaf"    : [1, 3, 10],
              "subsample"           : [.5, 1],
              "max_features"        : ["auto", "sqrt", "log2", None]
              }

    estimator = GradientBoostingRegressor()

    GBR_results, GBR_best_score, GBR_best_params = Run_Grid_Search(
            estimator, param_grid, X_train, y_train)

    """
    Random Forest Results:
    Best score: 0.7418130304838402
    best params:  {'bootstrap': False, 'criterion': 'mae', 'max_depth': None, 'max_features': 'sqrt',
    'max_leaf_nodes': None, 'min_samples_leaf': 1, 'min_samples_split': 8, 'n_estimators': 100}
    GridSearchCV took 961.49 seconds for 2592 candidate parameter settings.

    Gradient Boosted Regressor results:
    Best score: 0.782590603703688
    best params:  {'loss': 'huber', 'max_depth': 6, 'max_features': None, 'min_samples_leaf': 10,
    'min_samples_split': 4, 'n_estimators': 150, 'subsample': 1}
    """


def bar_plot(feature_names, feature_importances):
    y_ind = np.arange(9, -1, -1)  # 9 to 0
    fig = plt.figure(figsize=(8, 8))
    plt.barh(y_ind, feature_importances, height=0.3, align='center')
    plt.ylim(y_ind.min() + 0.5, y_ind.max() + 0.5)
    plt.yticks(y_ind, feature_names)
    plt.xlabel('Relative feature importances')
    plt.ylabel('Features')
    figname = '3_1_feature_importance_bar_plot.png'
    plt.tight_layout()
    plt.savefig(figname, dpi=100)
    plt.close()
    print ("\n1) {0} plot saved.".format(figname))


def GBR(X_train, X_test, y_train, y_test):

    '''
    DESCRIPTION:
    Runs Gradient Boosted Regressor on training set and reports score on test set

    INPUT:
    X_train: Pandas dataframe with features for model training
    X_test: Pandas dataframe with features for model testing
    y_train: Pandas data series with outcome variable (vote count) for model training
    y_test: Pandas data series with outcome variable (vote count) for model training

    RETURNS:
    GB_model: Object containing fitted Gradient Boosted Regressor model
    '''

    best_params =  {
        'loss': 'huber',
        'max_depth': 6,
        'max_features': None,
        'min_samples_leaf': 10,
        'min_samples_split': 4,
        'n_estimators': 150,
        'subsample': 1
        }

    GB_model = GradientBoostingRegressor(**best_params)
    GB_model.fit(X_train, y_train)
    GB_importances = GB_model.feature_importances_
    GB_zip = zip(X_train, GB_importances)

    sorted_zip = sorted(GB_zip, key=lambda x: x[1], reverse=True)
    print ("GB model score: ", GB_model.score(X_test, y_test))
    print ("\n GB model importances: ", sorted_zip )

    feature_names = [[x[0] for x in sorted_zip[:10]]]
    feature_importances = [[x[0] for x in sorted_zip[:10]]]
    make_plot(feature names, feature importances)

    return GB_model, sorted_zip


if __name__ == "__main__":

    pd.options.display.float_format = '{:,.3f}'.format
    pd.set_option('display.max_columns', 500)

    #Comment next line if pickle file already created
    #make_alldata()

    alldata = pickle.load( open( "save.p", "rb" ) )

    late_breaking = add_late_breaking(alldata)

    model_data, features = make_model_data(late_breaking)

    bellwether_CA45 = make_bellwether(late_breaking, 'CA', 45)
    model_data_CA45, _ = make_model_data(bellwether_CA45)

    writer = pd.ExcelWriter('model_data.xlsx')
    model_data.to_excel(writer,'Sheet1')
    writer.save()

    X_train, X_test, y_train, y_test = make_splits(model_data)

    #takes 30-45 minutes
    #grid_searches(X_train, y_train)

    GB_model, sorted_zip = GBR(X_train, X_test, y_train, y_test)

    CA45_votes = GB_model.predict(model_data_CA45)
