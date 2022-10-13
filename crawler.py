import webdev
import searchdata
import os

def crawl(seed):
    #first, make a list of all the links we've gone to
    #it'll only have the seed first
    lstPagesVisited=[seed]
    lstQueue = []
    dicPages = {}
    
    
    dicPages[seed]=searchdata.get_outgoing_links(seed)
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
    
    
    #the number of pages we visited will be the number of pages there are since we visited all of them
    return len(lstPagesVisited)

#this function will write down the info into a file
def recordInformation(strSubPage):
    #We'll open up the file for reading
    lstLines=webdev.read_url(strSubPage).strip().split("\n")
    intIndex=0
    lstWords = []
    dicWords={}
    blnParse = False
    
    #we'll read the whole thing
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
    
    #delete old directories
    strDirectory = strSubPage[strSubPage.rfind("/")+1:len(strSubPage)-5]
    if os.path.isdir(strDirectory):
        files = os.listdir(strDirectory)
        for file in files:
            os.remove(os.path.join(strDirectory, file))
        os.rmdir(strDirectory)
    #create new directory
    os.makedirs(strDirectory)
    
    #create a file and then write into it
    for strWord in dicWords:
        strFileName = strWord
        file_path = os.path.join(strDirectory,(strFileName+".txt"))
        fileout = open(file_path, "w")
        fileout.write(str(dicWords[strWord]))
        fileout.close()
    return None