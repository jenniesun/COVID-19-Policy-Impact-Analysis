import pandas as pd
import datetime

daily_cases = pd.read_csv("./data/us-counties-covid-cases.csv")
daily_cases = daily_cases[daily_cases["state"] == "North Carolina"]
daily_cases.head()

# set comparison period to be 14 days
numdays = 14

# retrieve policy date for Stay at Home Order
policy = datetime.datetime.strptime('27032020', "%d%m%Y").date()
date_before = [policy - datetime.timedelta(days=x) for x in range(numdays+1)]
date_after = [policy + datetime.timedelta(days=x) for x in range(numdays+1)]
date_list = date_before + date_after


### Mecklenburg County ###
##########################

daily_meck = daily_cases[daily_cases["county"] == "Mecklenburg"].copy()
daily_meck["date"] = pd.to_datetime(daily_meck["date"])
daily_meck_timed = daily_meck.loc[daily_meck["date"].isin(date_list)]

# covering a total of 29 days (14 + 1 + 1)
daily_meck_timed


### Wake County ###
###################

daily_wake = daily_cases[daily_cases["county"] == "Wake"].copy()
daily_wake["date"] = pd.to_datetime(daily_wake["date"])
daily_wake_timed = daily_wake.loc[daily_wake["date"].isin(date_list)]

# covering a total of 29 days (14 + 1 + 1)
daily_meck_timed
