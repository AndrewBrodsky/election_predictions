"""
Test downloading data from Census API.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import censusdata
import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal

class TestDownload(unittest.TestCase):

	def test_raw_download_state(self):
		self.assertEqual(censusdata._download('acs5', 2015, {'get': 'NAME,B01001_001E', 'for': 'state:17'}),
			{'NAME': ['Illinois'], 'B01001_001E': ['12873761'], 'state': ['17']})

	def test_raw_download_place(self):
		self.assertEqual(censusdata._download('acs5', 2015, {'get': 'NAME,B01001_001E', 'for': 'place:53000', 'in': 'state:06'}),
			{'NAME': ['Oakland city, California'], 'B01001_001E': ['408073'], 'state': ['06'], 'place': ['53000']})

	def test_geographies_state(self):
		for year in range(2009, 2015+1):
			self.assertEqual(censusdata.geographies(censusdata.censusgeo([('state', '*')]), 'acs5', year),
				{
				'Alaska': censusdata.censusgeo([('state', '02')]),
				'Alabama': censusdata.censusgeo([('state', '01')]),
				'Arkansas': censusdata.censusgeo([('state', '05')]),
				'Arizona': censusdata.censusgeo([('state', '04')]),
				'California': censusdata.censusgeo([('state', '06')]),
				'Colorado': censusdata.censusgeo([('state', '08')]),
				'Connecticut': censusdata.censusgeo([('state', '09')]),
				'District of Columbia': censusdata.censusgeo([('state', '11')]),
				'Delaware': censusdata.censusgeo([('state', '10')]),
				'Florida': censusdata.censusgeo([('state', '12')]),
				'Georgia': censusdata.censusgeo([('state', '13')]),
				'Hawaii': censusdata.censusgeo([('state', '15')]),
				'Iowa': censusdata.censusgeo([('state', '19')]),
				'Idaho': censusdata.censusgeo([('state', '16')]),
				'Illinois': censusdata.censusgeo([('state', '17')]),
				'Indiana': censusdata.censusgeo([('state', '18')]),
				'Kansas': censusdata.censusgeo([('state', '20')]),
				'Kentucky': censusdata.censusgeo([('state', '21')]),
				'Louisiana': censusdata.censusgeo([('state', '22')]),
				'Massachusetts': censusdata.censusgeo([('state', '25')]),
				'Maryland': censusdata.censusgeo([('state', '24')]),
				'Maine': censusdata.censusgeo([('state', '23')]),
				'Michigan': censusdata.censusgeo([('state', '26')]),
				'Minnesota': censusdata.censusgeo([('state', '27')]),
				'Missouri': censusdata.censusgeo([('state', '29')]),
				'Mississippi': censusdata.censusgeo([('state', '28')]),
				'Montana': censusdata.censusgeo([('state', '30')]),
				'North Carolina': censusdata.censusgeo([('state', '37')]),
				'North Dakota': censusdata.censusgeo([('state', '38')]),
				'Nebraska': censusdata.censusgeo([('state', '31')]),
				'New Hampshire': censusdata.censusgeo([('state', '33')]),
				'New Jersey': censusdata.censusgeo([('state', '34')]),
				'New Mexico': censusdata.censusgeo([('state', '35')]),
				'Nevada': censusdata.censusgeo([('state', '32')]),
				'New York': censusdata.censusgeo([('state', '36')]),
				'Ohio': censusdata.censusgeo([('state', '39')]),
				'Oklahoma': censusdata.censusgeo([('state', '40')]),
				'Oregon': censusdata.censusgeo([('state', '41')]),
				'Pennsylvania': censusdata.censusgeo([('state', '42')]),
				'Puerto Rico': censusdata.censusgeo([('state', '72')]),
				'Rhode Island': censusdata.censusgeo([('state', '44')]),
				'South Carolina': censusdata.censusgeo([('state', '45')]),
				'South Dakota': censusdata.censusgeo([('state', '46')]),
				'Tennessee': censusdata.censusgeo([('state', '47')]),
				'Texas': censusdata.censusgeo([('state', '48')]),
				'Utah': censusdata.censusgeo([('state', '49')]),
				'Virginia': censusdata.censusgeo([('state', '51')]),
				'Vermont': censusdata.censusgeo([('state', '50')]),
				'Washington': censusdata.censusgeo([('state', '53')]),
				'Wisconsin': censusdata.censusgeo([('state', '55')]),
				'West Virginia': censusdata.censusgeo([('state', '54')]),
				'Wyoming': censusdata.censusgeo([('state', '56')]),
				})

	def test_geographies_county(self):
		self.assertEqual(censusdata.geographies(censusdata.censusgeo([('state', '15'), ('county', '*')]), 'acs5', 2015), 
			{'Hawaii County, Hawaii': censusdata.censusgeo([('state', '15'), ('county', '001')]),
			'Honolulu County, Hawaii': censusdata.censusgeo([('state', '15'), ('county', '003')]),
			'Kalawao County, Hawaii': censusdata.censusgeo([('state', '15'), ('county', '005')]),
			'Kauai County, Hawaii': censusdata.censusgeo([('state', '15'), ('county', '007')]),
			'Maui County, Hawaii': censusdata.censusgeo([('state', '15'), ('county', '009')]),})
		self.assertEqual(censusdata.geographies(censusdata.censusgeo([('state', '15'), ('county', '*')]), 'acs1', 2015), 
			{'Hawaii County, Hawaii': censusdata.censusgeo([('state', '15'), ('county', '001')]),
			'Honolulu County, Hawaii': censusdata.censusgeo([('state', '15'), ('county', '003')]),
			'Kauai County, Hawaii': censusdata.censusgeo([('state', '15'), ('county', '007')]),
			'Maui County, Hawaii': censusdata.censusgeo([('state', '15'), ('county', '009')]),})

	def test_download_acs5_2015(self):
		assert_frame_equal(censusdata.download('acs5', 2015, censusdata.censusgeo([('state', '06'), ('place', '53000')]), ['B01001_001E', 'B01002_001E', 'B19013_001E']),
			pd.DataFrame({'B01001_001E': 408073, 'B01002_001E': 36.3, 'B19013_001E': 54618}, [censusdata.censusgeo([('state', '06'), ('place', '53000')], 'Oakland city, California')]))
		assert_frame_equal(censusdata.download('acs5', 2015, censusdata.censusgeo([('state', '15'), ('county', '*')]), ['B01001_001E', 'B01002_001E', 'B19013_001E']),
			pd.DataFrame({'B01001_001E': [191482, 984178, 85, 69691, 160863], 'B01002_001E': [41.1, 36.9, 51.9, 41.6, 40], 'B19013_001E': [52108, 74460, 66250, 65101, 66476]}, 
				[censusdata.censusgeo([('state', '15'), ('county', '001')], 'Hawaii County, Hawaii'), censusdata.censusgeo([('state', '15'), ('county', '003')], 'Honolulu County, Hawaii'),
				censusdata.censusgeo([('state', '15'), ('county', '005')], 'Kalawao County, Hawaii'),
				censusdata.censusgeo([('state', '15'), ('county', '007')], 'Kauai County, Hawaii'), censusdata.censusgeo([('state', '15'), ('county', '009')], 'Maui County, Hawaii')]))
		assert_frame_equal(censusdata.download('acs5', 2015, censusdata.censusgeo([('state', '17'), ('county', '031'), ('tract', '350100'), ('block group', '2')]), ['B01001_001E', 'B19013_001E']),
			pd.DataFrame({'B01001_001E': 1293, 'B19013_001E': 49375}, [censusdata.censusgeo([('state', '17'), ('county', '031'), ('tract', '350100'), ('block group', '2')], 'Block Group 2, Census Tract 3501, Cook County, Illinois')]))
		assert_frame_equal(censusdata.download('acs5', 2015, censusdata.censusgeo([('metropolitan statistical area/micropolitan statistical area', '16980')]), ['B01001_001E', 'B19013_001E']),
			pd.DataFrame({'B01001_001E': 9534008, 'B19013_001E': 61828}, [censusdata.censusgeo([('metropolitan statistical area/micropolitan statistical area', '16980')], 'Chicago-Naperville-Elgin, IL-IN-WI Metro Area')]))
		assert_frame_equal(censusdata.download('acs5', 2015, censusdata.censusgeo([('state', '06')]), ['DP03_0021PE'], tabletype='profile'),
			pd.DataFrame({'DP03_0021PE': 5.2}, [censusdata.censusgeo([('state', '06')], 'California')]))

	def test_download_acs5_200914(self):
		medhhinc = {2009: 55222, 2010: 55735, 2011: 56576, 2012: 56853, 2013: 56797, 2014: 57166}
		for year in range(2009, 2014+1):
			assert_frame_equal(censusdata.download('acs5', year, censusdata.censusgeo([('state', '17')]), ['B19013_001E']),
				pd.DataFrame({'B19013_001E': medhhinc[year]}, [censusdata.censusgeo([('state', '17')], 'Illinois')]))

	def test_download_acs1_2015(self):
		assert_frame_equal(censusdata.download('acs1', 2015, censusdata.censusgeo([('state', '17')]), ['B19013_001E']),
			pd.DataFrame({'B19013_001E': 59588}, [censusdata.censusgeo([('state', '17')], 'Illinois')]))

	def test_download_acs1_201214(self):
		medhhinc = {2012: 55137, 2013: 56210, 2014: 57444}
		for year in range(2012, 2014+1):
			assert_frame_equal(censusdata.download('acs1', year, censusdata.censusgeo([('state', '17')]), ['B19013_001E']),
				pd.DataFrame({'B19013_001E': medhhinc[year]}, [censusdata.censusgeo([('state', '17')], 'Illinois')]))

	def test_download_acsse(self):
		nocomputer = {2014: 731135, 2015: 658047}
		for year in range(2014, 2015+1):
			assert_frame_equal(censusdata.download('acsse', year, censusdata.censusgeo([('state', '17')]), ['K202801_006E']),
				pd.DataFrame({'K202801_006E': nocomputer[year]}, [censusdata.censusgeo([('state', '17')], 'Illinois')]))

	def test_download_acs3_detail(self):
		medhhinc = {2012: 55231, 2013: 55799}
		for year in medhhinc:
			assert_frame_equal(censusdata.download('acs3', year, censusdata.censusgeo([('state', '17')]), ['B19013_001E']),
				pd.DataFrame({'B19013_001E': medhhinc[year]}, [censusdata.censusgeo([('state', '17')], 'Illinois')]))

	def test_download_acs3_profile(self):
		insured = {2012: 78.3, 2013: 78.5}
		for year in insured:
			assert_frame_equal(censusdata.download('acs3', year, censusdata.censusgeo([('state', '17')]), ['DP03_0115PE'], tabletype='profile'),
				pd.DataFrame({'DP03_0115PE': insured[year]}, [censusdata.censusgeo([('state', '17')], 'Illinois')]))

	def test_download_sf1_2010(self):
		assert_frame_equal(censusdata.download('sf1', 2010, censusdata.censusgeo([('state', '17'), ('place', '14000')]), ['P0010001']),
			pd.DataFrame({'P0010001': 2695598}, [censusdata.censusgeo([('state', '17'), ('place', '14000')])]))

	def test_download_error_variable(self):
		self.assertRaises(ValueError, censusdata.download, 'acs5', 2015, censusdata.censusgeo([('state', '06'), ('place', '53000')]), ['B19013_010E'])

	def test_download_error_tabletype(self):
		self.assertRaises(ValueError, censusdata.download, 'acs5', 2015, censusdata.censusgeo([('state', '06')]), ['B19013_001E'], tabletype='cdetail')

if __name__ == '__main__':
	unittest.main()

