#this function returns a list of links
def get_outgoing_links(seed):
    
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