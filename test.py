import crawler
import search
import searchdata
import webdev
import time
start = time.time()
print(crawler.crawl("http://people.scs.carleton.ca/~davidmckenney/fruits/N-0.html"))
end = time.time()
print("crawl:",end-start)

start = time.time()
print(search.search("apple",True))
end = time.time()
print("search:",end-start)