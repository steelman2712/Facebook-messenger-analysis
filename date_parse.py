from datetime import datetime
import calendar
import csv
import os
import argparse


##Set up cli options
cmd_dir = os.getcwd() #Get CLI location
parser = argparse.ArgumentParser(description="Converts Facebook messenger html data to a csv format")
parser.add_argument("-i",'--infile', nargs='?',dest="infile", type=str,default=os.path.join(cmd_dir,"htmlcsv.csv"),help="Input html file to be converted, the default is in the current location of the cli and called 'htmlcsv.csv'") #Add input argument
parser.add_argument("-o",'--outfile', nargs='?',dest="outfile", type=str,default=os.path.join(cmd_dir,"htmlcsv.csv"), help="Output csv file to write to, the default the same file as the input")	#Out output file argument
args = parser.parse_args()


#Check input file is valid
try:
	open(args.infile,"r")
except:
	print("Input file not found, the input file is specified to be at "+args.infile)

infile = args.infile
outfile = args.outfile





def date_split(date_input):
    date_input= datetime.strptime(str(date_input), '%d %B %Y %H:%M')
    date0 = str(date_input).split()
    return(date0)

#print(date_split("6 September 2018 23:26"))

with open(infile,"r") as csvfile:
    htmlreader = csv.reader(csvfile, delimiter=',')
    next(htmlreader)
    new_rows_list = [['Name','Message','Date','Time','React']]
    for row in htmlreader:
        date = date_split(row[2])
        row.append(row[3])
        row[2] = date[0]
        row[3] = date[1]
        #print(row)
        new_rows_list.append(row)
    #print(new_rows_list[0])
    csvfile.close()


with open(outfile,"w") as csv_out:
    writer = csv.writer(csv_out, delimiter=",")
    writer.writerows(new_rows_list)
    csv_out.close()
