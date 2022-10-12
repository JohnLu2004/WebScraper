import webdev
import searchdata
def crawl(seed):
    #first, make a list of all the links we've gone to
    #it'll only have the seed first
    lstPagesVisited=[seed]
    lstQueue = []
    dicPages = {}
    
    
    dicPages[seed]=searchdata.get_outgoing_links(seed)
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
    lstLines=webdev.read_url(URL).strip().split("\n")
    intIndex=0
    lstWords = []
    dicWords={}
    
    #we'll read the whole thing
    while(lstLines[intIndex]!=""):
        #If it starts with "<p>", then we know it has a link to another pages
        if(lstLines[intIndex].startswith("<p>")):
            #go to the next line and put the words into a list
            intIndex+=1;
            for strWord in lstLines[intIndex].split():
                #if it's not in the dictionary, make it 1
                if(strWord not in dicWords):
                    dicWords[strWord]=1
                #otherwise, add 1
                else:
                    dicWords[strWord]+=1
        intIndex+=1
    
    #write this into a file
    file = open(URL[URL.rfind("/")+1:len(URL)]+".txt","w")
    for strWord in dicWord:
        file.write(strWord+":"+str(dicWords[strWord])
    file.close()
    return None