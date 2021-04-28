%load_ext nb_black
%config InlineBackend.figure_format = 'retina'
import pandas as pd
import datetime
import os
import sys
from plotnine import *
import warnings
warnings.filterwarnings("ignore")

# load data for covid cases
daily_cases = pd.read_csv("./data/us-counties-covid-cases.csv")
# treatment - MO
daily_cases_MO = daily_cases[daily_cases["state"] == "Missouri"]
# control - NE, IA, AR
daily_cases_NE = daily_cases[daily_cases["state"] == "Nebraska"]
daily_cases_IA = daily_cases[daily_cases["state"] == "Iowa"]
daily_cases_AR = daily_cases[daily_cases["state"] == "Arkansas"]

# load population data
pop =  pd.read_excel("./co-est2019-annres.xlsx",  header=[0,1,2,3])
pop.columns = pop.columns.droplevel([0,1,2])
pop.rename(columns={"Unnamed: 0_level_3": "Geographic Area"}, inplace = True)
pop["Geographic Area"] = pop["Geographic Area"].str.replace('.','', regex=True)

# subset population data to MO
pop_MO = pop[pop['Geographic Area'].str.endswith("Missouri")]
# use 2019 population
pop_MO = pop_MO.iloc[:, [0] + [-1]]
# rename county column
pop_MO['Geographic Area'] = pop_MO['Geographic Area'].str.replace(' County, Missouri', '')
pop_MO['Geographic Area'] = pop_MO['Geographic Area'].str.replace(', Missouri', '')
# rename county in daily cases dataframe to ensure naming consistency
daily_cases_MO['county'] = daily_cases_MO['county'].str.replace('.', '')
# drop counties where there is no population data
daily_cases_MO = daily_cases_MO[(daily_cases_MO['county'] != 'Joplin') & (daily_cases_MO['county'] != 'Kansas City')]
# rename dataframe columnes
pop_MO.columns = ['County', 'population']

# subset population data to NE
pop_NE = pop[pop['Geographic Area'].str.endswith(", Nebraska")]
pop_NE = pop_NE.iloc[:-1]
# use 2019 population
pop_NE = pop_NE.iloc[:, [0] + [-1]]
# rename county column
pop_NE['Geographic Area'] = pop_NE['Geographic Area'].str.replace(' County, Nebraska', '')
# drop counties where there is no population data
daily_cases_NE = daily_cases_NE[daily_cases_NE['county'] != 'York']
# rename dataframe columnes
pop_NE.columns = ['County', 'population']

# subset population data to IA
pop_IA = pop[pop['Geographic Area'].str.endswith("Iowa")]
# use 2019 population
pop_IA = pop_IA.iloc[:, [0] + [-1]]
# rename county column
pop_IA['Geographic Area'] = pop_IA['Geographic Area'].str.replace(' County, Iowa', '')
# rename dataframe columnes
pop_IA.columns = ['County', 'population']

# subset population data to AR
pop_AR = pop[pop['Geographic Area'].str.endswith("Arkansas")]
# use 2019 population
pop_AR = pop_AR.iloc[:, [0] + [-1]]
# rename county column
pop_AR['Geographic Area'] = pop_AR['Geographic Area'].str.replace(' County, Arkansas', '')
# rename county in daily cases dataframe to ensure naming consistency
daily_cases_AR['county'] = daily_cases_AR['county'].str.replace('.', '')
# rename dataframe columnes
pop_AR.columns = ['County', 'population']

# remove uknown counties
daily_cases_MO = daily_cases_MO[daily_cases_MO['county']!='Unknown']
daily_cases_NE = daily_cases_NE[daily_cases_NE['county']!='Unknown']
daily_cases_IA = daily_cases_IA[daily_cases_IA['county']!='Unknown']
daily_cases_AR = daily_cases_AR[daily_cases_AR['county']!='Unknown']

# make sure counties are matching in COVID cases & population datasets
sorted(pop_MO.County.unique()) == sorted(daily_cases_MO.county.unique())
sorted(pop_NE.County.unique()) == sorted(daily_cases_NE.county.unique())
sorted(pop_IA.County.unique()) == sorted(daily_cases_IA.county.unique())
sorted(pop_AR.County.unique()) == sorted(daily_cases_AR.county.unique())

# set comparison period to be 21 days
numdays = 21

# retrieve policy date for MO Stay at Home Order
policy_mo = datetime.datetime.strptime('06042020', "%d%m%Y").date()
date_before_mo = [policy_mo - datetime.timedelta(days=x) for x in range(numdays+1)]
date_after_mo = [policy_mo + datetime.timedelta(days=x) for x in range(numdays+1)]
date_list_mo = date_before_mo + date_after_mo


# data cleaning - treatment state: MO
daily_mo = daily_cases_MO.copy()
daily_mo["date"] = pd.to_datetime(daily_mo["date"])
daily_mo_timed = daily_mo.loc[daily_mo["date"].isin(date_list_mo)] # covering a total of 43 days (21 + 21 + 1)

# merge MO population with COVID cases
merged_MO = pd.merge(left=daily_mo_timed, right=pop_MO, how='left', left_on='county', right_on='County')

# drop duplicated MO County column
merged_MO = merged_MO.drop('County', axis=1)
# create MO standardized COVID cases column
merged_MO['cases_standardized'] = merged_MO['cases']/merged_MO['population']*10000

# create indicator variable - pre and post policy annoucement
merged_MO['post_policy'] = (merged_MO.date > '2020-04-06')


# data cleaning - control state: NE
daily_ne = daily_cases_NE.copy()
daily_ne["date"] = pd.to_datetime(daily_ne["date"])
daily_ne_timed = daily_ne.loc[daily_ne["date"].isin(date_list_mo)]

