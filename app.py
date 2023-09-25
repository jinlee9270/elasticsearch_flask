from elasticsearch import Elasticsearch
from flask import Flask, jsonify, request

host = '43.201.31.197'
# Connect to Elasticsearch
es = Elasticsearch(
    [
        {
            'host': host,
            'port': 9200,
            'scheme': "http"
        }
    ]
)

# Set up the Flask app
app = Flask(__name__)


def create_es_query(query):
    return {
        "match": {
            "product_name": query,
        }
    }


# Set up the search route
@app.route('/', methods=['GET'])
def search_product_name():
    results = []
    query_list = request.args.getlist('query')

    try:
        for query in query_list:
            es_query = create_es_query(query)

            search = es.search(index="product_list_v7", query=es_query, size=10)

            hits = search['hits']['hits']

            for hit in hits:
                results.append(hit)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = jsonify(results)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')