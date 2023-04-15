import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
from openpyxl import Workbook
from datetime import datetime

# 순위 파악 함수 정의
def check_rank(my_url, kwd_url_list):
    my_url_post_number = my_url[-12:]
    i = 0
    for url in kwd_url_list:
        url_post_number = url[-12:]
        if my_url_post_number == url_post_number:
            return i + 1
        i += 1
    return "-"
    # pc_url = 'https://' + my_url[10:]
    # m_url = 'https://m.' + my_url[8:]
    # if my_url in kwd_url_list:  # 검수요청이 완벽한경우
    #     return kwd_url_list.index(my_url) + 1
    # elif pc_url in kwd_url_list:  # 검수요청파일은 모바일링크인데 PC검색결과를 요청하는경우
    #     return kwd_url_list.index(pc_url) + 1
    # elif m_url in kwd_url_list:  # 검수요청파일은 피씨링크인데 모바일검색결과를 요청하는경우
    #     return kwd_url_list.index(m_url) + 1
    # else:
    #     return "-"

# 확보구좌 수 파악에 사용되는 함수
def check_secure_index(url, my_url_list):
    """
    :param url: 네이버 에서 현재 노출되어있는 URL 주소
    :param my_url_list: 지금까지 발행한 우리의 포스팅 URL 주소
    :return: 우리의 포스팅이 몇개 노출되어있고 당초 목적 키워드를 알기위해 리스트중에 노출되어있는 인덱스를 집합으로 리스트를 리턴한다
    """
    kwd_index = []
    url_post_number = url[-12:]
    i = 0
    for my_url in my_url_list:
        my_url_post_number = my_url[-12:]
        if url_post_number == my_url_post_number:
            kwd_index.append(i)
        i += 1
    # pc_url = 'https://' + url[10:]
    # m_url = 'https://m.' + url[8:]

    # j = 0
    # for i in my_url_list: # 네이버 url 과 엑셀 파일 내 url_list 에 있는 url 형식이 같은경우
    #     if url == i:
    #         kwd_index.append(j)
    #     j += 1
    # j = 0
    # for i in my_url_list: # 네이버 url은 PC형식링크인데 엑샐 파일 내 url_list 에 있는 url 형식이 모바일형식인경우
    #     if m_url == i:
    #         kwd_index.append(j)
    #     j += 1
    # j = 0
    # for i in my_url_list: # 네이버 url은 모바일링크인데 엑샐 파일 내 url_list 에 있는 url 형식이 PC형식인경우
    #     if pc_url == i:
    #         kwd_index.append(j)
    #     j += 1
    if len(kwd_index) != 0:
        return kwd_index
    else:
        return False

def choose_search_section(pc_or_m, main_or_view):
    if pc_or_m == '모바일':
        if main_or_view == '통합':
            return mobile_main_search
        elif main_or_view == '뷰탭':
            return mobile_view_search
    elif pc_or_m == 'PC':
        if main_or_view == '통합':
            return pc_main_search
        elif main_or_view == '뷰탭':
            return pc_view_search

def choose_main_or_view_tab(main_or_view):
    if main_or_view == '통합':
        return main
    elif main_or_view == '뷰탭':
        return view

# 네이버 URL 변수 지정
mobile_main_search = 'https://m.search.naver.com/search.naver?where=nexearch&sm=tab_jum&query={}'
pc_main_search = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_jum&query={}'
mobile_view_search = 'https://m.search.naver.com/search.naver?where=m_view&sm=mtb_jum&query={}'
pc_view_search = 'https://search.naver.com/search.naver?where=view&sm=tab_jum&query={}'
main = 'section._au_view_collection a.btn_save._keep_trigger'
view = 'section._au_view_tab a.btn_save._keep_trigger'

# 검수파일 지정 및 검수완료 폴더 지정
target_dir = 'C:\\Users\\ab526\\PycharmProjects\\순위검수\\검수요청'
target_file = os.listdir(target_dir)
destination_dir = 'C:\\Users\\ab526\\PycharmProjects\\순위검수\\검수결과'

