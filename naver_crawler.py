# -*- coding: utf-8 -*-
"""

#git-hub : dev-go-kor

def get_ranking_news()
    모바일 랭킹 뉴스 리스트 크롤링
def get_comment(url)
    해당 url에서 댓글 정보 크롤링

"""

import urllib.request
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from selenium import webdriver
import requests

def get_ranking_news():
    ranking_news_url = 'http://m.news.naver.com/rankingList.nhn'
    req = urllib.request.Request(ranking_news_url)
    urlopen = urllib.request.urlopen(req)
    status = urlopen.status

    if status == 200 :
        html = urlopen.read()
        soup = BeautifulSoup(html,'lxml')

        date_text = soup.find('div', class_='pg2 rank_pg2').strong.text
        date_re = re.compile(r'\d\d\d\d.\d\d.\d\d')
        date_search = date_re.search(date_text)
        date_get = date_search.group()
        date = date_get.translate({ord('.') : '-'})

        section_list = soup.find_all('div', class_='ranking_news')

        article_section = []
        article_title = []
        article_url = []
        article_thumbnail = []
        article_date = []

        for section in section_list:
            section_name = section.find('h2').text

            section_article = section.find_all('li')

            for list in section_article:
                title = list.find('div', class_='commonlist_tx_headline').text
                url = list.find('a')['href']
                try:
                    thumbnail = list.find('img')['src']
                except:
                    thumbnail = ""

                article_section.append(section_name)
                article_title.append(title)
                article_url.append('http://m.news.naver.com'+url)
                article_thumbnail.append(thumbnail)
                article_date.append(date)

    data_news_list = pd.DataFrame({'section' : article_section, 'title' : article_title, 'url' : article_url, 'thumbnail' : article_thumbnail,'date' : article_date})

    return data_news_list

def get_comment(url):
# later, if it's already crawled, check it's update
    if url.startswith('http://m.news.naver.com/'):
        driver = webdriver.PhantomJS(executable_path=r'C:\Users\dev\phantomjs\bin\Phantomjs.exe')
        # check your webdriver path
        driver.get(url)
        time.sleep(1)
        tmp_count = '댓글'
        while(tmp_count == '댓글'):

            print('loading....')
            tmp_count = driver.find_element_by_xpath(
                "//a[@class='media_end_head_cmtcount_button'][@id='comment_count']").text.replace("," , "")

        comment_total = int(0 if tmp_count == "" else tmp_count)
        time.sleep(1)

        comment_text = []
        comment_date = []
        comment_recommend = []
        comment_unrecommend = []

        if comment_total > 0:
            driver.find_element_by_xpath("//a[@data-log='RPS.new']").click()
            time.sleep(1)
            driver.find_element_by_xpath("//a[@class='u_cbox_btn_view_comment']").click()
            time.sleep(1)

            repeat = (comment_total-1) // 20
            # later, need to upgrade to check end of click RPC.more
            # check existence
            for i in range(repeat):
                driver.find_element_by_xpath("//a[@data-log='RPC.more']").click()
                time.sleep(1)
                #time.sleep(1)

            tmp = driver.find_elements_by_xpath("//div[@class='u_cbox_content_wrap']/ul[@class='u_cbox_list']/li[@*]")
            for line in tmp:
                line_text = line.find_element_by_class_name("u_cbox_text_wrap").text
                line_date = line.find_element_by_class_name("u_cbox_date").text

                try :
                    line_recommend = line.find_element_by_class_name("u_cbox_cnt_recomm").text
                    line_unrecommend = line.find_element_by_class_name("u_cbox_cnt_unrecomm").text
                    print("correct case : " + line_text)
                    comment_text.append(line_text)
                    comment_date.append(line_date)
                    comment_recommend.append(line_recommend)
                    comment_unrecommend.append(line_unrecommend)
                except :
                    line_recommend = "0"
                    line_unrecommend = "0"
                    print("except case : " + line_text)

    return pd.DataFrame({'text' : comment_text, 'date' : comment_date, 'recommend' : comment_recommend, 'unrecommend' : comment_unrecommend } )
