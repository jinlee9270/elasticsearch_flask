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
    # query_list = {"두부": "3장(약300g)",
    #            "밀가루": "약1컵(140g)",
    #             "식용유": "3큰술(21g)",
    #             "달걀": "3개",
    #             "맛소금": "약간(2g)",
    #             "후추가루": "약간",
    #             "식초": "2큰술(16g)",
    #             "진간장": "1큰술(10g)",
    #             "굵은고추가루": "약1/3큰술"
    #           }
    try:
        for query in query_list:
            # print(query, query_list[query])
            es_query = create_es_query(query)
            search = es.search(index="product_list_v7", query=es_query, size=10)
            print(query, search)
            hits = search['hits']['hits']
            results[f"{query}"] = hits

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = jsonify(results)
    response.headers.add("Access-Control-Allow-Origin", "*")
    print(response.json)
    return response.json


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')