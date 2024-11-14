# %%
import matlab.engine
import numpy as np
import tools
import os


directory = '181-1223/181-1232/DAY07_2016-09-01_12-02-01/'


tetrode_files = {"CA1": "TT2.ntt"} #,

'''
    "CA3b_1": "TT3.ntt",
    "CA3a": "TT4.ntt",
    "CA1": "TT5.ntt",
    "CA3b_2": "TT6.ntt",
    "CA2": "TT7.ntt"}
'''

tetrode_files = {
############################################################################################################################
# animal 144
    
    '''# day 13
        # task
    "144_D13_t_CA1_1": "144/DAY13_2014-05-26_14-31-16/TT1.ntt",
    "144_D13_t_CA2_1": "144/DAY13_2014-05-26_14-31-16/TT2.ntt",
    "144_D13_t_X_1": "144/DAY13_2014-05-26_14-31-16/TT3.ntt",
    "144_D13_t_X_2": "144/DAY13_2014-05-26_14-31-16/TT4.ntt",
    "144_D13_t_CA1_2": "144/DAY13_2014-05-26_14-31-16/TT5.ntt",
    "144_D13_t_CA1_3": "144/DAY13_2014-05-26_14-31-16/TT6.ntt",
    "144_D13_t_X_3": "144/DAY13_2014-05-26_14-31-16/TT7.ntt",
    "144_D13_t_CA2_2": "144/DAY13_2014-05-26_14-31-16/TT8.ntt",
        # sleep
    "144_D13_sleep_CA1_1": "144/DAY13_2014-05-26_14-31-16/02_Sleep1/TT1.ntt",
    "144_D13_sleep_CA2_1": "144/DAY13_2014-05-26_14-31-16/02_Sleep1/TT2.ntt",
    "144_D13_sleep_CA1_2": "144/DAY13_2014-05-26_14-31-16/02_Sleep1/TT5.ntt",
    "144_D13_sleep_CA1_3": "144/DAY13_2014-05-26_14-31-16/02_Sleep1/TT6.ntt",
    "144_D13_sleep_CA2_2": "144/DAY13_2014-05-26_14-31-16/02_Sleep1/TT8.ntt",
    '''
    
    # day 16
        # sleep1
    "144_D16_sleep1_CA1_1_pre": "144/DAY16_2014-05-29_10-40-02/02_Sleep1/TT1.ntt",
    "144_D16_sleep1_CA2_1_pre": "144/DAY16_2014-05-29_10-40-02/02_Sleep1/TT2.ntt",
    "144_D16_sleep1_CA1_2_pre": "144/DAY16_2014-05-29_10-40-02/02_Sleep1/TT5.ntt",
    "144_D16_sleep1_CA1_3_pre": "144/DAY16_2014-05-29_10-40-02/02_Sleep1/TT6.ntt",
    "144_D16_sleep1_CA2_2_pre": "144/DAY16_2014-05-29_10-40-02/02_Sleep1/TT8.ntt",
        # BoxA
    "144_D16_boxA_CA1_1_pre": "144/DAY16_2014-05-29_10-40-02/04_BoxA/TT1.ntt",
    "144_D16_boxA_CA2_1_pre": "144/DAY16_2014-05-29_10-40-02/04_BoxA/TT2.ntt",
    "144_D16_boxA_CA1_2_pre": "144/DAY16_2014-05-29_10-40-02/04_BoxA/TT5.ntt",
    "144_D16_boxA_CA1_3_pre": "144/DAY16_2014-05-29_10-40-02/04_BoxA/TT6.ntt",
    "144_D16_boxA_CA2_2_pre": "144/DAY16_2014-05-29_10-40-02/04_BoxA/TT8.ntt",
        # sleep2
    "144_D16_sleep2_CA1_1_pre": "144/DAY16_2014-05-29_10-40-02/06_Sleep2/TT1.ntt",
    "144_D16_sleep2_CA2_1_pre": "144/DAY16_2014-05-29_10-40-02/06_Sleep2TT2.ntt",
    "144_D16_sleep2_CA1_2_pre": "144/DAY16_2014-05-29_10-40-02/06_Sleep2TT5.ntt",
    "144_D16_sleep2_CA1_3_pre": "144/DAY16_2014-05-29_10-40-02/06_Sleep2TT6.ntt",
    "144_D16_sleep2_CA2_2_pre": "144/DAY16_2014-05-29_10-40-02/06_Sleep2TT8.ntt",
        # cno 2mgkg
    "144_D16_cno_CA1_1_post": "144/DAY16_2014-05-29_10-40-02/TT1.ntt",
    "144_D16_cno_CA2_1_post": "144/DAY16_2014-05-29_10-40-02/TT2.ntt",
    "144_D16_cno_CA1_2_post": "144/DAY16_2014-05-29_10-40-02/TT5.ntt",
    "144_D16_cno_CA1_3_post": "144/DAY16_2014-05-29_10-40-02/TT6.ntt",
    "144_D16_cno_CA2_2_post": "144/DAY16_2014-05-29_10-40-02/TT8.ntt",
        # boxC
    "144_D16_boxC_CA1_1_post": "144/DAY16_2014-05-29_10-40-02/TT1.ntt",
    "144_D16_boxC_CA2_1_post": "144/DAY16_2014-05-29_10-40-02/TT2.ntt",
    "144_D16_boxC_CA1_2_post": "144/DAY16_2014-05-29_10-40-02/TT5.ntt",
    "144_D16_boxC_CA1_3_post": "144/DAY16_2014-05-29_10-40-02/TT6.ntt",
    "144_D16_boxC_CA2_2_post": "144/DAY16_2014-05-29_10-40-02/TT8.ntt",
        # sleep4
    "144_D16_sleep4_CA1_1_post": "144/DAY16_2014-05-29_10-40-02/TT1.ntt",
    "144_D16_sleep4_CA2_1_post": "144/DAY16_2014-05-29_10-40-02/TT2.ntt",
    "144_D16_sleep4_CA1_2_post": "144/DAY16_2014-05-29_10-40-02/TT5.ntt",
    "144_D16_sleep4_CA1_3_post": "144/DAY16_2014-05-29_10-40-02/TT6.ntt",
    "144_D16_sleep4_CA2_2_post": "144/DAY16_2014-05-29_10-40-02/TT8.ntt",
        # boxA
    "144_D16_boxA_CA1_1_post": "144/DAY16_2014-05-29_10-40-02/TT1.ntt",
    "144_D16_boxA_CA2_1_post": "144/DAY16_2014-05-29_10-40-02/TT2.ntt",
    "144_D16_boxA_CA1_2_post": "144/DAY16_2014-05-29_10-40-02/TT5.ntt",
    "144_D16_boxA_CA1_3_post": "144/DAY16_2014-05-29_10-40-02/TT6.ntt",
    "144_D16_boxA_CA2_2_post": "144/DAY16_2014-05-29_10-40-02/TT8.ntt",

############################################################################################################################
# animal 161
    # day 3
        # sleep
    "161_D03_sleep_CA1_1_pre": "161/DAY03_2014-04-30_09-25-48/02_Sleep1/TT1.ntt",
    "161_D03_sleep_CA1_2_pre": "161/DAY03_2014-04-30_09-25-48/02_Sleep1/TT3.ntt",
    "161_D03_sleep_CA2_1_pre": "161/DAY03_2014-04-30_09-25-48/02_Sleep1/TT4.ntt",
    "161_D03_sleep_CA1_3_pre": "161/DAY03_2014-04-30_09-25-48/02_Sleep1/TT5.ntt",
    "161_D03_sleep_CA1_4_pre": "161/DAY03_2014-04-30_09-25-48/02_Sleep1/TT6.ntt",
    "161_D03_sleep_CA1_5_pre": "161/DAY03_2014-04-30_09-25-48/02_Sleep1/TT7.ntt",
    "161_D03_sleep_CA1_6_pre": "161/DAY03_2014-04-30_09-25-48/02_Sleep1/TT8.ntt",
        #cno 1mgkg
    "161_D03_cno_CA1_1_post": "161/DAY03_2014-04-30_09-25-48/04_CNO_1mgkg/TT1.ntt",
    "161_D03_cno_CA1_2_post": "161/DAY03_2014-04-30_09-25-48/04_CNO_1mgkg/TT3.ntt",
    "161_D03_cno_CA2_1_post": "161/DAY03_2014-04-30_09-25-48/04_CNO_1mgkg/TT4.ntt",
    "161_D03_cno_CA1_3_post": "161/DAY03_2014-04-30_09-25-48/04_CNO_1mgkg/TT5.ntt",
    "161_D03_cno_CA1_4_post": "161/DAY03_2014-04-30_09-25-48/04_CNO_1mgkg/TT6.ntt",
    "161_D03_cno_CA1_5_post": "161/DAY03_2014-04-30_09-25-48/04_CNO_1mgkg/TT7.ntt",
    "161_D03_cno_CA1_6_post": "161/DAY03_2014-04-30_09-25-48/04_CNO_1mgkg/TT8.ntt",
    
    # day 4
        # sleep
    "161_D04_sleep_CA1_1_pre": "161/DAY03_2014-04-30_09-25-48/02_Sleep1/TT1.ntt",
    "161_D04_sleep_CA1_2_pre": "161/DAY03_2014-04-30_09-25-48/02_Sleep1/TT3.ntt",
    "161_D04_sleep_CA2_1_pre": "161/DAY03_2014-04-30_09-25-48/02_Sleep1/TT4.ntt",
    "161_D04_sleep_CA1_3_pre": "161/DAY03_2014-04-30_09-25-48/02_Sleep1/TT5.ntt",
    "161_D04_sleep_CA1_4_pre": "161/DAY03_2014-04-30_09-25-48/02_Sleep1/TT6.ntt",
    "161_D04_sleep_CA1_5_pre": "161/DAY03_2014-04-30_09-25-48/02_Sleep1/TT7.ntt",
    "161_D04_sleep_CA1_6_pre": "161/DAY03_2014-04-30_09-25-48/02_Sleep1/TT8.ntt",
        #cno 2mgkg
    "161_D04_cno_CA1_1_post": "161/DAY03_2014-04-30_09-25-48/04_CNO_1mgkg/TT1.ntt",
    "161_D04_cno_CA1_2_post": "161/DAY03_2014-04-30_09-25-48/04_CNO_1mgkg/TT3.ntt",
    "161_D04_cno_CA2_1_post": "161/DAY03_2014-04-30_09-25-48/04_CNO_1mgkg/TT4.ntt",
    "161_D04_cno_CA1_3_post": "161/DAY03_2014-04-30_09-25-48/04_CNO_1mgkg/TT5.ntt",
    "161_D04_cno_CA1_4_post": "161/DAY03_2014-04-30_09-25-48/04_CNO_1mgkg/TT6.ntt",
    "161_D04_cno_CA1_5_post": "161/DAY03_2014-04-30_09-25-48/04_CNO_1mgkg/TT7.ntt",
    "161_D04_cno_CA1_6_post": "161/DAY03_2014-04-30_09-25-48/04_CNO_1mgkg/TT8.ntt",
    
    # day 5
        # sleep1
    "161_D05_sleep_CA1_1_pre": "161/DAY05_2014-05-02_11-38-39/02_Sleep1/TT1.ntt",
    "161_D05_sleep_CA1_2_pre": "161/DAY05_2014-05-02_11-38-39/02_Sleep1/TT3.ntt",
    "161_D05_sleep_CA2_1_pre": "161/DAY05_2014-05-02_11-38-39/02_Sleep1/TT4.ntt",
    "161_D05_sleep_CA1_3_pre": "161/DAY05_2014-05-02_11-38-39/02_Sleep1/TT5.ntt",
    "161_D05_sleep_CA1_4_pre": "161/DAY05_2014-05-02_11-38-39/02_Sleep1/TT6.ntt",
    "161_D05_sleep_CA1_5_pre": "161/DAY05_2014-05-02_11-38-39/02_Sleep1/TT7.ntt",
    "161_D05_sleep_CA1_6_pre": "161/DAY05_2014-05-02_11-38-39/02_Sleep1/TT8.ntt", 
        # cno 2mgkg
    "161_D05_cno_CA1_1_post": "161/DAY05_2014-05-02_11-38-39/04_CNO_2mgkg/TT1.ntt",
    "161_D05_cno_CA1_2_post": "161/DAY05_2014-05-02_11-38-39/04_CNO_2mgkg/TT3.ntt",
    "161_D05_cno_CA2_1_post": "161/DAY05_2014-05-02_11-38-39/04_CNO_2mgkg/TT4.ntt",
    "161_D05_cno_CA1_3_post": "161/DAY05_2014-05-02_11-38-39/04_CNO_2mgkg/TT5.ntt",
    "161_D05_cno_CA1_4_post": "161/DAY05_2014-05-02_11-38-39/04_CNO_2mgkg/TT6.ntt",
    "161_D05_cno_CA1_5_post": "161/DAY05_2014-05-02_11-38-39/04_CNO_2mgkg/TT7.ntt",
    "161_D05_cno_CA1_6_post": "161/DAY05_2014-05-02_11-38-39/04_CNO_2mgkg/TT8.ntt",
    
    # day 10
        # sleep1
    "161_D10_sleep1_CA1_1_pre": "161/DAY10_2014-05-07_13-07-20/02_Sleep1/TT1.ntt",
    "161_D10_sleep1_CA1_2_pre": "161/DAY10_2014-05-07_13-07-20/02_Sleep1/TT3.ntt",
    "161_D10_sleep1_CA2_1_pre": "161/DAY10_2014-05-07_13-07-20/02_Sleep1/TT4.ntt",
    "161_D10_sleep1_CA1_3_pre": "161/DAY10_2014-05-07_13-07-20/02_Sleep1/TT5.ntt",
    "161_D10_sleep1_CA1_4_pre": "161/DAY10_2014-05-07_13-07-20/02_Sleep1/TT6.ntt",
    "161_D10_sleep1_CA1_5_pre": "161/DAY10_2014-05-07_13-07-20/02_Sleep1/TT7.ntt",
    "161_D10_sleep1_CA1_6_pre": "161/DAY10_2014-05-07_13-07-20/02_Sleep1/TT8.ntt", 
        # cno 2mgkg
    "161_D10_cno_CA1_1_pre": "161/DAY10_2014-05-07_13-07-20/04_CNO_2mgkg/TT1.ntt",
    "161_D10_cno_CA1_2_pre": "161/DAY10_2014-05-07_13-07-20/04_CNO_2mgkg/TT3.ntt",
    "161_D10_cno_CA2_1_pre": "161/DAY10_2014-05-07_13-07-20/04_CNO_2mgkg/TT4.ntt",
    "161_D10_cno_CA1_3_pre": "161/DAY10_2014-05-07_13-07-20/04_CNO_2mgkg/TT5.ntt",
    "161_D10_cno_CA1_4_pre": "161/DAY10_2014-05-07_13-07-20/04_CNO_2mgkg/TT6.ntt",
    "161_D10_cno_CA1_5_pre": "161/DAY10_2014-05-07_13-07-20/04_CNO_2mgkg/TT7.ntt",
    "161_D10_cno_CA1_6_pre": "161/DAY10_2014-05-07_13-07-20/04_CNO_2mgkg/TT8.ntt", 
        # sleep2
    "161_D10_sleep2_CA1_1_pre": "161/DAY10_2014-05-07_13-07-20/06_Sleep1/TT1.ntt",
    "161_D10_sleep2_CA1_2_pre": "161/DAY10_2014-05-07_13-07-20/06_Sleep1/TT3.ntt",
    "161_D10_sleep2_CA2_1_pre": "161/DAY10_2014-05-07_13-07-20/06_Sleep1/TT4.ntt",
    "161_D10_sleep2_CA1_3_pre": "161/DAY10_2014-05-07_13-07-20/06_Sleep1/TT5.ntt",
    "161_D10_sleep2_CA1_4_pre": "161/DAY10_2014-05-07_13-07-20/06_Sleep1/TT6.ntt",
    "161_D10_sleep2_CA1_5_pre": "161/DAY10_2014-05-07_13-07-20/06_Sleep1/TT7.ntt",
    "161_D10_sleep2_CA1_6_pre": "161/DAY10_2014-05-07_13-07-20/06_Sleep1/TT8.ntt", 
    
    # day 12
        # sleep1
    "161_D12_sleep1_CA1_1_pre": "161/DAY12_2014-05-09_13-11-31/02_Sleep1/TT1.ntt",
    "161_D12_sleep1_CA1_2_pre": "161/DAY12_2014-05-09_13-11-31/02_Sleep1/TT3.ntt",
    "161_D12_sleep1_CA2_1_pre": "161/DAY12_2014-05-09_13-11-31/02_Sleep1/TT4.ntt",
    "161_D12_sleep1_CA1_3_pre": "161/DAY12_2014-05-09_13-11-31/02_Sleep1/TT5.ntt",
    "161_D12_sleep1_CA1_4_pre": "161/DAY12_2014-05-09_13-11-31/02_Sleep1/TT6.ntt",
    "161_D12_sleep1_CA1_5_pre": "161/DAY12_2014-05-09_13-11-31/02_Sleep1/TT7.ntt",
    "161_D12_sleep1_CA1_6_pre": "161/DAY12_2014-05-09_13-11-31/02_Sleep1/TT8.ntt", 
        # LT1
    "161_D12_lt11_CA1_1_pre": "161/DAY12_2014-05-09_13-11-31/04_LT1/TT1.ntt",
    "161_D12_lt11_CA1_2_pre": "161/DAY12_2014-05-09_13-11-31/04_LT1/TT3.ntt",
    "161_D12_lt11_CA2_1_pre": "161/DAY12_2014-05-09_13-11-31/04_LT1/TT4.ntt",
    "161_D12_lt11_CA1_3_pre": "161/DAY12_2014-05-09_13-11-31/04_LT1/TT5.ntt",
    "161_D12_lt11_CA1_4_pre": "161/DAY12_2014-05-09_13-11-31/04_LT1/TT6.ntt",
    "161_D12_lt11_CA1_5_pre": "161/DAY12_2014-05-09_13-11-31/04_LT1/TT7.ntt",
    "161_D12_lt11_CA1_6_pre": "161/DAY12_2014-05-09_13-11-31/04_LT1/TT8.ntt", 
        # sleep2
    "161_D12_sleep2_CA1_1_pre": "161/DAY12_2014-05-09_13-11-31/06_Sleep2/TT1.ntt",
    "161_D12_sleep2_CA1_2_pre": "161/DAY12_2014-05-09_13-11-31/06_Sleep2/TT3.ntt",
    "161_D12_sleep2_CA2_1_pre": "161/DAY12_2014-05-09_13-11-31/06_Sleep2/TT4.ntt",
    "161_D12_sleep2_CA1_3_pre": "161/DAY12_2014-05-09_13-11-31/06_Sleep2/TT5.ntt",
    "161_D12_sleep2_CA1_4_pre": "161/DAY12_2014-05-09_13-11-31/06_Sleep2/TT6.ntt",
    "161_D12_sleep2_CA1_5_pre": "161/DAY12_2014-05-09_13-11-31/06_Sleep2/TT7.ntt",
    "161_D12_sleep2_CA1_6_pre": "161/DAY12_2014-05-09_13-11-31/06_Sleep2/TT8.ntt", 
    
     # cno 2mgkg
    "161_D12_cno_CA1_1_post": "161/DAY12_2014-05-09_14-16-23/02_CNO_2mgkg/TT1.ntt",
    "161_D12_cno_CA1_2_post": "161/DAY12_2014-05-09_14-16-23/02_CNO_2mgkg/TT3.ntt",
    "161_D12_cno_CA2_1_post": "161/DAY12_2014-05-09_14-16-23/02_CNO_2mgkg/TT4.ntt",
    "161_D12_cno_CA1_3_post": "161/DAY12_2014-05-09_14-16-23/02_CNO_2mgkg/TT5.ntt",
    "161_D12_cno_CA1_4_post": "161/DAY12_2014-05-09_14-16-23/02_CNO_2mgkg/TT6.ntt",
    "161_D12_cno_CA1_5_post": "161/DAY12_2014-05-09_14-16-23/02_CNO_2mgkg/TT7.ntt",
    "161_D12_cno_CA1_6_post": "161/DAY12_2014-05-09_14-16-23/02_CNO_2mgkg/TT8.ntt", 
        # LT1
    "161_D12_lt12_CA1_1_post": "161/DAY12_2014-05-09_14-16-23/04_LT1/TT1.ntt",
    "161_D12_lt12_CA1_2_post": "161/DAY12_2014-05-09_14-16-23/04_LT1/TT3.ntt",
    "161_D12_lt12_CA2_1_post": "161/DAY12_2014-05-09_14-16-23/04_LT1/TT4.ntt",
    "161_D12_lt12_CA1_3_post": "161/DAY12_2014-05-09_14-16-23/04_LT1/TT5.ntt",
    "161_D12_lt12_CA1_4_post": "161/DAY12_2014-05-09_14-16-23/04_LT1/TT6.ntt",
    "161_D12_lt12_CA1_5_post": "161/DAY12_2014-05-09_14-16-23/04_LT1/TT7.ntt",
    "161_D12_lt12_CA1_6_post": "161/DAY12_2014-05-09_14-16-23/04_LT1/TT8.ntt", 
        # sleep2
    "161_D12_sleep3_CA1_1_post": "161/DAY12_2014-05-09_13-11-31/06_Sleep3/TT1.ntt",
    "161_D12_sleep3_CA1_2_post": "161/DAY12_2014-05-09_13-11-31/06_Sleep3/TT3.ntt",
    "161_D12_sleep3_CA2_1_post": "161/DAY12_2014-05-09_13-11-31/06_Sleep3/TT4.ntt",
    "161_D12_sleep3_CA1_3_post": "161/DAY12_2014-05-09_13-11-31/06_Sleep3/TT5.ntt",
    "161_D12_sleep3_CA1_4_post": "161/DAY12_2014-05-09_13-11-31/06_Sleep3/TT6.ntt",
    "161_D12_sleep3_CA1_5_post": "161/DAY12_2014-05-09_13-11-31/06_Sleep3/TT7.ntt",
    "161_D12_sleep3_CA1_6_post": "161/DAY12_2014-05-09_13-11-31/06_Sleep3/TT8.ntt", 
    
    
    
############################################################################################################################    
# animal 248
    # day 4
        # task
    "248_D04_t_CA2_1": "248/181-248/DAY04_2014-05-01_13-35-06/TT1.ntt",
    "248_D04_t_X_1": "248/181-248/DAY04_2014-05-01_13-35-06/TT2.ntt",
    "248_D04_t_CA1_1": "248/181-248/DAY04_2014-05-01_13-35-06/TT3.ntt",
    "248_D04_t_CA1_2": "248/181-248/DAY04_2014-05-01_13-35-06/TT4.ntt",
    "248_D04_t_CA1_3": "248/181-248/DAY04_2014-05-01_13-35-06/TT5.ntt",
    "248_D04_t_CA1_4": "248/181-248/DAY04_2014-05-01_13-35-06/TT6.ntt",
    "248_D04_t_CA1_5": "248/181-248/DAY04_2014-05-01_13-35-06/TT7.ntt",
    "248_D04_t_CA1_6": "248/181-248/DAY04_2014-05-01_13-35-06/TT8.ntt",
        # sleep
    "248_D04_sleep_CA2_1": "248/181-248/DAY04_2014-05-01_13-35-06/02_Sleep1/TT1.ntt",
    "248_D04_sleep_CA1_1": "248/181-248/DAY04_2014-05-01_13-35-06/02_Sleep1/TT3.ntt",
    "248_D04_sleep_CA1_2": "248/181-248/DAY04_2014-05-01_13-35-06/02_Sleep1/TT4.ntt",
    "248_D04_sleep_CA1_3": "248/181-248/DAY04_2014-05-01_13-35-06/02_Sleep1/TT5.ntt",
    "248_D04_sleep_CA1_4": "248/181-248/DAY04_2014-05-01_13-35-06/02_Sleep1/TT6.ntt",
    "248_D04_sleep_CA1_5": "248/181-248/DAY04_2014-05-01_13-35-06/02_Sleep1/TT7.ntt",
    "248_D04_sleep_CA1_6": "248/181-248/DAY04_2014-05-01_13-35-06/02_Sleep1/TT8.ntt",
        # cno
    "248_D04_cno_CA2_1": "248/181-248/DAY04_2014-05-01_13-35-06/04_CNO_2mgkg/TT1.ntt",
    "248_D04_cno_CA1_1": "248/181-248/DAY04_2014-05-01_13-35-06/04_CNO_2mgkg/TT3.ntt",
    "248_D04_cno_CA1_2": "248/181-248/DAY04_2014-05-01_13-35-06/04_CNO_2mgkg/TT4.ntt",
    "248_D04_cno_CA1_3": "248/181-248/DAY04_2014-05-01_13-35-06/04_CNO_2mgkg/TT5.ntt",
    "248_D04_cno_CA1_4": "248/181-248/DAY04_2014-05-01_13-35-06/04_CNO_2mgkg/TT6.ntt",
    "248_D04_cno_CA1_5": "248/181-248/DAY04_2014-05-01_13-35-06/04_CNO_2mgkg/TT7.ntt",
    "248_D04_cno_CA1_6": "248/181-248/DAY04_2014-05-01_13-35-06/04_CNO_2mgkg/TT8.ntt",

############################################################################################################################
# animal 368
    # day 8
        # task
    "368_D08_t_CA1_1": "368/181-368/DAY08_2014-07-17_09-15-41/TT1.ntt",
    "368_D08_t_CA1_2": "368/181-368/DAY08_2014-07-17_09-15-41/TT2.ntt",
    "368_D08_t_CA2_1": "368/181-368/DAY08_2014-07-17_09-15-41/TT3.ntt",
    "368_D08_t_CA3_1": "368/181-368/DAY08_2014-07-17_09-15-41/TT4.ntt",
    "368_D08_t_CA1_3": "368/181-368/DAY08_2014-07-17_09-15-41/TT5.ntt",
    "368_D08_t_CA1_4": "368/181-368/DAY08_2014-07-17_09-15-41/TT6.ntt",
    "368_D08_t_CA1_5": "368/181-368/DAY08_2014-07-17_09-15-41/TT7.ntt",
    "368_D08_t_CA1_6": "368/181-368/DAY08_2014-07-17_09-15-41/TT8.ntt",
        # sleep1
    "368_D08_sleep1_CA1_1": "368/181-368/DAY08_2014-07-17_09-15-41/02_Sleep1/TT1.ntt",
    "368_D08_sleep1_CA1_2": "368/181-368/DAY08_2014-07-17_09-15-41/02_Sleep1/TT2.ntt",
    "368_D08_sleep1_CA2_1": "368/181-368/DAY08_2014-07-17_09-15-41/02_Sleep1/TT3.ntt",
    "368_D08_sleep1_CA3_1": "368/181-368/DAY08_2014-07-17_09-15-41/02_Sleep1/TT4.ntt",
    "368_D08_sleep1_CA1_3": "368/181-368/DAY08_2014-07-17_09-15-41/02_Sleep1/TT5.ntt",
    "368_D08_sleep1_CA1_4": "368/181-368/DAY08_2014-07-17_09-15-41/02_Sleep1/TT6.ntt",
    "368_D08_sleep1_CA1_5": "368/181-368/DAY08_2014-07-17_09-15-41/02_Sleep1/TT7.ntt",
    "368_D08_sleep1_CA1_6": "368/181-368/DAY08_2014-07-17_09-15-41/02_Sleep1/TT8.ntt",
        # box A
    "368_D08_boxA_CA1_1": "368/181-368/DAY08_2014-07-17_09-15-41/04_BoxA/TT1.ntt",
    "368_D08_boxA_CA1_2": "368/181-368/DAY08_2014-07-17_09-15-41/04_BoxA/TT2.ntt",
    "368_D08_boxA_CA2_1": "368/181-368/DAY08_2014-07-17_09-15-41/04_BoxA/TT3.ntt",
    "368_D08_boxA_CA3_1": "368/181-368/DAY08_2014-07-17_09-15-41/04_BoxA/TT4.ntt",
    "368_D08_boxA_CA1_3": "368/181-368/DAY08_2014-07-17_09-15-41/04_BoxA/TT5.ntt",
    "368_D08_boxA_CA1_4": "368/181-368/DAY08_2014-07-17_09-15-41/04_BoxA/TT6.ntt",
    "368_D08_boxA_CA1_5": "368/181-368/DAY08_2014-07-17_09-15-41/04_BoxA/TT7.ntt",
    "368_D08_boxA_CA1_6": "368/181-368/DAY08_2014-07-17_09-15-41/04_BoxA/TT8.ntt",
        # sleep2
    "368_D08_sleep2_CA1_1": "368/181-368/DAY08_2014-07-17_09-15-41/06_Sleep2/TT1.ntt",
    "368_D08_sleep2_CA1_2": "368/181-368/DAY08_2014-07-17_09-15-41/06_Sleep2/TT2.ntt",
    "368_D08_sleep2_CA2_1": "368/181-368/DAY08_2014-07-17_09-15-41/06_Sleep2/TT3.ntt",
    "368_D08_sleep2_CA3_1": "368/181-368/DAY08_2014-07-17_09-15-41/06_Sleep2/TT4.ntt",
    "368_D08_sleep2_CA1_3": "368/181-368/DAY08_2014-07-17_09-15-41/06_Sleep2/TT5.ntt",
    "368_D08_sleep2_CA1_4": "368/181-368/DAY08_2014-07-17_09-15-41/06_Sleep2/TT6.ntt",
    "368_D08_sleep2_CA1_5": "368/181-368/DAY08_2014-07-17_09-15-41/06_Sleep2/TT7.ntt",
    "368_D08_sleep2_CA1_6": "368/181-368/DAY08_2014-07-17_09-15-41/06_Sleep2/TT8.ntt",
    
    # day 9
        # task
    "368_D09_t_CA1_1": "368/181-368/DAY09_2014-07-18_08-56-38/TT1.ntt",
    "368_D09_t_CA1_2": "368/181-368/DAY09_2014-07-18_08-56-38/TT2.ntt",
    "368_D09_t_CA2_1": "368/181-368/DAY09_2014-07-18_08-56-38/TT3.ntt",
    "368_D09_t_CA3_1": "368/181-368/DAY09_2014-07-18_08-56-38/TT4.ntt",
    "368_D09_t_CA1_3": "368/181-368/DAY09_2014-07-18_08-56-38/TT5.ntt",
    "368_D09_t_CA1_4": "368/181-368/DAY09_2014-07-18_08-56-38/TT6.ntt",
    "368_D09_t_CA1_5": "368/181-368/DAY09_2014-07-18_08-56-38/TT7.ntt",
    "368_D09_t_CA1_6": "368/181-368/DAY09_2014-07-18_08-56-38/TT8.ntt",
        # sleep1
    "368_D09_sleep1_CA1_1": "368/181-368/DAY09_2014-07-18_08-56-38/02_Sleep1/TT1.ntt",
    "368_D09_sleep1_CA1_2": "368/181-368/DAY09_2014-07-18_08-56-38/02_Sleep1/TT2.ntt",
    "368_D09_sleep1_CA2_1": "368/181-368/DAY09_2014-07-18_08-56-38/02_Sleep1/TT3.ntt",
    "368_D09_sleep1_CA3_1": "368/181-368/DAY09_2014-07-18_08-56-38/02_Sleep1/TT4.ntt",
    "368_D09_sleep1_CA1_3": "368/181-368/DAY09_2014-07-18_08-56-38/02_Sleep1/TT5.ntt",
    "368_D09_sleep1_CA1_4": "368/181-368/DAY09_2014-07-18_08-56-38/02_Sleep1/TT6.ntt",
    "368_D09_sleep1_CA1_5": "368/181-368/DAY09_2014-07-18_08-56-38/02_Sleep1/TT7.ntt",
    "368_D09_sleep1_CA1_6": "368/181-368/DAY09_2014-07-18_08-56-38/02_Sleep1/TT8.ntt",
        # box A
    "368_D09_boxA_CA1_1": "368/181-368/DAY08_2014-07-18_08-56-38/04_BoxA/TT1.ntt",
    "368_D09_boxA_CA1_2": "368/181-368/DAY08_2014-07-18_08-56-38/04_BoxA/TT2.ntt",
    "368_D09_boxA_CA2_1": "368/181-368/DAY08_2014-07-18_08-56-38/04_BoxA/TT3.ntt",
    "368_D09_boxA_CA3_1": "368/181-368/DAY08_2014-07-18_08-56-38/04_BoxA/TT4.ntt",
    "368_D09_boxA_CA1_3": "368/181-368/DAY08_2014-07-18_08-56-38/04_BoxA/TT5.ntt",
    "368_D09_boxA_CA1_4": "368/181-368/DAY08_2014-07-18_08-56-38/04_BoxA/TT6.ntt",
    "368_D09_boxA_CA1_5": "368/181-368/DAY08_2014-07-18_08-56-38/04_BoxA/TT7.ntt",
    "368_D09_boxA_CA1_6": "368/181-368/DAY08_2014-07-18_08-56-38/04_BoxA/TT8.ntt",
        # sleep2
    "368_D09_sleep2_CA1_1": "368/181-368/DAY08_2014-07-18_08-56-38/06_Sleep2/TT1.ntt",
    "368_D09_sleep2_CA1_2": "368/181-368/DAY08_2014-07-18_08-56-38/06_Sleep2/TT2.ntt",
    "368_D09_sleep2_CA2_1": "368/181-368/DAY08_2014-07-18_08-56-38/06_Sleep2/TT3.ntt",
    "368_D09_sleep2_CA3_1": "368/181-368/DAY08_2014-07-18_08-56-38/06_Sleep2/TT4.ntt",
    "368_D09_sleep2_CA1_3": "368/181-368/DAY08_2014-07-18_08-56-38/06_Sleep2/TT5.ntt",
    "368_D09_sleep2_CA1_4": "368/181-368/DAY08_2014-07-18_08-56-38/06_Sleep2/TT6.ntt",
    "368_D09_sleep2_CA1_5": "368/181-368/DAY08_2014-07-18_08-56-38/06_Sleep2/TT7.ntt",
    "368_D09_sleep2_CA1_6": "368/181-368/DAY08_2014-07-18_08-56-38/06_Sleep2/TT8.ntt",
    
    # day 9 again somehow...? I just call it day 10
        # task
    "368_D10_t_CA1_1": "368/181-368/DAY09_2014-07-18_10-13-37/TT1.ntt",
    "368_D10_t_CA1_2": "368/181-368/DAY09_2014-07-18_10-13-37/TT2.ntt",
    "368_D10_t_CA2_1": "368/181-368/DAY09_2014-07-18_10-13-37/TT3.ntt",
    "368_D10_t_CA3_1": "368/181-368/DAY09_2014-07-18_10-13-37/TT4.ntt",
    "368_D10_t_CA1_3": "368/181-368/DAY09_2014-07-18_10-13-37/TT5.ntt",
    "368_D10_t_CA1_4": "368/181-368/DAY09_2014-07-18_10-13-37/TT6.ntt",
    "368_D10_t_CA1_5": "368/181-368/DAY09_2014-07-18_10-13-37/TT7.ntt",
    "368_D10_t_CA1_6": "368/181-368/DAY09_2014-07-18_10-13-37/TT8.ntt",
        # sleep1
    "368_D10_sleep1_CA1_1": "368/181-368/DAY09_2014-07-18_10-13-37/02_Sleep1/TT1.ntt",
    "368_D10_sleep1_CA1_2": "368/181-368/DAY09_2014-07-18_10-13-37/02_Sleep1/TT2.ntt",
    "368_D10_sleep1_CA2_1": "368/181-368/DAY09_2014-07-18_10-13-37/02_Sleep1/TT3.ntt",
    "368_D10_sleep1_CA3_1": "368/181-368/DAY09_2014-07-18_10-13-37/02_Sleep1/TT4.ntt",
    "368_D10_sleep1_CA1_3": "368/181-368/DAY09_2014-07-18_10-13-37/02_Sleep1/TT5.ntt",
    "368_D10_sleep1_CA1_4": "368/181-368/DAY09_2014-07-18_10-13-37/02_Sleep1/TT6.ntt",
    "368_D10_sleep1_CA1_5": "368/181-368/DAY09_2014-07-18_10-13-37/02_Sleep1/TT7.ntt",
    "368_D10_sleep1_CA1_6": "368/181-368/DAY09_2014-07-18_10-13-37/02_Sleep1/TT8.ntt",
        # cno
    "368_D10_t_CA1_1": "368/181-368/DAY09_2014-07-18_10-13-37/05_CNO_2mgkg/TT1.ntt",
    "368_D10_t_CA1_2": "368/181-368/DAY09_2014-07-18_10-13-37/05_CNO_2mgkg/TT2.ntt",
    "368_D10_t_CA2_1": "368/181-368/DAY09_2014-07-18_10-13-37/05_CNO_2mgkg/TT3.ntt",
    "368_D10_t_CA3_1": "368/181-368/DAY09_2014-07-18_10-13-37/05_CNO_2mgkg/TT4.ntt",
    "368_D10_t_CA1_3": "368/181-368/DAY09_2014-07-18_10-13-37/05_CNO_2mgkg/TT5.ntt",
    "368_D10_t_CA1_4": "368/181-368/DAY09_2014-07-18_10-13-37/05_CNO_2mgkg/TT6.ntt",
    "368_D10_t_CA1_5": "368/181-368/DAY09_2014-07-18_10-13-37/05_CNO_2mgkg/TT7.ntt",
    "368_D10_t_CA1_6": "368/181-368/DAY09_2014-07-18_10-13-37/05_CNO_2mgkg/TT8.ntt",
    
####################################################################
# HOPEFULLY ALL ANALYZED BY NOW ####################################
# MIGHT ADD CONDITION TO CHECK IF FILE HAS BEEN ANALYZED ###########
####################################################################

    # day 13
        # task
    "368_D13_t_CA1_1": "368/181-368/DAY13_2014-07-22_10-25-46/TT1.ntt",
    "368_D13_t_CA1_2": "368/181-368/DAY13_2014-07-22_10-25-46/TT2.ntt",
    "368_D13_t_CA2_1": "368/181-368/DAY13_2014-07-22_10-25-46/TT3.ntt",
    "368_D13_t_CA3_1": "368/181-368/DAY13_2014-07-22_10-25-46/TT4.ntt",
    "368_D13_t_CA1_3": "368/181-368/DAY13_2014-07-22_10-25-46/TT5.ntt",
    "368_D13_t_CA1_4": "368/181-368/DAY13_2014-07-22_10-25-46/TT6.ntt",
    "368_D13_t_CA1_5": "368/181-368/DAY13_2014-07-22_10-25-46/TT7.ntt",
    "368_D13_t_CA1_6": "368/181-368/DAY13_2014-07-22_10-25-46/TT8.ntt",
        # sleep1
    "368_D13_sleep1_CA1_1": "368/181-368/DAY13_2014-07-22_10-25-46/02_Sleep1/TT1.ntt",
    "368_D13_sleep1_CA1_2": "368/181-368/DAY13_2014-07-22_10-25-46/02_Sleep1/TT2.ntt",
    "368_D13_sleep1_CA2_1": "368/181-368/DAY13_2014-07-22_10-25-46/02_Sleep1/TT3.ntt",
    "368_D13_sleep1_CA3_1": "368/181-368/DAY13_2014-07-22_10-25-46/02_Sleep1/TT4.ntt",
    "368_D13_sleep1_CA1_3": "368/181-368/DAY13_2014-07-22_10-25-46/02_Sleep1/TT5.ntt",
    "368_D13_sleep1_CA1_4": "368/181-368/DAY13_2014-07-22_10-25-46/02_Sleep1/TT6.ntt",
    "368_D13_sleep1_CA1_5": "368/181-368/DAY13_2014-07-22_10-25-46/02_Sleep1/TT7.ntt",
    "368_D13_sleep1_CA1_6": "368/181-368/DAY13_2014-07-22_10-25-46/02_Sleep1/TT8.ntt",
        # box A
    "368_D13_boxA_CA1_1": "368/181-368/DAY13_2014-07-22_10-25-46/04_BoxA/TT1.ntt",
    "368_D13_boxA_CA1_2": "368/181-368/DAY13_2014-07-22_10-25-46/04_BoxA/TT2.ntt",
    "368_D13_boxA_CA2_1": "368/181-368/DAY13_2014-07-22_10-25-46/04_BoxA/TT3.ntt",
    "368_D13_boxA_CA3_1": "368/181-368/DAY13_2014-07-22_10-25-46/04_BoxA/TT4.ntt",
    "368_D13_boxA_CA1_3": "368/181-368/DAY13_2014-07-22_10-25-46/04_BoxA/TT5.ntt",
    "368_D13_boxA_CA1_4": "368/181-368/DAY13_2014-07-22_10-25-46/04_BoxA/TT6.ntt",
    "368_D13_boxA_CA1_5": "368/181-368/DAY13_2014-07-22_10-25-46/04_BoxA/TT7.ntt",
    "368_D13_boxA_CA1_6": "368/181-368/DAY13_2014-07-22_10-25-46/04_BoxA/TT8.ntt",
        # sleep2
    "368_D13_sleep2_CA1_1": "368/181-368/DAY13_2014-07-22_10-25-46/06_Sleep2/TT1.ntt",
    "368_D13_sleep2_CA1_2": "368/181-368/DAY13_2014-07-22_10-25-46/06_Sleep2/TT2.ntt",
    "368_D13_sleep2_CA2_1": "368/181-368/DAY13_2014-07-22_10-25-46/06_Sleep2/TT3.ntt",
    "368_D13_sleep2_CA3_1": "368/181-368/DAY13_2014-07-22_10-25-46/06_Sleep2/TT4.ntt",
    "368_D13_sleep2_CA1_3": "368/181-368/DAY13_2014-07-22_10-25-46/06_Sleep2/TT5.ntt",
    "368_D13_sleep2_CA1_4": "368/181-368/DAY13_2014-07-22_10-25-46/06_Sleep2/TT6.ntt",
    "368_D13_sleep2_CA1_5": "368/181-368/DAY13_2014-07-22_10-25-46/06_Sleep2/TT7.ntt",
    "368_D13_sleep2_CA1_6": "368/181-368/DAY13_2014-07-22_10-25-46/06_Sleep2/TT8.ntt",
        # Box C
    "368_D13_boxC_CA1_1": "368/181-368/DAY13_2014-07-22_10-25-46/08_BoxC/TT1.ntt",
    "368_D13_boxC_CA1_2": "368/181-368/DAY13_2014-07-22_10-25-46/08_BoxC/TT2.ntt",
    "368_D13_boxC_CA2_1": "368/181-368/DAY13_2014-07-22_10-25-46/08_BoxC/TT3.ntt",
    "368_D13_boxC_CA3_1": "368/181-368/DAY13_2014-07-22_10-25-46/08_BoxC/TT4.ntt",
    "368_D13_boxC_CA1_3": "368/181-368/DAY13_2014-07-22_10-25-46/08_BoxC/TT5.ntt",
    "368_D13_boxC_CA1_4": "368/181-368/DAY13_2014-07-22_10-25-46/08_BoxC/TT6.ntt",
    "368_D13_boxC_CA1_5": "368/181-368/DAY13_2014-07-22_10-25-46/08_BoxC/TT7.ntt",
    "368_D13_boxC_CA1_6": "368/181-368/DAY13_2014-07-22_10-25-46/08_BoxC/TT8.ntt",
        # sleep3
    "368_D13_sleep3_CA1_1": "368/181-368/DAY13_2014-07-22_10-25-46/10_Sleep3/TT1.ntt",
    "368_D13_sleep3_CA1_2": "368/181-368/DAY13_2014-07-22_10-25-46/10_Sleep3/TT2.ntt",
    "368_D13_sleep3_CA2_1": "368/181-368/DAY13_2014-07-22_10-25-46/10_Sleep3/TT3.ntt",
    "368_D13_sleep3_CA3_1": "368/181-368/DAY13_2014-07-22_10-25-46/10_Sleep3/TT4.ntt",
    "368_D13_sleep3_CA1_3": "368/181-368/DAY13_2014-07-22_10-25-46/10_Sleep3/TT5.ntt",
    "368_D13_sleep3_CA1_4": "368/181-368/DAY13_2014-07-22_10-25-46/10_Sleep3/TT6.ntt",
    "368_D13_sleep3_CA1_5": "368/181-368/DAY13_2014-07-22_10-25-46/10_Sleep3/TT7.ntt",
    "368_D13_sleep3_CA1_6": "368/181-368/DAY13_2014-07-22_10-25-46/10_Sleep3/TT8.ntt",
   
   

# animal 550
    # day 16
        # task
    "550_D16_t_CA1_1": "550/181-550/DAY16_2014-10-30_12-57-54/TT1.ntt",
    "550_D16_t_CA1_2": "550/181-550/DAY16_2014-10-30_12-57-54/TT2.ntt",
    "550_D16_t_CA2_1": "550/181-550/DAY16_2014-10-30_12-57-54/TT3.ntt",
    "550_D16_t_X_1": "550/181-550/DAY16_2014-10-30_12-57-54/TT4.ntt",
    "550_D16_t_CA1_3": "550/181-550/DAY16_2014-10-30_12-57-54/TT5.ntt",
    "550_D16_t_DEEP_1": "550/181-550/DAY16_2014-10-30_12-57-54/TT6.ntt",
    "550_D16_t_X_2": "550/181-550/DAY16_2014-10-30_12-57-54/TT7.ntt",
    "550_D16_t_X_3": "550/181-550/DAY16_2014-10-30_12-57-54/TT8.ntt",
        # sleep1
    "550_D16_sleep1_CA1_1": "550/181-550/DAY16_2014-10-30_12-57-54/02_Sleep1/TT1.ntt",
    "550_D16_sleep1_CA1_2": "550/181-550/DAY16_2014-10-30_12-57-54/02_Sleep1/TT2.ntt",
    "550_D16_sleep1_CA2_1": "550/181-550/DAY16_2014-10-30_12-57-54/02_Sleep1/TT3.ntt",
    "550_D16_sleep1_X_1": "550/181-550/DAY16_2014-10-30_12-57-54/02_Sleep1/TT4.ntt",
    "550_D16_sleep1_CA1_3": "550/181-550/DAY16_2014-10-30_12-57-54/02_Sleep1/TT5.ntt",
    "550_D16_sleep1_DEEP_1": "550/181-550/DAY16_2014-10-30_12-57-54/02_Sleep1/TT6.ntt",
    "550_D16_sleep1_X_2": "550/181-550/DAY16_2014-10-30_12-57-54/02_Sleep1/TT7.ntt",
    "550_D16_sleep1_X_3": "550/181-550/DAY16_2014-10-30_12-57-54/02_Sleep1/TT8.ntt",
        # cno
    "550_D16_cno_CA1_1": "550/181-550/DAY16_2014-10-30_12-57-54/04_CNO_2mgkg/TT1.ntt",
    "550_D16_cno_CA1_2": "550/181-550/DAY16_2014-10-30_12-57-54/04_CNO_2mgkg/TT2.ntt",
    "550_D16_cno_CA2_1": "550/181-550/DAY16_2014-10-30_12-57-54/04_CNO_2mgkg/TT3.ntt",
    "550_D16_cno_X_1": "550/181-550/DAY16_2014-10-30_12-57-54/04_CNO_2mgkg/TT4.ntt",
    "550_D16_cno_CA1_3": "550/181-550/DAY16_2014-10-30_12-57-54/04_CNO_2mgkg/TT5.ntt",
    "550_D16_cno_DEEP_1": "550/181-550/DAY16_2014-10-30_12-57-54/04_CNO_2mgkg/TT6.ntt",
    "550_D16_cno_X_2": "550/181-550/DAY16_2014-10-30_12-57-54/04_CNO_2mgkg/TT7.ntt",
    "550_D16_cno_X_3": "550/181-550/DAY16_2014-10-30_12-57-54/04_CNO_2mgkg/TT8.ntt",
        # LT1
    "550_D16_lt1_CA1_1": "550/181-550/DAY16_2014-10-30_12-57-54/06_LT1/TT1.ntt",
    "550_D16_lt1_CA1_2": "550/181-550/DAY16_2014-10-30_12-57-54/06_LT1/TT2.ntt",
    "550_D16_lt1_CA2_1": "550/181-550/DAY16_2014-10-30_12-57-54/06_LT1/TT3.ntt",
    "550_D16_lt1_X_1": "550/181-550/DAY16_2014-10-30_12-57-54/06_LT1/TT4.ntt",
    "550_D16_lt1_CA1_3": "550/181-550/DAY16_2014-10-30_12-57-54/06_LT1/TT5.ntt",
    "550_D16_lt1_DEEP_1": "550/181-550/DAY16_2014-10-30_12-57-54/06_LT1/TT6.ntt",
    "550_D16_lt1_X_2": "550/181-550/DAY16_2014-10-30_12-57-54/06_LT1/TT7.ntt",
    "550_D16_lt1_X_3": "550/181-550/DAY16_2014-10-30_12-57-54/06_LT1/TT8.ntt",
        # sleep2
    "550_D16_sleep2_CA1_1": "550/181-550/DAY16_2014-10-30_12-57-54/08_Sleep2/TT1.ntt",
    "550_D16_sleep2_CA1_2": "550/181-550/DAY16_2014-10-30_12-57-54/08_Sleep2/TT2.ntt",
    "550_D16_sleep2_CA2_1": "550/181-550/DAY16_2014-10-30_12-57-54/08_Sleep2/TT3.ntt",
    "550_D16_sleep2_X_1": "550/181-550/DAY16_2014-10-30_12-57-54/08_Sleep2/TT4.ntt",
    "550_D16_sleep2_CA1_3": "550/181-550/DAY16_2014-10-30_12-57-54/08_Sleep2/TT5.ntt",
    "550_D16_sleep2_DEEP_1": "550/181-550/DAY16_2014-10-30_12-57-54/08_Sleep2/TT6.ntt",
    "550_D16_sleep2_X_2": "550/181-550/DAY16_2014-10-30_12-57-54/08_Sleep2/TT7.ntt",
    "550_D16_sleep2_X_3": "550/181-550/DAY16_2014-10-30_12-57-54/08_Sleep2/TT8.ntt",



# animal 556
    # day 12
        # task
    "556_D12_t_CA2_1": "/cns/share/Vincent/McHugh_lab/CA2Cre_DREADD/556/181-556/DAY12_2014-10-27_14-32-58/TT1.ntt",
    "556_D12_t_CA1_1": "/cns/share/Vincent/McHugh_lab/CA2Cre_DREADD/556/181-556/DAY12_2014-10-27_14-32-58/TT2.ntt",
    "556_D12_t_CA2_2": "/cns/share/Vincent/McHugh_lab/CA2Cre_DREADD/556/181-556/DAY12_2014-10-27_14-32-58/TT3.ntt",
    "556_D12_t_DEEP_1": "/cns/share/Vincent/McHugh_lab/CA2Cre_DREADD/556/181-556/DAY12_2014-10-27_14-32-58/TT4.ntt",
    "556_D12_t_CA2_3": "/cns/share/Vincent/McHugh_lab/CA2Cre_DREADD/556/181-556/DAY12_2014-10-27_14-32-58/TT5.ntt",
    "556_D12_t_CA2_4": "/cns/share/Vincent/McHugh_lab/CA2Cre_DREADD/556/181-556/DAY12_2014-10-27_14-32-58/TT6.ntt",
    "556_D12_t_CA1_2": "/cns/share/Vincent/McHugh_lab/CA2Cre_DREADD/556/181-556/DAY12_2014-10-27_14-32-58/TT7.ntt",
    "556_D12_t_CA1_3": "/cns/share/Vincent/McHugh_lab/CA2Cre_DREADD/556/181-556/DAY12_2014-10-27_14-32-58/TT8.ntt"
    
    
    
    
    
    
#####################################################
################# CONTROL ###########################
    
    
    
# and the remaining animals
# and the control condition!!!
    }




