from selenium  import webdriver
import csv
import time
import pymongo

Client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db=Client["pymongodb"]
col=db["dbfilm"]

#数据采集目标首先提取电影名称
#https://www.douban.com/doulist/45793279/?start=0&sort=seq&playable=0&sub_type=    这是豆瓣评分最多的550余部电影
#豆瓣网站爬虫变式太多，需要随机应变

driver = webdriver.Chrome("chromedriver")

for i in range(22):
    href1="https://www.douban.com/doulist/45793279/?start="
    href2="&sort=seq&playable=0&sub_type="
    js="window.open('{}','_blank');"
    driver.execute_script(js.format(href1+str(i*25)+href2))
    if i:
        driver.switch_to.window(driver.window_handles[-2])
        driver.close()
    driver.switch_to.window(driver.window_handles[-1])
    driver.implicitly_wait(10)
    print(driver.current_url)
    print(str(i+1)+"页")
    
    for ii in range(7,7+25):
        ## /html/body/div[3]/div[1]/div/div[1]/div[7]/div/div[2]/div[4]/a/text()
        ## /html/body/div[3]/div[1]/div/div[1]/div[8]/div/div[2]/div[3]/a/text()
        ##/html/body/div[3]/div[1]/div/div[1]/div[13]/div/div[2]/div[3]/a
        ##/html/body/div[3]/div[1]/div/div[1]/div[14]/div/div[2]/div[4]/a/text()
        ##/html/body/div[3]/div[1]/div/div[1]/div[15]/div/div[2]/div[4]/a/text()
        dict1={}
        
        num=len(driver.find_elements_by_xpath("/html/body/div[3]/div[1]/div/div[1]/div[%d]/div/div[2]/div/a"%ii))
        if num>3:
            num=4
        while driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div[1]/div[{0}]/div/div[2]/div[{1}]/a".format(ii,num)).text=="":
            num+=1
        dict1["电影"]=driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div[1]/div[{0}]/div/div[2]/div[{1}]/a".format(ii,num)).text
        dict1["url"]=driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div[1]/div[{0}]/div/div[2]/div[{1}]/a".format(ii,num)).get_attribute("href")
        print(dict1)
        col.insert_one(dict1)
    #/html/body/div[3]/div[1]/div/div[1]/div[8]/div/div[2]/div[5]/a
    #/html/body/div[3]/div[1]/div/div[1]/div[8]/div/div[2]/div[4]/a
    # for window in driver.window_handles:
    #     if window != driver.window_handles[-1]:
    #         driver.close() #关闭该窗口
print("豆瓣收工")
driver.quit()

