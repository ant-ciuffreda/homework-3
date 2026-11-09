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
FILE_RISULTATI = "risultati/test_query.txt"

query_di_prova = [
    ("Termine singolo", "contenuto", "market"),
    ("Maiuscole", "contenuto", "MARKET"),
    ("Plurale", "contenuto", "companies"),
    ("Singolare", "contenuto", "company"),
    ("Più termini", "contenuto", "mobile phones"),
    ("Frase esatta", "contenuto", '"mobile phones"'),
    ("Frase con ordine invertito", "contenuto", '"phones mobile"'),
    ("Solo stopwords", "contenuto", "the"),
    ("Parola inesistente", "contenuto", "xyzabc"),
    ("Nome file", "nome", "warner"),
    ("Nome file (categoria)", "nome", "business"),
]

with open(FILE_RISULTATI, "w", encoding="utf-8") as f:
    numero=0
    for descrizione, campo, testo in query_di_prova:
        numero += 1
        if campo == "nome":
            indice = INDICE_NOMI
        else:
            indice = INDICE_CONTENUTI
        if testo.startswith('"') and testo.endswith('"'):
            query = {"match_phrase": {campo: testo.strip('"')}}
        else:
            query = {"match": {campo: testo}}
        risposta = client.search(index=indice, query=query, size=5)
        totale = risposta["hits"]["total"]["value"]

        righe = [f"Query {numero}: {descrizione}, ({campo} '{testo}') Risultati: {totale}"]
        for hit in risposta["hits"]["hits"]:
            righe.append(f"  File: {hit['_source']['file']}, Score: {round(hit['_score'], 3)}")
        righe.append("")
        for riga in righe:
            print(riga)
            f.write(riga + "\n")