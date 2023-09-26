#!/usr/local/bin/python3
import hashlib
from elasticsearch import Elasticsearch

host = '43.201.164.141'

# Elasticsearch 클라이언트 생성
es = Elasticsearch([{'host': host, 'port': 9200, 'scheme': "http"}])

dict_of_duplicate_docs = {}

# 다음 줄은 문서의 중복 여부를
# 판단하는 데 사용될 필드를 정의합니다.
keys_to_include_in_hash = ["update_date", "product_id", "mart_num"]

# 현재 검색/스크롤에 의해 반환된 문서를 처리합니다.
def populate_dict_of_duplicate_docs(hits):
    for item in hits:
        combined_key = ""
        for mykey in keys_to_include_in_hash:
            combined_key += str(item['_source'][mykey])
        _id = item["_id"]
        hashval = hashlib.md5(combined_key.encode('utf-8')).digest()
        # hashval이 새로운 것이라면
        # dict_of_duplicate_docs에 새 키를 생성하며
        # 이 키에는 빈 어레이의 값이 할당됩니다.
        # 그런 다음 _id를 즉시 어레이로 푸시합니다.
        # hashval이 이미 존재한다면
        # 새로운 _id를 기존 어레이로 푸시합니다.
        dict_of_duplicate_docs.setdefault(hashval, []).append(_id)

# 인덱스의 모든 문서를 반복하고
# dict_of_duplicate_docs 데이터 구조를 채웁니다.
query = {"query": {"match_all": {}}}
scroll = '1m'

def scroll_over_all_docs():
    data = es.search(index="product_list_v7", scroll=scroll,  body=query)
    # 스크롤 ID를 가져옵니다.
    sid = data['_scroll_id']
    scroll_size = len(data['hits']['hits'])
    # 스크롤하기 전에 적중 결과의 현재 배치를 처리합니다.
    populate_dict_of_duplicate_docs(data['hits']['hits'])
    while scroll_size > 0:
        data = es.scroll(scroll_id=sid, scroll='2m')
        # 적중 결과의 현재 배치를 처리합니다.
        populate_dict_of_duplicate_docs(data['hits']['hits'])
        # 스크롤 ID를 업데이트합니다.
        sid = data['_scroll_id']
        # 마지막 스크롤에 반환된 결과 수를 가져옵니다.
        scroll_size = len(data['hits']['hits'])

def remove_duplicate_docs():
    # 중복 해시가 있는지 확인하기 위해
    # 문서 값의 해시를 검색합니다.
    for hashval, array_of_ids in dict_of_duplicate_docs.items():
        if len(array_of_ids) > 1:
            print("********** Duplicate docs hash=%s **********" % hashval)
            # 중복 문서 중에서 가장 처음 나오는 문서를 선택합니다.
            # 나머지 중복 문서를 삭제합니다.
            for doc_id_to_remove in array_of_ids[1:]:
                es.delete(index="product_list_v7", id=doc_id_to_remove)

def main():
    scroll_over_all_docs()
    remove_duplicate_docs()

if __name__ == "__main__":
    main()