import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import time


def read_indiv():
    #processes about 50,000 records/second
    #more than 20 million records

    headers = pd.read_csv('indiv16/indiv_header_file.csv')
    datafile = 'indiv16/itcont.txt'
    # headers = pd.read_csv('pas216/pas2.headers.csv')

    tic = time.time()
    indiv = pd.read_csv(datafile, sep = '|', error_bad_lines=False, names = headers, nrows=2000000 )
    indiv.fillna(value=0, inplace=True)
    indiv.ZIP_CODE = indiv.ZIP_CODE.astype(str)
    indiv.TRANSACTION_DT = indiv.TRANSACTION_DT.astype(str)

    for col in headers:
        dfsums = indiv.groupby(col)['TRANSACTION_AMT'].sum().astype(int)
        top50 = dfsums.sort_values(axis=0, ascending=False)[:min(50, dfsums.shape[0])]


    toc = time.time()
    print ("Elapsed time: ", str(round(toc-tic,1)), "seconds")
    print ("Total records: {:,}".format(indiv.shape[0]))

    return indiv

def read_pas2():
    headers = pd.read_csv('pas216/pas2.headers.csv')
    datafile = 'pas216/itpas2.txt'
    pas2 = pd.read_csv(datafile, sep = '|', error_bad_lines=False, names = headers)
    return pas2

def read_ccl():
    headers = pd.read_csv('ccl/ccl_header_file.csv')
    datafile = 'ccl/ccl.txt'
    ccl = pd.read_csv(datafile, sep = '|', error_bad_lines=False, names = headers)
    return ccl

def read_cn():
    headers = pd.read_csv('cn/cn_header_file.csv')
    datafile = 'cn/cn.txt'
    cn = pd.read_csv(datafile, sep = '|', error_bad_lines=False, names = headers)
    return cn


if __name__ == "__main__":
    indiv = read_indiv()
    pas2 = read_pas2()
    ccl = read_ccl()
    cn = read_cn()

    pd.set_option('display.precision', 2)
    pd.options.display.float_format = '{:,.0f}'.format

    pas2_trans = pas2.groupby('CMTE_ID')['TRANSACTION_AMT'].sum().astype(int)
    pas2_trans.rename("TRANS_BY_CMTE",inplace = True)
    indiv_trans = indiv.groupby('CMTE_ID')['TRANSACTION_AMT'].sum().astype(int)
    indiv_trans.rename("TRANS_BY_INDIV", inplace=True)

    transactions = pd.concat([indiv_trans,pas2_trans], axis=1)
    transactions['TOTAL_TRANS'] = transactions['TRANS_BY_INDIV'].fillna(0) + transactions['TRANS_BY_CMTE'].fillna(0)
    transactions['CMTE_ID'] = transactions.index

    trans_w_candID = pd.merge(transactions, ccl, on = 'CMTE_ID', how='left')
    trans_by_candID = trans_w_candID.groupby('CAND_ID')['TOTAL_TRANS'].sum().astype(int)
    trans_cand = pd.merge(trans_candID, cn, on = 'CAND_ID', how='left')



    cmte_trans = ccl.set_index('CMTE_ID').join(transactions)
