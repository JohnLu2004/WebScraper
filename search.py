import math
import searchdata

def search(phrase, boost):
    lstSearchWords = phrase.strip().split()
    
    # dicSearchWords is used to store query words info
    #       word : [count, tf-idf of this word in the query]
    # e.g., apple : [5,0.6]
    dicSearchWords = {}
    intTotalWords = len(lstSearchWords)
    
    #with this, we can record the number of times a word appears
    #we can also record the total number of words
    
    for strSearchWord in lstSearchWords:
        if(strSearchWord not in dicSearchWords):
            dicSearchWords[strSearchWord]=[1,0]
        elif(strSearchWord in dicSearchWords):
            dicSearchWords[strSearchWord][0]+=1
    
    #Now, we calculate the tf-idf for the query
    for strSearchWord in dicSearchWords:
        intTF = dicSearchWords[strSearchWord][0] / intTotalWords
        # intTFIDF = log2(1+intTF) * intIDF
        dicSearchWords[strSearchWord][1] = math.log2(1+intTF) * float(searchdata.get_idf(strSearchWord))

    # lstResults is a list of dictionaries
    # dicPage is each entry in lstResults that tracks url, title and (search) score for the page
    lstResults =[]
    dicPage = {}

    # store url and title to lstResults
    ioFile = open("pages.txt","r")
    strURL = ioFile.readline().strip()
    while(strURL!=""):
        dicPage["url"] = strURL
        dicPage["title"] = strURL[strURL.rfind("/")+1:len(strURL)-5]
        lstResults.append(dicPage)
        strURL = ioFile.readline().strip()
        dicPage = {}
    ioFile.close()
    
    # calculate the cosine similarity for all websites
    for intIndex in range(len(lstResults)):

        fltNumerator = 0
        fltDenominator = 0
        fltSumSqrDocTFIDF = 0
        fltSumSqrQryTFIDF = 0
            
        for strSearchWord in dicSearchWords:
            fltDocTFIDF = float(searchdata.get_tf_idf(lstResults[intIndex]["url"], strSearchWord))
            fltQryTFIDF = dicSearchWords[strSearchWord][1]

            # calculate the numerator
            fltNumerator += fltDocTFIDF * fltQryTFIDF

            # calculate the denominator factors
            fltSumSqrDocTFIDF += fltDocTFIDF**2
            fltSumSqrQryTFIDF += fltQryTFIDF**2
        
        # calculate the denominator
        fltDenominator = math.sqrt(fltSumSqrDocTFIDF * fltSumSqrQryTFIDF)

        # calculate the final result
        if(fltDenominator == 0):
            lstResults[intIndex]["score"] = 0
        else:
            score = fltNumerator/fltDenominator
            if boost:
                # score multiplied by page rank
                score *= searchdata.get_page_rank(lstResults[intIndex]["url"])
            lstResults[intIndex]["score"] = score

    # sort top 10 similar pages
    lstSorted = []
    if (len(lstResults) >= 10):
        for i in range(10):
            fltScore = -1
            intIndex = 0
            dicPage = {}
            for j in range(len(lstResults)):
                if(float(lstResults[j]["score"]) > fltScore):
                    dicPage = lstResults[j]
                    fltScore = float(lstResults[j]["score"])
                    intIndex = j
            lstSorted.append(dicPage)
            lstResults.pop(intIndex)
    
    # return top 10 pages
    return lstSorted

