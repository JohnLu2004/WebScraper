import webdev
import os
import math

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
    # # page rank for all the URLs
    
    # adjacencyMatrix = []
    # dict = {}
    # count = 0
    # filein = open("pages.txt", "r")
    # link = filein.readline().strip()
    # while link != "":
    #     dict[count] = link
    #     get_outgoing_links(link)
        
    #     count += 1

    
    # filein.close()
    # alpha = 0.1
    # euclideanDistThreshold = 0.0001
    # # mapping from matrix to URL:
    # # 0 -> N-0 ..
    
    # print(get_outgoing_links(URL))
    # print(get_incoming_links(URL))
    # # adjacency matrix
    
    
    # # page rank for this URL
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
    return get_idf(word)*get_tf(URL, word)