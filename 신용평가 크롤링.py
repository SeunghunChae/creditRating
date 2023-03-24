from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import requests

import time

####################################검색 리스트 입력#######################################

file=open('input.dat', 'r', encoding='utf-8')

list_search=[]

while True:
    line=file.readline()

    #기업명에서 (구 xx)를 잘라내자
    if line.find('(')!=-1:
        idx=line.find('(')
        line=line[0:idx].split()
    else :
        line=line.split()
    
    if len(line)==0:
        print('===end===\n')
        break
    
    list_search.append(line)

file.close()


#########################################입력 끝###########################################


search=input('회사명을 입력하세요.')

url1 = 'https://www.kisrating.com/ratingsSearch/corp_search.do'         #한국신용평가 searchKeyword
url2 = 'https://www.nicerating.com/disclosure/dayRatingNews.do'         #나이스신용평가
url3 = 'https://www.korearatings.com/cms/frCmnCon/index.do?MENU_ID=360' #한국기업평가

#options = webdriver.ChromeOptions()
#options.add_argument('--headless')
#options.add_argument('--disable-gpu')

#service = Service('c:\chromedriver.exe')
#driver = webdriver.Chrome(service=service, options=options)



driver = webdriver.Chrome('c:\chromedriver.exe')
driver.implicitly_wait(1)



######################한신평 시작#####################
#한신평 테이블 : 기업어음, 전단채, issuer rating, 보험금지급능력평가, 자산유동화증권, 유동화익스포져, 관련 자산유동화증권, 관련 유동화 익스포져 순
print("한신평 시작\n")
driver.get(url1)
driver.implicitly_wait(1)

driver.find_element(By.CSS_SELECTOR, '#searchKeyword').send_keys(search)
driver.find_element(By.CSS_SELECTOR, '#btnSearch').click()
WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tab > ul > li:nth-child(2) > a')))    #페이지를 넘어가서 등급 메뉴가 나타날 때까지 기다림
#여기서 오류
driver.find_element(By.CSS_SELECTOR, '#tab > ul > li:nth-child(2) > a').click()
time.sleep(1)

try:
    cp1=[]
    #print('기업어음포함')
    table = driver.find_element(By.CSS_SELECTOR, '#tb3')
    rows = table.find_elements(By.TAG_NAME, "tr")
    
    cp1.append(['재무기준일', '평가종류', '등급', '평가일', '유효일', '리포트', 'ESG인증'])
    
    del rows[0]
    for row in rows:
        temp=[]
        td = row.find_elements(By.TAG_NAME, "td")
        for i in td:
            temp.append(i.text)
        cp1.append(temp)
    print("한신평 "+search+"의 기업어음 리스트 : ")
    for i in cp1:
        print(i)
    
except Exception:
    print(search+" 기업은 한신평에 기업어음이 없습니다.\n")




try:
    stb1=[] #asset backed short-term bond
    
    #print('전단채포함')
    table = driver.find_element(By.CSS_SELECTOR, '#tb4')
    rows = table.find_elements(By.TAG_NAME, "tr")
        
    stb1.append(['재무기준일', '발행한도(억원)', '평가종류', '등급', '평가일', '유효일', '리포트', 'ESG인증'])    
    del rows[0]
    for row in rows:
        temp=[]
        td = row.find_elements(By.TAG_NAME, "td")
        for i in td:
            temp.append(i.text)
        stb1.append(temp)
        
    print("한신평 "+search+"의 전자단기사채 리스트 : ")
    for i in stb1:
        print(i)
        
except Exception:
    print(search+" 기업은 한신평에 전단채가 없습니다.\n")




print("나신평 시작\n")
#############################나신평 시작#####################
driver.get(url2)
WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainSText')))
driver.find_element(By.CSS_SELECTOR, '#mainSText').send_keys(search)
driver.find_element(By.CSS_SELECTOR, '#searchform > fieldset > input').click()
try:
    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tabCompany > li:nth-child(2) > a')))
    driver.find_element(By.CSS_SELECTOR, '#tabCompany > li:nth-child(2) > a').click()
except Exception:
    print("나신평 기업 여러건 검색됨.")
    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tbl1 > tbody > tr:nth-child(1) > td.cell_type01 > a')))
    driver.find_element(By.CSS_SELECTOR, '#tbl1 > tbody > tr:nth-child(1) > td.cell_type01 > a').click()
    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tabCompany > li:nth-child(2) > a')))
    driver.find_element(By.CSS_SELECTOR, '#tabCompany > li:nth-child(2) > a').click()

try:
    cp2=[]
    tablecp=driver.find_element(By.CSS_SELECTOR, '#tabGrade > div:nth-child(4) > h2').text
    if '기업어음' in tablecp:
        #print('기업어음포함')
        table = driver.find_element(By.CSS_SELECTOR, '#tbl2')
        
        cp2.append(['평정', '현재등급', '등급결정일', '등급확정일', '유효기간', '요지', '재무', '보고서'])

        rows=table.find_elements(By.CSS_SELECTOR, "#tbl2 > tbody")
        rows=rows[0].text.split('\n')
        for i in rows:
            cp2.append(i.split(' '))

        print("나신평 "+search+"의 기업어음 리스트 : ")
        for i in cp2:
            print(i)
            
    else:
        print(search+" 기업은 나신평에 기업어움이 없습니다.\n")    
           
except Exception:
    print(search+" 기업은 나신평에 기업어움이 없습니다.\n")

try:
    stb2=[]
    tablestb=driver.find_element(By.CSS_SELECTOR, '#tabGrade > div:nth-child(6) > h2').text
    if '전자단기사채' in tablestb:
        #print('전자단기사채포함')
        table = driver.find_element(By.CSS_SELECTOR, '#tbl3')
        
        temp=[]
        stb2.append(['평정', '현재등급', '등급결정일' ,'등급확정일', '발행한도(억원)', '발행금액(억원)', '요지', '재무', '보고서'])

        rows=table.find_elements(By.CSS_SELECTOR, "#tbl3 > tbody")
        rows=rows[0].text.split('\n')
        for i in rows:
            stb2.append(i.split(' '))

        print("나신평 "+search+"의 전자단기사채 리스트 : ")
        for i in stb2:
            print(i)
            
    else:
        print(search+" 기업은 나신평에 전자단기사채가 없습니다.\n")
   
        
except Exception:
    print(search+" 기업은 나신평에 전자단기사채가 없습니다.\n")



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
        print(search+" 기업은 한기평에 기업어음이 없습니다.\n")

    
except Exception:
    print(search+" 기업은 한기평에 기업어음이 없습니다.\n")

#driver.quit()
    
#mySheet13-table


