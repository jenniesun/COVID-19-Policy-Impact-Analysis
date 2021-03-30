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
sf_policy = datetime.datetime.strptime('16032020', "%d%m%Y").date()
date_before = [sf_policy - datetime.timedelta(days=x) for x in range(numdays+1)]
date_after = [sf_policy + datetime.timedelta(days=x) for x in range(numdays+1)]
sf_date_list = date_before + date_after

daily_sf = daily_cases[daily_cases["county"]== "San Francisco"].copy()
daily_sf["date"] = pd.to_datetime(daily_sf["date"])
daily_sf_timed = daily_sf.loc[daily_sf["date"].isin(date_list)]
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
daily_la_timed = daily_la.loc[daily_la["date"].isin(la_date_list)]
# covering a total of 43 days
daily_la_timed.shape

