import math
import webdev
import searchdata
import os
import json

prtDirectory = "crawling"

def crawl(seed):
    #first, make a list of all the links we've gone to
    lstPagesVisited=[seed]
    #make a queue for what pages we should visit
    lstQueue = []
    #dicPages will record what pages we've been to
    dicPages = {}
    #dicAllWords will basically record all the words we've been to
    dicAllWords={}
    
    #we need to reset what's inside the pages.txt file
    os.remove("pages.txt")
    #every time we come across a page, we add it to pages.txt
    ioPagesFile = open("pages.txt", "a")

    # reset directory "crawling"
    if os.path.isdir(prtDirectory):
        #for every directory in the directory, we...
        for subDirectory in os.listdir(prtDirectory):
            #delete the directory
            recursiveDeleteDirectory(os.path.join(prtDirectory,subDirectory))
        #then delete the directory inside the directory
        recursiveDeleteDirectory(prtDirectory)
    #then create a new directory
    createNewDirectory(prtDirectory)

    
    dicPages[seed]=searchdata.get_outgoing_links(seed)
    recordInformation(seed,dicAllWords)
    ioPagesFile.write(seed+"\n")

    #for every link in the seed page
    for strLink in dicPages[seed]:
        #add these links to the page
        lstQueue.append(strLink)
    
    #while there's still something in the queue
    while(len(lstQueue)>0):
        #each time we go through one link
        strSubPage = lstQueue[0]
        #If the links found in page aren't in the queue or in the pages visited, add it to the list
        dicPages[strSubPage]=searchdata.get_outgoing_links(strSubPage)
        #since we've gone on that page, let's add it to the pages we've visited
        lstPagesVisited.append(strSubPage)
        #We then add the page we've just visited to the text file
        ioPagesFile.write(strSubPage+"\n")
        
        #this function records all the info we need in searchdata.py
        recordInformation(strSubPage,dicAllWords)
        #we then get rid of the website we've just visitied which is at lstQueue[0]
        lstQueue.pop(0)
        #for every link inside the page we're on, 
        for strLink in dicPages[strSubPage]:
            #if it's not in the queue already and not a key in dicPages visited, then
            if((strLink not in lstQueue) and (strLink not in dicPages)):
                #add that page to the queue
                lstQueue.append(strLink)
    #after we're done going through all the pages, close pages.txt
    ioPagesFile.close()

    #record outgoing links
    createOutGoingLinksFile(dicPages)
    
    #Now that we have the pages we've been to, we can do the easy bit of recording IDF values
    recordIDF(dicAllWords, dicPages)

    #the number of pages we visited will be the number of pages there are since we visited all of them
    return len(lstPagesVisited)

#this function will write down the info into a file
#O(n) time due to functions called that are O(n)
def recordInformation(strSubPage, dicAllWords):
    #break down the lines
    lstLines=webdev.read_url(strSubPage).strip().split("\n")
    #dicWords will store the number of times a word appears
    #apple : 3
    #peach : 5
    dicWords={}
    
    #we'll read the whole thing
    countWord(lstLines, dicWords)
    
    #create new directory
    strDirectory = strSubPage[strSubPage.rfind("/")+1:len(strSubPage)-5]
    # recursiveDeleteDirectory(strDirectory)
    createNewDirectory(os.path.join(prtDirectory, strDirectory))
    
    #create a file and then write into it
    createWordFile(os.path.join(prtDirectory, strDirectory),dicWords,dicAllWords)
    
    #create a file that keeps track of how many words there are
    createTotalWordFile(os.path.join(prtDirectory, strDirectory),dicWords)

    #create a file that records outgoing links
    createOutGoingLinksFile(strDirectory)
    
    #store the term frequency
    record_tf(os.path.join(prtDirectory, strDirectory),dicWords)

