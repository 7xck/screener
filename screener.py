import pandas as pd
import numpy as np
import statistics as stat
from scipy import stats
import random

CSV_NAME = input(str("What is the name of the .csv? (of the form 'xxx.csv')> "))
YEARS = [int(x) for x in input("What is the last digit of each year that you have data on? i.e. if you have data for the years 2014, 2015, 2016, 2017 you would enter 14 15 16 17> ").split()]
DATA = pd.read_csv(CSV_NAME)

for i in DATA.columns:
    DATA = DATA[~DATA[i].isin(['n.a.'])]
for i in DATA.columns:
    DATA = DATA[~DATA[i].isin(['n.s.'])]
DATA = DATA.drop(columns=['Mark'])
for i in DATA.columns:
    DATA[str(i)] = DATA[str(i)].str.replace('[\,]', '')

def rocs(data, YEARS):
    companies = data.iloc[:, 0]
    for j in YEARS:
        rocs = []
        for i in companies:
            x = data[data['Company name'] == str(i)]
            a = float(x['EBIT th USD 20' + str(j)])
            b = float(x['Capital th USD 20' + str(j)])
            z = (a/b)
            rocs.append(z)
        data['ROC 20' + str(j)] = rocs
    return data
def eight_year_average_roa(data, years):
    companies = data.iloc[:, 0]
    list_of_years = []
    average_roa = []
    for i in years[::-1]:
        list_of_years.append(i)
    for j in companies:
        iterable = []
        x = data[data['Company name'] == str(j)]
        for i in list_of_years:
            iterable.append(1+(float(x['ROA using Net income % 20' + str(i)])/100))
        x = np.prod(iterable)
        x = ((x**(1/8))-1)
        average_roa.append(x) 
    data['ROA, 8yr GEO Average'] = average_roa
def eight_year_average_roc(data, years):
    companies = data.iloc[:, 0]
    list_of_years = []
    average_roc= []
    for i in years[::-1]:
        list_of_years.append(i)
    for j in companies:
        iterable = []
        x = data[data['Company name'] == str(j)]
        for i in list_of_years:
            iterable.append(1+(float(x['ROC 20' + str(i)])))
        x = np.prod(iterable)
        x = ((x**(1/8))-1)
        average_roc.append(x) 
    data['ROC, 8yr GEO Average'] = average_roc
def margin_growth(data, years):
    companies = data.iloc[:, 0]
    for i in years[::-1]:
        if i == years[0]:
            break
        margin_growth = []
        for j in companies:
            margin_differences = []
            iterable = []
            x = data[data['Company name'] == str(j)]
            a = float(x['Gross margin % 20' + str(i)])
            b = float(x['Gross margin % 20' + str(i-1)])
            z = (a/100)-(b/100)
            margin_differences.append(z)
            for x in margin_differences:
                y = 1+float(x) 
                iterable.append(y)
            x = np.prod(iterable)
            x = ((x**(1/8))-1)
            margin_growth.append(x*100) 
    data['Margin Growth'] = margin_growth
def margin_stability(data, years):
    companies = data.iloc[:, 0]
    for i in years[::-1]:
        if i == years[0]:
            break
        margin_stability = []
        for j in companies:
            list = []
            for i in years:
                x = (data[data['Company name'] == str(j)])
                list.append(float(x['Gross margin % 20' + str(i)])/100)
            average = stat.mean(list)
            pstdev = stat.pstdev(list)
            margin_stability.append(average/pstdev)
    data['Margin Stability'] = margin_stability
def percentile_calculator_fourth(data, years):
    fp_list = data['Franchise Power'].tolist()
    companies = data.iloc[:, 0]
    fp_percentiles = []
    for j in companies:
        company_data = (data[data['Company name'] == str(j)])
        fp = float(company_data['Franchise Power'])
        percentile_FP = stats.percentileofscore(fp_list, fp)
        fp_percentiles.append(percentile_FP)
    data['Percentile FP'] = fp_percentiles
