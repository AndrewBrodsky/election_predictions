"""
Test downloading data from Census API.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import censusdata
import unittest
try:
	import StringIO
except ModuleNotFoundError:
	import io
import textwrap

class TestExport(unittest.TestCase):

	def test_export(self):
		data = censusdata.download('acs5', 2015, censusdata.censusgeo([('state', '*')]), ['B01001_001E'])
		try:
			csv = StringIO.StringIO()
		except NameError:
			csv = io.StringIO()
		censusdata.exportcsv(csv, data)
		self.assertEqual(csv.getvalue(), textwrap.dedent("""\
		state,NAME,B01001_001E
		02,Alaska,733375
		01,Alabama,4830620
		05,Arkansas,2958208
		04,Arizona,6641928
		06,California,38421464
		08,Colorado,5278906
		09,Connecticut,3593222
		11,District of Columbia,647484
		10,Delaware,926454
		12,Florida,19645772
		13,Georgia,10006693
		15,Hawaii,1406299
		19,Iowa,3093526
		16,Idaho,1616547
		17,Illinois,12873761
		18,Indiana,6568645
		20,Kansas,2892987
		21,Kentucky,4397353
		22,Louisiana,4625253
		25,Massachusetts,6705586
		24,Maryland,5930538
		23,Maine,1329100
		26,Michigan,9900571
		27,Minnesota,5419171
		29,Missouri,6045448
		28,Mississippi,2988081
		30,Montana,1014699
		37,North Carolina,9845333
		38,North Dakota,721640
		31,Nebraska,1869365
		33,New Hampshire,1324201
		34,New Jersey,8904413
		35,New Mexico,2084117
		32,Nevada,2798636
		36,New York,19673174
		39,Ohio,11575977
		40,Oklahoma,3849733
		41,Oregon,3939233
		42,Pennsylvania,12779559
		72,Puerto Rico,3583073
		44,Rhode Island,1053661
		45,South Carolina,4777576
		46,South Dakota,843190
		47,Tennessee,6499615
		48,Texas,26538614
		49,Utah,2903379
		51,Virginia,8256630
		50,Vermont,626604
		53,Washington,6985464
		55,Wisconsin,5742117
		54,West Virginia,1851420
		56,Wyoming,579679
		"""))
		csv.close()

if __name__ == '__main__':
	unittest.main()