#This generally updates a dictionary with the number of words inside
#O(n^2) time
def countWord(lstLines, dicWords):
    #for every line in the html page
    for strLine in lstLines:
        #If it starts with "<p>", then we know it has paragraphs
        if(strLine.strip().endswith("<p>")):
            blnParse = True
        if(strLine.strip()==("</p>")):
            blnParse = False
            
        #if it's time to parse the paragraph, then...
        if(blnParse==True and not strLine.strip().endswith("<p>")):
            #if it's not in the dictionary, make it 1
            if(strLine not in dicWords):
                dicWords[strLine]=1
            #otherwise, add 1
            else:
                dicWords[strLine]+=1

#This function checks if a directory exists and deletes it
#O(n^n) time
def recursiveDeleteDirectory(strDirectory):
    for entry in os.listdir(strDirectory):
        print(entry)
        if os.path.isdir(os.path.join(strDirectory,entry)):
            recursiveDeleteDirectory(os.path.join(strDirectory,entry))
        elif os.path.isfile(os.path.join(strDirectory,entry)):
            os.remove(os.path.join(strDirectory,entry))
    os.rmdir(strDirectory)

#O(1)
def createNewDirectory(strDirectory):
    #If the directory doesn't exist
    if not os.path.exists(strDirectory):
        #make a directory
        os.makedirs(strDirectory)

#This function creates files for every word and prints the number of times that word appears
#O(n) time
def createWordFile(strDirectory, dicWords, dicAllWords):
    #for every key value(word) inside the dicWords dictionary,
    for strWord in dicWords:
        #create the file name
        strFileName = strWord+".txt"
        #make the path
        ioPath = os.path.join(strDirectory,(strFileName))
        #open the file
        ioFile = open(ioPath, "w")
        #write the amount of times that word pops up into the file
        ioFile.write(str(dicWords[strWord]))
        #then close the file
        ioFile.close()
        #if the word isn't a part of dictionary of all words, then
        if(strWord not in dicAllWords):
            #make the word a key and make the value(number of times it comes up) 1
            dicAllWords[strWord]=1
        #if it's already a key but it pops up anyway, then we know the word occurs again
        else:
            #so we add 1
            dicAllWords[strWord]+=1

#This function creates a file for every word term frequency
#O(n) time
def record_tf(strDirectory,dicWords):
    #first, we read the number of total numbre of word
    ioPath = os.path.join(strDirectory,("total.txt"))
    ioFile = open(ioPath, "r")
    fltTotal = float(ioFile.readline());
    ioFile.close()

    #for every word in dicWords
    for strWord in dicWords:     
        #now, we record the term frequencies
        ioPath = os.path.join(strDirectory,(strWord+"tf.txt"))
        #open the file
        ioFile = open(ioPath, "w")
        #write into it
        ioFile.write(str(float(dicWords[strWord])/fltTotal))
        #then close the file
        ioFile.close()

#This function creates a file that prints out the total words in a page
#O(n) time
def createTotalWordFile(strDirectory, dicWords):
    #initialize the total
    intTotal=0
    #find the path
    strPath = os.path.join(strDirectory,("total.txt"))
    ioFile = open(strPath, "w")
    #for every word in dicWords
    for strWord in dicWords:
        #add the number of times a word apears into inttotal
        intTotal+=dicWords[strWord]
    
    #then print out 
    ioFile.write(str(intTotal))
    ioFile.close()

#O(n) time
def recordIDF(dicAllWords,dicPages):
    recursiveDeleteDirectory("IDF Values")
    createNewDirectory("IDF Values")
    intTotalDocuments = len(dicPages)
    #for every word in the dictionary of all words
    for strWord in dicAllWords:
        intNumberOfDocumentsWithWord = 0
        #enter the idf directory
        ioPath = os.path.join("IDF Values", strWord+"idf.txt")
        #create the IDF value for the word
        ioFile = open(ioPath,"w")
        ioFile.write(str(math.log2(intTotalDocuments/(1+dicAllWords[strWord]))))
        ioFile.close()

#O(1)
def createOutGoingLinksFile(dict):
    #make the file in the general directory
    file = open( "outgoinglinks.json", "w")
    json.dump(dict,file)
    file.close()
