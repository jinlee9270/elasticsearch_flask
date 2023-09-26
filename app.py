from elasticsearch import Elasticsearch
from flask import Flask, jsonify, request

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
    results = dict()

    query_list = request.args.getlist('description_1')

    try:
        for query in query_list:
            # print(query, query_list[query])
            es_query = create_es_query(query)
            search = es.search(index="product_list_v7", query=es_query, size=10)
            hits = search['hits']['hits']

            if query not in results:
                results[query] = []

            for hit in hits:
                results[query].append(hit)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = jsonify(results)
    response.headers.add("Access-Control-Allow-Origin", "*")
    print(results)
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
