# Created: 2021/03/18
# Stuart de Haas
# Last Modified: 2021/03/18

import pandas as pd #used to import, hold, and manipulate data
import matplotlib as mpl
import matplotlib.pyplot as plt #Used to make plots
from datetime import datetime #Helps with dates
import sys #Works with getop to read flags
import getopt #Lets us send flags to the app
#import numpy as np
#import os

sensorBoxFile = "CSV/SensorBoxLog001_20210820.csv"
PBRlogFilename = "CSV/RawLog1.csv"
RAWPBRlogFilename = "CSV/62RawLog1.csv"

start_date = "2021-09-27" # Inclusive
end_date   = "2021-09-28" # Exclusive

Logger_Moving_Ave = 10

#tempLoggerfile = "CSV/PBR99_Temp_Test_1.csv"
#PBR_Moving_Ave = 500
#cleanPBRlogFilename = "CSV/PBR46_20210708.csv"
#eventLogFile = "CSV/eventLog001.csv"

def normalize(df):
    """ Takes a dataframe and normalizes all non-date columns (based on column title) """
    result = df.copy()
    for feature_name in df.columns:
        if(feature_name == ('Date' or 'Date-Time')):
            continue
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        #result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
        result[feature_name] = (df[feature_name] - df[feature_name].mean()) / df[feature_name].std()
    return result

def movingAve(df):
    """ Takes a dataframe and applies a moving average"""
    result = df.copy()
    for feature_name in df.columns:
        if(feature_name == ('Date' or 'Date-Time')):
            continue
        result[feature_name] = df.rolling(window=Logger_Moving_Ave)[feature_name].mean()

    return result

def filterDates(df):
    after_start_date = df["Date"] >= start_date
    before_end_date = df["Date"] <= end_date
    between_two_dates = after_start_date & before_end_date
    return df.loc[between_two_dates]


def plotRAWPBR():
    """ Plots a high-res RAW log file from a PBR """
    df = pd.read_csv(RAWPBRlogFilename, skiprows=1, parse_dates=["Date"])

    # df = filterDates(df)
    df = normalize(df)
    # df = movingAve(df)

    df.plot(kind='line', x='Date', y='RawPressure', ax=ax, color='cornflowerblue', label='RawPressure')
    df.plot(kind='line', x='Date', y='RawpH', ax=ax, color='cyan', title='PBR1250L Ferrari, from ' + start_date + ' to ' + end_date, label='RawpH')
    df.plot(kind='line', x='Date', y='RawTemp', ax=ax, color='r', label='RawTemp')
    df.plot(kind='line', x='Date', y='RawOD', ax=ax, color='g', label='RawOD')
   # df.plot(kind='line', x='Date', y='pH', ax=ax, label='pH')
   # df.plot(kind='line', x='Date', y='Temp', ax=ax, label='Temp')
   # df.plot(kind='line', x='Date', y='Vol', ax=ax, label='Vol')
   # df.plot(kind='line', x='Date', y='OD', ax=ax, label='OD')

def plotSensorBoxLogger():
    df = pd.read_csv(sensorBoxFile, parse_dates=["Date-Time"])
    df['Probe1'] = df.rolling(window=Logger_Moving_Ave)['Probe1'].mean()
    df['Probe2'] = df.rolling(window=Logger_Moving_Ave)['Probe2'].mean()
    df['Probe3'] = df.rolling(window=Logger_Moving_Ave)['Probe3'].mean()
    df['Probe4'] = df.rolling(window=Logger_Moving_Ave)['Probe4'].mean()
    df['ThermoCouple1'] = df.rolling(window=Logger_Moving_Ave)['ThermoCouple1'].mean()
    df['ThermoCouple2'] = df.rolling(window=Logger_Moving_Ave)['ThermoCouple2'].mean()
    df['ThermoCouple3'] = df.rolling(window=Logger_Moving_Ave)['ThermoCouple3'].mean()
    df['ThermoCouple4'] = df.rolling(window=Logger_Moving_Ave)['ThermoCouple4'].mean()
    after_start_date = df["Date-Time"] >= start_date
    before_end_date = df["Date-Time"] <= end_date
    between_two_dates = after_start_date & before_end_date
    filtered_dates = df.loc[between_two_dates]

    filtered_dates.plot(kind='line', x='Date-Time', y='Probe1', ax=ax, title='PBR1250L Temperature Test, from ' + start_date + ' to ' + end_date, label='Probe1 Temperature')
    filtered_dates.plot(kind='line', x='Date-Time', y='Probe2', ax=ax, label='Probe2')
    filtered_dates.plot(kind='line', x='Date-Time', y='Probe3', ax=ax, label='Probe3')
    filtered_dates.plot(kind='line', x='Date-Time', y='Probe4', ax=ax, label='Probe4')
    filtered_dates.plot(kind='line', x='Date-Time', y='ThermoCouple1', ax=ax, label='ThermoCouple1')
    filtered_dates.plot(kind='line', x='Date-Time', y='ThermoCouple2', ax=ax, label='ThermoCouple2')
    filtered_dates.plot(kind='line', x='Date-Time', y='ThermoCouple3', ax=ax, label='ThermoCouple3')
    filtered_dates.plot(kind='line', x='Date-Time', y='ThermoCouple4', ax=ax, label='ThermoCouple4')

