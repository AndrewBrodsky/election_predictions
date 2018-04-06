import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import time


def read_indiv(headerfile, datafile, year):

    '''
    DESCRIPTION:
    Reads individual contribution data for given years and converts to dataframe

    INPUT:
    headerfile: filename of CSV containing headers for individual contributions
    datafile: filename of CSV containing individual contribution data
    year: year of data in datafile

    RETURNS:
    indiv: dataframe containing a row for each individual contribution
    '''

    total_records = 20353316

    num_records = 50500500

    headers = pd.read_csv(headerfile)

    dtypes={'CMTE_ID'           : object,
            'AMNDT_IND'         : object,
            'RPT_TP'            : object,
            'TRANSACTION_PGI'   : object,
            'IMAGE_NUM'         : np.int64,
            'TRANSACTION_TP'    : object,
            'ENTITY_TP'         : object,
            'NAME'              : object,
            'CITY'              : object,
            'STATE'             : object,
            'ZIP_CODE'          : object,
            'EMPLOYER'          : object,
            'OCCUPATION'        : object,
            'TRANSACTION_DT'    : object,
            'TRANSACTION_AMT'   : np.int64,
            'OTHER_ID'          : object,
            'TRAN_ID'           : object,
            'FILE_NUM'          : np.int64,
            'MEMO_CD'           : object,
            'MEMO_TEXT'         : object,
            'SUB_ID'            : np.int64
            }

    tic = time.time()
    indiv = pd.read_csv(datafile, sep = '|', error_bad_lines=False, names = headers, nrows=num_records, encoding = 'latin1')
    indiv.fillna(value=0, inplace=True)
    indiv.ZIP_CODE = indiv.ZIP_CODE.astype(str)
    indiv.TRANSACTION_DT = indiv.TRANSACTION_DT.astype(str)

    #for col in headers:
    #    dfsums = indiv.groupby(col)['TRANSACTION_AMT'].sum().astype(int)
    #    top50 = dfsums.sort_values(axis=0, ascending=False)[:min(50, dfsums.shape[0])]


    toc = time.time()
    #print ("Elapsed time: ", str(round(toc-tic,1)), "seconds")
    print ("Year: ", year)
    print ("Total individual records: {:,}".format(indiv.shape[0]))
    #print ("Reading time was about {:,.0f} records per second".format(num_records/(toc-tic)))

    indiv['YEAR'] = year

    return indiv


def read_file(header_file, data_file, year):

    '''
    DESCRIPTION:
    Reads contribution data for given year and converts to dataframe

    INPUT:
    headerfile: filename of CSV containing headers for contribution data
    datafile: filename of CSV containing ontribution data
    year: year of data in datafile

    RETURNS:
    file: dataframe containing a row for each contribution
    '''

    headers = pd.read_csv(header_file)
    file = pd.read_csv(data_file, sep = '|', error_bad_lines = False, names = headers, encoding ='latin1')
    file['YEAR'] = year

    return file


def group_by_trans(filename, varname):

    '''
    DESCRIPTION:
    Creates data series with transacation totals, grouped by committee ID

    INPUT:
    filename: name of dataframe to aggregate
    varname: name of variable name to use as series index

    RETURNS:
    file_trans: Pandas data series containing a row for each committee and total
    transaction amounts
    '''

    file_trans = filename.groupby(['CMTE_ID'])['TRANSACTION_AMT'].sum().astype(int)
    file_trans.rename(varname,inplace = True)

    return file_trans


def make_transactions(indiv_trans, pas_trans):

    '''
    DESCRIPTION:
    Creates dataframe with transactions for individuals and committees

    INPUT:
    indiv_trans: data series with individual transactions
    pas_trans: data series with committee transactions

    RETURNS:
    transactions: Pandas dataframe with total transactions for each committee
    '''

    transactions = pd.concat([indiv_trans,pas_trans], axis=1)
    transactions['TOTAL_TRANS'] = transactions['TRANS_BY_INDIV'].fillna(0) + transactions['TRANS_BY_CMTE'].fillna(0)
    transactions['CMTE_ID'] = transactions.index

    return transactions


def make_fec(transactions, ccl, cn):

    '''
    DESCRIPTION:
    Creates Pandas dataframe with transaction totals for each candidate for given year

    INPUT:
    transactions: Pandas Dataframe with total tranascations for each committee
    ccl: Pandas Dataframe containing committee-candidate linkage data
    cn: Pandas Dataframe containing candidate information

    RETURNS:
    fec: Pandas Dataframe with transaction totals by candidate for given year
    '''

    trans_w_candID = pd.merge(transactions, ccl, on = 'CMTE_ID', how='left')
    trans_by_candID = trans_w_candID.groupby(['CAND_ID'])['TOTAL_TRANS', 'TRANS_BY_INDIV', 'TRANS_BY_CMTE'].sum().astype(int)
    trans_by_candID['CAND_ID'] = trans_by_candID.index
    fec = pd.merge(trans_by_candID, cn, on = 'CAND_ID', how='left')
    fec.rename(columns={'CAND_ST': 'STATE_ABBR', 'CAND_OFFICE_DISTRICT': 'DISTRICT'}, inplace=True)
    fec['LAST_NAME'] = fec.CAND_NAME.str.split(" ").str[0].str.replace(",","")
    fec.dropna(subset=['YEAR', 'DISTRICT'], inplace=True)
    fec['YEAR'] = fec['YEAR'].astype(int)
    fec['DISTRICT'] = fec['DISTRICT'].astype(int)

    return fec


