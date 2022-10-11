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