import webdev
def crawl(seed):
    #first, make a list of all the links we've gone to
    #it'll only have the seed first
    lstPagesVisited=[seed]
    lstQueue = []
    dicPages = {}
    
    
    dicPages[seed]=getLinks(seed)
    for strLink in dicPages[seed]:
        #add these links to the page
        lstQueue.append(strLink)
            
    
    #while there's still something in the queue
    while(len(lstQueue)>0):
        #each time we go through one link
        strSubPage = lstQueue[0]
        #If the links found in page aren't in the queue or in the pages visited, add it to the list
        dicPages[strSubPage]=getLinks(strSubPage)
        #since we've gone on that page, let's add it to the pages we've visited
        lstPagesVisited.append(strSubPage)
        lstQueue.pop(0)
        for strLink in dicPages[strSubPage]:
            #if it's not in the queue already or not in the pages visited, then
            if((strLink not in lstQueue) and (strLink not in lstPagesVisited) and (strLink not in dicPages)):
                lstQueue.append(strLink)
    
    # for key in dicPages:
    #     print(key)
    #the number of pages we visited will be the number of pages there are since we visited all of them
    return len(dicPages)

#this function returns a list of links
def getLinks(seed):
    
    #We'll open up the file for reading
    lstLines=webdev.read_url(seed).strip().split("\n")
    
    #I'll also have 2 variables to keep track of the beginning and end of a link
    intStart = 0
    intEnd = 0
    
    
    strBeginning = seed[0:seed.rfind("/")+1]
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