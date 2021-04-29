##################################################
# Contains functions for diff-in-diff plot 
##################################################
import pandas as pd
import numpy as np
import datetime
import os
import sys
from plotnine import *

# read in data
# convert date type
ca_df = pd.read_csv("../20_intermediate_files/CA_state_level.csv")
ca_df["date"] = pd.to_datetime(ca_df["date"])

control_df = pd.read_csv("../20_intermediate_files/CA_controls.csv")
control_df["date"] = pd.to_datetime(control_df["date"])

florida_df = pd.read_csv("../20_intermediate_files/Florida.csv")
florida_df["date"] = pd.to_datetime(florida_df["date"])

nevada_df = pd.read_csv("../20_intermediate_files/Nevada.csv")
nevada_df["date"] = pd.to_datetime(nevada_df["date"])

texas_df = pd.read_csv("../20_intermediate_files/Texas.csv")
texas_df["date"] = pd.to_datetime(texas_df["date"])

# add state column
ca_df["state"] = "California"
florida_df["state"] = "Florida"
nevada_df["state"] = "Nevada"
texas_df["state"] = "Texas"
control_df["state"] = "Control"


def diff_in_diff_plot(df_treatment, df_control):
 
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
    + xlab('Before/after CA Stay-At-Home Order (March 19, 2020)') 
    + ylab(' \n number of COVID-19 cases per 10,000')
    #+ scale_x_continuous(breaks=range(lower_lim,upper_lim,1))
    + theme(figure_size=(12, 6))
    + labs(title=str("Difference in Difference Plot - California vs Control States (FL, NV, TX)"))
        
    )
    return plot



def diff_in_diff_plot_sep(df_treatment, df_control1, df_control2, df_control3):
 
    plot = (
    ggplot() +
    geom_smooth(df_treatment[df_treatment["date"] < '2020-03-19'], 
                aes(x='date', y='cases', color = 'state')) 
        + 
     geom_smooth(df_treatment[df_treatment["date"] >= '2020-03-19'], 
                aes(x='date', y='cases', color = 'state'))  + 
    geom_smooth(df_control1[df_control1["date"] < '2020-03-19'], 
                aes(x='date', y='cases', color = 'state')) + 
    geom_smooth(df_control1[df_control1["date"] >= '2020-03-19'], 
                aes(x='date', y='cases', color = 'state')) +
    geom_smooth(df_control2[df_control2["date"] < '2020-03-19'], 
                aes(x='date', y='cases', color = 'state')) + 
    geom_smooth(df_control2[df_control2["date"] >= '2020-03-19'], 
                aes(x='date', y='cases', color = 'state')) +
    geom_smooth(df_control3[df_control3["date"] < '2020-03-19'], 
                aes(x='date', y='cases', color = 'state')) + 
    geom_smooth(df_control3[df_control3["date"] >= '2020-03-19'], 
                aes(x='date', y='cases', color = 'state'))
    + geom_vline(xintercept = '2020-03-19') 
    + xlab('Before/after CA Stay-At-Home Order (March 19, 2020)') 
    + ylab(' \n number of COVID-19 cases per 10,000')
    + theme(figure_size=(12, 6))
    + labs(title=str("Difference in Difference Plot - California vs Control States (FL, NV, TX)"))
        
    )
    return plot




graph = diff_in_diff_plot(ca_df, control_df)
graph_sep = diff_in_diff_plot_sep(ca_df, florida_df, nevada_df, texas_df)



graph.save('../20_intermediate_files/CA_diff.png', height=6, width=12)
graph_sep.save('../20_intermediate_files/CA_diff_sep.png', height=6, width=12)