def percentile_calculator_second(data, years):
    roc_eightyr = data['ROC, 8yr GEO Average'].tolist()
    roa_eightyr = data['ROA, 8yr GEO Average'].tolist()
    companies = data.iloc[:, 0]
    roa_list_percentiles = []
    roc_list_percentiles = []
    for j in companies:
        company_data = (data[data['Company name'] == str(j)])
        roa = float(company_data['ROA, 8yr GEO Average'])
        roc = float(company_data['ROC, 8yr GEO Average'])
        percentile_roa = stats.percentileofscore(roa_eightyr, roa)
        percentile_roc = stats.percentileofscore(roc_eightyr, roc)
        roa_list_percentiles.append(percentile_roa)
        roc_list_percentiles.append(percentile_roc)
    data['Percentile Geo Average ROC'] = roc_list_percentiles
    data['Percentile Geo Average ROA'] = roa_list_percentiles
def percentile_calculator_third(data, years):
    fcfa_list = data['FCFA'].tolist()
    companies = data.iloc[:, 0]
    fcfa_percentiles = []    
    for j in companies:
        company_data = (data[data['Company name'] == str(j)])
        fcfa = float(company_data['FCFA'])
        percentile_FCFA = stats.percentileofscore(fcfa_list, fcfa)
        fcfa_percentiles.append(percentile_FCFA)
    data['Percentile FCFA'] = fcfa_percentiles
def percentile_calculator_first(data, years):
    margin_stability_list = data['Margin Stability'].tolist()
    margin_growth_list = data['Margin Growth'].tolist()
    companies = data.iloc[:, 0]
    stab_list_percentiles = []
    growth_list_percentiles = []
    for j in companies:
        company_data = (data[data['Company name'] == str(j)])
        marg_stab = float(company_data['Margin Stability'])
        marg_growth = float(company_data['Margin Growth'])
        percentile_stab = stats.percentileofscore(margin_stability_list, marg_stab)
        percentile_growth = stats.percentileofscore(margin_growth_list, marg_growth)
        stab_list_percentiles.append(percentile_stab)
        growth_list_percentiles.append(percentile_growth)
    data['Percentile Margin Stability'] = stab_list_percentiles
    data['Percentile Margin Growth'] = growth_list_percentiles
def margin_max(data, years):
    companies = data.iloc[:, 0]
    list = []
    for j in companies:
        company_data = (data[data['Company name'] == str(j)])
        stab_percentile = float(company_data['Percentile Margin Stability'])
        growth_percentile = float(company_data['Percentile Margin Growth'])
        if stab_percentile > growth_percentile:
             list.append(stab_percentile)
        elif stab_percentile < growth_percentile:
            list.append(growth_percentile)
        else:
            # they're equal so it doesn't matter which one you choose
            list.append(stab_percentile)
    data['Margin Max'] = list
def FCFA(data, years):
    companies = data.iloc[:, 0]
    list = []
    summing = []
    for i in companies:
        company_data = (data[data['Company name'] == str(i)])
        for j in years:
            x = company_data['Free cash flow th USD 20' + str(j)]
            summing.append(float(x))
        y = sum(summing) / float(company_data['Total Assets th USD 2019'])
        list.append(y)
    data['FCFA'] = list
def franchisepower(data):
    companies = data.iloc[:,0]
    list = []
    for i in companies:
        company_data = (data[data['Company name'] == str(i)])
        p_roa = float(company_data['Percentile Geo Average ROA'])
        p_roc = float(company_data['Percentile Geo Average ROC'])
        p_fcfa = float(company_data['Percentile FCFA'])
        mm = float(company_data['Margin Max'])
        x = stat.mean([p_roa, p_roc, p_fcfa, mm])
        list.append(x)
    data['Franchise Power'] = list
