import pandas as pd


def make_dark_house():

    '''
    DESCRIPTION:
    Creates Pandas dataframe with dark money total for each candidate for further analysis

    INPUT:
    None

    RETURNS:
    dark_house: Pandas Dataframe with dark money contribution totals for each House candidate
    '''

    dark = pd.read_csv('open_secrets/dark_money.csv')
    dark.drop(columns = ['Name', 'State/Dist', 'For Dems', 'Against Dems',
        'For Repubs', 'AgainstRepubs'], inplace=True)

    dark_house = dark[~dark['DISTRICT'].str.contains('S', na=False)]
    dark_house['DISTRICT'] = pd.to_numeric(dark_house['DISTRICT'], errors = 'coerce')
    dark_house.dropna(subset=['DISTRICT'], inplace=True)
    dark_house['DISTRICT'] = dark_house['DISTRICT'].astype(int)

    dark_house['DARK_FOR'] = pd.to_numeric(dark_house['DARK_FOR'], errors = 'coerce')
    dark_house['DARK_AGAINST'] = pd.to_numeric(dark_house['DARK_AGAINST'], errors = 'coerce')
    dark_house['Total'] = pd.to_numeric(dark_house['Total'], errors = 'coerce')
    dark_house.rename(columns={'STATE': 'STATE_ABBR'}, inplace=True)

    return dark_house


if __name__ == '__main__':

    dark_house = make_dark_house()
