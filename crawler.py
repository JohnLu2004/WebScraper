import math
import webdev
import os
import json
import matmult

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
    #dicIncomingLinks will record incoming links of the pages
    dicIncomingLinks = {}

    # reset directory "crawling"
    resetInformation()

    #every time we come across a page, we add it to pages.txt
    ioPagesFile = open("pages.txt", "a")
    lstQueue.append(seed)

    
    #while there's still something in the queue
    while(len(lstQueue)>0):
        #each time we go through one link
        strSubPage = lstQueue[0]
        #If the links found in page aren't in the queue or in the pages visited, add it to the list
        outGoingLinks = getOutgoingLinks(strSubPage)
        dicPages[strSubPage] = outGoingLinks
        # add the links to the dictionary of incoming list
        for url in outGoingLinks:
            dictValueAppendElement(dicIncomingLinks, url, strSubPage)
        #since we've gone on that page, let's add it to the pages we've visited
        lstPagesVisited.append(strSubPage)
        #We then add the page we've just visited to the text file
        ioPagesFile.write(strSubPage+"\n")
        
        #this function records all the info we need in searchdata.py
        recordInformation(strSubPage, dicAllWords)
        #we then get rid of the website we've just visitied which is at lstQueue[0]
        lstQueue.pop(0)
        #for every link inside the page we're on, 
        for strLink in dicPages[strSubPage]:
            #if it's not in the queue already and not a key in dicPages visited, then
            if((strLink not in dicPages) and (strLink not in lstQueue)):
                #add that page to the queue
                lstQueue.append(strLink)
    #after we're done going through all the pages, close pages.txt
    ioPagesFile.close()

    #record outgoing links and incoming links
    recordOutgoingLinksFile(dicPages)
    recordIncomingLinksFile(dicIncomingLinks)
    
    #Now that we have the pages we've been to, we can do the easy bit of recording IDF values
    recordIDF(dicAllWords, dicPages)

    #create page rank file
    createPageRankFile()

    #the number of pages we visited will be the number of pages there are since we visited all of them
    return len(lstPagesVisited)

#O(n^m) due to finite number of processes
def resetInformation():
    # reset directory "crawling"
    if os.path.isdir(prtDirectory):
        recursiveDeleteDirectory(prtDirectory)
    #then create a new directory
    createNewDirectory(prtDirectory)
    #reset directory "IDF Values"
    if os.path.isdir("IDF Values"):
        recursiveDeleteDirectory("IDF Values")
    #then create a new directory
    createNewDirectory("IDF Values")
    #we need to reset what's inside the pages.txt file
    os.remove("pages.txt")

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
    
    # create new directory
    strDirectory = strSubPage[strSubPage.rfind("/")+1:len(strSubPage)-5]
    # joining parent directory
    strDirectory = os.path.join(prtDirectory, strDirectory)

    # recursiveDeleteDirectory(strDirectory)
    createNewDirectory(strDirectory)
    
    #create a file and then write into it
    recordWordCount(strDirectory,dicWords,dicAllWords)
    
    #create a file that keeps track of how many words there are
    recordTotalWordCount(strDirectory,dicWords)

    #store the term frequency
    record_tf(strDirectory,dicWords)

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
def recordWordCount(strDirectory, dicWords, dicAllWords):
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
def recordTotalWordCount(strDirectory, dicWords):
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

def getOutgoingLinks(url):
    lstLines = webdev.read_url(url).strip().split("\n")
    #I'll also have 2 variables to keep track of the beginning and end of a link
    intStart = 0
    intEnd = 0
    
    strBeginning = url[0:url.rfind("/")+1]
    strLink = ""
    lstLinks=[]
    
    #we'll read the whole thing
    for strLine in lstLines:
        #If it starts with "<a href", then we know it has a link to another pages
        if(strLine.startswith("<a href")):
            #find the index of the first "
            intStart = strLine.find('"')
            #find the index of the last "
            intEnd = strLine.rfind('"')
            #everything in between the " " will be the link
            strLink = strLine[intStart+1:intEnd]
            
            #If it's a relative link(it starts with "./", we'll add the absolute start onto the name of it
            #Instead of "./N-0.html
            if(strLink.startswith("./")):
                #It will be https://scs.carleton.N-0.html now I think
                strLink = strBeginning+strLink[2:len(strLink)]
            #now we add the link to our list of links
            lstLinks.append(strLink)
    return lstLinks

