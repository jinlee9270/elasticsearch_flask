from elasticsearch import Elasticsearch

es_host = "43.201.164.141"
es_port = 9200

# Elasticsearch 연결 설정
es = Elasticsearch([{'host': es_host, 'port': es_port, 'scheme': "http"}], basic_auth=("elastic", "123456"))

# 삭제할 인덱스 이름
index_name = 'product_list_20231013'

# 인덱스 삭제
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
    print(f"Deleted index: {index_name}")
else:
    print(f"Index {index_name} does not exist.")