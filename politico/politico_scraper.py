from bs4 import BeautifulSoup
import urllib.request
from collections import defaultdict



def parse_house_data(datadict, years, states):
    votesdict = defaultdict(dict)
    for year in years:
        votesdict[year] = {}

        for state in states:
            votesdict[year][state] = {}

            data = datadict[year][state]
            for district in data.find_all("article", {"class": "results-group"})

                distnum = district.find_all("fips-ID").attrs['data-fips']

                dem = district.find("class" : "type-democrat").next_sibling
                cand_name = dem.find(scope="row" class="results-name">)
                numvotes = cand_name.find(class="results-popular")

                votesdict[year][state][district][candidate][name] = candname
                votesdict[year][state][district][candidate][votes] = numvotes
                votesdict[year][state][district][candidate][party] = 'D'

                rep = district.find(<tr class = "type-democrat")
                cand_name = rep.find(<th scope="row" class="results-name">)
                numvotes = cand_name.find(td class="results-popular")

                votesdict[year][state][district][candidate][name] = candname
                votesdict[year][state][district][candidate][votes] = numvotes
                votesdict[year][state][district][candidate][party] = 'R'

    return votesdict

    '''
    Votes = {'2016': {'colorado': {1st:
                   {'name': 'D. DeGette', 'votes': '174756', 'party': 'D'},
                   {'name': 'M. Walsh'}} ...
    '''


def parse_senate_data(dict):
    counties = test.find_all("article", {"class": "results-group"})

    county_strings = []

    for county in range(1, len(counties)):
        county_strings.append(str(counties[county].find_all('h4')))

        county_names = []

        for name in county_names:
            county_names.append((name.split('>')[1]).split('<')[0])


def get_house_data(states, years):

    datadict = defaultdict(dict)

    for year in years:

        datadict[year] = {}

        for state in states:

            site = "https://www.politico.com/" + str(year) + "-election/results/map/house/"+state+"/"

            req= urllib.request.Request(site)
            page = urllib.request.urlopen(req)

            soup = BeautifulSoup(page, 'lxml')

            datadict[year][state] = soup

    return datadict

def convert_to_df(dict):
    pass

def get_cand_id(df):
    # match the cand id from somewhere else onto candidate names
    pass


if __name__ == "__main__":

    states = ['colorado']
    years = ['2016']

    datadict = get_house_data(states, years)

    #votesdict = parse_house_data(datadict, states, years)

    #votes_df = convert_to_df(votesdict)

    #get_cand_id(votes_df)