all_files = [f for f in os.listdir("/cns/share/Vincent/McHugh_lab/analysis_results/numpy_spike_trains/")]
raw_data_directory = "/cns/share/Vincent/McHugh_lab/CA2Cre_DREADD/"

# Start the MATLAB engine
eng = matlab.engine.start_matlab()

# Add the path to the Neuralynx Matlab ImportExport toolbox
eng.addpath('/home/dekorvyb/Documents/criticality_pipeline/MatlabImportExport_v6.0.0', nargout=0)


#################################################
all_files = []

tetrode_files = {
# day 16
        # sleep1
        
    "144_D16_sleep1_CA1_1_pre": "144/DAY16_2014-05-29_10-40-02/02_Sleep1/TT1.ntt",
    "144_D16_sleep1_CA2_1_pre": "144/DAY16_2014-05-29_10-40-02/02_Sleep1/TT2.ntt",
    "144_D16_sleep1_CA1_2_pre": "144/DAY16_2014-05-29_10-40-02/02_Sleep1/TT5.ntt",
    "144_D16_sleep1_CA1_3_pre": "144/DAY16_2014-05-29_10-40-02/02_Sleep1/TT6.ntt",
    "144_D16_sleep1_CA2_2_pre": "144/DAY16_2014-05-29_10-40-02/02_Sleep1/TT8.ntt",
        # BoxA
    "144_D16_boxA_CA1_1_pre": "144/DAY16_2014-05-29_10-40-02/04_BoxA/TT1.ntt",
    "144_D16_boxA_CA2_1_pre": "144/DAY16_2014-05-29_10-40-02/04_BoxA/TT2.ntt",
    "144_D16_boxA_CA1_2_pre": "144/DAY16_2014-05-29_10-40-02/04_BoxA/TT5.ntt",
    "144_D16_boxA_CA1_3_pre": "144/DAY16_2014-05-29_10-40-02/04_BoxA/TT6.ntt",
    "144_D16_boxA_CA2_2_pre": "144/DAY16_2014-05-29_10-40-02/04_BoxA/TT8.ntt",
        #sleep2
    "144_D16_sleep2_CA1_1_pre": "144/DAY16_2014-05-29_10-40-02/06_Sleep2/TT1.ntt",
    "144_D16_sleep2_CA2_1_pre": "144/DAY16_2014-05-29_10-40-02/06_Sleep2/TT2.ntt",
    "144_D16_sleep2_CA1_2_pre": "144/DAY16_2014-05-29_10-40-02/06_Sleep2/TT5.ntt",
    "144_D16_sleep2_CA1_3_pre": "144/DAY16_2014-05-29_10-40-02/06_Sleep2/TT6.ntt",
    "144_D16_sleep2_CA2_2_pre": "144/DAY16_2014-05-29_10-40-02/06_Sleep2/TT8.ntt",
        # boxC
    "144_D16_boxC_CA1_1_post": "144/DAY16_2014-05-29_10-40-02/10_BoxC/TT1.ntt",
    "144_D16_boxC_CA2_1_post": "144/DAY16_2014-05-29_10-40-02/10_BoxC/TT2.ntt",
    "144_D16_boxC_CA1_2_post": "144/DAY16_2014-05-29_10-40-02/10_BoxC/TT5.ntt",
    "144_D16_boxC_CA1_3_post": "144/DAY16_2014-05-29_10-40-02/10_BoxC/TT6.ntt",
    "144_D16_boxC_CA2_2_post": "144/DAY16_2014-05-29_10-40-02/10_BoxC/TT8.ntt",
        # sleep 4
    "144_D16_sleep4_CA1_1_post": "144/DAY16_2014-05-29_10-40-02/12_Sleep4/TT1.ntt",
    "144_D16_sleep4_CA2_1_post": "144/DAY16_2014-05-29_10-40-02/12_Sleep4/TT2.ntt",
    "144_D16_sleep4_CA1_2_post": "144/DAY16_2014-05-29_10-40-02/12_Sleep4/TT5.ntt",
    "144_D16_sleep4_CA1_3_post": "144/DAY16_2014-05-29_10-40-02/12_Sleep4/TT6.ntt",
    "144_D16_sleep4_CA2_2_post": "144/DAY16_2014-05-29_10-40-02/12_Sleep4/TT8.ntt",
        # Box A2
    "144_D16_boxA2_CA1_1_post": "144/DAY16_2014-05-29_10-40-02/14_BoxA2/TT1.ntt",
    "144_D16_boxA2_CA2_1_post": "144/DAY16_2014-05-29_10-40-02/14_BoxA2/TT2.ntt",
    "144_D16_boxA2_CA1_2_post": "144/DAY16_2014-05-29_10-40-02/14_BoxA2/TT5.ntt",
    "144_D16_boxA2_CA1_3_post": "144/DAY16_2014-05-29_10-40-02/14_BoxA2/TT6.ntt",
    "144_D16_boxA2_CA2_2_post": "144/DAY16_2014-05-29_10-40-02/14_BoxA2/TT8.ntt",
        # sleep 5
    "144_D16_sleep5_CA1_1_post": "144/DAY16_2014-05-29_10-40-02/16_Sleep5/TT1.ntt",
    "144_D16_sleep5_CA2_1_post": "144/DAY16_2014-05-29_10-40-02/16_Sleep5TT2.ntt",
    "144_D16_sleep5_CA1_2_post": "144/DAY16_2014-05-29_10-40-02/16_Sleep5TT5.ntt",
    "144_D16_sleep5_CA1_3_post": "144/DAY16_2014-05-29_10-40-02/16_Sleep5TT6.ntt",
    "144_D16_sleep5_CA2_2_post": "144/DAY16_2014-05-29_10-40-02/16_Sleep5TT8.ntt"
        
    }
        
        
