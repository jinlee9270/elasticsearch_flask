import pandas as pd

# CSV 파일 경로
csv_file_path = './after_NPL_without_delete/after_NPL_without_delete20231013.csv'

# CSV 파일을 DataFrame으로 불러오기
df = pd.read_csv(csv_file_path)

# 'search' 컬럼에서 고유한 데이터와 빈도수 계산
unique_data = df['search'].value_counts().reset_index()

# 열 이름 설정
unique_data.columns = ['Data', 'Frequency']

# 결과를 CSV 파일로 저장
unique_data.to_csv('results.csv', index=False)

print("결과가 'results.csv'로 저장되었습니다.")