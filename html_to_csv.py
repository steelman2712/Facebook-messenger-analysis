#!/usr/bin/env python3


from bs4 import BeautifulSoup 
import csv
import re
import os
import argparse

from datetime import datetime
import calendar


##Set up cli options
cmd_dir = os.getcwd() #Get CLI location
parser = argparse.ArgumentParser(description="Converts Facebook messenger html data to a csv format")
parser.add_argument("-i",'--infile', nargs='?',dest="infile", type=str,default=os.path.join(cmd_dir,"message.html"),help="Input html file to be converted, the default is in the current location of the cli and called 'message.html'") #Add input argument
parser.add_argument("-o",'--outfile', nargs='?',dest="outfile", type=str,default=os.path.join(cmd_dir,"htmlcsv.csv"), help="Output csv file to write to, the default is in the current location of the cli and called 'htmlcsv.csv'")	#Out output file argument
parser.add_argument("-d",'--date',nargs=1,dest="date_yes",type=int,default=1,help="Decide whether to split the date and time columns. yes = 1, no = 0 with a default of 1. Subsequent analysis scripts provided assume date and time are split.") #Add date splitting option
args = parser.parse_args()


#Check input file is valid
try:
	open(args.infile,"r")
except:
	print("Input file not found, the input file is specified to be at "+args.infile)

infile = args.infile


#Adding lines to the html file so it's easier to read. Also makes it compatible with BeautifulSoup

def clean_html(file):
	with open(file,"r") as myfile:
		data=myfile.readlines()
		data = str(data)
		data2 = data.replace("<div>", "\n <div>")
		data2 = data2.replace("</div>", "\n </div>")
	return(data2)
	

#Creates text with the html data then puts it in a list.
soup = BeautifulSoup(clean_html(infile), "lxml")
text = soup.get_text()
split_text = text.splitlines()
l = [l for l in split_text if l.strip()]
del l[0:4]

#Getting names of people in chat. Messages sent by person will be written as "at_person" to make it easier to use later and avoid clashes with names in messages 
names = l[0]
names = names.replace(" and ",", ")
names = re.split('[:,]',names)
names[len(names)-1] = names[len(names)-1].replace("\n","")
del names[0]
new_names = []
for i in range(0,len(names)):
    names[i] = names[i][1:]
    new_names.append(str("at_"+names[i]))


#Setting reacts and changing ";" to "~" since ";" messes up csv and it's not important enough to sanitise it properly
for i in range(0,len(l)):
    l[i] = l[i].replace("\n","")
    for j in range(0,len(names)):
        l[i] = l[i].replace(names[j],new_names[j])
    l[i] = l[i].replace(u"\U0001F60D", "react_love")
    l[i] = l[i].replace(u"\U0001F606", "react_laugh")
    l[i] = l[i].replace(u"\U0001F62E", "react_shock")
    l[i] = l[i].replace(u"\U0001F622", "react_cry")
    l[i] = l[i].replace(u"\U0001F620", "react_angry")
    l[i] = l[i].replace(u"\U0001F44D", "react_up")
    l[i] = l[i].replace(u"\U0001F44E", "react_down")
    l[i] = l[i].replace(";", "~")

#Setting column names
l.insert(1,'Name')
l.insert(2,'Message')
l.insert(3,'Time')
l.insert(4,'React')



#Get stuff into the right columns
i = 5
while i < len(l)-2:
    #Remove that thing where it creates a duplicate entry for urls
    if l[i+2].startswith('http'):
        del l[i+2]
    #Plans - can containg details of time, place etc. which need moving into one cell
    if l[i+1].startswith('Plan created:'):
        if l[i+5].startswith("at_"):
            l[i+1] = str(l[i+1]+" at "+l[i+2]+"at time"+l[i+3])
            del l[i+2]
            del l[i+2]
        elif l[i+5].startswith("react_"):
            l[i+1] = str(l[i+1]+" at "+l[i+2]+"at time"+l[i+3])
            del l[i+2]
            del l[i+2]
        elif l[i+4].startswith("at_"):
            l[i+1] = str(l[i+1]+"at time"+l[i+3])
            del l[i+2]
            
    #Media with no reacts
    if l[i].startswith('at_') and l[i+2].startswith('at_'):
        l.insert(i+1,'media')
        l.insert(i+3,'react_none')
        
    #Message with react
    elif l[i+2].startswith('react_'):
        l[i+2],l[i+3] = l[i+3],l[i+2]
        
    #Media with react
    elif l[i+1].startswith('react_'):
        l.insert(i+1, 'media')
        l[i+2],l[i+3] = l[i+3],l[i+2]

    #Message with no react
    else:
        l.insert(i+3, "react_none")
    i=i+4


    
#Writing to csv file
if not args.outfile.endswith("csv"):
    csv_out = args.outfile+".csv"
else:
    csv_out=args.outfile

with open(csv_out, 'w') as csvfile:
    htmlwriter = csv.writer(csvfile, delimiter=',')
    for i in range(1,len(l)-3,4):
        htmlwriter.writerow([l[i],l[i+1],l[i+2],l[i+3]])
        
        
        
#Split date
if args.date_yes==1:
    #Define date splitting function
    def date_split(date_input):
        date_input= datetime.strptime(str(date_input), '%d %B %Y %H:%M')
        date0 = str(date_input).split()
        return(date0)


    with open(csv_out,"r") as csvfile:
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
        csvfile.close()


    with open(csv_out,"w") as csv_out:
        writer = csv.writer(csv_out, delimiter=",")
        writer.writerows(new_rows_list)
        csv_out.close()
        
        
