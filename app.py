from elasticsearch import Elasticsearch
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json
import csv
import datetime

host = '43.201.164.141'
# Connect to Elasticsearch
es = Elasticsearch(
    [
        {
            'host': host,
            'port': 9200,
            'scheme': "http"
        }
    ]
    , basic_auth=("elastic", "123456")
)

# Set up the Flask app
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# 현재 날짜를 가져옵니다.
today = datetime.date.today().strftime("%Y%m%d")

# CSV 파일을 열고 데이터를 기록합니다.
csv_filename = f"rank_name_{today}.csv"


def create_es_query(keyword):
    query = {
        "bool": {
            "should": [
                {
                    "match": {
                        "name": {
                            "query": keyword,
                            "boost": 1.0
                        }
                    }
                },
                {
                    "match": {
                        "search": {
                            "query": keyword,
                            "boost": 2.0
                        }
                    }
                }
            ]
        }
    }

    return query


# Set up the search route
@app.route('/', methods=['POST'])
@cross_origin()
def search_product_name():
    results = dict()

    print(request.json.items())
    try:
        with open(csv_filename, mode='w', newline='') as csv_file:
            fieldnames = ['Key', 'Search Results']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()

            for key, _ in request.json.items():
                es_query = create_es_query(key)
                search = es.search(index="product_list_20231013", query=es_query, size=10)
                print(key, search)
                hits = search['hits']['hits']
                results[f"{key}"] = hits
                writer.writerow({'Key': key, 'Search Results': str(hits)})

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

    response = jsonify(results)
    response.headers.add("Content-Type", "application/json;charset=UTF-8")
    print(response.json)
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

