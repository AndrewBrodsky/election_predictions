import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import time


def read_indiv():
    #processes about 50,000 records/second
    #more than 20 million records

    indiv_headers = pd.read_csv('indiv16/indiv_header_file.csv')
    datafile = 'indiv16/itcont.txt'
    # headers = pd.read_csv('pas216/pas2.headers.csv')

    tic = time.time()
    df_indiv = pd.read_csv(datafile, sep = '|', error_bad_lines=False, names = indiv_headers, nrows=20000 )
    df_indiv.fillna(value=0, inplace=True)
    df_indiv.ZIP_CODE = df_indiv.ZIP_CODE.astype(str)
    df_indiv.TRANSACTION_DT = df_indiv.TRANSACTION_DT.astype(str)

    for col in indiv_headers:
        dfsums = df_indiv.groupby(col)['TRANSACTION_AMT'].sum().astype(int)
        top50 = dfsums.sort_values(axis=0, ascending=False)[:min(50, dfsums.shape[0])]
        print (col, top50, "\n\n")

    toc = time.time()
    print ("Elapsed time: ", str(round(toc-tic,1)), "seconds")
    print ("Total records: {:,}".format(df_indiv.shape[0]))

def read_pas2():
    pas2_headers = pd.read_csv('pas216/pas2.headers.csv')
    datafile = 'pas216/itpas2.txt'
    df_pas2 = pd.read_csv(datafile, sep = '|', error_bad_lines=False, names = pas2_headers)
    return df_pas2

def read_ccl():
    ccl_headers = pd.read_csv('ccl/ccl_header_file.csv')
    datafile = 'ccl/ccl.txt'
    df_ccl = pd.read_csv(datafile, sep = '|', error_bad_lines=False, names = ccl_headers)
    return df_ccl

def read_cn():
    cn_headers = pd.read_csv('cn/cn_header_file.csv')
    datafile = 'cn/cn.txt'
    df_cn = pd.read_csv(datafile, sep = '|', error_bad_lines=False, names = cn_headers)
    return df_cn

def read_oppexp():
    pass


if __name__ == "__main__":
    read_indiv()
    df_pas2 = read_pas2()
    df_ccl = read_ccl()
    oppexp()

    pd.set_option('display.precision', 2)
    pd.options.display.float_format = '{:,.0f}'.format

    trans_by_cmte = df_pas2.groupby('CMTE_ID')['TRANSACTION_AMT'].sum().astype(int)
    result = df_ccl.set_index('CMTE_ID').join(trans_by_cmte)
