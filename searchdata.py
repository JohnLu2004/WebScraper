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
    lstQueue = get_outgoing_links(URL)
    lstPages = []
    lstAllPages = []
    
    #for every link in the main page, we will...
    for strLinks in lstQueue:
        #get a list of all the links in the subpage of a page
        lstPages = get_outgoing_links(strLinks)
        #for every link in that subpage, we will...
        for strPage in lstPages:
            #if that link isn't in the pages part yet, then...
            if strPage not in lstAllPages:
                #add it to the list of pages
                lstAllPages.append(strPage)
    #return a list of all the pages in subpages
    return lstAllPages

def get_page_rank(URL):
    return -1

def get_idf(word):
    intTotalDocuments=1
    intNumberOfDocumentsWithWord=1
    return intTotalDocuments/(1+intNumberOfDocumentsWithWord)
    
def get_tf(URL, word):
    #make some variables
    dicWords = {}
    strWord = ""
    intFrequency = 0
    intTotalWords = 0
    
    #we read from the file
    file = open(URL[URL.rfind("/")+1:len(URL)]+".txt","r")
    strLine = file.readline()
    
    #while there's still stuff to read
    while(strLine!=""):
        #eg. strLine = "apple:4"
        #make the word equal to what comes before the :
        strWord = strLine[0:strLine.find(":")
        #make the frequency equal to what comes after the :
        intFrequency = int(strLine[strLine.find(":")+1:len(strLine)])
        
        #add the word to the dictionary and to total words
        dicWords[strWord]=intFrequency
        intTotalWords+=intFrequency
    
    #if the word is in the dictionary, return the term frequency calculation
    if(word in dicWords):
        intOccurences = dicWords[word]
        return intOccurences/intTotalWords
    #otherwise, return 0
    else:
        return -1

def tf_idf(URL, word):
    return 1