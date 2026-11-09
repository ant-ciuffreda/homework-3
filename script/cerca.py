import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()
client = Elasticsearch(
    os.getenv("ES_URL"),
    basic_auth=(os.getenv("ES_USER"), os.getenv("ES_PASSWORD")),
)

INDICE_NOMI = "homework3-nomi"
INDICE_CONTENUTI = "homework3-contenuti"

print('Sintassi: nome <termini> | contenuto <termini> | contenuto "frase esatta" | esci')

while True:
    riga = input("Query> ").strip()
    if riga == "esci":
        break
    parti = riga.split(" ", 1)
    if len(parti) < 2 or parti[0] not in ("nome", "contenuto"):
        print("Query non valida: inizia con nome o contenuto, poi i termini.")
        continue
    campo = parti[0]
    testo = parti[1].strip()

    if campo == "nome":
        indice = INDICE_NOMI
    else:
        indice = INDICE_CONTENUTI

    if len(testo) > 2 and testo.startswith('"') and testo.endswith('"'):
        query = {"match_phrase": {campo: testo.strip('"')}}
    else:
        query = {"match": {campo: testo}}

    risposta = client.search(index=indice, query=query, size=10)
    totale = risposta["hits"]["total"]["value"]
    print(f"Risultati trovati: {totale}")
    for hit in risposta["hits"]["hits"]:
        print(f"File: {hit['_source']['file']}, Score: {round(hit['_score'], 3)}")