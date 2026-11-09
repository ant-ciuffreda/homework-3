# Homework 3: indicizzazione e ricerca di file di testo con Elasticsearch

Due programmi Python che indicizzano in Elasticsearch una cartella di file `.txt`
(due indici: nome del file e contenuto) e li interrogano da console.

## Struttura della repository

```
homework3-idd/
├── data/                 file di testo da indicizzare
├── script/
│   ├── rinomina.py       rinomina i file (già eseguito, vedi sotto)
│   ├── test_connessione.py   verifica il collegamento a Elasticsearch
│   ├── indicizza.py      crea i due indici e indicizza i file
│   ├── verifica_analyzer.py  mostra come gli analyzer spezzano il testo
│   ├── cerca.py          programma di ricerca da console
│   └── test_query.py     esegue le query di prova e salva i risultati
├── risultati/            output di verifica_analyzer.py e test_query.py
├── requirements.txt
└── README.md
```

## Dataset

45 articoli del dataset BBC News (Kaggle): 25 della categoria business e 20 della categoria tech.
I file originali si chiamavano da `001.txt` a `045.txt` (001-025 business, 026-045 tech).
Sono stati rinominati con `script/rinomina.py` nel formato
`categoria_numero_prime-parole-del-titolo.txt`, ad esempio
`business_001_ad_sales_boost_time_warner.txt`.
Lo script è già stato eseguito: rilanciarlo non modifica i file già rinominati.

## Requisiti

- Docker Desktop
- Python 3.10 o superiore
- Elasticsearch 9.5.6 (eseguito con Docker)

## Installazione

**1. Avviare Elasticsearch** (da fare una sola volta, scegliendo una password):

```
docker run -d --name elasticsearch -p 127.0.0.1:9200:9200 -e "discovery.type=single-node" -e "xpack.security.http.ssl.enabled=false" -e "ELASTIC_PASSWORD=scegli_una_password" docker.elastic.co/elasticsearch/elasticsearch:9.5.6
```

Dopo un riavvio del computer basta `docker start elasticsearch`.
Si può controllare che funzioni aprendo `http://localhost:9200` nel browser
(utente `elastic` e la password scelta).

**2. Creare l'ambiente Python** dalla cartella principale del progetto:

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Su Mac o Linux l'attivazione è `source .venv/bin/activate`.

**3. Creare il file `.env`** nella cartella principale (non è incluso nella repository):

```
ES_URL=http://localhost:9200
ES_USER=elastic
ES_PASSWORD=la_password_scelta
```

## Utilizzo

Tutti i comandi vanno eseguiti dalla cartella principale, con Elasticsearch acceso
e l'ambiente virtuale attivo.

1. Controllo del collegamento (facoltativo): `python script/test_connessione.py`
2. Indicizzazione: `python script/indicizza.py`
   Ricrea gli indici `homework3-nomi` e `homework3-contenuti`, quindi può essere rilanciato
   senza duplicare i documenti. Va eseguito dopo ogni ricreazione del container.
3. Ricerca da console: `python script/cerca.py`
4. Query di prova: `python script/test_query.py` (scrive `risultati/test_query.txt`)
5. Verifica degli analyzer (facoltativo): `python script/verifica_analyzer.py`

## Sintassi delle query

```
nome <termini>
contenuto <termini>
contenuto "frase esatta"
esci
```

- Con più termini senza virgolette basta che ne compaia uno (operatore OR di `match`).
- Tra virgolette si cerca la frase esatta, con le parole consecutive e nell'ordine dato (`match_phrase`).
- Esempi: `nome warner`, `contenuto companies`, `contenuto "mobile phones"`.

## Indici e analyzer

| Indice | Campo | Analyzer |
|---|---|---|
| `homework3-nomi` | `nome` | personalizzato: tokenizer `whitespace`, filtri `word_delimiter_graph` e `lowercase` |
| `homework3-contenuti` | `contenuto` | `english` (predefinito) |

In entrambi gli indici il campo `file` (nome completo) è di tipo `keyword` e serve per mostrare i risultati.

## Note

- Una query formata solo da stopword inglesi (per esempio `contenuto the`) non restituisce risultati,
  perché l'analyzer `english` le elimina anche dalla query.
- Le motivazioni delle scelte, i tempi di indicizzazione e i risultati dei test sono nella relazione.
