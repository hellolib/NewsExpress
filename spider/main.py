#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import html
import time

import requests
import vars
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from spider.extract_summary import extract_summary

# 新闻列表地址
xwlb_url = "http://tv.cctv.com/lm/xwlb/day/%s.shtml"


class NewsItem(object):
    """
    新闻条目
    """
    title = None  # 标题
    link = ""  # 链接
    content = None  # 内容
    is_abstract = False  # 是否是摘要
    image_base64 = ""  # 图片 base64
    image_link = ""  # 图片链接
    summary = []  # 摘要
    items = []  # 子条目


class News(object):
    """
    新闻
    """
    date = None  # 日期
    link = ""  # 链接
    abstract_link = ""  # 摘要链接
    abstract = ""  # 摘要
    news_item = []  # NewsItem


def get_date():
    """
    获取当前日期
    :return: '%Y%m%d' 格式的日期字符串
    """
    now = datetime.now()
    if now.hour < 19 or (now.hour == 19 and now.minute < 45):
        now = now - timedelta(days=1)
    return now.strftime('%Y%m%d')


def get_news_list(_xwlb_url: str) -> (str, list):
    """
    获取新闻列表
    :param _xwlb_url: 新闻列表地址
    :return: abstract_link, news_links
    """
    # format xwlb_url with date

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


def get_news(links: list) -> list:
    """
    获取新闻
    :param links:
    :return:
    """
    print(f'共 {len(links)} 则新闻, 开始获取')
    news = []
    for i, url in enumerate(links):
        try:
            time.sleep(0.5)
            response = requests.get(url)
            response.raise_for_status()  # 如果请求失败，将引发 HTTPError 异常
            soup = BeautifulSoup(response.content, 'html.parser')
            # 查找标题
            title_element = soup.select_one('#page_body > div.allcontent > div.video18847 > div.playingVideo > div.tit')
            title = title_element.get_text(strip=True) if title_element else None
            if title:
                title = title.replace('[视频]', '')
                # 查找内容
            content_element = soup.select_one('#content_area')
            content = content_element.get_text(strip=True) if content_element else None

            news.append((title, content))
            print(f'获取的新闻则数: {i + 1}')
        except requests.RequestException as e:
            print(f'在获取 {url} 时发生错误: {e}')
    print('成功获取所有新闻')
    return news


def run():
    date_str = get_date()
    print(f"date_str: {date_str}")

    news = News()
    news.date = date_str
    news.link = xwlb_url % date_str

    abstract_link, news_links = get_news_list(news.link)
    news.abstract_link = abstract_link

    print(f"Abstract Link: {abstract_link}")
    print(get_abstract(abstract_link))
    print("News Links:")
    for news_link in news_links:
        print(news_link)
    news_list = get_news(news_links)
    # 从 news_list 的第二个遍历
    for item in news_list[1:]:
        print(item[0])
        print(extract_summary(item[1]))


if __name__ == '__main__':
    run()
