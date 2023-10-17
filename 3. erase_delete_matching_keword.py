import pandas as pd
from datetime import datetime
# CSV 파일 경로 설정
current_date = datetime.now().strftime('%Y%m%d')
# file_path = f"after_NPL/after_NPL_{current_date}.csv"
file_path = "after_NPL/after_NPL_20231013.csv"

# CSV 파일 읽어오기
data = pd.read_csv(file_path)

# "search" 컬럼 값이 "delete"인 행 제거
data = data[data['search'] != 'delete']

# 결과를 새로운 CSV 파일로 저장 (선택사항)
# output_file_path = f"after_NPL_without_delete/after_NPL_without_delete{current_date}.csv"
output_file_path = "after_NPL_without_delete/after_NPL_without_delete20231013.csv"

data.to_csv(output_file_path, index=False)

print("3번 파일 끝")