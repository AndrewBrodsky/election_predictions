import pandas as pd
from sklearn.linear_model import LogisticRegression as LogReg
from sklearn.ensemble import (RandomForestRegressor as RFReg, GradientBoostingRegressor as GBReg)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

from politico import get_politico
from fec import get_fec
from acs import get_acs
from open_secrets import make_dark_house

def join_files(politico, fec, acs, dark_house):
    alldata1 = pd.merge(politico, fec, left_on = ['year', 'STATE_ABBR', 'district', 'LAST_NAME'],
              right_on = ['CAND_ELECTION_YR', 'STATE', 'DISTRICT', 'LAST_NAME'], how='left')

    alldata2 = pd.merge(alldata, acs, left_on = ['STATE_ABBR', 'district'],
              right_on = ['STATE_ABBR', 'DISTRICT'], how = 'left')

    alldata3 = pd.merge(alldata2, dark_house, left_on = ['STATE_ABBR', 'DISTRICT_x', 'LAST_NAME', 'year'],
              right_on = ['STATE', 'DISTRICT', 'LAST_NAME', 'Year'], how = 'left')

    return alldata3



if __name__ == "__main__":

    politico = get_politico()
    print ("Politico data imported")
    fec = get_fec()
    print ("FEC data imported")
    acs = get_acs()
    print ("ACS data imported")
    dark_house = make_dark_house()
    print ("Dark Money data imported")

    #eventually move this to subfiles and rename dark_house.Total to DarkTotal
    acs['DISTRICT'] = pd.to_numeric(acs['DISTRICT'], errors = 'coerce')
    dark_house['DISTRICT'] = pd.to_numeric(dark_house['DISTRICT'], errors = 'coerce')

    alldata = join_files(politico, fec, acs, dark_house)

    features = ['year', 'party', 'incumbent', 'TRANS_BY_INDIV', 'TRANS_BY_CMTE',
       'B01003_001E', 'B01002_001E', 'B02001_002E', 'B02001_003E',
       'B02001_004E', 'B02001_005E', 'B02001_006E', 'B02001_008E',
       'B05001_006E', 'B05001_005E', 'B05002_003E', 'B05012_001E',
       'B06007_001E', 'B06007_002E', 'B06007_003E', 'B06009_002E',
       'B06009_003E', 'B06009_004E', 'B06009_011E', 'B06009_012E',
       'B06010_001E', 'B06010_002E', 'B06011_001E', 'B06012_001E',
       'B06012_002E', 'B06012_003E']

    X = alldata[features]
    y = alldata[vote_count]
