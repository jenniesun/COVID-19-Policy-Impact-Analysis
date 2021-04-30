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
# treatment - NC
daily_cases_NC = daily_cases[daily_cases["state"] == "North Carolina"]
# control - VA, GA, SC
daily_cases_VA = daily_cases[daily_cases["state"] == "Virginia"]
daily_cases_GA = daily_cases[daily_cases["state"] == "Georgia"]
daily_cases_SC = daily_cases[daily_cases["state"] == "South Carolina"]

# load population data
pop =  pd.read_excel("./co-est2019-annres.xlsx",  header=[0,1,2,3])
pop.columns = pop.columns.droplevel([0,1,2])
pop.rename(columns={"Unnamed: 0_level_3": "Geographic Area"}, inplace = True)
pop["Geographic Area"] = pop["Geographic Area"].str.replace('.','', regex=True)

# subset population data to NC
pop_NC = pop[pop['Geographic Area'].str.contains("North Carolina")]
# use 2019 population
pop_NC = pop_NC.iloc[:, [0] + [-1]]
# rename county column
pop_NC['Geographic Area'] = pop_NC['Geographic Area'].str.replace(' County, North Carolina', '')
# rename dataframe columnes
pop_NC.columns = ['County', 'population']

# subset population data to VA
pop_VA = pop[pop['Geographic Area'].str.contains(", Virginia")]
pop_VA = pop_VA.iloc[:-1]
# use 2019 population
pop_VA = pop_VA.iloc[:, [0] + [-1]]
# rename county column
pop_VA['Geographic Area'] = pop_VA['Geographic Area'].str.replace(' County, Virginia', '')
pop_VA['Geographic Area'] = pop_VA['Geographic Area'].str.replace(', Virginia', '')
# rename dataframe columnes
pop_VA.columns = ['County', 'population']

# subset population data to GA
pop_GA = pop[pop['Geographic Area'].str.contains("Georgia")]
# use 2019 population
pop_GA = pop_GA.iloc[:, [0] + [-1]]
# rename county column
pop_GA['Geographic Area'] = pop_GA['Geographic Area'].str.replace(' County, Georgia', '')
# rename dataframe columnes
pop_GA.columns = ['County', 'population']

# subset population data to SC
pop_SC = pop[pop['Geographic Area'].str.contains("South Carolina")]
# use 2019 population
pop_SC = pop_SC.iloc[:, [0] + [-1]]
# rename county column
pop_SC['Geographic Area'] = pop_SC['Geographic Area'].str.replace(' County, South Carolina', '')
# rename dataframe columnes
pop_SC.columns = ['County', 'population']

# remove uknown counties
daily_cases_NC = daily_cases_NC[daily_cases_NC['county']!='Unknown']
daily_cases_GA = daily_cases_GA[daily_cases_GA['county']!='Unknown']
daily_cases_SC = daily_cases_SC[daily_cases_SC['county']!='Unknown']
daily_cases_VA = daily_cases_VA[daily_cases_VA['county']!='Unknown']

# set comparison period to be 21 days
numdays = 21

# retrieve policy date for NC Stay at Home Order
policy_nc = datetime.datetime.strptime('27032020', "%d%m%Y").date()
date_before_nc = [policy_nc - datetime.timedelta(days=x) for x in range(numdays+1)]
date_after_nc = [policy_nc + datetime.timedelta(days=x) for x in range(numdays+1)]
date_list_nc = date_before_nc + date_after_nc

# data cleaning - treatment state: NC
daily_nc = daily_cases_NC.copy()
daily_nc["date"] = pd.to_datetime(daily_nc["date"])
daily_nc_timed = daily_nc.loc[daily_nc["date"].isin(date_list_nc)] # covering a total of 43 days (21 + 21 + 1)

# merge NC population with COVID cases
merged_NC = pd.merge(left=daily_nc_timed, right=pop_NC, how='left', left_on='county', right_on='County')

# drop duplicated NC County column
merged_NC = merged_NC.drop('County', axis=1)
# create NC standardized COVID cases column
merged_NC['cases_standardized'] = merged_NC['cases']/merged_NC['population']*10000

# create indicator variable - pre and post policy annoucement
merged_NC['post_policy'] = (merged_NC.date > '2020-03-27')


# data cleaning - control state: VA
daily_va = daily_cases_VA.copy()
daily_va["date"] = pd.to_datetime(daily_va["date"])
daily_va_timed = daily_va.loc[daily_va["date"].isin(date_list_nc)]

# merge VA population with COVID cases
merged_VA = pd.merge(left=daily_va_timed, right=pop_VA, how='left', left_on='county', right_on='County')

# drop duplicated VA County column
merged_VA = merged_VA.drop('County', axis=1)
# create VA standardized COVID cases column
merged_VA['cases_standardized'] = merged_VA['cases']/merged_VA['population']*10000

# create indicator variable - pre and post policy annoucement
merged_VA['post_policy'] = (merged_VA.date > '2020-03-27')

# data cleaning - control state: GA
daily_ga = daily_cases_GA.copy()
daily_ga["date"] = pd.to_datetime(daily_ga["date"])
daily_ga_timed = daily_ga.loc[daily_ga["date"].isin(date_list_nc)]

