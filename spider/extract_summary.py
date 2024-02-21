# !/usr/bin/env python
# -*-coding:utf-8 -*-

from pyhanlp import HanLP

from spider import settings


def extract_summary(document: str) -> list:
    """
    从新闻正文中提取摘要
    :param document: 新闻正文
    :return: 摘要
    """
    return HanLP.extractSummary(document, settings.EXTRACT_SUMMARY_LENGTH)
