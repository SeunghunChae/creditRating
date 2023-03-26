from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import requests

import time
import csv

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
nostp1=[]
nocp2=[]
nostp2=[]
nocp3=[]
nostp3=[]

del list_search[0]


url1 = 'https://www.kisrating.com/ratingsSearch/corp_search.do'         #한국신용평가 searchKeyword
url2 = 'https://www.nicerating.com/disclosure/dayRatingNews.do'         #나이스신용평가
url3 = 'https://www.korearatings.com/cms/frCmnCon/index.do?MENU_ID=360' #한국기업평가



#driver = webdriver.Chrome('c:\chromedriver.exe')

k=0
no_repeat=5

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
    search=search[1]
    print('회사명 : '+search+"\n")   

    print("한기평 시작\n")
    #############################한기평 시작#####################
    driver.get(url3)
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




    #ib-container2 : 기업어음
    #mySheet2-table
    #ib-container13 : stb

    while(1):
        time.sleep(1)
        table=driver.find_element(By.ID, 'ib-container2')
        table=table.find_element(By.ID, 'mySheet2-table')
        #GMSection
        tr=table.find_elements(By.TAG_NAME, "tr")

        print("6 : "+tr[6].text)
        print("10 : "+tr[10].text)


        cp3.append(['평가기준일','본_평가일','본_공시일','본_등급','수_평가일','수_공시일','수_등급','정_평가일','정_공시일','정_등급','유효기간'])
        table=driver.find_element(By.CSS_SELECTOR, '#mySheet2-table > tbody > tr:nth-child(3) > td > div > div.GMPageOne > table > tbody')    
        rows=table.find_elements(By.TAG_NAME, "tr")
        


'''    
    if 
    
    print("6 : "+tr[6].text)
    print("8 : "+tr[8].text)
    
    try:
        table=driver.find_elements(By.ID, "mySheet2-table")
        table=table[0].find_elements(By.TAG_NAME, "table")
        tr=table.find_elements(By.TAG_NAME, "tr")

        print("6 : "+tr[6].text)
        print("10 : "+tr[10].text)
        
    except Exception:
        print(search+" 기업은 한기평 기업어음이 없습니다.\n")
    
    

    try:
        cp3=[]
        tablecp=driver.find_element(By.CSS_SELECTOR, '#tabcont2 > div:nth-child(9) > div.title').text
        if '기업어음' in tablecp:
            cp3.append(['평가기준일','본_평가일','본_공시일','본_등급','수_평가일','수_공시일','수_등급','정_평가일','정_공시일','정_등급','유효기간'])
            table=driver.find_element(By.CSS_SELECTOR, '#mySheet2-table > tbody > tr:nth-child(3) > td > div > div.GMPageOne > table > tbody')    
            rows=table.find_elements(By.TAG_NAME, "tr")
            #사이트가 발로 만들어져있어서 행을 직접 찍는다.
            del rows[0]
            for i in rows:
                td=i.find_elements(By.TAG_NAME, "td")
                temp=[]
                temp.append(td[1].text)
                for j in range(4, 25):
                    temp.append(td[j].text)
                cp3.append(temp)
                
            print("한기평 기업어음 :")        
            for i in cp3:
                print(i)
        else:
            print(search+" 기업은 한기평에 기업어음이 없습니다.\n")    
            
    except Exception:
        print(search+" 기업은 한기평에 기업어음이 없습니다.\n")



    #한기평 전단채
    try:
        stp3=[]
        tablestp=driver.find_element(By.CSS_SELECTOR, '#tabcont2 > div:nth-child(13) > div.title').text
        if '전자단기사채' in tablestp:
            stp3.append(['평가기준일','한도설정일','발행한도','본_평가일','본_공시일','본_등급','수_평가일','수_공시일','수_등급','정_평가일','정_공시일','정_등급','유효기간'])
            table=driver.find_element(By.CSS_SELECTOR, '#mySheet13-table > tbody > tr:nth-child(3) > td > div > div.GMPageOne > table > tbody')    
            rows=table.find_elements(By.TAG_NAME, "tr")
            del rows[0]
            for i in rows:
                td=i.find_elements(By.TAG_NAME, "td")
                temp=[]
                for j in range(1, 14):
                    temp.append(td[j].text)
                stp3.append(temp)
                
            print("한기평 전단채 :")
            for i in stp3:
                print(i)
            
        else:
            print(search+" 기업은 한기평에 전단채가 없습니다.\n")

        
    except Exception:
        print(search+" 기업은 한기평에 전단채가 없습니다.\n")
        
#메모리 누수 방지
    k+=1
    if k%no_repeat==0:
        driver.quit()

'''
