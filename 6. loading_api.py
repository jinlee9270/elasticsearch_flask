import pandas as pd
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import BulkIndexError
from datetime import datetime

host = '43.201.164.141'
# Elasticsearch 클라이언트 생성
es = Elasticsearch([{'host': host, 'port': 9200, 'scheme': "http"}], basic_auth=("elastic", "123456"))

# CSV 파일을 pandas DataFrame으로 읽기
current_date = datetime.now().strftime('%Y%m%d')
df = pd.read_csv(f'./after_NPL_without_delete/after_NPL_without_delete{current_date}.csv')

# loading 하려고 하는 index명
index_name = f'product_list_{current_date}'

# 데이터프레임 순회
docs = []
fail_product_id = set()
batch_size = 100  # 한 번에 색인화할 문서 수

for index, row in df.iterrows():
    product_id = int(row['product_id'])

    # 중복 데이터 확인 및 중복 처리

    doc = {
        "_index": index_name,
        "_source": {
            "product_id": int(row['product_id']),
            "product_code": int(row['product_code']),
            "mart_id": int(row['mart_id']),
            "name": row['name'],
            "capacity": row['capacity'],
            "original_price": int(row['original_price']),
            "sale_price": int(row['sale_price']),
            "detail_url": row['detail_url'],
            "img_url": row['img_url'],
            "add_date": row['add_date'],
            "manufacture": row['manufacture'],
            "capacity_2": row['capacity_2'],
            "search": row["search"]
        }
    }

    docs.append(doc)
    # 일정 개수의 문서가 모일 때 벌크로 전송
    if len(docs) >= batch_size:
        try:
            data = helpers.bulk(es, docs, stats_only=True)
        except BulkIndexError as e:
            # BulkIndexError 예외 처리
            print(f"{len(e.errors)} document(s) failed to index.")
            for error in e.errors:
                product_id = error['index']['_id']
                fail_product_id.add(product_id)
                print(f"Failed to index document with ID: {product_id}")

        # docs 리스트 초기화
        docs = []

# 남은 문서가 있다면 나머지도 벌크로 전송
if docs:
    try:
        data = helpers.bulk(es, docs, stats_only=True)
    except BulkIndexError as e:
        # BulkIndexError 예외 처리
        print(docs)
        print(len(docs))
        print(f"{len(e.errors)} document(s) failed to index.")
        for error in e.errors:
            print(f"Failed to index document with ID: {error['index']}")
            print(f"Error reason: {error['index']['error']['reason']}")

print(f"Total failed documents: {len(fail_product_id)}")