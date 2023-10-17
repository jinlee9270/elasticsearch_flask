import pandas as pd

# CSV 파일 경로 설정
file_path = "after_NPL.csv"

# CSV 파일 읽어오기
data = pd.read_csv(file_path)

# "search" 컬럼 값이 "delete"인 행 제거
data = data[data['search'] != 'delete']

# 결과를 새로운 CSV 파일로 저장 (선택사항)
output_file_path = "after_NPL_without_delete.csv"
data.to_csv(output_file_path, index=False)