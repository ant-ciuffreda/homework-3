import re
from pathlib import Path

ANTEPRIMA = False   # True: mostra solo i nuovi nomi. False: rinomina davvero

cartella = Path(__file__).resolve().parent.parent / "data"

for file in sorted(cartella.glob("*.txt")):
    if not file.stem.isdigit():      # salta i file già rinominati
        continue
    categoria = "business" if int(file.stem) <= 25 else "tech"
    with open(file, encoding="utf-8", errors="replace") as f:
        testo = f.read().strip()
    titolo = testo.splitlines()[0] if testo else ""
    parole = re.findall(r"[a-z0-9]+", titolo.lower())[:5]
    nuovo_nome = "_".join([categoria, file.stem] + parole) + ".txt"
    print(file.name, "->", nuovo_nome)
    if not ANTEPRIMA:
        file.rename(cartella / nuovo_nome)