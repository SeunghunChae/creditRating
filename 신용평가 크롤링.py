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
nostb1=[]
nocp2=[]
nostb2=[]
nocp3=[]
nostb3=[]
overflow=[]

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
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        service = Service('c:\chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=options)
    
    company=[]
    company.append(search[1])
    search=search[1]
    print('회사명 : '+search+"\n")
 
    ######################한신평 시작#####################
    #한신평 테이블 : 기업어음, 전단채, issuer rating, 보험금지급능력평가, 자산유동화증권, 유동화익스포져, 관련 자산유동화증권, 관련 유동화 익스포져 순
    print("한신평 시작\n")
    driver.get(url1)
    driver.implicitly_wait(1)

    driver.find_element(By.CSS_SELECTOR, '#searchKeyword').send_keys(search)
    driver.find_element(By.CSS_SELECTOR, '#btnSearch').click()
    #페이지를 넘어가서 등급 메뉴가 나타날 때까지 기다림
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tab > ul > li:nth-child(2) > a')))    
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
                temp[5]=''
                cp1.append(temp)
                if len(temp)>7:
                    overflow.append(search)

            
          #  print("한신평 "+search+"의 기업어음 리스트 : ")
          #  for i in cp1:
          #     print(i)
            
        except Exception:
            nocp1.append(search)
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
                temp[6]=''
                stb1.append(temp)
                if len(temp)>8:
                    overflow.append(search)
                
           # print("한신평 "+search+"의 전자단기사채 리스트 : ")
           # for i in stb1:
           #     print(i)
                
        except Exception:
            nostb1.append(search)
            print(search+" 기업은 한신평에 전단채가 없습니다.\n")

    except Exception:
        no_exist.append(search)
        print(search+" 기업은 한신평에 검색결과가 없습니다.\n")
        print(search+" 기업은 한신평에 기업어음이 없습니다.\n")
        print(search+" 기업은 한신평에 전단채가 없습니다.\n")
        cp1=[]
        stb1=[]




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
        multi.append(search)
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tbl1 > tbody > tr:nth-child(1) > td.cell_type01 > a')))
            driver.find_element(By.CSS_SELECTOR, '#tbl1 > tbody > tr:nth-child(1) > td.cell_type01 > a').click()
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tabCompany > li:nth-child(2) > a')))
            driver.find_element(By.CSS_SELECTOR, '#tabCompany > li:nth-child(2) > a').click()
        except Exception:
            no_exist.append(search)
            print(search +" 회사는 나신평 내 검색결과 없음")

    try:
        cp2=[]
        tablecp=driver.find_element(By.CSS_SELECTOR, '#tabGrade > div:nth-child(4) > h2').text
        if '기업어음' in tablecp:
            #print('기업어음포함')
            table = driver.find_element(By.CSS_SELECTOR, '#tbl2')
            
            rows=table.find_elements(By.CSS_SELECTOR, "#tbl2 > tbody")
            rows=rows[0].text.split('\n')

            if rows[0]=='등록된 정보가 없습니다.':
                print(search+" 기업은 나신평에 기업어움이 없습니다.\n")
            else:
                cp2.append(['평정', '현재등급', '등급결정일', '등급확정일', '유효기간', '요지', '재무', '보고서'])
                for i in rows:
                    temp=i.split(' ')
                    #등급에 보증이 들어간 경우
                    if temp[2].find(')')!=-1:
                        temp[1]=temp[1]+' '+temp[2]
                        del temp[2]
                    cp2.append(temp)
                    if len(temp)>8:
                        overflow.append(search)
                '''
                print("나신평 "+search+"의 기업어음 리스트 : ")
                for i in cp2:
                    print(i)           
               '''
    except Exception:
        nocp2.append(search)
        print(search+" 기업은 나신평에 기업어움이 없습니다.\n")

    try:
        stb2=[]
        tablestb=driver.find_element(By.CSS_SELECTOR, '#tabGrade > div:nth-child(6) > h2').text
        if '전자단기사채' in tablestb:
            #print('전자단기사채포함')
            table = driver.find_element(By.CSS_SELECTOR, '#tbl3')
            
            temp=[]
            
            rows=table.find_elements(By.CSS_SELECTOR, "#tbl3 > tbody")
            rows=rows[0].text.split('\n')

            if rows[0]=='등록된 정보가 없습니다.':
                print(search+" 기업은 나신평에 전자단기사채가 없습니다.\n")
            else:
                stb2.append(['평정', '현재등급', '등급결정일' ,'등급확정일', '발행한도(억원)', '발행금액(억원)', '요지', '재무', '보고서'])
                for i in rows:
                    temp=i.split(' ')
                    #등급에 보증이 들어간 경우
                    if temp[2].find(')')!=-1:
                        temp[1]=temp[1]+' '+temp[2]
                        del temp[2]
                    stb2.append(temp)
                    if len(temp)>9:
                        overflow.append(search)
                    
                '''
                print("나신평 "+search+"의 전자단기사채 리스트 : ")
                for i in stb2:
                    print(i)
                '''
    except Exception:
        nostb2.append(search)
        print(search+" 기업은 나신평에 전자단기사채가 없습니다.\n")

    company.append(cp1)
    company.append(stb1)
    company.append(cp2)
    company.append(stb2)
#    company.append(cp3)
#    company.append(stb3)
    output.append(company)
    
    with open('output2.csv','a',newline='') as f:
        name=company[0]
        for row in company[1]:
            line=','.join(s for s in row)
            line=name+',한신평cp,'+line           
            f.write(line)
            f.write('\n')
        for row in company[3]:
            line=','.join(s for s in row)
            line=name+',나신평cp,'+line
            f.write(line)
            f.write('\n')
        for row in company[2]:
            line=','.join(s for s in row)
            line=name+',한신평stb,'+line
            f.write(line)
            f.write('\n')
        for row in company[4]:
            line=','.join(s for s in row)
            line=name+',나신평stb,'+line
            f.write(line)
            f.write('\n')

    k+=1
    if k%no_repeat==0:
        driver.quit()

    
'''
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
    stb3=[]
    tablestb=driver.find_element(By.CSS_SELECTOR, '#tabcont2 > div:nth-child(13) > div.title').text
    if '전자단기사채' in tablestb:
        stb3.append(['평가기준일','한도설정일','발행한도','본_평가일','본_공시일','본_등급','수_평가일','수_공시일','수_등급','정_평가일','정_공시일','정_등급','유효기간'])
        table=driver.find_element(By.CSS_SELECTOR, '#mySheet13-table > tbody > tr:nth-child(3) > td > div > div.GMPageOne > table > tbody')    
        rows=table.find_elements(By.TAG_NAME, "tr")
        del rows[0]
        for i in rows:
            td=i.find_elements(By.TAG_NAME, "td")
            temp=[]
            for j in range(1, 14):
                temp.append(td[j].text)
            stb3.append(temp)
            
        print("한기평 전단채 :")
        for i in stb3:
            print(i)
        
    else:
        print(search+" 기업은 한기평에 전단채가 없습니다.\n")

    
except Exception:
    print(search+" 기업은 한기평에 전단채가 없습니다.\n")

#driver.quit()
    
#mySheet13-table
'''

#출력소스
for i in output:
    print('회사명 :'+i[0])
    print('한신평 cp : ')
    for j in i[1]:
        print(j)
    print('나신평 cp: ')
    for j in i[3]:
        print(j)
    print('한신평 stb :')
    for j in i[2]:
        print(j)
    print('나신평 stb :')
    for j in i[4]:
        print(j)
    print('\n')

'''

with open('output.csv','a',newline='') as f:
    for i in output:
        name=i[0]
        for row in i[1]:
            line=','.join(s for s in row)
            line=name+',한신평cp,'+line           
            f.write(line)
            f.write('\n')
        for row in i[3]:
            line=','.join(s for s in row)
            line=name+',나신평cp,'+line
            f.write(line)
            f.write('\n')
        for row in i[2]:
            line=','.join(s for s in row)
            line=name+',한신평stb,'+line
            f.write(line)
            f.write('\n')
        for row in i[4]:
            line=','.join(s for s in row)
            line=name+',나신평stb,'+line
            f.write(line)
            f.write('\n')
'''
'''
with open('output.csv','a',newline='') as f:
    for i in output:
        name=i[0]
        cpline=''
        stbline=''
        for row in i[1]:
            line=','.join(s for s in row)
            line=name+',한신평cp,'+line
            cpline+=line
        for row in i[3]:
            line=','.join(s for s in row)
            line=',나신평cp,'+line
            cpline+=line
        for row in i[2]:
            line=','.join(s for s in row)
            line=name+',한신평stb,'+line
            stbline+=line
        for row in i[4]:
            line=','.join(s for s in row)
            line=',나신평stb,'+line
            stbline+=line
        f.write(stbline)
        f.write('\n')
        f.write(cpline)
        f.write('\n')

'''