# merge NE population with COVID cases
merged_NE = pd.merge(left=daily_ne_timed, right=pop_NE, how='left', left_on='county', right_on='County')

# drop duplicated NE County column
merged_NE = merged_NE.drop('County', axis=1)
# create NE standardized COVID cases column
merged_NE['cases_standardized'] = merged_NE['cases']/merged_NE['population']*10000

# create indicator variable - pre and post policy annoucement
merged_NE['post_policy'] = (merged_NE.date > '2020-04-06')


# data cleaning - control state: IA
daily_ia = daily_cases_IA.copy()
daily_ia["date"] = pd.to_datetime(daily_ia["date"])
daily_ia_timed = daily_ia.loc[daily_ia["date"].isin(date_list_mo)]

# merge IA population with COVID cases
merged_IA = pd.merge(left=daily_ia_timed, right=pop_IA, how='left', left_on='county', right_on='County')

# drop duplicated IA County column
merged_IA = merged_IA.drop('County', axis=1)
# create IA standardized COVID cases column
merged_IA['cases_standardized'] = merged_IA['cases']/merged_IA['population']*10000

# create indicator variable - pre and post policy annoucement
merged_IA['post_policy'] = (merged_IA.date > '2020-04-06')


# data cleaning - control state: AR
daily_ar = daily_cases_AR.copy()
daily_ar["date"] = pd.to_datetime(daily_ar["date"])
daily_ar_timed = daily_ar.loc[daily_ar["date"].isin(date_list_mo)]

# merge AR population with COVID cases
merged_AR = pd.merge(left=daily_ar_timed, right=pop_AR, how='left', left_on='county', right_on='County')

# drop duplicated AR County column
merged_AR = merged_AR.drop('County', axis=1)
# create AR standardized COVID cases column
merged_AR['cases_standardized'] = merged_AR['cases']/merged_AR['population']*10000

# create indicator variable - pre and post policy annoucement
merged_AR['post_policy'] = (merged_AR.date > '2020-04-06')


# stack 3 control states
merged_control = merged_NE.append([merged_IA, merged_AR])

# pre-post plot - MO
(ggplot() +
    geom_smooth(merged_MO[merged_MO['date'] < '2020-04-06'],
                aes(x='date', y='cases_standardized', color='post_policy'), method='lowess') +
    geom_smooth(merged_MO[merged_MO['date'] > '2020-04-06'],
                aes(x='date', y='cases_standardized', color='post_policy'), method='lowess')
    + xlab('Before/after MO Stay-At-Home Order (April 6, 2020)')
    + ylab(str("cases standardized") + ' \n(Adding 95% confidence interval)')
    + geom_vline(xintercept = '2020-04-06')
    + labs(title=str("Pre Post Plot - Missouri")))
    
# pre-post plot - control States (NE, IA, AR)
(ggplot() +
    geom_smooth(merged_control[merged_control['date'] < '2020-04-06'],
                aes(x='date', y='cases_standardized', color='post_policy'), method='lowess') +
    geom_smooth(merged_control[merged_control['date'] > '2020-04-06'],
                aes(x='date', y='cases_standardized', color='post_policy'), method='lowess')
    + xlab('Before/after MO Stay-At-Home Order (April 6, 2020)')
    + ylab(str("cases standardized") + ' \n(Adding 95% confidence interval)')
    + geom_vline(xintercept = '2020-04-06')
    + labs(title=str("Pre Post Plot - Control States (NE, IA, AR)")))
    
# diff-in-diff plot - MO vs control States
(ggplot() +
    geom_smooth(merged_MO[merged_MO['date'] < '2020-04-06'],
                aes(x='date', y='cases_standardized', color='state'), method='lowess') +
    geom_smooth(merged_MO[merged_MO['date'] > '2020-04-06'],
                aes(x='date', y='cases_standardized', color='state'), method='lowess') +
        
    geom_smooth(merged_control[merged_control['date'] < '2020-04-06'],
                aes(x='date', y='cases_standardized', color='state'), method='lowess') +
    geom_smooth(merged_control[merged_control['date'] > '2020-04-06'],
                aes(x='date', y='cases_standardized', color='state'), method='lowess')
    + geom_vline(xintercept = '2020-04-06')
    + xlab('Before/after MO Stay-At-Home Order (April 6, 2020)')
    + ylab(str("number of COVID-19 Cases per 10,000") + ' \n(Adding 95% confidence interval)')
    + labs(title=str("Difference in Difference Plot - Missouri vs Control States (NE, IA, AR)")))

# create indicator variable for treatment and control state
merged_MO['State'] = "Missouri"
merged_control['State'] = "Control States"


# diff-in-diff plot - MO vs control counties
(ggplot() +
    geom_smooth(merged_control[merged_control['date'] < '2020-04-06'],
                aes(x='date', y='cases_standardized', color='State'), method='lowess') +
    geom_smooth(merged_control[merged_control['date'] > '2020-04-06'],
                aes(x='date', y='cases_standardized', color='State'), method='lowess') +
    geom_smooth(merged_MO[merged_MO['date'] < '2020-04-06'],
                aes(x='date', y='cases_standardized', color='State'), method='lowess') +
    geom_smooth(merged_MO[merged_MO['date'] > '2020-04-06'],
                aes(x='date', y='cases_standardized', color='State'), method='lowess')
    + geom_vline(xintercept = '2020-04-06')
    + xlab('Before/after MO Stay-At-Home Order (April 6, 2020)')
    + ylab(str("number of COVID-19 Cases per 10,000") + ' \n(Adding 95% confidence interval)')
    + labs(title=str("Difference in Difference Plot - Missouri vs Control States (NE, IA, AR)")))