def current_profitability(data, years_list):
    companies = data.iloc[:, 0]
    years = years_list[::-1]
    years = [str(i) for i in years]
    roa_list = []
    fcfta=[]
    accrual=[]
    lever=[]
    liquid=[]
    delta_roa=[]
    delta_fcfta =[]
    delta_margin = []
    delta_turnover = []
    p_fs = []
    for i in companies:
        company_data = (data[data['Company name'] == str(i)])
        #FS_ROA
        FS_ROA = float(company_data['ROA using Net income % 20' + years[0]])
        FCFTA = float(company_data['Free cash flow th USD 20' + years[0]]) / float(company_data['Total Assets th USD 20' + years[0]])
        ACCRUAL = FCFTA - float(company_data['ROA using Net income % 20' + years[0]])
        LEVER = (float(company_data['Long Term Debt th USD 20' + years[1]]) / float(company_data['Total Assets th USD 20' + years[1]])) / (float(company_data['Long Term Debt th USD 20' + years[0]]) / float(company_data['Total Assets th USD 20' + years[0]]))
        LIQUID = float(company_data['Current Ratio (%) % 20' + years[0]]) - float(company_data['Current Ratio (%) % 20' + years[1]])
        DELTA_ROA = float(company_data['ROA using Net income % 20' + years[0]]) - float(company_data['ROA using Net income % 20' + years[1]])
        DELTA_FCFTA = (float(company_data['Free cash flow th USD 20' + years[0]]) / float(company_data['Total Assets th USD 20' + years[0]])) - (float(company_data['Free cash flow th USD 20' + years[1]]) / float(company_data['Total Assets th USD 20' + years[1]]))
        DELTA_MARGIN = float(company_data['Gross margin % 20' + years[0]]) - float(company_data['Gross margin % 20' + years[1]])
        DELTA_TURNOVER = float(company_data['Net assets turnover 20' + years[0]]) - float(company_data['Net assets turnover 20' + years[1]])
        if FS_ROA > 0:
            FS_ROA = 1
        else:
            FS_ROA = 0
        roa_list.append(FS_ROA)
        if FCFTA > 0:
            FCFTA = 1
        else:
            FCFTA = 0
        fcfta.append(FCFTA)
        if ACCRUAL > 0:
            ACCRUAL = 1
        else:
            ACCRUAL = 0
        accrual.append(ACCRUAL)
        if LEVER > 0:
            LEVER = 1
        else:
            LEVER = 0
        lever.append(LEVER)
        if LIQUID > 0:
            LIQUID = 1
        else:
            LIQUID = 0
        liquid.append(LIQUID)
        if DELTA_ROA > 0:
            DELTA_ROA = 1
        else:
            DELTA_ROA = 0
        delta_roa.append(DELTA_ROA)
        if DELTA_FCFTA > 0:
            DELTA_FCFTA = 1
        else:
            DELTA_FCFTA = 0
        delta_fcfta.append(DELTA_FCFTA)
        if DELTA_TURNOVER > 0:
            DELTA_TURNOVER = 1
        else:
            DELTA_TURNOVER= 0
        delta_turnover.append(DELTA_TURNOVER)
        if DELTA_MARGIN > 0:
            DELTA_MARGIN = 1
        else:
            DELTA_MARGIN = 0
        delta_margin.append(DELTA_MARGIN)
        P_FS = (DELTA_MARGIN+ DELTA_TURNOVER+ DELTA_FCFTA+ LIQUID+ DELTA_ROA+ LEVER+ ACCRUAL+ FS_ROA+ FCFTA)
        p_fs.append(P_FS)
    data['DELTA MARGIN'] = delta_margin
    data['DELTA TURNOVER'] = delta_turnover
    data['DELTA FCFTA'] = delta_fcfta
    data['LIQUID'] = liquid
    data['DELTA ROA'] = delta_roa
    data['LEVER'] = lever
    data['ACCRUAL'] = accrual
    data['FS ROA'] = roa_list
    data['FCFTA'] = fcfta
    data['P_FS'] = p_fs

rocs(DATA, YEARS)
eight_year_average_roa(DATA, YEARS)
eight_year_average_roc(DATA, YEARS)
margin_growth(DATA, YEARS)

DATA = DATA[~DATA['Margin Growth'].isin([0])]
DATA = DATA[~DATA['Margin Growth'].isin(['NaN'])]

margin_stability(DATA, YEARS)
percentile_calculator_first(DATA, YEARS)
FCFA(DATA, YEARS)
percentile_calculator_second(DATA, YEARS)
percentile_calculator_third(DATA, YEARS)
margin_max(DATA, YEARS)
franchisepower(DATA)
percentile_calculator_fourth(DATA, YEARS)
current_profitability(DATA, YEARS)

companies = DATA.iloc[:, 0]
list = []
for i in companies:
    company_data = (DATA[DATA['Company name'] == str(i)])
    QUALITY = 0.5*float((company_data['P_FS'])) + 0.5*float(company_data['Percentile FP'])
    list.append(QUALITY)
DATA['QUALITY'] = list
print(DATA.sort_values(by=['QUALITY']))