from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from selenium.webdriver.common.keys import Keys
import datetime as dt
import urllib.parse

#binary=FirefoxBinary('C:/Program Files/Mozilla Firefox/firefox.exe')
#driver=webdriver.Firefox(executable_path='C:/Users/DELL/Documents/Python/geckodriver.exe',firefox_binary=binary)
path = r"/Users/ksy/Desktop/text2moji/crawling/chromedriver"
driver = webdriver.Chrome(path)

# 검색을 위한 변수 설정 
startdate=dt.date(year=2017,month=12,day=24)
untildate=dt.date(year=2017,month=12,day=25)
enddate=dt.date(year=2017,month=12,day=25)

totalfreq=[]
tweet_bag=[]

emojis = []
emojis.append('%f0%9f%91%8c') #sample
#for emoji in emojis:
emoji = '%f0%9f%91%8c'
for i in range(1):
#while enddate != startdate:
    url = f"https://twitter.com/search?q={emoji}&src=typd&lang=ko"
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    for j in range(1):
    #while True:
        dailyfreq={'Date':startdate}
        wordfreq=0
        tweets = soup.find_all("p", {"class": "TweetTextSize"})
        wordfreq += len(tweets)
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    
        newHeight = driver.execute_script("return document.body.scrollHeight")
        print(newHeight)
        if newHeight != lastHeight:
            html = driver.page_source
            soup = BeautifulSoup(html,'html.parser')
            tweets = soup.find_all("p", {"class": "TweetTextSize"})
            wordfreq = len(tweets)
            tweet_bag.append(tweets)
        else:
            dailyfreq['Frequency'] = wordfreq
            wordfreq = 0
            totalfreq.append(dailyfreq)
            startdate = untildate
            untildate += dt.timedelta(days = 1)
            dailyfreq = {}
            break
        lastHeight = newHeight

driver.close()
for tweet in tweet_bag:
    print(tweet)
