##################################################
# Contains functions for diff-in-diff plot 
##################################################
import pandas as pd
import numpy as np
import datetime
import os
import sys
from plotnine import *

ca_df = pd.read_csv("../20_intermediate_files/CA_state_level.csv")
ca_df["date"] = pd.to_datetime(ca_df["date"])
control_df = pd.read_csv("../20_intermediate_files/CA_controls.csv")
control_df["date"] = pd.to_datetime(control_df["date"])
ca_df["state"] = "CA"
control_df["state"] = "control"
# sf_df["standardized_date"] = sf_df["standardized_date"].str.replace(' days','', regex=True).astype(int)
# la_df["standardized_date"] = la_df["standardized_date"].str.replace(' days','', regex=True).astype(int)


# # Diff in Diff Plot
# def diff_in_diff_plot(df_treatment, df_control):
    
#     #treatment_state = str(list(df_treatment.state.unique())[0])
      #lower_lim = df_treatment['standardized_date'].min()
#     upper_lim = df_treatment['standardized_date'].max()+1
    
#     plot = (
#     ggplot() +
#     geom_smooth(df_treatment[df_treatment['standardized_date'] < 0], 
#                 aes(x='standardized_date', y='cases', color='county')) 
#         + 
#     geom_smooth(df_treatment[df_treatment['standardized_date'] >= 0], 
#                 aes(x='standardized_date', y='cases', color='county')) + 
        
#     geom_smooth(df_control[df_control['standardized_date'] < 0], 
#                 aes(x='standardized_date', y='cases', color='county')) + 
#     geom_smooth(df_control[df_control['standardized_date'] >= 0], 
#                 aes(x='standardized_date', y='cases', color='county'))
#     + geom_vline(xintercept = 0) 
#     + xlab('Days before/after Policy Implementation: ' + '. \nRepresented as "0" on the x-axis.') 
#     + ylab(' \n number of Covid cases per 10,000')
#     + scale_x_continuous(breaks=range(lower_lim,upper_lim,1))
#     + theme(figure_size=(12, 6))
#     + labs(title=str("Difference in Difference Plot - "+treatment_state))
        
#     )
#     return plot

def diff_in_diff_plot(df_treatment, df_control):
    treatment = "red"
    control = "black"
    plot = (
    ggplot() +
    geom_smooth(df_treatment[df_treatment["date"] < '2020-03-19'], 
                aes(x='date', y='cases', color = 'state')) 
        + 
     geom_smooth(df_treatment[df_treatment["date"] >= '2020-03-19'], 
                aes(x='date', y='cases', color = 'state'))  + 
    geom_smooth(df_control[df_control["date"] < '2020-03-19'], 
                aes(x='date', y='cases', color = 'state')) + 
    geom_smooth(df_control[df_control["date"] >= '2020-03-19'], 
                aes(x='date', y='cases', color = 'state'))
    + geom_vline(xintercept = '2020-03-19') 
    + xlab('Days before/after Policy Implementation: ' + '. \nRepresented as "0" on the x-axis.') 
    + ylab(' \n number of Covid cases per 10,000')
    #+ scale_x_continuous(breaks=range(lower_lim,upper_lim,1))
    + theme(figure_size=(12, 6))
    + labs(title=str("Difference in Difference Plot - "))
        
    )
    return plot



graph = diff_in_diff_plot(ca_df, control_df)
graph.save('./20_intermediate_file/CA_diff.pdf', height=6, width=12)
