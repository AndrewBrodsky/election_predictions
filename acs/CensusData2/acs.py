import numpy as np
import pandas as pd
import censusdata

import pandas as pd
import censusdata
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.precision', 2)
pd.options.display.float_format = '{:,.0f}'.format

censusdata.search('acs5', '2015', 'label', 'poverty')

first_tables = ['B16009_001E']

#Not included in the first round:
#Place of Birth
#Geographical Mobility
#Means of Transportation to Work
#Women who had a birth in past 12 months
#School enrollment level

#censusdata.printtable(censusdata.censustable('acs5', '2015', 'B16009'))

dists = censusdata.download('acs5', '2015',
          censusdata.censusgeo([('congressional district', '*')]), first_tables)
#dists.describe()

dists['index1'] = dists.index.astype(str)
dists['A'], dists['B'] = dists.index1.str.split(',',1).str
dists['state'], dists['C'] = dists.B.str.split(':',1).str
dists['D'], dists['E'], dists["district"], dists["F"] = dists.A.str.split(' ',3).str
dists.drop(['index1','A', 'B', 'C', 'D', 'E', 'F'], axis = 1, inplace = True)
dists.reset_index(drop=True, inplace = True)

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

dists.state = dists.state.str.strip()
dists['state_abbr'] =dists['state'].map(state_abbrev)
