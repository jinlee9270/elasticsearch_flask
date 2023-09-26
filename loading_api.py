import pandas as pd
from elasticsearch import Elasticsearch, helpers

host = '43.201.164.141'
# Elasticsearch 클라이언트 생성
es = Elasticsearch([{'host': host, 'port': 9200, 'scheme': "http"}])

# CSV 파일을 pandas DataFrame으로 읽기
df = pd.read_csv('modified_product_list_0911_2.csv')
# 중복 데이터를 방지하기 위한 집합(set)을 생성
unique_product_ids = set()

# 데이터를 Elasticsearch에 벌크로 보낼 리스트
docs = []

# DataFrame의 각 행을 반복하며 데이터를 리스트에 추가
for index, row in df.iterrows():
    product_id = int(row['product_id'])

    # 중복 데이터인지 확인
    if product_id not in unique_product_ids:
        unique_product_ids.add(product_id)

        doc = {
            '_index': 'product_list_v7',  # 인덱스 이름을 'product_list'로 설정 후에 날짜 추가로 바꿀 예정
            '_source': {
                "mart_num": int(row['mart_num']),
                "product_id": product_id,
                "product_name": row['product_name'],
                "product_capacity": row['product_capacity'],
                "before_discount_price": int(row['before_discount_price']),
                "after_discount_price": int(row['after_discount_price']),
                "product_picture": row['product_picture'],
                "product_url": row['product_url'],
                "update_date": row['update_date'],
                "manufacture": row['manufacture'],
                "product_capacity_2": row['product_capacity_2'],
            }
        }
        docs.append(doc)

# helpers.bulk 함수를 통해 bulk 데이터 ES에 입력
if docs:
    data = helpers.bulk(es, docs, stats_only=True)

    print(data)

print("done")
