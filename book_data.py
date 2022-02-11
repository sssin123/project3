#교보문고 연간 베스트셀러에서 분야 종합을 카테고리의 페이지 수와 제목, 가격을 크롤링
#연간 데이터(2021.01.01~2021.12.31)
from numpy import genfromtxt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time

def save_csv(df):
    df.to_csv('yes24.csv',mode ='w',encoding='utf-8')


# 책 제목, 작가, 줄거리, 가격, 평점 
# label : 장르
browser = webdriver.Chrome(r"e:\third_project\data_crawling\chromedriver.exe")
title_list = []
author_list = []
content_list = []
price_list = []
grade_list = []
genre_list = []
page_number = 1
category_address = '001001046011001'
category_number = 1 
run = True
while run:
    #처음 접속해서 받아오는 정보 -> 각 책 상세정보에 들어가기 위한 url, 가격 정보, pagination
    browser.get(f'http://www.yes24.com/24/category/bestseller?CategoryNumber={category_address}&sumgb=06&FetchSize=80&PageNumber={str(page_number)}')
    time.sleep(3)
    #pagination
    page_list = browser.find_element_by_css_selector('#bestList > div:nth-child(6) > div.bosSortTop > div.sortLft > p')
    pages = page_list.find_elements_by_tag_name('a')
    last_page = pages[-1].get_attribute('href')[-1:]
    print(last_page)
    
    
    book_list = browser.find_elements_by_css_selector('td.goodsTxtInfo > p:nth-child(1) > a:nth-child(1)')
    # price_items = browser.find_elements_by_css_selector('#category_layout > tbody > tr:nth-child(1) > td.goodsTxtInfo > p:nth-child(3) > span.priceB')
    # price_list = [price.get_attribute('innerHTML') for price in price_items]
    # print(price_list)
    #한 페이지 안에 있는 도서들 상세정보 가져오기
    for url in book_list:
        print(url.get_attribute('href'))
        response = requests.get(url.get_attribute('href'))
        soup = BeautifulSoup(response.text,'html.parser')
        
        #책의 상세정보(제목, 작가, 줄거리, 평점, 장르(label))
        #가격
        price_list.append(soup.select_one('#total_order_scrollbar > span').get_text())
        print(soup.select_one('#total_order_scrollbar > span').get_text())
        #제목        
        title_list.append(soup.select_one('#yDetailTopWrap > div.topColRgt > div.gd_infoTop > div > h2').get_text())
        print(soup.select_one('#yDetailTopWrap > div.topColRgt > div.gd_infoTop > div > h2').get_text())
        #작가
        author_list.append(soup.select_one('#yDetailTopWrap > div.topColRgt > div.gd_infoTop > span.gd_pubArea > span.gd_auth').get_text())
        #줄거리
       
        
        try:
            content = soup.select_one('#infoset_introduce > .infoSetCont_wrap').get_text()
            content_list.append(content)
        except AttributeError:
            content_list.append(None)
            pass

        #평점
        #1-추리/미스터리 2-공포/스릴러 3-판타지 4-무협 5-SF 6-역사 7-로맨스
        grade = soup.select_one('#spanGdRating > a > em')
        if grade == None :
            grade_list.append(None)
        else :
            grade_list.append(grade.get_text())   
        genre_list.append(category_number)
        print(len(title_list))
    
    #마지막페이지 확인
    if int(last_page) == page_number : 
        run = False
    else :
        page_number += 1

    print(len(title_list),len(author_list),len(content_list),len(price_list),len(grade_list),len(genre_list))

book_df = pd.DataFrame({'title':title_list,'author':author_list,'content':content_list,'price':price_list,'grade':grade_list,'genre':genre_list})
browser.close()
print(book_df)
save_csv(book_df)