for tetrode in tetrode_files.keys():
    
    if f'{tetrode}.npy' in all_files:
        continue
    
    try:
        file_path = f'{raw_data_directory}{tetrode_files[tetrode]}'
        print("ANALYSING", tetrode)

        # Convert FieldSelectionFlags to MATLAB's double array format
        FieldSelectionFlags = matlab.double([1, 1, 1, 1, 1])  # This is essential for proper argument passing

        # Set HeaderExtractionFlag as a double (1 to extract header)
        HeaderExtractionFlag = matlab.double([1])

        # Use ExtractionMode 1 (Extract All Records)
        ExtractionMode = matlab.double([1])

        # Empty ExtractionModeVector as it's not needed for ExtractionMode 1 (set it as an empty matrix)
        ExtractionModeVector = matlab.double([])

        # Call the Nlx2MatSpike function

        timestamps_mat, ScNumbers, CellNumbers, Features, Samples, Header = eng.Nlx2MatSpike(
                file_path,
                FieldSelectionFlags,
                HeaderExtractionFlag,
                ExtractionMode,
                ExtractionModeVector,
                nargout=6
            )

        # Convert the MATLAB arrays to NumPy arrays
        timestamps = np.array(timestamps_mat)[0]
        print("extracted spike train")
        
        binned = tools.bin_timestamps(timestamps, unit = "us") # data unit according to https://neuralynx.com/_software/NeuralynxDataFileFormats.pdf
        # np.save(f'/cns/share/Vincent/McHugh_lab/analysis_results/test/{tetrode}', binned)
        print("binned and saved")
        # print(binned, len(binned), max(binned))
        
        
        tools.mr_estimator_for_prepared_epoch_data(binned, window_size = 90, bin_size = 5, filename = f'/cns/share/Vincent/McHugh_lab/analysis_results/test/{tetrode}', fit_func = "f_complex")
        
    except Exception as e:
        with open('/cns/share/Vincent/McHugh_lab/analysis_results/failed_analysis.txt', 'a') as f:
            f.write(f"{tetrode}\n")
        continue
        
