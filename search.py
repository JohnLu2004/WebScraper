import math
import searchdata
import os
def search(phrase, boost):
    strPhrase = input("Enter search word(s): ")
    lstSearchWords = strPhrase.split()
    
    #this variable will be useful for storing query info
    # word : [count,tf-idf]
    # apple : [5,0.6]
    dicSearchWords = {}
    
    intTotalWords = 0
    
    #with this, we can record the number of times a word appears
    #we can also record the total number of words
    for strSearchWord in lstSearchWords:
        if(strSearchWord not in dicSearchWords):
            dicSearchWords[strSearchWord]=[1,0]
        elif(strSearchWord in dicSearchWords):
            dicSearchWords[strSearchWord][0]+=1
        intTotalWords+=1
    
    #Now, we calculate the tf-idf for the query
    for strSearchWord in dicSearchWords:
        if os.path.isdir("IDF Values"):
            ioPath = os.path.join("IDF Values", strSearchWord+"idf.txt")
            if os.path.isfile(ioPath):
                ioFile = open(ioPath, "r")
                dicSearchWords[strSearchWord][1]=float(ioFile.readline())
                ioFile.close()

    #this array will keep track of the name of the URL and the cosine similarity score
    lstSimilarity =[]
    ioFile = open("pages.txt","r")
    strURL = ioFile.readline()
    while(strURL!=""):
        lstSimilarity.append([strURL])
        strURL = ioFile.readline()
    ioFile.close()
    
    #calculate the cosine similarity for all websites
    for intIndex in range(len(lstSimilarity)):
        #inside a loop, we calculate the stuff we need
        #we'll need some variables to keep track of the answer
        fltNumerator = 0.0
        fltDenominator = 1.0
        
        #calculate the numerator    
        #we're gonna want to get the tf-idf of the word from every doc and compare

        for strSearchWord in dicSearchWords:
            fltNumerator+=dicSearchWords[strSearchWord][1] * dicSearchWords[strSearchWord][1]
        
        #calculate the denominator
        for strSearchWord in dicSearchWords:
            fltDenominator*=math.sqrt(float(dicSearchWords[strSearchWord][1])*float(searchdata.tf_idf(lstSimilarity[intIndex][0],strSearchWord)))

        #calculate the final product
        if(fltDenominator==0):
            lstSimilarity[intIndex].append(0)
        else:
            lstSimilarity[intIndex].append(fltNumerator/fltDenominator)
    
    lstSorted = []
    #do a sort
    for i in range(10):
        strURL = ""
        fltSimilarity=0.0
        intIndex = 0
        for x in range(len(lstSimilarity)):
            if(lstSimilarity[x][1]>fltSimilarity):
                strURL=lstSimilarity[x][0]
                fltSimilarity=lstSimilarity[x][1]
                intIndex=x
        lstSorted.append([strURL])
        lstSorted[i].append(fltSimilarity)
        lstSimilarity.pop(intIndex)
    
    #return top 10
    lstSearchWords.sort()
    for i in range(len(lstSorted)):
        print(lstSorted[i][0],":",lstSorted[i][1])
    return lstSorted
search("d",True)