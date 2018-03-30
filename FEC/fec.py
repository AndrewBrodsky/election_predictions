import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import time


def read_indiv():
    #takes about 210 seconds to read
    #20,353,316 records

    num_records = 40100100

    headers = pd.read_csv('indiv16/indiv_header_file.csv')
    datafile = 'indiv16/itcont.txt'
    # headers = pd.read_csv('pas216/pas2.headers.csv')

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
    indiv = pd.read_csv(datafile, sep = '|', error_bad_lines=False, names = headers, nrows=num_records )
    indiv.fillna(value=0, inplace=True)
    indiv.ZIP_CODE = indiv.ZIP_CODE.astype(str)
    indiv.TRANSACTION_DT = indiv.TRANSACTION_DT.astype(str)

    #for col in headers:
    #    dfsums = indiv.groupby(col)['TRANSACTION_AMT'].sum().astype(int)
    #    top50 = dfsums.sort_values(axis=0, ascending=False)[:min(50, dfsums.shape[0])]


    toc = time.time()
    print ("Elapsed time: ", str(round(toc-tic,1)), "seconds")
    print ("Total records: {:,}".format(num_records))
    print ("Reading time was about {:,.0f} records per second".format(num_records/(toc-tic)))

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
    #trans_by_candID = trans_w_candID.groupby('CAND_ID')['TOTAL_TRANS'].sum().astype(int)

    trans_by_candID = trans_w_candID.groupby('CAND_ID')['TOTAL_TRANS', 'TRANS_BY_INDIV', 'TRANS_BY_CMTE'].sum().astype(int)
    trans_by_candID['CAND_ID'] = trans_by_candID.index
    trans_cand = pd.merge(trans_by_candID, cn, on = 'CAND_ID', how='left')
    trans_cand.rename(columns={'CAND_ST': 'state', 'CAND_OFFICE_DISTRICT': 'district'}, inplace=True)

    #need to create new columns instead:
    trans_cand.ln = trans_cand.CAND_NAME.str.split(" ").str[0]
    trans_cand.ln.str.replace(",","")
