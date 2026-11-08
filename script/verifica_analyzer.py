import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()
client = Elasticsearch(
    os.getenv("ES_URL"),
    basic_auth=(os.getenv("ES_USER"), os.getenv("ES_PASSWORD")),
)

def mostra_token(indice, analyzer, testo):
    risposta = client.indices.analyze(index=indice, analyzer=analyzer, text=testo)
    token = []
    for t in risposta["tokens"]:
        token.append(t["token"])
    print(analyzer, "->", token)

def mostra_token_campo(indice, campo, testo):
    risposta = client.indices.analyze(index=indice, field=campo, text=testo)
    token = []
    for t in risposta["tokens"]:
        token.append(t["token"])
    print("campo", campo, "->", token)

# 1. Nome
nome_esempio = "business_001_ad_sales_boost_time_warner"
print("Testo:", nome_esempio)
mostra_token("homework3-nomi", "standard", nome_esempio)
mostra_token("homework3-nomi", "analyzer_nome", nome_esempio)
mostra_token_campo("homework3-nomi", "nome", nome_esempio)

# 2. Contenuto
frase = "The companies are growing their profits"
print("Testo:", frase)
mostra_token("homework3-contenuti", "standard", frase)
mostra_token("homework3-contenuti", "english", frase)
mostra_token_campo("homework3-contenuti", "contenuto", frase)