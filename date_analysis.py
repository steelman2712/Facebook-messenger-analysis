#!/usr/bin/env python3

import numpy as np
import pandas as pd
import csv
import os
import argparse
import matplotlib.pyplot as plt
from datetime import datetime



#Check input file is valid
def infile_check(infile):
    try:
        open(infile,"r")
    except:
        print("Input file not found, the input file is specified to be at "+infile)


def plot_by_date(infile,person):
    df = pd.read_csv(infile)
    df_datetime = pd.read_csv(infile,parse_dates={'DateTime': ['Date', 'Time']})

    df["Date"] = pd.to_datetime(df["Date"],infer_datetime_format=True) 

        
    #def name_date():
    date_list = df["Date"]
    date_list = list(dict.fromkeys(date_list))

    name_list = df["Name"]
    name_list = list(dict.fromkeys(name_list))

    date_rng = pd.date_range(start=min(df["Date"]), end=max(df["Date"]),freq="d")


    name_dict = {}
    for i in name_list:
        name_dict[i]=df.loc[df["Name"]==i]

    df_name_date = pd.DataFrame(name_dict[person])[["Name","Date"]]
    df_name_date = df_name_date["Date"].value_counts(sort=False).resample("D").mean().fillna(0)
    df_name_date.plot(kind="line")
    plt.title("Messages sent by "+person)
    plt.xlabel("Date")
    plt.ylabel("Number of messages sent")
    plt.show()


if __name__ == "__main__":
    ##Set up cli options
    cmd_dir = os.getcwd() #Get CLI location
    parser = argparse.ArgumentParser(description="Converts Facebook messenger html data to a csv format")
    parser.add_argument("-i",'--infile', nargs='?',dest="infile", type=str,default=os.path.join(cmd_dir,"htmlcsv.csv"),help="Input html file to be converted, the default is in the current location of the cli and called 'htmlcsv.csv', currently: "+os.path.join(cmd_dir,"htmlcsv.csv")) #Add input argument
    parser.add_argument("-n","--name", nargs=1, dest="name", type=str, help="Name of person to graph")

    args = parser.parse_args()
    infile_check(args.infile)
    plot_by_date(args.infile,args.name[0])
