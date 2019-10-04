# Facebook-messenger-analysis
Scripts for analysing facebook messenger data

Facebook allows for the downloading of messenger data in two formats, html and json. 

The python script html_to_csv.py converts messenger html data into a csv format to allow for analysis. 


## html_to_csv.py

This script converts messenger html data into a csv format to allow for analysis.


This script takes three optional commands:

- -i, --input: used to specify a messenger html file. Defaults to one called "message.html" in the location where the terminal is.

- -o, --output: used to specify the location of the csv file to output. Defaults to one called "output.csv" in the location where the terminal is.

- -r, --rename: Creates a csv file where you can rename people's names. Defaults to one called "rename.csv" in the location where the terminal is.

### Output

This script produces a csv file, by default and from hereon called htmlcsv.csv, with the following columns:

| Message number | Name | Message contents | Date | Time | Reaction

Names are produced to be in an "at_Firstname Surname" format but this can be changed later through the rename.py script. 

Any media such as photos or video is replaced by the string "media"



## rename.py

Since html_to_csv.py outputs names in a "at_Firstname Surname" format it can be time consuming to type this out each time you want to refer to someone. Fortunately, rename.py can change people's names to something simpler.

### Usage

1) Open the rename.csv file created from running html_to_csv.

2) Change people's names in the second column

3) Run rename.py


## date_analysis.py

Creates a graph displaying the amount of messages sent by a person against the date sent.

This script takes two commands, one required and one optional:

- -n, --name: The name of the person you want a graph for. If you've not renamed them it will be in the form "at_Firstname Surname"

- -i, --input: used to specify the location of the htmlcsv.csv file. Defaults to one called "message.html" in the location where the terminal is. (Optional)

## date_analysis.R

Creates a graph comparing number of messages sent by people against time.

### Usage

1) Change where "data" variable is pointing to to match the location of htmlcsv.csv

2) Run the code
