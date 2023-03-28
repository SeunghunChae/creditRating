from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from datetime import datetime

import re

import requests

import time
import csv

from rename import * #중복검색 이름 수정 함수

url1 = 'https://www.kisrating.com/ratingsSearch/corp_search.do'         #한국신용평가 searchKeyword
url2 = 'https://www.nicerating.com/disclosure/dayRatingNews.do'         #나이스신용평가
url3 = 'https://www.korearatings.com/cms/frCmnCon/index.do?MENU_ID=360' #한국기업평가


options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument('--disable-gpu')

service = Service('c:\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

company=[]
company.append('한국수력원자력')



driver.get(url3)
search=rename(3,'한국수력원자력')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#searchTxt')))
driver.find_element(By.CSS_SELECTOR, '#searchTxt').send_keys(search)
driver.find_element(By.CSS_SELECTOR, '#sub_total_search > div.input-group > button.btn.btn-search').click()
table='#mySheet-table > tbody > tr:nth-child(3) > td > div > div.GMPageOne > table > tbody'
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, table)))
table=driver.find_element(By.CSS_SELECTOR, table)
rows=table.find_elements(By.TAG_NAME, "tr")
rows[1].find_elements(By.TAG_NAME, "u")[0].click()
#클릭 겁나 복잡하네.. 검색 결과가 여러개 나올 시 맨 위에 목록 클릭함
WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tabBtn2')))
driver.find_element(By.CSS_SELECTOR, '#tabBtn2').click()
#등급 페이지 들어왔다.
WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tabcont2')))


try:
    cp3=[]
    tablecp=driver.find_element(By.CSS_SELECTOR, '#tabcont2 > div:nth-child(9) > div.title').text
    if '기업어음' in tablecp:
        cp3.append(['평가기준일','본_평가일','본_공시일','본_등급','수_평가일','수_공시일','수_등급','정_평가일','정_공시일','정_등급','유효기간'])
        table=driver.find_element(By.XPATH, '//*[@id="mySheet2-table"]/tbody/tr[3]/td/div/div[1]/table/tbody')
        rows=table.find_elements(By.TAG_NAME, "tr")

        del rows[0]
        k=1
        for i in rows:
            td=i.find_elements(By.TAG_NAME, "td")
            temp=[]
            temp.append(td[1].text)
            for j in range(4, 25):
                temp.append(td[j].text)

            #등급
            code1='document.querySelector("#tabcont2 > div:nth-child(9) > div.title").textContent='
            code2='document.querySelector("#mySheet2-table > tbody > tr:nth-child(3) > td > div > div.GMPageOne > table > tbody").childNodes['+str(k)+'].childNodes[12].textContent'
            code=code1+code2
            driver.execute_script(code)
            temp[9]=driver.find_element(By.CSS_SELECTOR, '#tabcont2 > div:nth-child(9) > div.title').text

            #유효기간
            code1='document.querySelector("#tabcont2 > div:nth-child(9) > div.title").textContent='
            code2='document.querySelector("#mySheet2-table > tbody > tr:nth-child(3) > td > div > div.GMPageOne > table > tbody").childNodes['+str(k)+'].childNodes[13].textContent'
            code=code1+code2
            driver.execute_script(code)
            temp[10]=driver.find_element(By.CSS_SELECTOR, '#tabcont2 > div:nth-child(9) > div.title').text
            
            k+=1

            cp3.append(temp)
            


        print("한기평 기업어음 :")        
        for i in cp3:
            print(i)

except Excption:
    print(1)