#O(1)
def recordOutgoingLinksFile(dict):
    #make the file in the general directory
    file = open( "outgoinglinks.json", "w")
    json.dump(dict,file)
    file.close()

def recordIncomingLinksFile(dict):
    #make the file in the general directory
    file = open( "incominglinks.json", "w")
    json.dump(dict,file)
    file.close()

# create a dictionary with all the urls and their page rank and store it in a json file 
def createPageRankFile():
    # page rank for all the URLs
    alpha = 0.1
    euclideanDistThreshold = 0.0001
    
    row = [] # row of the adjacency matrix
    adjacencyMatrix = [] # N * N matrix
    dict = {} # id -> link, e.g., 1:'http://.../N-3.html'
    reversedDict = {} # link -> id, e.g., 'http://.../N-3.html':1
    
    # create dict and reverse dict
    count = 0
    filein = open("pages.txt", "r")
    link = filein.readline().strip()
    while link != "":
        dict[count] = link
        reversedDict[link] = count
        count += 1
        link = filein.readline().strip()
    filein.close()
    
    # load outgoing links
    file = open("outgoinglinks.json", "r")
    outgoinglinks = json.load(file)
    file.close()

    # create adjacency matrix
    adjacencyMatrix = [-1] * len(dict)
    row = [-1] * len(dict)
    for id in dict:
        for link in reversedDict:
            if link in outgoinglinks[dict[id]]:
                row[reversedDict[link]] = 1
            else:
                row[reversedDict[link]] = 0
        adjacencyMatrix[id] = row
        row = [-1] * len(dict)
    
    # scaled adjacency matrix after adding alpha/N to each entry
    count = 0
    for i in range(len(adjacencyMatrix)):
        for j in range(len(adjacencyMatrix[0])):
            if adjacencyMatrix[i][j] == 1:
                count += 1
        if count == 0:
            for j in range(len(adjacencyMatrix[0])):
                adjacencyMatrix[i][j] = (1 / len(adjacencyMatrix)) * (1-alpha) + (alpha / len(adjacencyMatrix))
        else:
            for j in range(len(adjacencyMatrix[0])):
                adjacencyMatrix[i][j] = (adjacencyMatrix[i][j] / count) * (1-alpha) + (alpha / len(adjacencyMatrix))
        count = 0
    
    # power iteration with adjacency matrix
    # initialize iterating vector
    iteratingVector = [[1 / len(adjacencyMatrix)] * len(adjacencyMatrix)]
    
    # use modules of matmult in tutorial4 to calculate
    finalPageRankVector = matmult.mult_matrix(iteratingVector, adjacencyMatrix) 
    dist = matmult.euclidean_dist(finalPageRankVector, iteratingVector)

    # iterate until dist < euclideanDistThreshold when we find the stable final page rank vector
    while dist >= euclideanDistThreshold:
        iteratingVector = finalPageRankVector
        finalPageRankVector = matmult.mult_matrix(iteratingVector, adjacencyMatrix)
        dist = matmult.euclidean_dist(finalPageRankVector, iteratingVector)
    
    # write a json file contains all the page urls and their page rank.
    # key = url, value = page rank
    dicPageRank = {}
    for url in reversedDict:
        # reversedDict: key=url, value=id. So finalPageRankVector[0][id] is the page rank result for the url with this id
        dicPageRank[url] = finalPageRankVector[0][reversedDict[url]]
    fileout = open("pagerank.json", "w")
    json.dump(dicPageRank,fileout)
    fileout.close()

def dictValueAppendElement(dict, key, value):
    if not(key in dict):
        dict[key] = [value]
    else:
        dict[key].append(value)
