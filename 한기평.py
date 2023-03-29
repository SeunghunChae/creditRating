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

####################################검색 리스트 입력#######################################

file=open('input.dat', 'r', encoding='utf-8')

list_search=[]

while True:
    line=file.readline()

    #기업명에서 (구 xx)를 잘라내자
    if line.find('(')!=-1:
        idx=line.find('(')
        if len(line[0:idx].split())!=1:
            line=line[0:idx].split()
        else:
            line=line.split()
    else :
        line=line.split()
    
    if len(line)==0:
        print('===end===\n')
        break
    
    list_search.append(line)

file.close()


#########################################입력 끝###########################################
output=[]
no_exist=[]
multi=[]
nocp1=[]
nostb1=[]
nocp2=[]
nostb2=[]
nocp3=[]
nostb3=[]
overflow=[]

del list_search[0]

k=0
no_repeat=5

url1 = 'https://www.kisrating.com/ratingsSearch/corp_search.do'         #한국신용평가 searchKeyword
url2 = 'https://www.nicerating.com/disclosure/dayRatingNews.do'         #나이스신용평가
url3 = 'http://www.korearatings.com/cms/frDisclosureCon/compView.do?MENU_ID=90&CONTENTS_NO=1&COMP_CD=304944' #한국기업평가


for search in list_search:

    #메모리 누수를 막기위해 5번마다 크롬 드라이버를 끈다.
    if k%no_repeat==0:
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        service = Service('c:\chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=options)
    
    company=[]
    company.append(search[1])    
    company.append(search[0])
    print('회사명 : '+search[1]+"\n")


    
    ########한기평 시작#######
    search=rename(1,search[1])

    driver.get(url3)
    driver.find_element(By.XPATH, '//*[@id="COMNM"]').send_keys(search)
    driver.find_element(By.XPATH, '//*[@id="sendForm"]/div/div/div[1]/button').click()
    try:
        #등급 페이지 들어왔다.
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tabBtn2')))
        driver.find_element(By.CSS_SELECTOR, '#tabBtn2').click()
    except Exception:
        #여러건 검색됨 => 맨 위에꺼 클릭
        driver.find_element(By.XPATH, '//*[@id="mySheet-table"]/tbody/tr[3]/td/div/div[1]/table/tbody/tr[2]/td[2]/u').click()
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tabBtn2')))
        driver.find_element(By.CSS_SELECTOR, '#tabBtn2').click()
        

    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'ib-container2'))) 
        cp3=[]
        cp3.append(['평가기준일','본_평가일','본_공시일','본_등급','수_평가일','수_공시일','수_등급','정_평가일','정_공시일','정_등급','유효기간','변환등급'])
        table=driver.find_element(By.XPATH, '//*[@id="mySheet2-table"]/tbody/tr[3]/td/div/div[1]/table/tbody')
        rows=table.find_elements(By.TAG_NAME, "tr")

        #js코드로 h2태그에 값을 읽어서 가져온다.
        del rows[0]
        k=1 #rowcount
        for i in rows:
            temp=[]
            for j in range(1, 14):
                if j!=2 and j!=3:
                    code1='document.querySelector("#tabcont2 > div.grid-guide.mgb0 > span").textContent='
                    code2='document.querySelector("#mySheet2-table > tbody > tr:nth-child(3) > td > div > div.GMPageOne > table > tbody").childNodes['+str(k)+'].childNodes['+str(j)+'].textContent'
                    code=code1+code2
                    driver.execute_script(code)
                    temp.append(driver.find_element(By.CSS_SELECTOR, '#tabcont2 > div.grid-guide.mgb0 > span').text)
                    
            temp.append('')
            temp.append('')
            
            if cp3[k-1][9]!='':
                pos=9
            elif cp3[k-1][6]!='':
                pos=6
            elif cp3[k-1][3]!='':
                pos=3
            
            #변환등급
            if cp3[k-1][pos].find('A1')!=-1:
                temp.append('110')
            elif cp3[k-1][pos].find('A2+')!=-1:
                temp.append('120')
            elif cp3[k-1][pos].find('A2-')!=-1:
                temp.append('122')
            elif cp3[k-1][pos].find('A2')!=-1:
                temp.append('121')
            elif cp3[k-1][pos].find('A3+')!=-1:
                temp.append('130')
            elif cp3[k-1][pos].find('A3-')!=-1:
                temp.append('132')
            elif cp3[k-1][pos].find('A3')!=-1:
                temp.append('131')
            elif cp3[k-1][pos].find('B+')!=-1:
                temp.append('210')
            elif cp3[k-1][pos].find('B-')!=-1:
                temp.append('212')
            elif cp3[k-1][pos].find('B')!=-1:
                temp.append('211')
            elif cp3[k-1][pos].find('C')!=-1:
                temp.append('310')
            elif cp3[k-1][pos].find('D')!=-1:
                temp.append('410')
            
            cp3.append(temp)
            k+=1
            
        print("한기평 기업어음 :")        
        for i in cp3:
            print(i)
    except Exception:
        no_exist.append(search)
        print(search+" 기업은 한기평에 기업어음이 없습니다")

    stb3=[]
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'ib-container13')))
        stb3.append(['평가기준일','한도설정일','발행한도','본_평가일','본_공시일','본_등급','수_평가일','수_공시일','수_등급','정_평가일','정_공시일','정_등급','유효기간','변환등급'])
        table=driver.find_element(By.CSS_SELECTOR, '#mySheet13-table > tbody > tr:nth-child(3) > td > div > div.GMPageOne > table > tbody')    
        rows=table.find_elements(By.TAG_NAME, "tr")

        #js코드로 h2태그에 값을 읽어서 가져온다.
        del rows[0]
        k=1 #rowcount
        for i in rows:
            temp=[]
            for j in range(1, 16):
                code1='document.querySelector("#tabcont2 > div.grid-guide.mgb0 > span").textContent='
                code2='document.querySelector("#mySheet13-table > tbody > tr:nth-child(3) > td > div > div.GMPageOne > table > tbody").childNodes['+str(k)+'].childNodes['+str(j)+'].textContent'
                code=code1+code2
                driver.execute_script(code)
                temp.append(driver.find_element(By.CSS_SELECTOR, '#tabcont2 > div.grid-guide.mgb0 > span').text)
                
            temp[13]=''
            temp[14]=''

            if stb3[k-1][11]!='':
                pos=9
            elif stb3[k-1][8]!='':
                pos=6
            elif stb3[k-1][5]!='':
                pos=3
            
            #변환등급
            if stb3[k-1][pos].find('A1')!=-1:
                temp.append('110')
            elif stb3[k-1][pos].find('A2+')!=-1:
                temp.append('120')
            elif stb3[k-1][pos].find('A2-')!=-1:
                temp.append('122')
            elif stb3[k-1][pos].find('A2')!=-1:
                temp.append('121')
            elif stb3[k-1][pos].find('A3+')!=-1:
                temp.append('130')
            elif stb3[k-1][pos].find('A3-')!=-1:
                temp.append('132')
            elif stb3[k-1][pos].find('A3')!=-1:
                temp.append('131')
            elif stb3[k-1][pos].find('B+')!=-1:
                temp.append('210')
            elif stb3[k-1][pos].find('B-')!=-1:
                temp.append('212')
            elif stb3[k-1][pos].find('B')!=-1:
                temp.append('211')
            elif stb3[k-1][pos].find('C')!=-1:
                temp.append('310')
            elif stb3[k-1][pos].find('D')!=-1:
                temp.append('410')
                
            stb3.append(temp)          
            k+=1

        print("한기평 전단채 :")        
        for i in stb3:
            print(i)
    except Exception:
        no_exist.append(search)
        print(search+" 기업은 한기평에 전단채가 없습니다.")
            

    company.append(cp3)
    company.append(stb3)
    output.append(company)
