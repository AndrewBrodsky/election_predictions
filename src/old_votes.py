import pandas as pd

def get_old_votes():

  votes_2010 = pd.read_csv('house_votes_2010.csv')
  votes_2012 = pd.read_csv('house_votes_2012.csv')
  votes_2010['YEAR'] = 2010
  votes_2012['YEAR'] = 2012

  old_votes = pd.concat([votes_2010, votes_2012])

  old_votes['VOTE_COUNT'] = pd.to_numeric(old_votes['VOTE_COUNT'], errors = 'coerce')
  old_votes['DISTRICT'] = pd.to_numeric(old_votes['DISTRICT'], errors = 'coerce')
  old_votes['INCUMBENT'] = old_votes['INCUMBENT'] == 'TRUE'
  old_votes['LAST_NAME'] = old_votes['LAST_NAME'].str.upper()

  old_votes.dropna(subset=['DISTRICT', 'VOTE_COUNT'], inplace=True)
  old_votes = old_votes[(old_votes.PARTY == 'DEM') | (old_votes.PARTY == 'REP')]
  old_votes['DEM'] = old_votes['PARTY'] == 'DEM'

  return old_votes

if __name__ == '__main__':

  old_votes = get_old_votes()
