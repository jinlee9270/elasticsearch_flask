from konlpy.tag import Komoran
import pandas as pd
from datetime import datetime
import re

komoran=Komoran()
current_date = datetime.now().strftime('%Y%m%d')

# data = pd.read_csv(f'data_from_s3/{current_date}.csv')
data = pd.read_csv('data_from_s3/20231013.csv')
df = pd.DataFrame(data)

df['search'] = ''
matching_keywords = ['카레', '라면', '햄','두부', '주스', '청양고추', '귤', '거봉', '무', '가지', '사과', '낙지', '거봉']
delete_matching_keywords = ['울', '피죤', '퍼퓸', '비누', '에센스', '샴푸', '린스', '다우니', '비트', '샤프', '무궁화', '페브리즈', '화이트', '세제', '모음', '기획',
                        '모제', "치약", "듀라셀", "물티슈", "트리오", '순수', '로즈', '종량제', '고무장갑', '형광', '섬유', '리필']
skip_keywords = ['인분', '멀티', '입', '드', '번들', '-3', '기획', '실속', '미', '매', '개', '국내', '마리', '소', '팩']

except_data = []
for index, row in df.iterrows():
    row['name'] = re.sub(r'[+},{/*)(\]]', ' ', row['name'])
    temp = komoran.nouns(row['name'])

    if temp:
        if temp[-1] in delete_matching_keywords:
            df.at[index, 'search'] = 'delete'
        elif temp[-1] in skip_keywords:
            if len(temp) > 2:
                df.at[index, 'search'] = temp[-2]
            else:
                df.at[index, 'search'] = temp[0]
                # print(index, temp)
        else:
            df.at[index, 'search'] = temp[-1]

        for i in matching_keywords:
            for j in temp:
                if i == j:
                    df.at[index, 'search'] = i
                break
    else:
        df.at[index, 'search'] = row['name']

    print(row['name'], df.at[index, 'search'])


for index, row in df.iterrows():
    if df.at[index, 'search'] == '후':
        df.at[index, 'search'] = '후랑크'


# csv_filename = f'./after_NPL/after_NPL_{current_date}.csv'
csv_filename = './after_NPL/after_NPL_20231013.csv'
df.to_csv(csv_filename, index=False)

print("2번 파일 끝")