# merge GA population with COVID cases
merged_GA = pd.merge(left=daily_ga_timed, right=pop_GA, how='left', left_on='county', right_on='County')

# drop duplicated GA County column
merged_GA = merged_GA.drop('County', axis=1)
# create GA standardized COVID cases column
merged_GA['cases_standardized'] = merged_GA['cases']/merged_GA['population']*10000

# create indicator variable - pre and post policy annoucement
merged_GA['post_policy'] = (merged_GA.date > '2020-03-27')

# data cleaning - control state: SC
daily_sc = daily_cases_SC.copy()
daily_sc["date"] = pd.to_datetime(daily_sc["date"])
daily_sc_timed = daily_sc.loc[daily_sc["date"].isin(date_list_nc)]

# merge SC population with COVID cases
merged_SC = pd.merge(left=daily_sc_timed, right=pop_SC, how='left', left_on='county', right_on='County')

# drop duplicated SC County column
merged_SC = merged_SC.drop('County', axis=1)
# create SC standardized COVID cases column
merged_SC['cases_standardized'] = merged_SC['cases']/merged_SC['population']*10000

# create indicator variable - pre and post policy annoucement
merged_SC['post_policy'] = (merged_SC.date > '2020-03-27')

# stack 3 control states
merged_control = merged_VA.append([merged_GA, merged_SC])

# pre-post plot - NC
(ggplot() +
    geom_smooth(merged_NC[merged_NC['date'] < '2020-03-27'],
                aes(x='date', y='cases_standardized', color='post_policy'), method='lowess') +
    geom_smooth(merged_NC[merged_NC['date'] > '2020-03-27'],
                aes(x='date', y='cases_standardized', color='post_policy'), method='lowess')
    + xlab('Before/after NC Stay-At-Home Order (Mar 27, 2020)')
    + ylab(str("cases standardized") + ' \n(Adding 95% confidence interval)')
    + geom_vline(xintercept = '2020-03-27')
    + labs(title=str("Pre Post Plot - North Carolina")))
    
# pre-post plot - control States (VA, GA, SC)
(ggplot() +
    geom_smooth(merged_control[merged_control['date'] < '2020-03-27'],
                aes(x='date', y='cases_standardized', color='post_policy'), method='lowess') +
    geom_smooth(merged_control[merged_control['date'] > '2020-03-27'],
                aes(x='date', y='cases_standardized', color='post_policy'), method='lowess')
    + xlab('Before/after NC Stay-At-Home Order (Mar 27, 2020)')
    + ylab(str("cases standardized") + ' \n(Adding 95% confidence interval)')
    + geom_vline(xintercept = '2020-03-27')
    + labs(title=str("Pre Post Plot - Control States (VA, GA, SC)")))

# diff-in-diff plot - NC vs control States
(ggplot() +
    geom_smooth(merged_NC[merged_NC['date'] < '2020-03-27'],
                aes(x='date', y='cases_standardized', color='state'), method='lowess') +
    geom_smooth(merged_NC[merged_NC['date'] > '2020-03-27'],
                aes(x='date', y='cases_standardized', color='state'), method='lowess') +
        
    geom_smooth(merged_control[merged_control['date'] < '2020-03-27'],
                aes(x='date', y='cases_standardized', color='state'), method='lowess') +
    geom_smooth(merged_control[merged_control['date'] > '2020-03-27'],
                aes(x='date', y='cases_standardized', color='state'), method='lowess')
    + geom_vline(xintercept = '2020-03-27')
    + xlab('Before/after NC Stay-At-Home Order (Mar 27, 2020)')
    + ylab(str("number of COVID-19 Cases per 10,000") + ' \n(Adding 95% confidence interval)')
    + labs(title=str("Difference in Difference Plot - North Carolina vs Control States (VA, GA, SC)")))
    
# create indicator variable for treatment and control state
merged_NC['State'] = "North Carolina"
merged_control['State'] = "Control States"

# diff-in-diff plot - NC vs control counties
(ggplot() +
    geom_smooth(merged_control[merged_control['date'] < '2020-03-27'],
                aes(x='date', y='cases_standardized', color='State'), method='lowess') +
    geom_smooth(merged_control[merged_control['date'] > '2020-03-27'],
                aes(x='date', y='cases_standardized', color='State'), method='lowess') +
    geom_smooth(merged_NC[merged_NC['date'] < '2020-03-27'],
                aes(x='date', y='cases_standardized', color='State'), method='lowess') +
    geom_smooth(merged_NC[merged_NC['date'] > '2020-03-27'],
                aes(x='date', y='cases_standardized', color='State'), method='lowess')
    + geom_vline(xintercept = '2020-03-27')
    + xlab('Before/after NC Stay-At-Home Order (Mar 27, 2020)')
    + ylab(str("number of COVID-19 Cases per 10,000") + ' \n(Adding 95% confidence interval)')
    + labs(title=str("Difference in Difference Plot - North Carolina vs Control States (VA, GA, SC)")))
