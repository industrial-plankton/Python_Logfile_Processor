import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
#import os

filename = "CSV/PBR99_Temp_Test_1.csv"
LogFilename = "CSV/PBR99_Logfile.csv"

start_date = "2021-03-10"
end_date   = "2021-03-20"

Logger_Moving_Ave = 500

def plotStuff():
    plt.close('all')
    df = pd.read_csv(filename)
    df['DateTime'] = df['DateTime'].astype('datetime64[ns]')
    #df['DateTime'] = df['DateTime'].DateOffset(hours=1)
    df['Ch1_Value'] = df.rolling(window=Logger_Moving_Ave)['Ch1_Value'].mean()
    df['Ch2_Value'] = df.rolling(window=Logger_Moving_Ave)['Ch2_Value'].mean()
    df['Ch3_Value'] = df.rolling(window=Logger_Moving_Ave)['Ch3_Value'].mean()
    after_start_date = df["DateTime"] >= start_date
    before_end_date = df["DateTime"] <= end_date
    between_two_dates = after_start_date & before_end_date
    filtered_dates = df.loc[between_two_dates]

    ax = plt.gca()
    #filtered_dates.plot(kind='line', x='DateTime', y='Ch1_Value', ax=ax, title='PBR99 High Delta Test', label='Floor Temp')
    filtered_dates.plot(kind='line', x='DateTime', y='Ch2_Value', ax=ax, label='Front of PBR', title='PBR99 High Delta Test')
    filtered_dates.plot(kind='line', x='DateTime', y='Ch3_Value', ax=ax, label='Rear of PBR')

    df2 = pd.read_csv(LogFilename)
    df2['Date'] = df2['Date'].astype('datetime64[ns]')

    after_start_date = df2["Date"] >= start_date
    before_end_date = df2["Date"] <= end_date
    between_two_dates = after_start_date & before_end_date
    filtered_dates = df2.loc[between_two_dates]

    filtered_dates.plot(kind='line', x='Date', y='Temperature_C', ax=ax, label='PBR Algae Temp')

    plt.grid(True)

    plt.show()

plotStuff()
