##################################################
# Contains functions for diff-in-diff plot 
# and pre-post plot.
##################################################
import pandas as pd
import numpy as np
import datetime
import os
import sys
from plotnine import *

sf_df = pd.read_csv("../20_intermediate_files/SF_data.csv", index_col = 0)
la_df = pd.read_csv("../20_intermediate_files/LA_data.csv", index_col = 0)
sf_df["standardized_date"] = sf_df["standardized_date"].str.replace(' days','', regex=True).astype(int)
la_df["standardized_date"] = la_df["standardized_date"].str.replace(' days','', regex=True).astype(int)


# # Diff in Diff Plot
def diff_in_diff_plot(df_treatment, df_control):
    
    treatment_state = str(list(df_treatment.county.unique())[0])
    
 
    lower_lim = df_treatment['standardized_date'].min()
    upper_lim = df_treatment['standardized_date'].max()+1
    
    plot = (
    ggplot() +
    geom_smooth(df_treatment[df_treatment['standardized_date'] < 0], 
                aes(x='standardized_date', y='cases', color='county')) 
        + 
    geom_smooth(df_treatment[df_treatment['standardized_date'] >= 0], 
                aes(x='standardized_date', y='cases', color='county')) + 
        
    geom_smooth(df_control[df_control['standardized_date'] < 0], 
                aes(x='standardized_date', y='cases', color='county')) + 
    geom_smooth(df_control[df_control['standardized_date'] >= 0], 
                aes(x='standardized_date', y='cases', color='county'))
    + geom_vline(xintercept = 0) 
    + xlab('Years before/after Policy Implementation Year: ' + '. \nRepresented as "0" on the x-axis.') 
    + ylab(' \n(Adding 95% confidence interval)')
    + scale_x_continuous(breaks=range(lower_lim,upper_lim,1))
    + labs(title=str("Difference in Difference Plot - "+treatment_state))
        
    )
    return plot


diff_in_diff_plot(sf_df, la_df)
