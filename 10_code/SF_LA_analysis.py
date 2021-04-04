import pandas as pd 
import datetime

###### read in data ###### 
###### ###### ###### #####

daily_cases = pd.read_csv("../00_source_data/us-counties.csv")
daily_cases.head()


##### subset county and 3 week span #####
#########################################

### SF ###
##########
# policy date for shelter in place
numdays = 21
sf_policy = datetime.datetime.strptime('16032020', "%d%m%Y").date()
date_before = [sf_policy - datetime.timedelta(days=x) for x in range(numdays+1)]
date_after = [sf_policy + datetime.timedelta(days=x) for x in range(numdays+1)]
sf_date_list = date_before + date_after

daily_sf = daily_cases[daily_cases["county"]== "San Francisco"].copy()
daily_sf["date"] = pd.to_datetime(daily_sf["date"])
daily_sf_timed = daily_sf.loc[daily_sf["date"].isin(sf_date_list)].copy()
# covering a total of 43 days
daily_sf_timed.shape


### LA ###
##########
la_policy = datetime.datetime.strptime('19032020', "%d%m%Y").date()
date_before = [la_policy - datetime.timedelta(days=x) for x in range(numdays+1)]
date_after = [la_policy + datetime.timedelta(days=x) for x in range(numdays+1)]
la_date_list = date_before + date_after

daily_la = daily_cases[daily_cases["county"]== "Los Angeles"].copy()
daily_la["date"] = pd.to_datetime(daily_la["date"])
daily_la_timed = daily_la.loc[daily_la["date"].isin(la_date_list)].copy()
# covering a total of 43 days
daily_la_timed.shape


######## normalize by population ########
#########################################

# data cleaning
# us census data 2010 - 2019
pop =  pd.read_excel("../00_source_data/co-est2019-annres.xlsx",  header=[0,1,2,3])
pop.columns = pop.columns.droplevel([0,1,2])
pop.rename(columns={"Unnamed: 0_level_3": "Geographic Area"}, inplace = True)
pop["Geographic Area"] = pop["Geographic Area"].str.replace('.','', regex=True)



SF_pop = pop.loc[pop["Geographic Area"] == "San Francisco County, California"]
LA_pop = pop.loc[pop["Geographic Area"] == "Los Angeles County, California"]


daily_sf_timed["cases"] = daily_sf_timed["cases"] / SF_pop[2019].values[0] * 100000
daily_la_timed["cases"] = daily_la_timed["cases"] / LA_pop[2019].values[0] * 100000

