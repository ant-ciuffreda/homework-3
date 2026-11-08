import os
import time
from pathlib import Path
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

#Connesione a Elasticsearch
load_dotenv()
client = Elasticsearch(
    os.getenv("ES_URL"),
    basic_auth=(os.getenv("ES_USER"), os.getenv("ES_PASSWORD")),
)
INDICE_NOMI = "homework3-nomi"
INDICE_CONTENUTI = "homework3-contenuti"
CARTELLA_DATI = Path("data")

#Analyzer per il nome
settings_nomi = {
    "analysis": {
        "analyzer": {
            "analyzer_nome": {
                "type": "pattern",
                "pattern": "[\\W_]+",
                "lowercase": True,
            }
        }
    }
}
mappings_nomi = {
    "properties": {
        "nome": {"type": "text", "analyzer": "analyzer_nome"},
        "file": {"type": "keyword"},
    }
}

#Analyzer per il contenuto
settings_contenuti = {}
mappings_contenuti = {
    "properties": {
        "contenuto": {"type": "text", "analyzer": "english"},
        "file": {"type": "keyword"},
    }
}

def ricrea_indice(nome_indice, settings, mappings):
    if client.indices.exists(index=nome_indice):
        client.indices.delete(index=nome_indice)
    client.indices.create(index=nome_indice, settings=settings, mappings=mappings)

ricrea_indice(INDICE_NOMI,settings_nomi,mappings_nomi)
ricrea_indice(INDICE_CONTENUTI,settings_contenuti,mappings_contenuti)

file_txt = sorted(CARTELLA_DATI.glob("*.txt"))
print("File trovati:", len(file_txt))

#Indice dei nomi
inizio = time.time()
for percorso in file_txt:
    testo = percorso.read_text(encoding="utf-8",errors="replace")
    client.index(index=INDICE_NOMI,
                 document={"nome": percorso.stem, "file": percorso.name},
    )
client.indices.refresh(index=INDICE_NOMI)
tempo_nomi = time.time() - inizio

#Indice dei contenuti
inizio = time.time()
for percorso in file_txt:
    testo = percorso.read_text(encoding="utf-8",errors="replace")
    client.index(index=INDICE_CONTENUTI,
                 document={"contenuto": testo, "file": percorso.name},
    )
client.indices.refresh(index=INDICE_CONTENUTI)
tempo_contenuti = time.time() - inizio

print("Documenti nell'indice nomi:", client.count(index=INDICE_NOMI)["count"])
print("Documenti nell'indice contenuti:", client.count(index=INDICE_CONTENUTI)["count"])
print("Tempo indicizzazione nomi (s):", round(tempo_nomi, 3))
print("Tempo indicizzazione contenuti:", round(tempo_contenuti, 3))
