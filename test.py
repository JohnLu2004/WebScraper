import crawler
import search
import searchdata
import webdev
import time
start = time.time()
print(crawler.crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))
end = time.time()
print("crawl:",end-start)

# start = time.time()
# print(search.search("coconut coconut orange blueberry lime lime lime tomato",True))
# end = time.time()
# print("get_page_rank:",end-start)


# print("hk")