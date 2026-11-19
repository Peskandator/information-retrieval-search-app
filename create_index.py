import json
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")


def main():
    if es.indices.exists(index="news"):
        es.indices.delete(index="news")

    es.indices.create(index="news", mappings={
        "properties": {
            "title": {"type": "text", "analyzer": "english"},
            "text": {"type": "text", "analyzer": "english"},
            "source": {"type": "keyword"},
            "url": {"type": "keyword"},
            "date": {"type": "date"},
            "language": {"type": "keyword"}
        }
    })

    with open("documents.json", encoding="utf-8") as f:
        documents = json.load(f)

    for doc in documents:
        es.index(index="news", id=doc["id"], document=doc)
        print("indexed", doc["id"], doc["title"])

    es.indices.refresh(index="news")
    print(len(documents), "documents indexed")
    print(es.count(index="news")["count"], "documents in index")


if __name__ == "__main__":
    main()
