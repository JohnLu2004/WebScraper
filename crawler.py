import webdev
def crawl(seed):
    #first, make a list of all the links we've gone to
    #it'll only have the seed first
    lstPagesVisited=[seed]
    lstQueue = []
    dicPages = {}
    
    
    dicPages[seed]=getLinks(seed)
    for strLinks in dicPages[seed]:
        #add these links to the page
        lstQueue.append[strLinks]
            
    
    #while there's still something in the queue
    while(len(lstQueue)>0):
        #go through the links we need to go through
        for strSubPage in lstQueue
            #since we're going to be on that page, let's add it to the pages we've visited
            lstPagesVisited.append(strSubPage)
            #If the links found in page aren't in the queue or in the pages visited, add it to the list
            dicPages[strSubPage]=getLinks(strSubPage)
            for strLink in dicPages[strSubPage]:
                #if it's not in the queue already and not in the pages visited, then
                if((strLink not in lstQueue) and (strLink not in lstPagesVisited)):
                    lstQueue.append(strLink)
            
            
            
    #I put the hrefs into a list(queue)
    for strLink in lstQueue:
        print(strLink)
    
    #the number of pages we visited will be the number of pages there are since we visited all of them
    return len(lstQueue)

#this function returns a list of links
def getLinks(strPage):
    
    #We'll open up the file for reading
    lstLines=webdev.read_url(seed).strip().split("\n")
    
    #I'll also have 2 variables to keep track of the beginning and end of a link
    intStart = 0
    intEnd = 0
    
    strBeginning = seed[0:seed.rfind("/")]
    strLink = ""
    
    
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