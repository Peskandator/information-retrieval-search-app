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


@app.route("/")
def search():
    keywords = request.args.get("q", "")
    logic = request.args.get("logic", "ranked")
    hits = []
    if keywords:
        result = es.search(index="news", query=build_query(keywords, logic), size=20,
                           highlight={"fields": {"text": {}}})
        hits = result["hits"]["hits"]
    return render_template("index.html", keywords=keywords, logic=logic, hits=hits)


if __name__ == "__main__":
    app.run()