def plotTempLogger():
    df = pd.read_csv(tempLoggerfile, parse_dates=["DateTime"])
    df['Ch1_Value'] = df.rolling(window=Logger_Moving_Ave)['Ch1_Value'].mean()
    df['Ch2_Value'] = df.rolling(window=Logger_Moving_Ave)['Ch2_Value'].mean()
    df['Ch3_Value'] = df.rolling(window=Logger_Moving_Ave)['Ch3_Value'].mean()
    after_start_date = df["DateTime"] >= start_date
    before_end_date = df["DateTime"] <= end_date
    between_two_dates = after_start_date & before_end_date
    filtered_dates = df.loc[between_two_dates]

    #filtered_dates.plot(kind='line', x='DateTime', y='Ch1_Value', ax=ax, title='PBR99 High Delta Test', label='Floor Temp')
    filtered_dates.plot(kind='line', x='DateTime', y='Ch2_Value', ax=ax, label='Front of PBR', title='PBR99 High Delta Test')
    filtered_dates.plot(kind='line', x='DateTime', y='Ch3_Value', ax=ax, label='Rear of PBR')

def plotCleanLog():
    df = pd.read_csv(PBRlogFilename, skiprows=2, comment='E', parse_dates=["Date"])

    after_start_date = df["Date"] >= start_date
    before_end_date = df["Date"] <= end_date
    between_two_dates = after_start_date & before_end_date
    filtered_dates = df.loc[between_two_dates]

    filtered_dates.plot(kind='line', x='Date', y='Temperature_C', ax=ax, label='PBR Algae Temp')
    #ax2 = ax.twinx()
    #ax2.set_ylim([0,150])
    #filtered_dates.plot(kind='line', x='Date', y='LightIntensity', ax=ax2, label='Light Intensity')

