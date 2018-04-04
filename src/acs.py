import numpy as np
import pandas as pd
from acs_api.CensusData2 import censusdata
import api_keys

census_key = api_keys.census_api

def make_dicts():
    #censusdata.search('acs5', '2015', 'label', 'poverty')

    acs_tables = {
        'Total Pop.': 'B01003_001E',
        'Median Age' : 'B01002_001E',
        'White' : 'B02001_002E',
        'Black' : 'B02001_003E',
        'Amer Ind' : 'B02001_004E',
        'Asian' : 'B02001_005E',
        'Pacific' : 'B02001_006E',
        '2+ Races' : 'B02001_008E',
        'Not U.S. Citizen' : 'B05001_006E',
        'U.S. Citizen by Naturalization' : 'B05001_005E',
        'Born in state of residence' : 'B05002_003E',
        'Born in U.S.' : 'B05012_001E',
        'Total Language Universe' : 'B06007_001E',
        'Speak only English' : 'B06007_002E',
        'Speak Spanish' : 'B06007_003E',
        'Less than HS Grad' : 'B06009_002E',
        'HS grad' : 'B06009_003E',
        'Some college' : 'B06009_004E',
        'Bachelors degree' : 'B06009_011E',
        'Grad degree' : 'B06009_012E',
        'Income universe' : 'B06010_001E',
        'No income' : 'B06010_002E',
        'Median income' : 'B06011_001E',
        'Poverty Universe' : 'B06012_001E',
        'Below 100 pct FPL' : 'B06012_002E',
        '100-149 FPL' : 'B06012_003E',
        'Income below poverty (White male)' : 'B17001A_003E',
        'Income below poverty (White male)' : 'B17001A_003E',
        'Income below poverty (White female)' : 'B17001A_017E',
        'Income above poverty (White male)' : 'B17001A_032E',
        'Income above poverty (White female)' : 'B17001A_046E',
        'Income below poverty (Black male)' : 'B17001B_003E',
        'Income below poverty (Black female)' : 'B17001B_017E',
        'Income above poverty (Black male)' : 'B17001B_032E',
        'Income above poverty (Black female)' : 'B17001B_046E',
        'Transportation by CTV - below 100 pct FPL' : 'B08122_006E',
        'Transportation by CTV - 100-149 pct FPL' : 'B08122_007E',
        'Transportation by CTV - 150 FPL +' : 'B08122_008E',
        'Transportation by CTV - below 100 pct FPL' : 'B08122_018E',
        'Transportation by CTV - 100-149 pct FPL' : 'B08122_019E',
        'Transportation by CTV - 150 FPL +' : 'B08122_020E'
        }


    state_abbrev = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY',
        'Puerto Rico': 'PY'
        }

    bad_tables = {
        'White Male Under 18' : 'C01001A_003E',
        'White Male 18-64': 'C01001A_004E',
        'White Male 65+' : 'C01001A_005E',
        'White Female Under 18' : 'C01001A_007E',
        'White Female 18-64' : 'C01001A_008E',
        'White Female 65+' : 'C01001A_009E',
        'Black Male Under 18' : 'C01001B_003E',
        'Black Male 18-64': 'C01001B_004E',
        'Black Male 65+' : 'C01001B_005E',
        'Black Female Under 18' : 'C01001B_007E',
        'Black Female 18-64' : 'C01001B_008E',
        'Black Female 65+' : 'C01001B_009E',
        'Hipsanic Male Under 18' : 'C01001I_003E',
        'Hispanic Male 18-64': 'C01001I_004E',
        'Hispanic Male 65+' : 'C01001I_005E',
        'Hispanic Female Under 18' : 'C01001I_007E',
        'Hispanic Female 18-64' : 'C01001I_008E',
        'Hispanic Female 65+' : 'C01001I_009E',
        'Reporting Ancestry' : 'C04004_001E',
        'American Ancestry' : 'C04004_002E',
        'Black women wtih birth in past 12 months' : 'B13002B_002E',
        'Mobility for income below 100 pct FPL' : 'B07012-002E',
        'Black women with no birth in past 12 months' : 'B13002B_005E',
        'Mobility for income below 100 pct FPL' : 'B07012-002E',
        'White women wtih birth in past 12 months' : 'B13002A_002E',
        'White women with no birth in past 12 months' : 'B13002A_005E',
        }

    return acs_tables, state_abbrev


def make_dists(acs_tables, census_key):

    tables = []

    for k, v in acs_tables.items():
       tables.append(v)

    #censusdata.printtable(censusdata.censustable('acs5', '2015', 'B16009'))

    dists = pd.DataFrame
    state_df=[]

    state_FIPS = [1, 2, 4, 5, 6, 8, 9, 10, 12, 13,
                  15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                  25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
                  35, 36, 37, 38, 39, 40, 41, 42, 44, 45,
                  46, 47, 48, 49, 50, 51, 53, 54, 55, 56]

    for st in state_FIPS:
        state_df.append(censusdata.download('acs5', '2015',
              censusdata.censusgeo([('state', str(st)), ('congressional district', '*')]), tables, census_key))

    dists = pd.concat(state_df[x] for x in range(50))

    return dists


def make_acs(dists, state_abbrev):

    dists['INDEX1'] = dists.index.astype(str)
    dists['A'], dists['B'] = dists.INDEX1.str.split(',',1).str
    dists['STATE'], dists['C'] = dists.B.str.split(':',1).str
    dists['D'], dists['E'], dists['DISTRICT'], dists["F"] = dists.A.str.split(' ',3).str
    dists.drop(['INDEX1','A', 'B', 'C', 'D', 'E', 'F'], axis = 1, inplace = True)
    dists.reset_index(drop=True, inplace = True)

    dists.STATE = dists.STATE.str.strip()
    dists['STATE_ABBR'] = dists['STATE'].map(state_abbrev)
    dists['DISTRICT'] = pd.to_numeric(dists['DISTRICT'], errors = 'coerce')

    return dists


def get_acs(census_key):

    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('display.precision', 2)
    pd.options.display.float_format = '{:,.0f}'.format

    acs_tables, state_abbrev = make_dicts()

    dists = make_dists(acs_tables, census_key)

    acs = make_acs(dists, state_abbrev)

    return acs


if __name__ == "__main__":

    acs = get_acs(census_key)
