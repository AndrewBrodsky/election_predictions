from bs4 import BeautifulSoup
import urllib.request
from collections import defaultdict
import pandas as pd


def get_house_data(years, states):

    datadict = defaultdict(dict)

    for year in years:
        datadict[year] = {}

        for state in states:

            site = "https://www.politico.com/" + str(year) + "-election/results/map/house/"+state+"/"
            #print (site)
            req= urllib.request.Request(site)
            page = urllib.request.urlopen(req)
            soup = BeautifulSoup(page, 'lxml')
            datadict[year][state] = soup

    print ("Done with getting data")
    return datadict


def make_politico(datadict, years, states):

    votesdict = defaultdict(dict)

    for year in years:
        votesdict[year] = defaultdict(dict)

        for state in states:
            votesdict[year][state] = defaultdict(dict)

            data = datadict[year][state]

            #loop through each district in the BS object and add district ID and candidates'
            #party, names, and vote counts

            for i, district in enumerate(data.find_all("article", {"class": "results-group"})):

                #distnum = district.find("fips-ID").attrs['data-fips']
                distnum = i+1
                votesdict[year][state][distnum] = defaultdict(dict)

                #Democratic candidate

                democrat = district.find(class_="type-democrat")


                if democrat is not None:

                    if democrat.find(class_="results-popular") is not None:

                        demcount = democrat.find(class_="results-popular").get_text()
                        demname = democrat.find(class_="results-name").get_text()

                        if demname[-4:] == ' (i)':
                            votesdict[year][state][distnum]['dem']['incumbent'] = True
                            demname = demname[:-4]
                        else:
                            votesdict[year][state][distnum]['dem']['incumbent'] = False

                        if demname[:9] == 'D Winner ':
                             demname = demname[9:]
                        else:
                             demname = demname[2:]

                        votesdict[year][state][distnum]['dem']['cand_name'] = demname
                        votesdict[year][state][distnum]['dem']['vote_count'] = int(demcount.replace(',',''))


                #Republican candidate

                republican = district.find(class_="type-republican")

                if republican is not None:

                    if republican.find(class_="results-popular") is not None:

                        repcount = republican.find(class_="results-popular").get_text()
                        repname = republican.find(class_="results-name").get_text()

                        if repname[-4:] == ' (i)':
                            votesdict[year][state][distnum]['rep']['incumbent'] = True
                            repname = repname[:-4]
                        else:
                            votesdict[year][state][distnum]['rep']['incumbent'] = False

                        if repname[:9] == 'R Winner ':
                             repname = repname[9:]
                        else:
                             repname = repname[2:]

                        votesdict[year][state][distnum]['rep']['cand_name'] = repname
                        votesdict[year][state][distnum]['rep']['vote_count'] = int(repcount.replace(',',''))


    votes_df= pd.DataFrame.from_dict({(i,j,k,l): votesdict[i][j][k][l]
        for i in votesdict.keys()
        for j in votesdict[i].keys()
        for k in votesdict[i][j].keys()
        for l in votesdict[i][j][k].keys()},
        orient='index')

    votes_df.reset_index(inplace=True)
    votes_df.rename(index=str, columns={"level_0":"year", "level_1": "state", "level_2": "district", "level_3":"party"}, inplace=True)

    return votes_df


def parse_senate_data(dict):
    counties = test.find_all("article", {"class": "results-group"})
    county_strings = []

    for county in range(1, len(counties)):
        county_strings.append(str(counties[county].find_all('h4')))
        county_names = []

        for name in county_names:
            county_names.append((name.split('>')[1]).split('<')[0])


def get_politico():

    states = ['alabama','alaska','arizona','arkansas','california','colorado',
     'connecticut','delaware','florida','georgia','hawaii','idaho',
     'illinois','indiana','iowa','kansas','kentucky','louisiana',
     'maine', 'maryland','massachusetts','michigan','minnesota',
     'mississippi', 'missouri','montana','nebraska','nevada',
     'new-hampshire','new-jersey','new-mexico','new-york',
     'north-carolina','north-dakota','ohio',
     'oklahoma','oregon','pennsylvania','rhode-island',
     'south-carolina','south-dakota','tennessee','texas','utah',
     'vermont','virginia','washington','west-virginia',
     'wisconsin','wyoming']

    years = [2014, 2016]

    datadict = get_house_data(years, states)

    politico = make_politico(datadict, years, states)

    state_dict = {
    'alabama': 'AL',
    'alaska': 'AK',
    'arizona': 'AZ',
    'arkansas': 'AR',
    'california': 'CA',
    'colorado': 'CO',
    'connecticut': 'CT',
    'delaware': 'DE',
    'florida': 'FL',
    'georgia': 'GA',
    'hawaii': 'HI',
    'idaho': 'ID',
    'illinois': 'IL',
    'indiana': 'IN',
    'iowa': 'IA',
    'kansas': 'KS',
    'kentucky': 'KY',
    'louisiana': 'LA',
    'maine': 'ME',
    'maryland': 'MD',
    'massachusetts': 'MA',
    'michigan': 'MI',
    'minnesota': 'MN',
    'mississippi': 'MS',
    'missouri': 'MO',
    'montana': 'MT',
    'nebraska': 'NE',
    'nevada': 'NV',
    'new-hampshire': 'NH',
    'new-jersey': 'NJ',
    'new-mexico': 'NM',
    'new-york': 'NY',
    'north-carolina': 'NC',
    'north-dakota': 'ND',
    'ohio': 'OH',
    'oklahoma': 'OK',
    'oregon': 'OR',
    'pennsylvania': 'PA',
    'rhode-island': 'RI',
    'south-carolina': 'SC',
    'south-dakota': 'SD',
    'tennessee': 'TN',
    'texas': 'TX',
    'utah': 'UT',
    'vermont': 'VT',
    'virginia': 'VA',
    'washington': 'WA',
    'west-virginia': 'WV',
    'wisconsin': 'WI',
    'wyoming': 'WY'
    }

    politico['STATE_ABBR'] = politico['state'].map(state_dict)
    politico['LAST_NAME'] = politico.cand_name.str.upper().str.split(" ").str[-1]
    politico['DEM'] = politico['party'] == 'dem'
    politico['YEAR2016'] = politico['year'] == 2016

    return politico


if __name__ == "__main__":
    politico = get_politico()
