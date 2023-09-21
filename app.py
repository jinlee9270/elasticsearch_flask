from elasticsearch import Elasticsearch
from flask import Flask, jsonify, request
import requests

# Connect to Elasticsearch
es = Elasticsearch(
    [
        {
            'host': "localhost",
            'port': 9200,
            'scheme': "http"
        }
    ],
    basic_auth=('elastic', 'MgUGx1NboAm6EQLzsqkX')
)

# Set up the Flask app
app = Flask(__name__)


def create_es_query(query):
    return {
        "size": 10,
        "query": {
            "match": {
                "product_name": query,
            }
        }
    }


# Set up the search route
@app.route('/search', methods=['GET'])
def search_product_name():
    results = []
    query_list = request.args.getlist('query')
    target_server_url = 'http://example.com/target_endpoint'  # 대상 서버의 엔드포인트 URL

    try:
        for query in query_list:
            es_query = create_es_query(query)
            response = requests.post(target_server_url, json={'query': query, 'es_query': es_query})

            if response.status_code == 200:
                results.append({
                    'query': query,
                    'results': response.json()  # 대상 서버의 응답을 결과로 추가
                })
            else:
                results.append({
                    'query': query,
                    'error': 'Failed to fetch results from the target server'
                })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
