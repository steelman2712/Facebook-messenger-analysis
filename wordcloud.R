#install.packages("tm")
#install.packages("SnowballC")
#install.packages("wordcloud")
#install.packages("RColorBrewer")
library("tm")
library("SnowballC")
library("RColorBrewer")
library("wordcloud")
library("textclean")

#Set folder we want to pull data from and to. 
#Should be wherever the python script outputted the csv file.
folder <- "##Folder wherever the htmlcsv.csv folder is##"

#Load file
data = read.csv(paste(folder,"htmlcsv.csv",sep = ""))


#Save messages to a text file as a list 
writer <- function(){
to_write<-paste()
message_file <- file(paste(folder,"message_file.txt",sep=""))
for (i in 1:length(data$Message)){
  to_write <- c(to_write,toString(droplevels(data$Message[i])))
  
}
writeLines(to_write,message_file)
close(message_file)
}


make_wordcloud <- function(){

#Pulling data back out of text. Legacy from when this and the bit above were different files, but I'm leaving it in as it works

text_file <- paste(folder,"message_file.txt",sep="")
filetext <- readLines(con <- file(text_file,encoding="UTF-8"))
text <- as.list(filetext)
text <- replace_word_elongation(text)
text <- replace_non_ascii(text,remove.nonconverted = TRUE)
text <- replace_contraction(text)
## Formatting data for wordcloud, mainly stripping anything we don't want ##
#Remove emojis
text <- gsub("/[\u{D088}-\u{F6FF}]/", "", text)
#Replace right quotation marks with apostrophies
text <- gsub("’", "'", text)
docs <- Corpus(VectorSource(text))
toSpace <- content_transformer(function (x , pattern ) gsub(pattern, " ", x))
docs <- tm_map(docs, toSpace, "/")
docs <- tm_map(docs, toSpace, "@")
docs <- tm_map(docs, toSpace, "\\|")
docs <- tm_map(docs, content_transformer(tolower))
docs <- tm_map(docs, removeNumbers)
#Remove common english words
docs <- tm_map(docs, removeWords, stopwords("english"))
#Custom list of words to remove, removing media as this would overwhelm it otherwise
docs <- tm_map(docs, removeWords, c("media"))
docs <- tm_map(docs, removePunctuation)
docs <- tm_map(docs, stripWhitespace)
print("Text cleaning complete")
dtm <- TermDocumentMatrix(docs)
m <- as.matrix(dtm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)
head(d, 10)


#Create wordcloud
set.seed(1234)
dev.new(width = 1000, height = 1000, unit = "px")
#Can change scale with scale= parameter.
par(bg="white")
print("Creating wordcloud")
wordcloud(words = d$word, freq = d$freq, min.freq = 50,
          max.words=200, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(8, "Dark2"))
#Save copy of the wordcloud as a png in the selected folder. Make sure you dev.off() to save
dev.copy(png,paste(folder,"wordcloud",sep=""))
dev.off()
}

#Call the function to create the wordcloud
writer()
make_wordcloud()