eng.quit()



# %%
####################################
# Create linear Model
####################################

import os
import pandas as pd
import statsmodels.formula.api as smf

filepath = "/cns/share/Vincent/McHugh_lab/analysis_results/test/"
results = [f for f in os.listdir(filepath)]

big_df = []

for result in results:
    try:
        # Create a new DataFrame for each result file
        df = pd.DataFrame()

        # Extract the area (e.g., "CA1") from the filename
        area = result.split("_")[3] 
        state = result.split("_")[2][:-1]
        cno = result.split("_")[-1][:-11]

        # Read the "beta" column from the parquet file
        tau = pd.read_parquet(f"{filepath}{result}")["tau"].values[0]
        
        file_data = {
                    "tau": tau,
                    "area": str(area),
                    "state": str(state),
                    "cno": str(cno)
                }
        big_df.append(file_data)
        
    except:
        continue
    
    '''
    df["tau"] = tau
    
    # Add the 'area' as a new column
    df["area"] = str(area)

    print(df)
    # Append this DataFrame to the list
    big_df.append(df)
    '''
    
combined_df = pd.DataFrame(big_df)
    
combined_df = combined_df.dropna()
print(combined_df)

formula = "tau ~ area * state * cno"

# Fit the linear model using Ordinary Least Squares (OLS)
model = smf.ols(formula=formula, data=combined_df).fit()

# Print the summary of the model
print(model.summary())

# %%