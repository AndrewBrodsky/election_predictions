import pandas as pd


def make_dark_house():

    dark = pd.read_csv('open_secrets/dark_money.csv')
    dark.drop(columns = ['Name', 'State/Dist', 'For Dems', 'Against Dems',
        'For Repubs', 'AgainstRepubs'], inplace=True)
    dark_house = dark[~dark['DISTRICT'].str.contains('S')]
    dark_house['DISTRICT'] = pd.to_numeric(dark_house['DISTRICT'], errors = 'coerce')

    return dark_house


if __name__ == '__main__':

    dark_house = make_dark_house()
