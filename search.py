import math
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
    
    #Now, we calculate the tf-idf
    for strSearchWord in dicSearchWords:
        dicSearchWords[strSearchWord][2]=math.log2(dicSearchWords[strSearchWord][0]/intTotalWords)*get_idf(dicSearchWords[strSearchWord][0])
    
    #calculate the cosine similarity for all websites
    for URL in lstWebsites:
        #inside a loop, we calculate the stuff we need
        #we'll need some variables to keep track of the answer
        fltNumerator = 0.0
        fltDenominator = 1.0
        
        #calculate the numerator    
        #we're gonna want to get the tf-idf of the word from every doc and compare
        fltNumerator+=query tf-idf * website tf-idf
        
        #calculate the denominator
        fltDenominator*=sqrt(queryword1 tf-idf * queryword1 tf-idf + queryword2 tf-idf * queryword2 tf-idf)
        fltDenominator*=sqrt(doc1word1 tf-idf * docw1word1 tf-idf + doc1word2 tf-idf * doc1word2 tf-idf)
        fltDenominator*=sqrt(doc2word1 tf-idf * docw2word1 tf-idf + doc2word2 tf-idf * doc2word2 tf-idf)
        
        #calculate the final product
        url consine similarity = fltNumerator/fltDenominator
        
        
    #do a sort
    
    #return top 10
    
    
    print(lstSearchWords)

search("hi",True)