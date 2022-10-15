from genericpath import isdir
import webdev
import searchdata
import os
import json

prtDirectory = "crawling"

def crawl(seed):
    #first, make a list of all the links we've gone to
    #it'll only have the seed first
    lstPagesVisited=[seed]
    lstQueue = []
    dicPages = {}
    
    dicPages[seed]=searchdata.get_outgoing_links(seed)

    # reset directory "crawling"
    if os.path.isdir(prtDirectory):
        for subDirectory in os.listdir(prtDirectory):
            deleteOlderDirectory(os.path.join(prtDirectory,subDirectory))
        deleteOlderDirectory(prtDirectory)
    createNewDirectory(prtDirectory)

    recordInformation(seed)
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
        recordInformation(strSubPage)
        lstQueue.pop(0)
        for strLink in dicPages[strSubPage]:
            #if it's not in the queue already or not in the pages visited, then
            if((strLink not in lstQueue) and (strLink not in lstPagesVisited) and (strLink not in dicPages)):
                lstQueue.append(strLink)
    
    #record the pages we've been to
    recordPages(dicPages)

    #record outgoing links
    createOutGoingLinksFile(dicPages)
    
    #the number of pages we visited will be the number of pages there are since we visited all of them
    return len(lstPagesVisited)

#this function will write down the info into a file
#O(n) time due to function called that is O(n)
def recordInformation(strSubPage):
    #We'll open up the file for reading
    lstLines=webdev.read_url(strSubPage).strip().split("\n")
    intIndex=0
    lstWords = []
    dicWords={}
    blnParse = False
    
    #we'll read the whole thing
    countWord(lstLines, dicWords)
    
    #create new directory
    strDirectory = strSubPage[strSubPage.rfind("/")+1:len(strSubPage)-5]
    createNewDirectory(os.path.join(prtDirectory, strDirectory))
    
    #create a file and then write into it
    createWordFile(os.path.join(prtDirectory, strDirectory),dicWords)
    
    #create a file that keeps track of how many words there are
    createTotalWordFile(os.path.join(prtDirectory, strDirectory),dicWords)

    #create a file that records outgoing links
    createOutGoingLinksFile(strDirectory)
    
    return None

#This generally updates a dictionary with the number of words inside
#O(n) time
def countWord(lstLines, dicWords):
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
    return None

#This function checks if a directory exists and deletes it
#O(1) time
def deleteOlderDirectory(strDirectory):
    if os.path.isdir(strDirectory):
        files = os.listdir(strDirectory)
        for file in files:
            os.remove(os.path.join(strDirectory,file))
        os.rmdir(strDirectory)
    return None

def createNewDirectory(strDirectory):
    if not os.path.exists(strDirectory):
        os.makedirs(strDirectory)
    return None

#This function creates files for every word and prints the number of times that word appears
#O(n) time
def createWordFile(strDirectory, dicWords):
    for strWord in dicWords:
        strFileName = strWord
        file_path = os.path.join(strDirectory,(strFileName+".txt"))
        fileout = open(file_path, "w")
        fileout.write(str(dicWords[strWord]))
        fileout.close()

#This function creates a file that prints out the total words in a page
#O(n) time
def createTotalWordFile(strDirectory, dicWords):
    intTotal=0
    strPath = os.path.join(strDirectory,("total.txt"))
    fileout = open(strPath, "w")
    for strWord in dicWords:
        intTotal+=dicWords[strWord]
    
    fileout.write(str(intTotal))
    fileout.close()
    return None

#This function records the pages that we've been to
#O(n) time
def recordPages(dicPages):
    #make the file in the general directory
    file = open("pages.txt","w")
    #write the page name into the file
    for strPage in dicPages:
        file.write(strPage+"\n")
    file.close()
    return None

def createOutGoingLinksFile(dict):
    #make the file in the general directory
    file = open( "outgoinglinks.json", "w")
    json.dump(dict,file)
    file.close()
    return None