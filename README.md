

#Project. creditRating
==========================================
## 0. 진행도
2023-03-23 : 단일 기업 검색기능 구현 <br>
2023-03-24 : cp나 stp가 없을 경우 검색 안되는 오류 해결 => 예외처리 추가

<br><br>
trouble shooting : 한국기업평가에 크롤링에 문제가 있음
## 1. 개요
회사명 리스트를 input으로 제공하면 한국신용평가, 나이스 신용평가, 한국기업평가에서 기업어음(cp), 전자단기사채(stp)의 신용평가 내역 리스트를 크롤링하여 제공한다. 


## 2. 사용법

[기본 환경]
Python

[추가 설치 라이브러리]
[ lxml, requests, selenium, besutifulsoup]

* c:\에 크롬에 맞는 크롬드라이버를 넣어야한다.
크롬 버전 확인 : 크롬 도구 > 도움말 > chrome 정보

* pip ssl 오류 해결법 :
 1) pip --trusted-host pypi.org --trusted-host files.pythonhosted.org install [라이브러리]
 2) C:\Users\KOSCOM\AppData\Local\Programs\Python\Python38\Lib\site-packages\pip\_vendor\requests\session.py
에서 self.verify=False로 변경
