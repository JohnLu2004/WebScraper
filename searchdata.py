import webdev
import os
import math
import json

#this function searches outgoing links from the outgoinglinks.json file
def get_outgoing_links(URL):
    filein = open("outgoinglinks.json", "r")
    dicOutGoingLinks = json.load(filein)
    filein.close()
    
    if URL in dicOutGoingLinks:
        return dicOutGoingLinks[URL]
    else:
        return None
    
def get_incoming_links(URL):

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

    if incomingLinks != []:
        return incomingLinks
    else:
        return None

def get_page_rank(URL):
    filein = open("pagerank.json", "r")
    dicPageRank = json.load(filein)
    filein.close()

    if URL in dicPageRank:
        return dicPageRank[URL]
    else:
        return -1

def get_idf(word):
    fltIDF = 0
    #so we're going to go into the IDF Value folder
    strFile = word+"idf.txt"
    ioPath = os.path.join("IDF Values", strFile)
    if os.path.exists(ioPath):
        ioFile = open(ioPath,"r")
        fltIDF = float(ioFile.readline())
        ioFile.close()
    #i forgot to use the log function on this. 
    return fltIDF
    
def get_tf(URL, word):
    fltTF=0
    #we go into the directory with the URL name
    prtDirectory = "crawling"
    strDirectory = os.path.join(prtDirectory,URL[URL.rfind("/")+1:len(URL)-5])
    if os.path.isdir(strDirectory):
        #if it's a directory, go ahead
        ioFile = (word+"tf.txt")
        ioPath = os.path.join(strDirectory, ioFile)
        if os.path.isfile(ioPath):
            #we go into the word file
            ioFile = open(ioPath, "r")
            #we read that word file
            fltTF = float(ioFile.read())
            ioFile.close()
    return fltTF

def get_tf_idf(URL, word):
    return math.log2(1+get_tf(URL, word))*get_idf(word)