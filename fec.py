import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import time


def read_indiv():
    #takes about 210 seconds to read
    #20,353,316 records

    num_records = 100000

    headers = pd.read_csv('fec/indiv16/indiv_header_file.csv')
    datafile = 'fec/indiv16/itcont.txt'
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
    #print ("Elapsed time: ", str(round(toc-tic,1)), "seconds")
    print ("Total records: {:,}".format(indiv.shape[0]))
    #print ("Reading time was about {:,.0f} records per second".format(num_records/(toc-tic)))

    return indiv


def read_file(header_file, data_file):
    headers = pd.read_csv(header_file)
    file = pd.read_csv(data_file, sep = '|', error_bad_lines = False, names = headers)
    return file


def group_by_trans(filename, varname):
    file_trans = filename.groupby('CMTE_ID')['TRANSACTION_AMT'].sum().astype(int)
    file_trans.rename(varname,inplace = True)

    return file_trans


def make_transactions(indiv_trans, pas2_trans):

    transactions = pd.concat([indiv_trans,pas2_trans], axis=1)
    transactions['TOTAL_TRANS'] = transactions['TRANS_BY_INDIV'].fillna(0) + transactions['TRANS_BY_CMTE'].fillna(0)
    transactions['CMTE_ID'] = transactions.index

    return transactions


def make_fec(transactions, ccl, cn):

    trans_w_candID = pd.merge(transactions, ccl, on = 'CMTE_ID', how='left')
    trans_by_candID = trans_w_candID.groupby('CAND_ID')['TOTAL_TRANS', 'TRANS_BY_INDIV', 'TRANS_BY_CMTE'].sum().astype(int)
    trans_by_candID['CAND_ID'] = trans_by_candID.index
    fec = pd.merge(trans_by_candID, cn, on = 'CAND_ID', how='left')
    fec.rename(columns={'CAND_ST': 'STATE', 'CAND_OFFICE_DISTRICT': 'DISTRICT'}, inplace=True)
    fec['LAST_NAME'] = fec.CAND_NAME.str.split(" ").str[0].str.replace(",","")

    return fec


def get_fec():
    pd.set_option('display.precision', 2)
    pd.options.display.float_format = '{:,.0f}'.format

    indiv = read_indiv()
    pas2 = read_file('fec/pas216/pas2.headers.csv', 'fec/pas216/itpas2.txt')
    ccl = read_file('fec/ccl/ccl_header_file.csv', 'fec/ccl/ccl.txt')
    cn = read_file('fec/cn/cn_header_file.csv', 'fec/cn/cn.txt')

    pas2_trans = group_by_trans(pas2, 'TRANS_BY_CMTE')
    indiv_trans = group_by_trans(indiv, 'TRANS_BY_INDIV')

    transactions = make_transactions(indiv_trans, pas2_trans)

    fec = make_fec(transactions, ccl, cn)

    return fec


if __name__ == "__main__":

    fec = get_fec()
