import pandas as pd
from datetime import date

today_date = date.today().strftime("%Y%m%d")
# csv_file_path = f'after_NPL_without_delete/after_NPL_without_delete{today_date}.csv'
csv_file_path = 'after_NPL_without_delete/after_NPL_without_delete20231013.csv'

df = pd.read_csv(csv_file_path)
df = df.drop_duplicates(subset='product_id', keep='first')

df.to_csv(csv_file_path, index=False)

print(df)
print("5번 파일 끝")