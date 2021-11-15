import requests
from bs4 import BeautifulSoup
from lxml import etree
from selenium  import webdriver
import csv
import time
import pymongo
import re
import random

Client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db=Client["pymongodb"]
col=db["dbfilmm"]
#提取适才mongo中爬取的所有电影名称，制作百度搜索网页
filenames=[]
sosuos=[]
flag=0
for x in col.find():
    ppp=x["电影"]
    lll=x["url"]
    if ppp=="肖申克的救赎 The Shawshank Redemption":
        flag=1
        #continue
    if flag:
        filenames.append(ppp)
        sosuos.append(lll)
print(len(filenames))


driver = webdriver.Chrome("chromedriver")
kk=0
col=db["db"]
for baseurl in sosuos:
   js="window.open('{}','_blank');"
   driver.execute_script(js.format(baseurl))
   #time.sleep(15)
   if kk:
      driver.switch_to.window(driver.window_handles[-2])
      driver.close()
   driver.switch_to.window(driver.window_handles[-1])
   driver.implicitly_wait(3)

   print(driver.current_url)
   if(len(driver.find_elements_by_xpath("//*[@id=\"info\"]/span[3]/span[2]/a"))!=0):
      stringeg=driver.find_elements_by_xpath("//*[@id=\"info\"]/span[3]/span[2]/a")[-1].text
      if stringeg[0:2]=="更多":
         driver.find_elements_by_xpath("//*[@id=\"info\"]/span[3]/span[2]/a")[-1].click()
   if(len(driver.find_elements_by_xpath("//*[@id=\"link-report\"]/span[1]/a"))!=0):
      stringeg=driver.find_elements_by_xpath("//*[@id=\"link-report\"]/span[1]/a")[-1].text
      if stringeg[1:5]=="展开全部":
         driver.find_elements_by_xpath("//*[@id=\"link-report\"]/span[1]/a")[-1].click()
     
   news=driver.find_elements_by_xpath("//*[@id=\"info\"]")[-1].text
   #regs=regions.text
   print(news)

   about=driver.find_elements_by_xpath("//*[@id=\"link-report\"]")[-1].text
   #regs=regions.text
   print(about)
   
   awards=driver.find_elements_by_xpath("//*[@id=\"content\"]/div[3]/div[1]/div[8]/ul")
   if len(awards)==0:
      awards=driver.find_elements_by_xpath("//*[@id=\"content\"]/div[2]/div[1]/div[8]/ul")
   stringa=""
   for award in awards:
      stringa+=award.text+"\n"
   stringa=stringa[:-1]
   print(stringa)

   score=driver.find_elements_by_xpath("//*[@id=\"interest_sectl\"]/div[1]/div[2]/strong")[-1].text
   print(score)

   scorepeople=driver.find_elements_by_xpath("//*[@id=\"interest_sectl\"]/div[1]/div[2]/div/div[2]/a/span")[-1].text
   print(scorepeople)
   d1={}
   d1["name"]=filenames[kk]
   d1["url"]=baseurl
   d1["xinxi"]=news
   d1["about"]=about
   d1["awards"]=stringa
   d1["score"]=score
   d1["scorepeople"]=scorepeople
   col.insert_one(d1)
   kk+=1


print("豆瓣收工")
driver.quit()