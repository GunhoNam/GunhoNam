import gspread
from google.oauth2.service_account import Credentials
from funtions import *
from naver_openapi import *
import time

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'C:\\Users\\ab526\\PycharmProjects\\순위검수\\regal-campus-340108-9f96ee2ad4b2.json',
    scopes=scopes
)

gc = gspread.authorize(credentials)
sumsei = gc.open_by_url('https://docs.google.com/spreadsheets/d/1ROyw4w8zIt0FXnF24Q0DT58tEw9qytIWtTrdmFPDMOg/edit#gid=1150226745')
ws = sumsei.worksheet('현황(섬세이)')
today_col_alphabet = ws.acell('X43').value.strip()  # 오늘날짜 영어열 변수 지정
today_col_alphabet_secure = ws.acell('X44').value.strip()  # 오늘날짜 영어열 변수 지정 확보구좌 시트용
today_text = ws.acell('X45').value.strip()
if today_col_alphabet == None:
    print('검수시트에 열을 추가하고 다시 실행하세요')
    exit()
pc_or_m = ws.acell('X40').value #검수 옵션 지정
print('{} 으로 검수옵션 설정'.format(pc_or_m))
main_or_view = ws.acell('X41').value #검수 옵션 지정
print('{} 으로 검수옵션 설정'.format(main_or_view))
deadline_rank = ws.acell('X42').value #검수 옵션 지정

ws = sumsei.worksheet('통합관리')
keyword_col = 11
url_col = 14
keyword_list = ws.col_values(keyword_col)
url_list = ws.col_values(url_col)
# pc_vol_list = []
# mo_vol_list = []
keyword_vol_list = []
rank_list = []
secure_list = []
if len(keyword_list) != len(url_list):
    print('키워드갯수와 링크갯수가 맞지 않습니다 누락된부분 있는지 확인하고 다시 실행해주세요')
    exit()
paste_length = len(keyword_list)
rank_paste_range = '{}3:{}{}'.format(today_col_alphabet, today_col_alphabet, paste_length)
# mo_vol_paste_range = '{}3:{}{}'.format('M', 'M', paste_length)
# pc_vol_paste_range = '{}3:{}{}'.format('L', 'L', paste_length)


#  모바일, pc 검색량 및 검수순위 리스트로 만들기
i = 0
temp_keyword_list = []
for keyword in keyword_list[2:]:
    temp_keyword_list.append(sumsei_keyword_converter(keyword))
    # time.sleep(0.5)
    # mo_vol_list.append([volume[1]])
    # pc_vol_list.append([volume[0]])
    url_data = []
    response = requests.get(str(choose_search_section(pc_or_m, main_or_view)).format(sumsei_keyword_converter(keyword)))  # HTML 코드 받아오기
    soup = BeautifulSoup(response.text, 'html.parser')
    raw_data = soup.select(str(choose_main_or_view_tab(main_or_view)))  # 검색결과 범위 받아오기
    for data in raw_data[:int(deadline_rank)]:  # 검색결과 범위 편집하기
        url_data.append(data['data-url'])  # 데이터 속성값(URL) 추출
    rank = check_rank(url_list[2:][i], url_data)
    rank_list.append([rank])
    i += 1
    print('({}/{})   '.format(i, len(keyword_list[2:])) + '{}: {}'.format(keyword, rank))
    if temp_keyword_list.count(sumsei_keyword_converter(keyword)) < 2:
        volume = search_volume(keyword)
        keyword_vol_list.append([volume[2]])
        # time.sleep(0.35)
        secure = 0
        for data in url_data:
            check_secure_index_result = check_secure_index(data, url_list)
            if check_secure_index_result:
                secure += 1
        secure_list.append([secure])


#  검수결과 통합관리 시트에 일괄 붙여넣기
# ws.update(mo_vol_paste_range, mo_vol_list)
# ws.update(pc_vol_paste_range, pc_vol_list)
ws.update(rank_paste_range, rank_list)

#  키워드별 노출량 시트에 일괄 붙여넣기
secure_paste_range = '{}3:{}{}'.format(today_col_alphabet_secure, today_col_alphabet_secure, len(secure_list) + 2)
ws = sumsei.worksheet('키워드별 노출량')
ws.update(secure_paste_range, secure_list)

#  키워드별 검색량 시트에 일괄 붙여넣기
keyword_vol_paste_range = '{}3:{}{}'.format(today_col_alphabet_secure, today_col_alphabet_secure, len(secure_list) + 2)
ws = sumsei.worksheet('키워드별 검색량')
ws.update(keyword_vol_paste_range, keyword_vol_list)


#  브랜드 검색량 업데이트
sumsei_volume = ['섬세이', '섬세이 바디드라이어', '섬세이 에어샤워', '섬세이 전신건조기', '섬세이 바디건조기', '섬세이 바디드라이기', '생활도감 혀클리너', '생활도감 칫솔', '갓생도세트', '생활도감']
sumsei_volume_list = []  # 형식 맞추기 전
sumsei_volume_list_1 = []  # 형식 맞춘 후
for keyword in sumsei_volume:
    time.sleep(0.5)
    sumsei_volume_list.append(search_volume(keyword)[2])
sumsei_volume_list_1.append(sumsei_volume_list)
ws = sumsei.worksheet('브랜드 검색량')
today_row = ws.find(today_text).row
sumsei_vol_paste_range = 'H{}:Q{}'.format(today_row, today_row)


ws.update(sumsei_vol_paste_range, sumsei_volume_list_1)

import luffypuppyautomation