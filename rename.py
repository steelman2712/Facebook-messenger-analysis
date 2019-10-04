import csv
import pandas as pd
import os
import argparse


def rename(infile):
    df_rename = pd.read_csv(infile)
    os.rename('htmlcsv.csv', 'htmlcsv.csv.bak')


    name_list = df_rename.Name
    react_list = df_rename.React


    with open("rename.csv","r") as rename:
        reader = csv.reader(rename)
        name_dict = {rows[0]:rows[1] for rows in reader}


    for i in range(len(name_list)):
        name_list[i] = name_dict[name_list[i]]

    for i in range(len(react_list)):
        for key in name_dict.keys():
            react_list[i] = react_list[i].replace(key,name_dict[key])


    df_rename.Name = name_list
    df_rename.React = react_list
    df_rename.to_csv(infile)
    
if __name__=="__main__":
    #Get CLI location
    cmd_dir = os.getcwd() 
    parser = argparse.ArgumentParser(description="Converts Facebook messenger html data to a csv format")
    parser.add_argument("-i",'--infile', nargs='?',dest="infile", type=str,default=os.path.join(cmd_dir,"htmlcsv.csv"),help="Input html file to be converted, the default is in the current location of the cli and called 'htmlcsv.csv', currently: "+os.path.join(cmd_dir,"htmlcsv.csv")) 
    args = parser.parse_args()
    rename(args.infile)
