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


def import_data():

    politico = get_politico()
    print ("Politico data imported")
    fec = get_fec()
    print ("FEC data imported")
    acs = get_acs(census_key)
    print ("ACS data imported")
    dark_house = make_dark_house()
    print ("Dark Money data imported")

    #eventually move these to subfiles and rename dark_house.Total to DarkTotal
    #acs['DISTRICT'] = pd.to_numeric(acs['DISTRICT'], errors = 'coerce')
    #dark_house['DISTRICT'] = pd.to_numeric(dark_house['DISTRICT'], errors = 'coerce')

    alldata = join_files(politico, fec, acs, dark_house)

    return alldata


def join_files(politico, fec, acs, dark_house):

    alldata1 = pd.merge(politico, fec, left_on = ['year', 'STATE_ABBR', 'district', 'LAST_NAME'],
              right_on = ['CAND_ELECTION_YR', 'STATE', 'DISTRICT', 'LAST_NAME'], how='left')

    alldata2 = pd.merge(alldata1, acs, left_on = ['STATE_ABBR', 'district'],
              right_on = ['STATE_ABBR', 'DISTRICT'], how = 'left')

    alldata3 = pd.merge(alldata2, dark_house, left_on = ['STATE_ABBR', 'DISTRICT_x', 'LAST_NAME', 'year'],
              right_on = ['STATE', 'DISTRICT', 'LAST_NAME', 'Year'], how = 'left')

    return alldata3


def make_model_data(dataframe):

    model_data = dataframe.filter(items = ['YEAR2016', 'DEM', 'incumbent', 'TRANS_BY_INDIV', 'TRANS_BY_CMTE',
       'DARK_FOR', 'DARK_AGAINST', 'B01003_001E', 'B01002_001E', 'B02001_002E',
       'B02001_003E', 'B02001_004E', 'B02001_005E', 'B02001_006E', 'B02001_008E',
       'B05001_006E', 'B05001_005E', 'B05002_003E', 'B05012_001E',
       'B06007_001E', 'B06007_002E', 'B06007_003E', 'B06009_002E',
       'B06009_003E', 'B06009_004E', 'B06009_011E', 'B06009_012E',
       'B06010_001E', 'B06010_002E', 'B06011_001E', 'B06012_001E',
       'B06012_002E', 'B06012_003E', 'vote_count'])


    model_data['TRANS_BY_INDIV'].fillna(0, inplace = True)
    model_data['TRANS_BY_CMTE'].fillna(0, inplace = True)
    model_data['DARK_FOR'].fillna(0, inplace = True)
    model_data['DARK_AGAINST'].fillna(0, inplace = True)
    model_data = model_data.dropna(axis=0, how='any')

    return model_data


if __name__ == "__main__":

    beforepickle = False
    afterpickle = True

    if beforepickle == True:
        census_key = api_keys.census_api
        alldata = import_data()
        pickle.dump( alldata, open( "save.p", "wb" ) )

    if afterpickle == True:
        alldata = pickle.load( open( "save.p", "rb" ) )

        model_data = make_model_data(alldata)

        X = model_data.drop('vote_count', axis=1)
        y = model_data['vote_count']
        X_train, X_test, y_train, y_test = train_test_split(X,y)

        linear_model = LinearRegression()
        RF_model = RandomForestRegressor()
        GBR_model = GradientBoostingRegressor()
        MLP_model = MLPRegressor()

        # linear_model.fit(X_train, y_train)
        # lin_pred = Linear_model.predict(X_test)
        #
        # RF_model.fit(X_train, y_train)
        # RF_model.score
        #
        # GBR_model.fit(X_train, y_train)


        pipeline.fit(X_train, y_train)
        #thescore = pipeline.score(X_test)


        predicted_train = pipeline.fit(X_train).predict(X_train)
        predicted_test = pipeline.predict(X_test)
