import time
import requests
import pandas as pd
import signaturehelper
import re


def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp,
            'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}


BASE_URL = 'https://api.naver.com'
API_KEY = '010000000046a726bc4c0d463bae47954758aeecb6d93b74bf422e4de806b171a63eb66e8e'
SECRET_KEY = 'AQAAAABGpya8TA1GO65HlUdYruy24zzMNKeNYtBu7wC/3oo6fA=='
CUSTOMER_ID = '1941899'

uri = '/keywordstool'
method = 'GET'


def sumsei_keyword_converter(keyword):
    """섬세이 키워드 뒤에 붙은 중복작업된 횟수를 나타내는 숫자를 제거해주는 함수"""
    keyword = keyword[:-2] + re.sub("[0-9]", "", keyword[-2:])
    return keyword


def search_volume(keyword):
    """키워드를 파라미터로 받아서 모바일 검색량, PC 검색량을 받아와 pc, mobile, total 리스트를 만든다"""
    keyword = sumsei_keyword_converter(keyword)
    r = requests.get(BASE_URL + uri + '?hintKeywords={}&showDetail=0'.format(keyword.replace(" ", "")),
                     headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
    # print(r.status_code)
    if r.status_code == 200:
        df = pd.DataFrame(r.json()['keywordList'])
        if type(list(df.loc[0])[1]) == str:
            pc = 0
        else:
            pc = list(df.loc[0])[1]
        if type(list(df.loc[0])[2]) == str:
            mobile = 0
        else:
            mobile = list(df.loc[0])[2]
        total = 0
        if type(pc) != str:
            total += pc
        if type(mobile) != str:
            total += mobile
        return [int(pc), int(mobile), int(total)]
        #print('키워드 : {}\nPC검색량 : {}\n모바일검색량 : {}\n총 검색량 : {}'.format(keyword, pc, mobile, total))
    elif r.status_code == 400:
        pc = 0
        mobile = 0
        total = 0
        if type(pc) != str:
            total += pc
        if type(mobile) != str:
            total += mobile
        return [int(pc), int(mobile), int(total)]
        #print('키워드 : {}\nPC검색량 : {}\n모바일검색량 : {}\n총 검색량 : {}'.format(keyword, pc, mobile, total))



if __name__ == "__main__":
    search_keyword = input('키워드 입력\n')
    r = requests.get(BASE_URL + uri+'?hintKeywords={}&showDetail=0'.format(search_keyword.replace(" ","")),
                     headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
    # print("response status_code = {}".format(r.status_code))
    # print("response body = {}".format(r.json()))
    # print(type(r.json()))
    if r.status_code == 200:
        df = pd.DataFrame(r.json()['keywordList'])
        if type(list(df.loc[0])[1]) == str:
            pc = 0
        else:
            pc = list(df.loc[0])[1]
        if type(list(df.loc[0])[2]) == str:
            mobile = 0
        else:
            mobile = list(df.loc[0])[2]
        total = 0
        if type(pc) != str:
            total += pc
        if type(mobile) != str:
            total += mobile
        print([int(pc), int(mobile), int(total)])
        # print('키워드 : {}\nPC검색량 : {}\n모바일검색량 : {}\n총 검색량 : {}'.format(keyword, pc, mobile, total))
    elif r.status_code == 400:
        pc = 0
        mobile = 0
        total = 0
        if type(pc) != str:
            total += pc
        if type(mobile) != str:
            total += mobile
        print([int(pc), int(mobile), int(total)])
        # print('키워드 : {}\nPC검색량 : {}\n모바일검색량 : {}\n총 검색량 : {}'.format(keyword, pc, mobile, total))






    # print(df)
    # df.rename({ 'monthlyMobileQcCnt': '월간검색수_모바일',
    #            'monthlyPcQcCnt': '월간검색수_PC',
    #            'relKeyword': '연관키워드'}, axis=1, inplace=True)
    #
    # df = df[['연관키워드', '월간검색수_PC', '월간검색수_모바일']]




