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
luffypuppy = gc.open_by_url('https://docs.google.com/spreadsheets/d/1PKl2eUct1tvmx3t8H3ZzMnNxLMBz9IMiIvllFi3QC-k/edit#gid=250551072')
ws = luffypuppy.worksheet('현황판')
today_col_alphabet = ws.acell('AA4').value.strip()  # 오늘날짜 영어열 변수 지정
today_col_alphabet_vol = ws.acell('AA8').value.strip()  # 오늘날짜 검색량 시트용 변수 지정
today_text = ws.acell('AA1').value.strip()
if today_col_alphabet == None:
    print('검수시트에 열을 추가하고 다시 실행하세요')
    exit()
pc_or_m = ws.acell('AA5').value #검수 옵션 지정
print('{} 으로 검수옵션 설정'.format(pc_or_m))
main_or_view = ws.acell('AA6').value #검수 옵션 지정
print('{} 으로 검수옵션 설정'.format(main_or_view))
deadline_rank = ws.acell('AA7').value #검수 옵션 지정

keyword_col = 12
url_col = 7
ws = luffypuppy.worksheet('작업내역')
url_list = ws.col_values(url_col)
ws = luffypuppy.worksheet('통합관리')
keyword_list = ws.col_values(keyword_col)

rank_list = []
keyword_vol_list = []

paste_length = len(keyword_list)
rank_paste_range = '{}3:{}{}'.format(today_col_alphabet, today_col_alphabet, paste_length)
keyword_vol_paste_range = '{}3:{}{}'.format(today_col_alphabet_vol, today_col_alphabet_vol, paste_length)


#  모바일, pc 검색량 및 검수순위 리스트로 만들기
i = 0

for keyword in keyword_list[2:]:
    url_data = []
    response = requests.get(str(choose_search_section(pc_or_m, main_or_view)).format(keyword))  # HTML 코드 받아오기
    soup = BeautifulSoup(response.text, 'html.parser')
    raw_data = soup.select(str(choose_main_or_view_tab(main_or_view)))  # 검색결과 범위 받아오기
    for data in raw_data[:int(deadline_rank)]:  # 검색결과 범위 편집하기
        url_data.append(data['data-url'])  # 데이터 속성값(URL) 추출
    rank_counter = []
    secure_counter = 0
    keyword_vol_list.append([search_volume(keyword)[2]])
    for url in url_list[2:]:
        temp = check_rank(url, url_data)
        if temp != '-':
            rank_counter.append(temp)
            secure_counter += 1
    if secure_counter > 0:
        rank = min(rank_counter)
    else:
        rank = '-'
    rank_list.append([rank])
    i += 1
    print('({}/{})   '.format(i, len(keyword_list[2:])) + '{}: {}'.format(keyword, rank))


#  검수결과 통합관리 시트에 일괄 붙여넣기
ws.update(rank_paste_range, rank_list)




#  브랜드 검색량 업데이트
luffypuppy_volume = search_volume('루피퍼피')
ws = luffypuppy.worksheet('브랜드검색량')
today_row = ws.find(today_text).row
ws.update_cell(today_row, 8, luffypuppy_volume[2])

#  키워드 검색량 업데이트
ws = luffypuppy.worksheet('키워드 별 검색량')
ws.update(keyword_vol_paste_range, keyword_vol_list)
