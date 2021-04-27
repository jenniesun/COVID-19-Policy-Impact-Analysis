import pandas as pd 
import numpy as np
import datetime

daily_cases = pd.read_csv("../00_source_data/us-counties.csv")
daily_cases.head()

##### subset states and 3 week span #####
#########################################

numdays = 21

### CA ###
##########
ca_policy = datetime.datetime.strptime('19032020', "%d%m%Y").date()
date_before = [ca_policy - datetime.timedelta(days=x) for x in range(numdays+1)]
date_after = [ca_policy + datetime.timedelta(days=x) for x in range(numdays+1)]
ca_date_list = date_before + date_after

daily_ca = daily_cases[daily_cases["state"]== "California"].copy()
daily_ca["date"] = pd.to_datetime(daily_ca["date"])
daily_ca_timed = daily_ca.loc[daily_ca["date"].isin(ca_date_list)].copy()
# covering a total of 43 days
daily_ca_timed.shape

### Florida ###
###############

daily_fl = daily_cases[daily_cases["state"]== "Florida"].copy()
daily_fl["date"] = pd.to_datetime(daily_fl["date"])
daily_fl_timed = daily_fl.loc[daily_fl["date"].isin(ca_date_list)].copy()
# covering a total of 43 days
daily_fl_timed.shape

### Nevada ###
###############

daily_nv = daily_cases[daily_cases["state"]== "Nevada"].copy()
daily_nv["date"] = pd.to_datetime(daily_nv["date"])
daily_nv_timed = daily_nv.loc[daily_nv["date"].isin(ca_date_list)].copy()
# covering a total of 43 days
daily_nv_timed.shape

### Texas ###
###############

daily_tx = daily_cases[daily_cases["state"]== "Texas"].copy()
daily_tx["date"] = pd.to_datetime(daily_tx["date"])
daily_tx_timed = daily_tx.loc[daily_tx["date"].isin(ca_date_list)].copy()
# covering a total of 43 days
daily_tx_timed.shape


######### population data cleaning #########
############################################
# us census data 2010 - 2019
pop =  pd.read_excel("../00_source_data/co-est2019-annres.xlsx",  header=[0,1,2,3])
pop.columns = pop.columns.droplevel([0,1,2])
pop.rename(columns={"Unnamed: 0_level_3": "Geographic Area"}, inplace = True)
pop["Geographic Area"] = pop["Geographic Area"].str.replace('.','', regex=True)


########  get total population  ########
CA_pop = pop.loc[pop["Geographic Area"].str.contains("California")].sum()[2019]
FL_pop = pop.loc[pop["Geographic Area"].str.contains("Florida")].sum()[2019]
NV_pop = pop.loc[pop["Geographic Area"].str.contains("Nevada")].sum()[2019]
TX_pop = pop.loc[pop["Geographic Area"].str.contains("Texas")].sum()[2019]
control_pop = FL_pop + NV_pop + TX_pop

########  get state daily cases  ########
daily_ca_total = daily_ca_timed.groupby(by=["date"]).sum()["cases"]
daily_fl_total = daily_fl_timed.groupby(by=["date"]).sum()["cases"]
daily_nv_total = daily_nv_timed.groupby(by=["date"]).sum()["cases"]
daily_tx_total = daily_tx_timed.groupby(by=["date"]).sum()["cases"]
control_cases =daily_fl_total.add(daily_nv_total, fill_value = 0)
control_cases = control_cases.add(daily_tx_total, fill_value = 0)


daily_ca_total= daily_ca_total / CA_pop * 100000
daily_control_total= control_cases / control_pop * 100000



# sf = np.datetime64(sf_policy)
# la = np.datetime64(la_policy)
# daily_sf_timed["standardized_date"] = (daily_sf_timed["date"] - sf)
# daily_la_timed["standardized_date"] = (daily_la_timed["date"] - la)



daily_ca_total.to_csv("../20_intermediate_files/CA_state_level.csv")
daily_control_total.to_csv("../20_intermediate_files/CA_controls.csv")
