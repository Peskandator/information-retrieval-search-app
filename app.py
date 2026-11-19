import sys
import json
from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch("http://localhost:9200")


def build_query(keywords, logic):
    if logic == "boolean":
        return {"bool": {"filter": {"multi_match": {
            "query": keywords, "fields": ["title", "text"],
            "type": "cross_fields", "operator": "and"}}}}
    if logic == "ranked":
        return {"multi_match": {
            "query": keywords, "fields": ["title^2", "text"], "operator": "or"}}
    return {"multi_match": {
        "query": keywords, "fields": ["title", "text"], "type": "phrase"}}


def run_search(keywords, logic):
    query = build_query(keywords, logic)
    print(json.dumps(query, indent=2))
    result = es.search(index="news", query=query, size=20,
                       highlight={"fields": {"text": {}}})
    return result["hits"]["hits"]


@app.route("/")
def search():
    keywords = request.args.get("q", "")
    logic = request.args.get("logic", "ranked")
    hits = []
    if keywords:
        hits = run_search(keywords, logic)
    return render_template("index.html", keywords=keywords, logic=logic, hits=hits)


def main():
    if len(sys.argv) < 2:
        app.run()
        return

    keywords = sys.argv[1]
    logic = sys.argv[2] if len(sys.argv) > 2 else "ranked"
    hits = run_search(keywords, logic)
    print(len(hits), "hits")
    for hit in hits:
        print(hit["_id"], round(hit["_score"], 3), hit["_source"]["title"])


if __name__ == "__main__":
    main()
