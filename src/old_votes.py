import pandas as pd

def get_old_votes():

    '''
    DESCRIPTION:
    Creates Pandas dataframe with vote totals for each candidate in 2010 and 2012

    INPUT:
    None

    RETURNS:
    old_votes: Pandas Dataframe with vote totals by candidate
    '''

    votes_2010 = pd.read_csv('house_votes_2010.csv')
    votes_2012 = pd.read_csv('house_votes_2012.csv')
    votes_2010['YEAR'] = 2010
    votes_2012['YEAR'] = 2012

    old_votes = pd.concat([votes_2010, votes_2012])

    old_votes['VOTE_COUNT'] = pd.to_numeric(old_votes['VOTE_COUNT'], errors = 'coerce')
    old_votes['DISTRICT'] = pd.to_numeric(old_votes['DISTRICT'], errors = 'coerce')
    old_votes.dropna(subset=['DISTRICT', 'VOTE_COUNT'], inplace=True)

    old_votes['VOTE_COUNT'] = old_votes['VOTE_COUNT'].astype(int)
    old_votes['DISTRICT'] = old_votes['DISTRICT'].astype(int)
    old_votes['INCUMBENT'] = old_votes['INCUMBENT'] == 'TRUE'
    old_votes['LAST_NAME'] = old_votes['LAST_NAME'].str.upper()


    old_votes = old_votes[(old_votes.PARTY == 'DEM') | (old_votes.PARTY == 'REP')]
    old_votes['DEM'] = old_votes['PARTY'] == 'DEM'
    # old_votes.rename(columns={'YEAR' : "year"}, inplace=True)
    # old_votes.rename(columns={'DISTRICT' : "district"}, inplace=True)
    # old_votes.rename(columns={'INCUMBENT' : "incumbent"}, inplace=True)
    # old_votes.rename(columns={'VOTE_COUNT' : "vote_count"}, inplace=True)
    # old_votes.rename(columns={'PARTY' : "party"}, inplace=True)

    return old_votes

if __name__ == '__main__':

    old_votes = get_old_votes()
