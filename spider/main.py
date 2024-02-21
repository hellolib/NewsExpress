#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import html

import requests
import vars
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# 新闻列表地址
xwlb_url = "http://tv.cctv.com/lm/xwlb/day/%s.shtml"


def get_date():
    """
    获取当前日期
    :return: '%Y%m%d' 格式的日期字符串
    """
    now = datetime.now()
    if now.hour < 19 or (now.hour == 19 and now.minute < 45):
        now = now - timedelta(days=1)
    return now.strftime('%Y%m%d')


# 获取新闻列表 (Abstract and News Links)
def get_news_list(date: str) -> (str, list):
    """
    获取新闻列表
    :param date: 日期
    :return: abstract_link, news_links
    """
    # format xwlb_url with date
    _xwlb_url = xwlb_url % date
    print(f"Getting news list for xwlb_url: {_xwlb_url}")
    try:
        response = requests.get(_xwlb_url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        links = soup.find_all('a')
        news_links = []
        abstract_link = None
        for link in links:
            href = link.get('href')
            if href and href not in news_links:  # Check if the link is not already in the list
                news_links.append(href)
                # Assuming the first link is the abstract
            if not abstract_link:
                abstract_link = href
        print("成功获取新闻列表")
        return abstract_link, news_links
    except requests.RequestException as e:
        print(f"An error occurred: {e}")


def get_abstract(link: str) -> str:
    """
    获取新闻摘要 (简介)
    :param link: 简介的链接
    :return: 简介内容
    """
    try:
        response = requests.get(link, headers=vars.xwlb_headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        abstract = soup.select_one(
            '#page_body > div.allcontent > div.video18847 > div.playingCon > div.nrjianjie_shadow > div > ul > '
            'li:nth-child(1) > p'
        )
        return abstract.text
    except requests.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    date_str = get_date()
    print(f"date_str: {date_str}")
    # abstract_link, news_links = get_news_list(date_str)
    # print(f"Abstract Link: {abstract_link}")
    # print(get_abstract(abstract_link))
    # print("News Links:")
    # for news_link in news_links:
    #     print(news_link)