def plotPBRlog(filename = PBRlogFilename):

    df = pd.read_csv(filename, skiprows=2, comment='E', parse_dates=["Date"])

    after_start_date = df["Date"] >= start_date
    before_end_date = df["Date"] <= end_date
    between_two_dates = after_start_date & before_end_date
    df = df.loc[between_two_dates]

    # makes lots of little plots
    #df.plot(subplots=True, figsize=(8, 8))

    fig, temperature = plt.subplots(figsize=(16,8)) # (width, height) in inches

    pH = temperature.twinx()
    CO2 = temperature.twinx()
    rho = temperature.twinx()
    light = temperature.twinx()
    volume = temperature.twinx()
    nutrients = temperature.twinx()

    temperature.set_ylim(10,30)
    pH.set_ylim(5,9)
    CO2.set_ylim(0,15)
    rho.set_ylim(0,12)
    light.set_ylim(0,110)
    volume.set_ylim(0,1300)
    nutrients.set_ylim(0,100)

    temperature.set_xlabel("Date")
    temperature.set_ylabel("Temperature")
    pH.set_ylabel("pH")
    CO2.set_ylabel("CO2 Injections")
    rho.set_ylabel("Relative Density")
    light.set_ylabel("Light Intensity")
    volume.set_ylabel("Tank Volume")
    nutrients.set_ylabel("Total Nutrients")

    p1, = temperature.plot(df['Date'], df['Temperature_C'], color='r', label="Temperaure")
    p2, = pH.plot(df['Date'], df['pH'], color='b', label="pH")
    p3, = CO2.plot(df['Date'], df['CO2_Injectionsper10min'], color='y', label="CO2 Injections/10min")
    p4, = rho.plot(df['Date'], df['RelativeDensity'], color='g', label="Relative Density")
    p5, = light.plot(df['Date'], df['LightIntensity'], color='y', label="light Intensity")
    p6, = volume.plot(df['Date'], df['TankVolume'], color='b', label="Tank Volume")
    p7, = nutrients.plot(df['Date'], df['TotalNutrients_mLper10min'], color='m', label="Total Nutrients")

    lns = [p1, p2, p3, p4, p5, p6, p7]
    temperature.legend(handles=lns, loc='best')
    CO2.spines['right'].set_position(('outward', 60))
    rho.spines['right'].set_position(('outward', 120))
    light.spines['left'].set_position(('outward', 120))
    volume.spines['left'].set_position(('outward', 60))
    nutrients.spines['right'].set_position(('outward', 180))

    make_patch_spines_invisible(light)
    make_patch_spines_invisible(volume)
    light.spines["left"].set_visible(True)
    light.yaxis.set_label_position('left')
    light.yaxis.set_ticks_position('left')

    volume.spines["left"].set_visible(True)
    volume.yaxis.set_label_position('left')
    volume.yaxis.set_ticks_position('left')

    temperature.yaxis.label.set_color(p1.get_color())
    #temperature.spines['right'].set_edgecolor(p1.get_color())
    temperature.tick_params(axis='y', colors=p1.get_color())

    fig.tight_layout()
    plt.grid(True)
    plt.show()
    #plt.savefig("pyplot.pdf")
    #filtered_dates.plot(kind='line', x='Date', y='Temperature_C', ax=ax, label='PBR Algae Temp')
    #filtered_dates.plot(kind='line', ax=ax, label='PBR Algae Temp')

def plotEvents():
    df = pd.read_csv(eventLogFile, parse_dates=["Date-Time"])
    after_start_date = df["Date-Time"] >= start_date
    before_end_date = df["Date-Time"] <= end_date
    between_two_dates = after_start_date & before_end_date
    filtered_dates = df.loc[between_two_dates]
    plt.vlines(df.iloc[:,0], 0, 5)


# taken from here: https://matplotlib.org/2.0.2/examples/pylab_examples/multiple_yaxis_with_spines.html
def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

def main():
    menu()


def menu():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "tlfhr")
    except getopt.GetoptError as e:
        print( str(e))
        print("Not a valid instruction")
        sys.exit(2)

    if len(opts) == 0:
        print("Please use a flag to indicate desired output. Try t l f or h")
        return

    for opt, arg in opts:
        if opt == '-h':
            print("You want help? Too bad.")
            return
        elif opt == '-r':
            plt.close('all')
            COLOR = 'white'
            mpl.rcParams['text.color'] = COLOR
            mpl.rcParams['axes.labelcolor'] = COLOR
            mpl.rcParams['xtick.color'] = COLOR
            mpl.rcParams['ytick.color'] = COLOR

            fig = plt.figure()
            fig.patch.set_facecolor('#353535')
            #fig.patch.set_alpha(0.7)

            global ax
            #ax = plt.gca()
            ax = fig.add_subplot(111)

            #plotCleanLog()
            #plotSensorBoxLogger()
            plotRAWPBR()
            #plotEvents()

            plt.grid(True)
            #plt.figure(facecolor='grey')
            ax.set_facecolor('#353535')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')
            #plt.set_facecolor('grey')
            plt.show()
            return
        elif opt == '-l':
            plotPBRlog()
            return
        elif opt == '-j':
            plotRAWPBR()
            return
        elif opt == '-f':
            userFile = input("\nPlease provide a raw PBR Log filename located in CSV folder\n")
            plotPBRlog("CSV/" + userFile)
            return
        else:
            continue

# Only run this code if we called this file (otherwise it acts like a library)
if __name__ == "__main__":
    # Catch keyboard interrupts (like cntl-C) and output a less messy message
    try:
        main()
        #plotPBRlog()
    except(KeyboardInterrupt, SystemExit):
        print()
        print("Exiting")
    except:
        raise