def get_fec():

    '''
    DESCRIPTION:
    Draws in FEC campaign contribution data from CSV and TXT files and compiles it into
    a dataframe at the candidate level

    INPUT:
    None

    RETURNS:
    fec: Pandas Dataframe with transaction totals by candidate for further analysis
    '''

    pd.set_option('display.precision', 2)
    pd.options.display.float_format = '{:,.0f}'.format

    indiv2010 = read_indiv('fec/indiv/indiv_headers_2010.csv', 'fec/indiv/indiv2010.txt', 2010)
    pas2010 = read_file('fec/pas/pas_headers_2010.csv', 'fec/pas/pas2010.txt', 2010)
    ccl2010 = read_file('fec/ccl/ccl_headers_2010.csv', 'fec/ccl/ccl2010.txt', 2010)
    cn2010 = read_file('fec/cn/cn_headers_2010.csv', 'fec/cn/cn2010.txt', 2010)

    indiv2012 = read_indiv('fec/indiv/indiv_headers_2012.csv', 'fec/indiv/indiv2012.txt', 2012)
    pas2012 = read_file('fec/pas/pas_headers_2012.csv', 'fec/pas/pas2012.txt', 2012)
    ccl2012 = read_file('fec/ccl/ccl_headers_2012.csv', 'fec/ccl/ccl2012.txt', 2012)
    cn2012 = read_file('fec/cn/cn_headers_2012.csv', 'fec/cn/cn2012.txt', 2012)

    indiv2014 = read_indiv('fec/indiv/indiv_headers_2014.csv', 'fec/indiv/indiv2014.txt', 2014)
    pas2014 = read_file('fec/pas/pas_headers_2014.csv', 'fec/pas/pas2014.txt', 2014)
    ccl2014 = read_file('fec/ccl/ccl_headers_2014.csv', 'fec/ccl/ccl2014.txt', 2014)
    cn2014 = read_file('fec/cn/cn_headers_2014.csv', 'fec/cn/cn2014.txt', 2014)

    indiv2016 = read_indiv('fec/indiv/indiv_headers_2016.csv', 'fec/indiv/indiv2016.txt', 2016)
    pas2016 = read_file('fec/pas/pas_headers_2016.csv', 'fec/pas/pas2016.txt', 2016)
    ccl2016 = read_file('fec/ccl/ccl_headers_2016.csv', 'fec/ccl/ccl2016.txt', 2016)
    cn2016 = read_file('fec/cn/cn_headers_2016.csv', 'fec/cn/cn2016.txt', 2016)


    # indiv = pd.concat([indiv2014, indiv2016])
    # pas = pd.concat([pas2014, pas2016])
    # ccl = pd.concat([ccl2014, ccl2016])
    # cn = pd.concat([cn2014, cn2016])

    pas_trans2010 = group_by_trans(pas2010, 'TRANS_BY_CMTE')
    indiv_trans2010 = group_by_trans(indiv2010, 'TRANS_BY_INDIV')
    transactions2010 = make_transactions(indiv_trans2010, pas_trans2010)
    fec2010 = make_fec(transactions2010, ccl2010, cn2010)


    pas_trans2012 = group_by_trans(pas2012, 'TRANS_BY_CMTE')
    indiv_trans2012 = group_by_trans(indiv2012, 'TRANS_BY_INDIV')
    transactions2012 = make_transactions(indiv_trans2012, pas_trans2012)
    fec2012 = make_fec(transactions2012, ccl2012, cn2012)

    pas_trans2014 = group_by_trans(pas2014, 'TRANS_BY_CMTE')
    indiv_trans2014 = group_by_trans(indiv2014, 'TRANS_BY_INDIV')
    transactions2014 = make_transactions(indiv_trans2014, pas_trans2014)
    fec2014 = make_fec(transactions2014, ccl2014, cn2014)

    pas_trans2016 = group_by_trans(pas2016, 'TRANS_BY_CMTE')
    indiv_trans2016 = group_by_trans(indiv2016, 'TRANS_BY_INDIV')
    transactions2016 = make_transactions(indiv_trans2016, pas_trans2016)
    fec2016 = make_fec(transactions2016, ccl2016, cn2016)

    fec = pd.concat([fec2010, fec2012, fec2014, fec2016])

    return fec


if __name__ == "__main__":

    fec = get_fec()
