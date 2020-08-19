# -*- coding: utf-8 -*-
def insta_searching(word):
    url = "http://www.instagram.com/explore/tags/" + word
    return url

from selenium import webdriver

# ① 크롬 브라우저 열기
driver = webdriver.Chrome('D:/source/instragram_crawling/extension/chromedriver.exe')

# 예제 4-2 selenium으로 URL 접속하기 - 2
# 인스타그램 로그인 부분 추가
import time

# 인스타그램 접속하기
driver.get('http://www.instargram.com')
time.sleep(3)

# 인스타그램 접속하기
######## 인스타 계정 로그인이 필요합니다 #########

email = 'pap5608@naver.com' 
input_id = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[0]
input_id.clear()
input_id.send_keys(email)

password = 'rushngo%608' 
input_pw = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
input_pw.clear()
input_pw.send_keys(password)
input_pw.submit()
time.sleep(3)

word = "양재맛집"         #찾고자 하는 태그
url = insta_searching(word)
driver.get(url)
time.sleep(3)

# 예제 4-3 HTML에서 첫번째 게시글 찾아 클릭하기
def select_first(driver):
    first = driver.find_element_by_css_selector("div._9AhH0")
    first.click()
    time.sleep(3)
    
select_first(driver)    # 함수 실행

results = []

import re
from bs4 import BeautifulSoup
from requests import get
def get_content(driver):
    # ① 현재 페이지 html 정보 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml',from_encoding='utf-8')
    
    #soup = BeautifulSoup(html, 'lxml')
    # ② 본문 내용 가져오기
    try:
        content = soup.select('div.C4VMK > span')[0].text
    except:
        content = ' '
    # ③ 본문 내용에서 해시태그 가져오기(정규식 활용)
    tags = re.findall(r'#[^\s#,\\]+', content)  
    # ④ 작성일자 정보 가져오기
    date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10]
    # ⑤ 좋아요 수 가져오기
    try:
        like = soup.select('div.Nm9Fw > button')[0].text[4:-1]   
    except:
        like = 0
    # ⑥ 위치정보 가져오기
    try: 
        place = soup.select('div.M30cS')[0].text
    except:
        place = ''
        # ⑤ 좋아요 수 가져오기
    try:
        img_url = soup.select_one('.KL4Bh').img['src']
    except:
        img_url = 0
    print(img_url)
    # ⑦ 수집한 정보 저장하기
    data = [content, date, like, place, tags,img_url]
    return data

get_content(driver)

def move_next(driver):
    right = driver.find_element_by_css_selector ('a.coreSpriteRightPaginationArrow')
    right.click()
    time.sleep(2)
    
move_next(driver)

target = 5      # 크롤링할 게시글 수 (50개 너무 많아서 5개로 바꿈)

for i in range(target):
    # 게시글 수집에 오류 발생시(네트워크 문제 등의 이유로)  2초 대기 후, 다음 게시글로 넘어가도록 try, except 구문 활용
    try:
        data = get_content(driver)    # 게시글 정보 가져오기
        results.append(data)
        move_next(driver)
    except:
        time.sleep(2)
        move_next(driver)
    

print(results[:2])

import pandas as pd

results_df = pd.DataFrame(results)
results_df.columns = ['content','data','like','place','tags','img_url']
results_df.to_excel('d:/source/instragram_crawling/data/3_1_crawling_jejudoMatJip.xlsx',encoding='utf-8')

# 예제 4-8 여러 개의 저장파일 통합하기
jeju_insta_df = pd.DataFrame( [ ] )

folder = 'd:/source/instragram_crawling/data/'
f_list = ['3_1_crawling_jejudoMatJip.xlsx']
for fname in f_list:
    fpath = folder + fname
    temp = pd.read_excel(fpath)
    jeju_insta_df = jeju_insta_df.append(temp)

jeju_insta_df.columns =['index_col','content','data','like','place','tags','img_url']

# 예제 4-9 중복 데이터 제거하고 저장하기
jeju_insta_df.drop_duplicates(subset = ['content'] , inplace = True)
jeju_insta_df.to_excel('d:/source/instragram_crawling/data/3_1_crawling_raw.xlsx', index = False,encoding='utf-8')