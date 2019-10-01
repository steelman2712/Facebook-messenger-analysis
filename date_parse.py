from datetime import datetime
import calendar
import csv

def date_split(date_input):
    date_input= datetime.strptime(str(date_input), '%d %B %Y %H:%M')
    date0 = str(date_input).split()
    return(date0)

#print(date_split("6 September 2018 23:26"))

with open("/home/reynolds/Documents/analysis/htmlcsv.csv","r") as csvfile:
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


with open("/home/reynolds/Documents/analysis/htmlcsv.csv","w") as csv_out:
    writer = csv.writer(csv_out, delimiter=",")
    writer.writerows(new_rows_list)
    csv_out.close()
