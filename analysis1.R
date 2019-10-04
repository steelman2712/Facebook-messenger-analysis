#install.packages("dplyr")
#install.packages("lubridate")
#install.packages("hms")

#library(data.table)
#library(ggplot2)
library(dplyr)
library(lubridate)
library(hms)

#Read data from html_to_csv.py output csv
data = read.csv("E:\\Documents\\R\\Facebook - Copy\\analysis\\htmlcsv.csv")

#Split date and time into two different columns
data$Date<-as.Date(strptime(data$Time, format = "%d %b %Y"))
data$Time <- strptime(data$Time, format = "%d %b %Y %H:%M")
data$Time <- strftime(data$Time, format = "%H:%M")

#Assigns how many messages a person sent on a date or list of dates (I think)
name_date <- function(x) {
  date2 <- integer(0)
  date2
  class(date2) <- "Date"
  j <- 1
  for (i in 1:(length(data$Name))){
    if (data$Name[i] == x){
      date2[j] <- data$Date[i]
      j <- j+1
    }    
  }
  date2
  date2 <- table(date2)
  return(date2)
  plot(date2, type="l")
  cumdate2 <- cumsum(date2)
  plot(cumdate2,xaxt='n',type="l")
  #axis(1,at=1:length(cumdate2), labels=names(cumdate2),srt=45)
}

#Creates sequence of dates between start and end of time period selected
dates_function <- function(x){
  NMN <- c()
  for (i in 1:length(x)){
    NMN <- c(NMN,names(x[i]))
  }
  start_sub <- min(NMN)
  finish_sub <- max(NMN)
  dates_sub <- seq(as.Date(start_sub),as.Date(finish_sub),by=1)
  return(dates_sub)
}
#Counts the number of messages sent by a person
message_count <-function(x) {
  j <- 1
  date_list <- c()
  message_count_sub <- c()
  for (i in as.list(dates)){
    if(i==names(x[j])){
      date_list <- c(date_list,unname(x[j]))
      j <- j+1
    }
    else {
      date_list <- c(date_list,0)
    }
  }
  message_count_sub <- date_list[1:length(date_list)]
  return(message_count_sub)
}
#Creates a dataframe of number messages sent by each person each day
dfmessages <- function(x){
  message_amounts_list <- c()
  #Get NM from list
  for (i in 1:length(x)){
    dates_sub <- name_date(x[i])
    message_amounts_list <- c(message_amounts_list,dates_sub)
  }
  #Get dates list, set as first column in dataframe
  dates <<- dates_function(message_amounts_list)
  message_df <- data.frame(as.Date(dates))
  colnames(message_df)[1] <- "Dates"
  #Create new columns for each name
  for(i in 1:length(x)){
    name <- name_date(x[i])
    #print(name)
    name_out <- message_count(name)
    message_df <- cbind(message_df,name_out) 
    colnames(message_df)[i+1] <- x[i]
  }
  return(message_df)
}

#Gets a list of names of everyone who has sent messages
at_names <- levels(data$Name)

#Creates a dataframe of number of messages sent by each person in at_names each day
df_message <- dfmessages(at_names)

#Multi person plotting
x <- cbind(df_message$Dates)
y <- cbind(df_message[,at_names])
matplot(x,y,type='l',xaxt='n', main="Messages sent per person",xlab="Date",ylab ="Number of messages")
axis.Date(1,at=seq(min(df_message$Dates),max(df_message$Dates),by="days"), format = "%d/%m")
nn <- ncol(df_message)
legend_names <- gsub("at_","",colnames(df_message[2:ncol(df_message)]))
legend("topleft", legend_names,col=seq_len(nn)-1,cex=0.8,fill=seq_len(nn))



#Number of messages sent by person given by at_names[1]
length(which(data$Name==at_names[1]))
#Amount of media fies sent
length(which(data$Message=="media"))







"7 September 2018 16:50"








