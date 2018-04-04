"""" Test showing information on variables from Census API.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import censusdata
import unittest
from collections import OrderedDict
import io
import textwrap

class TestVariableInfo(unittest.TestCase):

	def test_censusvar_acs5(self):
		for year in range(2009, 2013+1):
			predicateType = 'int'
			if year == 2011: predicateType = ''
			expected = {'B01001_001E': ['B01001.  Sex by Age', 'Total:', predicateType],
				'B01002_001E': ['B01002.  Median Age by Sex', 'Median age --!!Total:', predicateType],
				'B19013_001E': ['B19013.  Median Household Income'.format(year),
					'Median household income in the past 12 months (in {0} inflation-adjusted dollars)'.format(year), predicateType]}
			self.assertEqual(censusdata.censusvar('acs5', year, ['B01001_001E', 'B01002_001E', 'B19013_001E']), expected)
		for year in range(2014, 2015+1):
			expected = {'B01001_001E': ['B01001.  Sex by Age', 'Total:', 'int'],
				'B01002_001E': ['B01002.  Median Age by Sex', 'Median age --!!Total:', 'int'],
				'B19013_001E': ['B19013. Median Household Income in the Past 12 Months (in {0} Inflation-Adjusted Dollars)'.format(year),
					'Median household income in the past 12 months (in {0} Inflation-adjusted dollars)'.format(year), 'int']}
			self.assertEqual(censusdata.censusvar('acs5', year, ['B01001_001E', 'B01002_001E', 'B19013_001E']), expected)

	def test_censusvar_acs1(self):
		expected = {'S0101_C02_001E': ['Age and Sex', 'Male!!Total population', 'string'],
			'DP03_0021PE': ['SELECTED ECONOMIC CHARACTERISTICS', 'COMMUTING TO WORK!!Workers 16 years and over!!Public transportation (excluding taxicab)', 'int'],
			'CP02_2011_030E': ['COMPARATIVE SOCIAL CHARACTERISTICS IN THE UNITED STATES', '2011 Estimate!!MARITAL STATUS!!Females 15 years and over', 'string']}
		self.assertEqual(censusdata.censusvar('acs1', 2015, ['S0101_C02_001E', 'DP03_0021PE', 'CP02_2011_030E']), expected)

	def test_censusvar_acsse(self):
		expected = {'K202801_006E': ['K202801. Presence of A Computer and Type of Internet Subscription in Household', 'No computer', 'int']}
		for year in range(2014, 2015+1):
			self.assertEqual(censusdata.censusvar('acsse', year, ['K202801_006E']), expected)

	def test_censusvar_acs3(self):
		for year in range(2013, 2013+1):
			expected = {'B19013_001E': ['B19013.  Median Household Income'.format(year),
				'Median household income in the past 12 months (in {0} inflation-adjusted dollars)'.format(year), 'int']}
			self.assertEqual(censusdata.censusvar('acs3', year, ['B19013_001E']), expected)

	def test_censusvar_sf1(self):
		self.assertEqual(censusdata.censusvar('sf1', 2010, ['P0010001']),
			{'P0010001': ['P1. Total Population [1]', 'Total Population', '']})

	def test_unknownvar(self):
		self.assertRaises(ValueError, censusdata.censusvar, 'acs5', 2015, ['B19013_010E'])

	def test_censustable_acs1_201215_detail(self):
		for year in range(2012, 2015+1):
			predicateType = 'int'
			if year == 2012: predicateType = ''
			expected = OrderedDict()
			expected['B23025_001E'] = {'label': 'Total:', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_001M'] = {'label': 'Margin of Error for!!Total:', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_002E'] = {'label': 'In labor force:', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_002M'] = { 'label': 'Margin of Error for!!In labor force:', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_003E'] = {'label': 'In labor force:!!Civilian labor force:', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_003M'] = {'label': 'Margin of Error for!!In labor force:!!Civilian labor force:', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_004E'] = {'label': 'In labor force:!!Civilian labor force:!!Employed', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_004M'] = {'label': 'Margin of Error for!!In labor force:!!Civilian labor force:!!Employed', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_005E'] = {'label': 'In labor force:!!Civilian labor force:!!Unemployed', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_005M'] = {'label': 'Margin of Error for!!In labor force:!!Civilian labor force:!!Unemployed', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_006E'] = {'label': 'In labor force:!!Armed Forces', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_006M'] = { 'label': 'Margin of Error for!!In labor force:!!Armed Forces', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_007E'] = {'label': 'Not in labor force', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_007M'] = {'label': 'Margin of Error for!!Not in labor force', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			self.assertEqual(censusdata.censustable('acs1', year, 'B23025'), expected)

	def test_censustable_acs5_2015_detail(self):
		expected = OrderedDict()
		expected['B23025_001E'] = {'label': 'Total:', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': 'int'}
		expected['B23025_001M'] = {'label': 'Margin Of Error For!!Total:', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': 'int'}
		expected['B23025_002E'] = {'label': 'In labor force:', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': 'int'}
		expected['B23025_002M'] = { 'label': 'Margin Of Error For!!In labor force:', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': 'int'}
		expected['B23025_003E'] = {'label': 'In labor force:!!Civilian labor force:', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': 'int'}
		expected['B23025_003M'] = {'label': 'Margin Of Error For!!In labor force:!!Civilian labor force:', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': 'int'}
		expected['B23025_004E'] = {'label': 'In labor force:!!Civilian labor force:!!Employed', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': 'int'}
		expected['B23025_004M'] = {'label': 'Margin Of Error For!!In labor force:!!Civilian labor force:!!Employed', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': 'int'}
		expected['B23025_005E'] = {'label': 'In labor force:!!Civilian labor force:!!Unemployed', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': 'int'}
		expected['B23025_005M'] = {'label': 'Margin Of Error For!!In labor force:!!Civilian labor force:!!Unemployed', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': 'int'}
		expected['B23025_006E'] = {'label': 'In labor force:!!Armed Forces', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': 'int'}
		expected['B23025_006M'] = { 'label': 'Margin Of Error For!!In labor force:!!Armed Forces', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': 'int'}
		expected['B23025_007E'] = {'label': 'Not in labor force', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': 'int'}
		expected['B23025_007M'] = {'label': 'Margin Of Error For!!Not in labor force', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': 'int'}
		self.assertEqual(censusdata.censustable('acs5', 2015, 'B23025'), expected)

	def test_censustable_acs5_2015_subject(self):
		expected = OrderedDict()
		expected['S0101_C02_001E'] = {'label': 'Male!!Total population', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_001EA'] = {'label': 'Male!!Total population', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_001M'] = {'label': 'Male MOE!!Total population', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_001MA'] = {'label': 'Male MOE!!Total population', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_002E'] = {'label': 'Male!!Total population!!AGE!!Under 5 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_002EA'] = {'label': 'Male!!Total population!!AGE!!Under 5 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_002M'] = {'label': 'Male MOE!!Total population!!AGE!!Under 5 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_002MA'] = {'label': 'Male MOE!!Total population!!AGE!!Under 5 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_003E'] = {'label': 'Male!!Total population!!AGE!!5 to 9 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_003EA'] = {'label': 'Male!!Total population!!AGE!!5 to 9 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_003M'] = {'label': 'Male MOE!!Total population!!AGE!!5 to 9 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_003MA'] = {'label': 'Male MOE!!Total population!!AGE!!5 to 9 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_004E'] = {'label': 'Male!!Total population!!AGE!!10 to 14 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_004EA'] = {'label': 'Male!!Total population!!AGE!!10 to 14 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_004M'] = {'label': 'Male MOE!!Total population!!AGE!!10 to 14 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_004MA'] = {'label': 'Male MOE!!Total population!!AGE!!10 to 14 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_005E'] = {'label': 'Male!!Total population!!AGE!!15 to 19 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_005EA'] = {'label': 'Male!!Total population!!AGE!!15 to 19 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_005M'] = {'label': 'Male MOE!!Total population!!AGE!!15 to 19 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_005MA'] = {'label': 'Male MOE!!Total population!!AGE!!15 to 19 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_006E'] = {'label': 'Male!!Total population!!AGE!!20 to 24 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_006EA'] = {'label': 'Male!!Total population!!AGE!!20 to 24 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_006M'] = {'label': 'Male MOE!!Total population!!AGE!!20 to 24 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_006MA'] = {'label': 'Male MOE!!Total population!!AGE!!20 to 24 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_007E'] = {'label': 'Male!!Total population!!AGE!!25 to 29 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_007EA'] = {'label': 'Male!!Total population!!AGE!!25 to 29 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_007M'] = {'label': 'Male MOE!!Total population!!AGE!!25 to 29 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_007MA'] = {'label': 'Male MOE!!Total population!!AGE!!25 to 29 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_008E'] = {'label': 'Male!!Total population!!AGE!!30 to 34 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_008EA'] = {'label': 'Male!!Total population!!AGE!!30 to 34 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_008M'] = {'label': 'Male MOE!!Total population!!AGE!!30 to 34 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_008MA'] = {'label': 'Male MOE!!Total population!!AGE!!30 to 34 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_009E'] = {'label': 'Male!!Total population!!AGE!!35 to 39 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_009EA'] = {'label': 'Male!!Total population!!AGE!!35 to 39 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_009M'] = {'label': 'Male MOE!!Total population!!AGE!!35 to 39 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_009MA'] = {'label': 'Male MOE!!Total population!!AGE!!35 to 39 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_010E'] = {'label': 'Male!!Total population!!AGE!!40 to 44 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_010EA'] = {'label': 'Male!!Total population!!AGE!!40 to 44 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_010M'] = {'label': 'Male MOE!!Total population!!AGE!!40 to 44 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_010MA'] = {'label': 'Male MOE!!Total population!!AGE!!40 to 44 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_011E'] = {'label': 'Male!!Total population!!AGE!!45 to 49 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_011EA'] = {'label': 'Male!!Total population!!AGE!!45 to 49 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_011M'] = {'label': 'Male MOE!!Total population!!AGE!!45 to 49 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_011MA'] = {'label': 'Male MOE!!Total population!!AGE!!45 to 49 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_012E'] = {'label': 'Male!!Total population!!AGE!!50 to 54 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_012EA'] = {'label': 'Male!!Total population!!AGE!!50 to 54 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_012M'] = {'label': 'Male MOE!!Total population!!AGE!!50 to 54 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_012MA'] = {'label': 'Male MOE!!Total population!!AGE!!50 to 54 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_013E'] = {'label': 'Male!!Total population!!AGE!!55 to 59 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_013EA'] = {'label': 'Male!!Total population!!AGE!!55 to 59 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_013M'] = {'label': 'Male MOE!!Total population!!AGE!!55 to 59 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_013MA'] = {'label': 'Male MOE!!Total population!!AGE!!55 to 59 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_014E'] = {'label': 'Male!!Total population!!AGE!!60 to 64 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_014EA'] = {'label': 'Male!!Total population!!AGE!!60 to 64 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_014M'] = {'label': 'Male MOE!!Total population!!AGE!!60 to 64 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_014MA'] = {'label': 'Male MOE!!Total population!!AGE!!60 to 64 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_015E'] = {'label': 'Male!!Total population!!AGE!!65 to 69 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_015EA'] = {'label': 'Male!!Total population!!AGE!!65 to 69 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_015M'] = {'label': 'Male MOE!!Total population!!AGE!!65 to 69 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_015MA'] = {'label': 'Male MOE!!Total population!!AGE!!65 to 69 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_016E'] = {'label': 'Male!!Total population!!AGE!!70 to 74 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_016EA'] = {'label': 'Male!!Total population!!AGE!!70 to 74 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_016M'] = {'label': 'Male MOE!!Total population!!AGE!!70 to 74 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_016MA'] = {'label': 'Male MOE!!Total population!!AGE!!70 to 74 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_017E'] = {'label': 'Male!!Total population!!AGE!!75 to 79 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_017EA'] = {'label': 'Male!!Total population!!AGE!!75 to 79 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_017M'] = {'label': 'Male MOE!!Total population!!AGE!!75 to 79 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_017MA'] = {'label': 'Male MOE!!Total population!!AGE!!75 to 79 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_018E'] = {'label': 'Male!!Total population!!AGE!!80 to 84 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_018EA'] = {'label': 'Male!!Total population!!AGE!!80 to 84 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_018M'] = {'label': 'Male MOE!!Total population!!AGE!!80 to 84 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_018MA'] = {'label': 'Male MOE!!Total population!!AGE!!80 to 84 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_019E'] = {'label': 'Male!!Total population!!AGE!!85 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_019EA'] = {'label': 'Male!!Total population!!AGE!!85 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_019M'] = {'label': 'Male MOE!!Total population!!AGE!!85 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_019MA'] = {'label': 'Male MOE!!Total population!!AGE!!85 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_020E'] = {'label': 'Male!!Total population!!SELECTED AGE CATEGORIES!!5 to 14 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_020EA'] = {'label': 'Male!!Total population!!SELECTED AGE CATEGORIES!!5 to 14 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_020M'] = {'label': 'Male MOE!!Total population!!SELECTED AGE CATEGORIES!!5 to 14 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_020MA'] = {'label': 'Male MOE!!Total population!!SELECTED AGE CATEGORIES!!5 to 14 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_021E'] = {'label': 'Male!!Total population!!SELECTED AGE CATEGORIES!!15 to 17 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_021EA'] = {'label': 'Male!!Total population!!SELECTED AGE CATEGORIES!!15 to 17 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_021M'] = {'label': 'Male MOE!!Total population!!SELECTED AGE CATEGORIES!!15 to 17 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_021MA'] = {'label': 'Male MOE!!Total population!!SELECTED AGE CATEGORIES!!15 to 17 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_022E'] = {'label': 'Male!!Total population!!SELECTED AGE CATEGORIES!!18 to 24 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_022EA'] = {'label': 'Male!!Total population!!SELECTED AGE CATEGORIES!!18 to 24 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_022M'] = {'label': 'Male MOE!!Total population!!SELECTED AGE CATEGORIES!!18 to 24 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_022MA'] = {'label': 'Male MOE!!Total population!!SELECTED AGE CATEGORIES!!18 to 24 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_023E'] = {'label': 'Male!!Total population!!SELECTED AGE CATEGORIES!!15 to 44 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_023EA'] = {'label': 'Male!!Total population!!SELECTED AGE CATEGORIES!!15 to 44 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_023M'] = {'label': 'Male MOE!!Total population!!SELECTED AGE CATEGORIES!!15 to 44 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_023MA'] = {'label': 'Male MOE!!Total population!!SELECTED AGE CATEGORIES!!15 to 44 years', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_024E'] = {'label': 'Male!!Total population!!SELECTED AGE CATEGORIES!!16 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_024EA'] = {'label': 'Male!!Total population!!SELECTED AGE CATEGORIES!!16 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_024M'] = {'label': 'Male MOE!!Total population!!SELECTED AGE CATEGORIES!!16 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_024MA'] = {'label': 'Male MOE!!Total population!!SELECTED AGE CATEGORIES!!16 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_025E'] = {'label': 'Male!!Total population!!SELECTED AGE CATEGORIES!!18 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_025EA'] = {'label': 'Male!!Total population!!SELECTED AGE CATEGORIES!!18 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_025M'] = {'label': 'Male MOE!!Total population!!SELECTED AGE CATEGORIES!!18 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_025MA'] = {'label': 'Male MOE!!Total population!!SELECTED AGE CATEGORIES!!18 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_026E'] = {'label': 'Male!!Total population!!SELECTED AGE CATEGORIES!!60 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_026EA'] = {'label': 'Male!!Total population!!SELECTED AGE CATEGORIES!!60 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_026M'] = {'label': 'Male MOE!!Total population!!SELECTED AGE CATEGORIES!!60 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_026MA'] = {'label': 'Male MOE!!Total population!!SELECTED AGE CATEGORIES!!60 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_027E'] = {'label': 'Male!!Total population!!SELECTED AGE CATEGORIES!!62 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_027EA'] = {'label': 'Male!!Total population!!SELECTED AGE CATEGORIES!!62 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_027M'] = {'label': 'Male MOE!!Total population!!SELECTED AGE CATEGORIES!!62 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_027MA'] = {'label': 'Male MOE!!Total population!!SELECTED AGE CATEGORIES!!62 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_028E'] = {'label': 'Male!!Total population!!SELECTED AGE CATEGORIES!!65 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_028EA'] = {'label': 'Male!!Total population!!SELECTED AGE CATEGORIES!!65 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_028M'] = {'label': 'Male MOE!!Total population!!SELECTED AGE CATEGORIES!!65 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_028MA'] = {'label': 'Male MOE!!Total population!!SELECTED AGE CATEGORIES!!65 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_029E'] = {'label': 'Male!!Total population!!SELECTED AGE CATEGORIES!!75 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_029EA'] = {'label': 'Male!!Total population!!SELECTED AGE CATEGORIES!!75 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_029M'] = {'label': 'Male MOE!!Total population!!SELECTED AGE CATEGORIES!!75 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_029MA'] = {'label': 'Male MOE!!Total population!!SELECTED AGE CATEGORIES!!75 years and over', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_030E'] = {'label': 'Male!!Total population!!SUMMARY INDICATORS!!Median age (years)', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_030EA'] = {'label': 'Male!!Total population!!SUMMARY INDICATORS!!Median age (years)', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_030M'] = {'label': 'Male MOE!!Total population!!SUMMARY INDICATORS!!Median age (years)', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_030MA'] = {'label': 'Male MOE!!Total population!!SUMMARY INDICATORS!!Median age (years)', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_031E'] = {'label': 'Male!!Total population!!SUMMARY INDICATORS!!Sex ratio (males per 100 females)', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_031EA'] = {'label': 'Male!!Total population!!SUMMARY INDICATORS!!Sex ratio (males per 100 females)', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_031M'] = {'label': 'Male MOE!!Total population!!SUMMARY INDICATORS!!Sex ratio (males per 100 females)', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_031MA'] = {'label': 'Male MOE!!Total population!!SUMMARY INDICATORS!!Sex ratio (males per 100 females)', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_032E'] = {'label': 'Male!!Total population!!SUMMARY INDICATORS!!Age dependency ratio', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_032EA'] = {'label': 'Male!!Total population!!SUMMARY INDICATORS!!Age dependency ratio', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_032M'] = {'label': 'Male MOE!!Total population!!SUMMARY INDICATORS!!Age dependency ratio', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_032MA'] = {'label': 'Male MOE!!Total population!!SUMMARY INDICATORS!!Age dependency ratio', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_033E'] = {'label': 'Male!!Total population!!SUMMARY INDICATORS!!Old-age dependency ratio', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_033EA'] = {'label': 'Male!!Total population!!SUMMARY INDICATORS!!Old-age dependency ratio', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_033M'] = {'label': 'Male MOE!!Total population!!SUMMARY INDICATORS!!Old-age dependency ratio', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_033MA'] = {'label': 'Male MOE!!Total population!!SUMMARY INDICATORS!!Old-age dependency ratio', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_034E'] = {'label': 'Male!!Total population!!SUMMARY INDICATORS!!Child dependency ratio', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_034EA'] = {'label': 'Male!!Total population!!SUMMARY INDICATORS!!Child dependency ratio', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_034M'] = {'label': 'Male MOE!!Total population!!SUMMARY INDICATORS!!Child dependency ratio', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_034MA'] = {'label': 'Male MOE!!Total population!!SUMMARY INDICATORS!!Child dependency ratio', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_035E'] = {'label': 'Male!!PERCENT IMPUTED!!Sex', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_035EA'] = {'label': 'Male!!PERCENT IMPUTED!!Sex', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_035M'] = {'label': 'Male MOE!!PERCENT IMPUTED!!Sex', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_035MA'] = {'label': 'Male MOE!!PERCENT IMPUTED!!Sex', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_036E'] = {'label': 'Male!!PERCENT IMPUTED!!Age', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_036EA'] = {'label': 'Male!!PERCENT IMPUTED!!Age', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_036M'] = {'label': 'Male MOE!!PERCENT IMPUTED!!Age', 'concept': 'Age and Sex', 'predicateType': 'string'}
		expected['S0101_C02_036MA'] = {'label': 'Male MOE!!PERCENT IMPUTED!!Age', 'concept': 'Age and Sex', 'predicateType': 'string'}
		self.assertEqual(censusdata.censustable('acs5', 2015, 'S0101_C02'), expected)

	def test_censustable_acsse(self):
		expected = OrderedDict()
		expected['K201601_001E'] = {'label': 'Total:', 'concept': 'K201601. Household Language', 'predicateType': 'int'}
		expected['K201601_001EA'] = {'label': 'Total:', 'concept': 'K201601. Household Language', 'predicateType': 'string'}
		expected['K201601_001M'] = {'label': 'Margin of Error for!!Total:', 'concept': 'K201601. Household Language', 'predicateType': 'int'}
		expected['K201601_001MA'] = {'label': 'Margin of Error for!!Total:', 'concept': 'K201601. Household Language', 'predicateType': 'string'}
		expected['K201601_002E'] = {'label': 'English only', 'concept': 'K201601. Household Language', 'predicateType': 'int'}
		expected['K201601_002EA'] = {'label': 'English only', 'concept': 'K201601. Household Language', 'predicateType': 'string'}
		expected['K201601_002M'] = {'label': 'Margin of Error for!!English only', 'concept': 'K201601. Household Language', 'predicateType': 'int'}
		expected['K201601_002MA'] = {'label': 'Margin of Error for!!English only', 'concept': 'K201601. Household Language', 'predicateType': 'string'}
		expected['K201601_003E'] = {'label': 'Spanish:', 'concept': 'K201601. Household Language', 'predicateType': 'int'}
		expected['K201601_003EA'] = {'label': 'Spanish:', 'concept': 'K201601. Household Language', 'predicateType': 'string'}
		expected['K201601_003M'] = {'label': 'Margin of Error for!!Spanish:', 'concept': 'K201601. Household Language', 'predicateType': 'int'}
		expected['K201601_003MA'] = {'label': 'Margin of Error for!!Spanish:', 'concept': 'K201601. Household Language', 'predicateType': 'string'}
		expected['K201601_004E'] = {'label': 'Spanish:!!Limited English speaking household', 'concept': 'K201601. Household Language', 'predicateType': 'int'}
		expected['K201601_004EA'] = {'label': 'Spanish:!!Limited English speaking household', 'concept': 'K201601. Household Language', 'predicateType': 'string'}
		expected['K201601_004M'] = {'label': 'Margin of Error for!!Spanish:!!Limited English speaking household', 'concept': 'K201601. Household Language', 'predicateType': 'int'}
		expected['K201601_004MA'] = {'label': 'Margin of Error for!!Spanish:!!Limited English speaking household', 'concept': 'K201601. Household Language', 
			'predicateType': 'string'}
		expected['K201601_005E'] = {'label': 'Spanish:!!Not a limited English speaking household', 'concept': 'K201601. Household Language', 'predicateType': 'int'}
		expected['K201601_005EA'] = {'label': 'Spanish:!!Not a limited English speaking household', 'concept': 'K201601. Household Language', 'predicateType': 'string'}
		expected['K201601_005M'] = {'label': 'Margin of Error for!!Spanish:!!Not a limited English speaking household', 'concept': 'K201601. Household Language', 
			'predicateType': 'int'}
		expected['K201601_005MA'] = {'label': 'Margin of Error for!!Spanish:!!Not a limited English speaking household', 'concept': 'K201601. Household Language', 
			'predicateType': 'string'}
		expected['K201601_006E'] = {'label': 'Other languages:', 'concept': 'K201601. Household Language', 'predicateType': 'int'}
		expected['K201601_006EA'] = {'label': 'Other languages:', 'concept': 'K201601. Household Language', 'predicateType': 'string'}
		expected['K201601_006M'] = {'label': 'Margin of Error for!!Other languages:', 'concept': 'K201601. Household Language', 'predicateType': 'int'}
		expected['K201601_006MA'] = {'label': 'Margin of Error for!!Other languages:', 'concept': 'K201601. Household Language', 'predicateType': 'string'}
		expected['K201601_007E'] = {'label': 'Other languages:!!Limited English speaking household', 'concept': 'K201601. Household Language', 'predicateType': 'int'}
		expected['K201601_007EA'] = {'label': 'Other languages:!!Limited English speaking household', 'concept': 'K201601. Household Language', 'predicateType': 'string'}
		expected['K201601_007M'] = {'label': 'Margin of Error for!!Other languages:!!Limited English speaking household', 'concept': 'K201601. Household Language', 
			'predicateType': 'int'}
		expected['K201601_007MA'] = {'label': 'Margin of Error for!!Other languages:!!Limited English speaking household', 'concept': 'K201601. Household Language', 
			'predicateType': 'string'}
		expected['K201601_008E'] = {'label': 'Other languages:!!Not a limited English speaking household', 'concept': 'K201601. Household Language', 'predicateType': 'int'}
		expected['K201601_008EA'] = {'label': 'Other languages:!!Not a limited English speaking household', 'concept': 'K201601. Household Language', 'predicateType': 'string'}
		expected['K201601_008M'] = {'label': 'Margin of Error for!!Other languages:!!Not a limited English speaking household', 'concept': 'K201601. Household Language', 
			'predicateType': 'int'}
		expected['K201601_008MA'] = {'label': 'Margin of Error for!!Other languages:!!Not a limited English speaking household', 'concept': 'K201601. Household Language', 
			'predicateType': 'string'}
		for year in range(2014, 2015+1):
			self.assertEqual(censusdata.censustable('acsse', year, 'K201601'), expected)

	def test_censustable_acs3(self):
		for year in range(2012, 2013+1):
			predicateType = 'int'
			if year == 2012: predicateType = ''
			expected = OrderedDict()
			expected['B23025_001E'] = {'label': 'Total:', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_001M'] = {'label': 'Margin of Error for!!Total:', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_002E'] = {'label': 'In labor force:', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_002M'] = { 'label': 'Margin of Error for!!In labor force:', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_003E'] = {'label': 'In labor force:!!Civilian labor force:', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_003M'] = {'label': 'Margin of Error for!!In labor force:!!Civilian labor force:', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_004E'] = {'label': 'In labor force:!!Civilian labor force:!!Employed', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_004M'] = {'label': 'Margin of Error for!!In labor force:!!Civilian labor force:!!Employed', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_005E'] = {'label': 'In labor force:!!Civilian labor force:!!Unemployed', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_005M'] = {'label': 'Margin of Error for!!In labor force:!!Civilian labor force:!!Unemployed', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_006E'] = {'label': 'In labor force:!!Armed Forces', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_006M'] = { 'label': 'Margin of Error for!!In labor force:!!Armed Forces', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_007E'] = {'label': 'Not in labor force', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			expected['B23025_007M'] = {'label': 'Margin of Error for!!Not in labor force', 'concept': 'B23025.  Employment Status for the Population 16 Years and Over', 'predicateType': predicateType}
			self.assertEqual(censusdata.censustable('acs3', year, 'B23025'), expected)

	def test_censustable_sf1(self):
		expected = OrderedDict()
		expected['P0020001'] = {'label': 'Total Population', 'concept': 'P2. Urban And Rural [6]', 'predicateType': ''}
		expected['P0020002'] = {'label': 'Urban:', 'concept': 'P2. Urban And Rural [6]', 'predicateType': ''}
		expected['P0020003'] = {'label': 'Urban: !! Inside urbanized areas', 'concept': 'P2. Urban And Rural [6]', 'predicateType': ''}
		expected['P0020004'] = {'label': 'Urban: !! Inside urban clusters', 'concept': 'P2. Urban And Rural [6]', 'predicateType': ''}
		expected['P0020005'] = {'label': 'Rural !! Inside urban clusters', 'concept': 'P2. Urban And Rural [6]', 'predicateType': ''}
		expected['P0020006'] = {'label': 'Not defined for this file !! Inside urban clusters', 'concept': 'P2. Urban And Rural [6]', 'predicateType': ''}
		self.assertEqual(censusdata.censustable('sf1', 2010, 'P002'), expected)

	def test_unknowntable(self):
		self.assertRaises(ValueError, censusdata.censustable, 'acs5', 2015, 'B24444')

	def test_search(self):
		self.assertEqual(censusdata.search('acs5', 2015, 'concept', 'unweighted sample'), [
		('B00001_001E', 'B00001.  Unweighted Sample Count of the Population', 'Total'),
		('B00001_001M', 'B00001.  Unweighted Sample Count of the Population', 'Margin Of Error For!!Total'),
		('B00002_001E', 'B00002.  Unweighted Sample Housing Units', 'Total'),
		('B00002_001M', 'B00002.  Unweighted Sample Housing Units', 'Margin Of Error For!!Total'),
		])

	def test_printtable(self):
		testtable = censusdata.censustable('acs5', 2015, 'B19013')
		printedtable = io.StringIO()
		sys.stdout = printedtable
		censusdata.printtable(testtable)
		sys.stdout = sys.__stdout__
		self.assertEqual(printedtable.getvalue(), textwrap.dedent(
			'''\
			Variable     | Table                          | Label                                                    | Type 
			-------------------------------------------------------------------------------------------------------------------
			B19013_001E  | B19013. Median Household Incom | Median household income in the past 12 months (in 2015 I | int  
			-------------------------------------------------------------------------------------------------------------------
			'''))
		printedtable.close()
		printedtable = io.StringIO()
		sys.stdout = printedtable
		censusdata.printtable(testtable, moe=True)
		sys.stdout = sys.__stdout__
		self.assertEqual(printedtable.getvalue(), textwrap.dedent(
			'''\
			Variable     | Table                          | Label                                                    | Type 
			-------------------------------------------------------------------------------------------------------------------
			B19013_001E  | B19013. Median Household Incom | Median household income in the past 12 months (in 2015 I | int  
			B19013_001M  | B19013. Median Household Incom | !! Margin of Error for Median household income in the pa | int  
			-------------------------------------------------------------------------------------------------------------------
			'''))
		printedtable.close()


	def test_unknown_tabletype(self):
		self.assertRaises(ValueError, censusdata.censusvar, 'acs5', 2015, ['B19013_001E', 'D19013_002E'])
		self.assertRaises(ValueError, censusdata.censustable, 'acs5', 2015, 'C19013')
		self.assertRaises(ValueError, censusdata.search, 'acs5', 2015, 'concept', 'unweighted sample', tabletype='cdetail')


if __name__ == '__main__':
	unittest.main()

