from funtions import *

# 실행문
for file in target_file:
    print('{} 검수시작!'.format(file))
    target_path = os.path.join(target_dir, file)
    file_name, extension = os.path.splitext(file)
    complited_file_name = file_name + ' {} 검수완료'.format(datetime.today().strftime('%m%d')) + extension
    destination_path = os.path.join(destination_dir, complited_file_name)
    df = pd.read_excel(target_path, usecols='A:D', sheet_name='검수요청')

    pc_or_m = df.columns[0]
    print('{} 으로 검수영역을 설정합니다!'.format(pc_or_m))
    main_or_view = df.columns[1]
    print('{} 으로 검수탭을 설정합니다!'.format(main_or_view))
    deadline_rank = df.columns[2]
    print('{} 위까지 검수합니다!'.format(deadline_rank))
    secure_check = df.columns[3]
    kwd_list = []
    url_list = []
    wb = Workbook()
    ws = wb.create_sheet('검수완료')
    ws.append(['키워드', '링크', '순위'])
    secure_check_process = False
    if secure_check == '추가검수':
        secure_check_process = True
        print('추가적 확보구좌 검수 진행합니다!')
        ws_secure_check = wb.create_sheet('키워드별 확보 구좌')
        ws_secure_check.append(['키워드', '확보 구좌 수', '당초 목적 키워드'])

    i = 0
    while i < len(df):
        kwd_list.append(list(df.loc[i])[0])
        url_list.append(list(df.loc[i])[1])
        i += 1
    total_num = i
    print('총 {}개의 키워드를 검수합니다!'.format(total_num))

    i = 0
    temp_kwd_list = []
    for kwd in kwd_list:
        temp_kwd_list.append(kwd)
        url_data = []
        response = requests.get(str(choose_search_section(pc_or_m, main_or_view)).format(kwd))  # HTML 코드 받아오기
        soup = BeautifulSoup(response.text, 'html.parser')
        raw_data = soup.select(str(choose_main_or_view_tab(main_or_view)))  # 검색결과 범위 받아오기
        for data in raw_data[:int(deadline_rank)]:  # 검색결과 범위 편집하기
            url_data.append(data['data-url'])  # 데이터 속성값(URL) 추출
        rank = check_rank(url_list[i], url_data)
        row = [kwd, url_list[i], rank]
        ws.append(row)
        if secure_check_process:  # 섬세이 추가검수
            if temp_kwd_list.count(kwd) < 2:  # 검수 키워드 동일여부 확인
                secure = 0
                kwd_index_secure = []
                kwd_secure_list = []
                for data in url_data:  # 네이버에서 받아온 url
                    secure_index = check_secure_index(data, url_list)
                    if secure_index:
                        secure += 1
                        kwd_index_secure += secure_index
                for index in kwd_index_secure:
                    kwd_secure_list.append(kwd_list[index])
                kwd_secure_str = ', '.join(kwd_secure_list)
                row = [kwd, secure, kwd_secure_str]
                row_1 = [kwd, secure]
                if secure > 0:
                    ws_secure_check.append(row)
                else:
                    ws_secure_check.append(row_1)
        if type(rank) == int:
            print('({}/{}) {}: {}위'.format(i+1, total_num, kwd, rank))
        else:
            print('({}/{}) {}: '.format(i+1, total_num, kwd))
        i += 1

    print('검수완료!')
    wb.save(destination_path)
