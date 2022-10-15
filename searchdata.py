import webdev
import os
import math
import matmult

#this function returns a list of links
def get_outgoing_links(URL):
    
    #We'll open up the file for reading
    lstLines=webdev.read_url(URL).strip().split("\n")
    
    #I'll also have 2 variables to keep track of the beginning and end of a link
    intStart = 0
    intEnd = 0
    
    
    strBeginning = URL[0:URL.rfind("/")+1]
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
    
def get_incoming_links(URL):
    # for John: the previous algorithm is problemetic. While this one seems to work, it's a bit slow. We can think of other ways if time permits.
    incomingLinks = []
    filein = open("pages.txt", "r")
    #lstQueue is all the files that could contain incoming links of the URL
    lstQueue = filein.readlines()
    filein.close()
    
    for link in lstQueue:
        link = link.strip()
        if URL in get_outgoing_links(link) and not (link in incomingLinks):
            incomingLinks.append(link)
            continue
    return incomingLinks

def get_page_rank(URL):
    # page rank for all the URLs
    alpha = 0.1
    euclideanDistThreshold = 0.0001
    
    row = [] # row of the adjacency matrix
    adjacencyMatrix = [] # N * N matrix
    dict = {} # id -> link, e.g, 1:'http://.../N-3.html'
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
    
    # create adjacency matrix
    adjacencyMatrix = [-1] * len(dict)
    row = [-1] * len(dict)
    for id in dict:
        for link in reversedDict:
            if link in get_outgoing_links(dict[id]):
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
    
    # reversedDict: key=url, value=id. So finalPageRankVector[0][id] is the page rank result for the url with this id
    if URL in reversedDict:
        return finalPageRankVector[0][reversedDict[URL]]
    else:
        return -1

def get_idf(word):
    #initialize variables
    intNumberOfDocumentsWithWord=1
    intTotalDocuments=0
    #so we're going to check which pages in the pages.txt file has the word
    for page in lstPages:
        strDirectory = page
        if os.path.isdir(strDirectory):
            strFile = word+".txt"
            strPath = os.path.join(strDirectory, strFile)
            if os.path.isfile(strPage):
                intNumberOfDocumentsWithWord+=1
        intTotalDocuments+=1
    
    #i forgot to use the log function on this. 
    return math.log2(intTotalDocuments/(1+intNumberOfDocumentsWithWord))
    
def get_tf(URL, word):
    #we make the 2 variables we need
    fltWord = 1
    fltTotal = 1
    #we go into the directory with the URL name
    strDirectory = URL[URL.rfind("/")+1:len(URL)-5]
    if os.path.isdir(strDirectory):
        strFile = (word+".txt")
        strPath = os.path.join(strDirectory, strFile)
        if os.path.isfile(strPath):
            #we go into the word file
            ioFile = open(strPath, "r")
            #we read that word file
            fltWord = int(ioFile.read())
            ioFile.close()
        #read the total words file
        strFile = ("total.txt")
        strPath = os.path.join(strDirectory, strFile)
        if os.path.isfile(strPath):
            #we go into the word file
            ioFile = open(strPath, "r")
            #we read that word file
            fltTotal = int(ioFile.read())
            ioFile.close()
    return fltWord/fltTotal

def tf_idf(URL, word):
    return math.log10(1+get_tf(URL, word))*get_idf(word)