from elasticsearch import Elasticsearch
from datetime import datetime
from decouple import config

es_host = config('es_host')
es_port = config('es_port', cast=int)
elasticID = config('elasticID')
elasticPW = config('elasticPW')

es = Elasticsearch([{'host': es_host, 'port': es_port, 'scheme': "http"}], basic_auth=(elasticID, elasticPW))
print(es.ping())


# CSV 파일 경로 설정
current_date = datetime.now().strftime('%Y%m%d')

# Define the index name
index_name = f'product_list_{current_date}'
# index_name = 'product_list_20231013'


settings = {
    "analysis": {
      "analyzer": {
        "nori": {
          "tokenizer": "nori_tokenizer"
        },
        "synonym_test": {
          "tokenizer": "whitespace",
          "filter": ["synonym"]
        }
      },
      "filter": {
        "synonym": {
          "type": "synonym",
          "synonyms_path": "analysis/synonym.txt"
        }
      }
    }
  }

mappings = {
    "properties": {
      "product_id": {"type": "long"},
      "product_code": {"type": "integer"},
      "mart_id": {"type": "integer"},
      "name": {"type": "text", "analyzer": "nori"},
      "capacity": {"type": "text"},
      "original_price": {"type": "integer"},
      "sale_price": {"type": "integer"},
      "product_picture": {"type": "text"},
      "detail_url": {"type": "text"},
      "img_url": {"type": "text"},
      "add_date": {"type": "date", "format": "yyyy-MM-dd"},
      "manufacture": {"type": "text"},
      "capacity_2": {"type": "text"},
      "search": {"type": "text", "analyzer": "synonym_test"}
    }
}



# Create the index with the specified settings and mappings
es.indices.create(index=index_name, ignore=400, body={"settings": settings, "mappings": mappings})

print(f"Created index: {index_name}")
print("4번 파일 끝")