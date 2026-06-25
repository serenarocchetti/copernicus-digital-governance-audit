"""
Script di estrazione e analisi dei metadati Sentinel-2 dal catalogo CREODIAS.

Librerie utilizzate:
- requests
- pandas

Endpoint interrogato:
https://datahub.creodias.eu/odata/v1/Products

Lo script interroga l'API OData del catalogo CREODIAS, estrae un campione di
metadati relativi ai prodotti Sentinel-2 e costruisce un dataset utilizzato
per analizzare alcune metriche di audit informativo (disponibilità, integrità,
performance).

Per eseguire lo script:
python "audit_creodias_master.py"
"""


import requests
import pandas as pd

# ============================================================
# 1. CONFIGURAZIONE E RICHIESTA DATI
# ============================================================

url = ("https://datahub.creodias.eu/odata/v1/Products?"
       "$filter=startswith(Name, 'S2')"
       "&$top=100&$format=json")

print("--- Avvio Procedura di Audit ---")
print(f"Interrogazione server: {url}")

try:
    # Esecuzione della chiamata API
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Creazione del DataFrame originale con tutti i metadati
    df = pd.DataFrame(data['value'])
    print(f"Dati estratti con successo: {len(df)} record rilevati.\n")

    colonne_presenti = df.columns.tolist()
    print("Colonne trovate nei metadati:")
    print(colonne_presenti, "\n")

    # ============================================================
    # 2. NORMALIZZAZIONE DELLA DATA DI ACQUISIZIONE
    # ============================================================

    # CREODIAS restituisce ContentDate come:
    # "ContentDate": {"Start":"...","End":"..."}
    # -> estraggo SOLO il campo Start
    if "ContentDate" in colonne_presenti:
        df["ContentDate_Start"] = df["ContentDate"].apply(
            lambda x: x.get("Start") if isinstance(x, dict) else None
        )
        campo_acq = "ContentDate_Start"

    elif "OriginDate" in colonne_presenti:
        campo_acq = "OriginDate"

    else:
        campo_acq = None

    # ============================================================
    # 3. DIMENSIONE 1: PERFORMANCE (CALCOLO LATENZA)
    # ============================================================

    if campo_acq and "PublicationDate" in colonne_presenti:
        df[campo_acq] = pd.to_datetime(df[campo_acq], errors='coerce')
        df["PublicationDate"] = pd.to_datetime(df["PublicationDate"], errors='coerce')

        df["Latenza_Ore"] = (df["PublicationDate"] - df[campo_acq]).dt.total_seconds() / 3600

        latenza_media = df["Latenza_Ore"].mean()
        print(f"[AUDIT PERFORMANCE] Latenza media rilevata: {latenza_media:.2f} ore")

        print("\nEsempio valori latenza (prime righe):")
        print(df[[campo_acq, "PublicationDate", "Latenza_Ore"]].head(), "\n")

    else:
        print("[ALERTA AUDIT] Non è possibile calcolare la latenza (manca ContentDate o PublicationDate).\n")

    # ============================================================
    # 4. DIMENSIONE 2: DISPONIBILITÀ (ONLINE STATUS)
    # ============================================================

    possibili_nomi_stato = ["OnlineStatus", "Online", "Status", "IsOnline"]
    colonna_stato = next((c for c in possibili_nomi_stato if c in colonne_presenti), None)

    if colonna_stato:
        print(f"[AUDIT DISPONIBILITÀ] Campo usato: '{colonna_stato}'")
        print(df[colonna_stato].value_counts(), "\n")
    else:
        print("[ALERTA AUDIT] Campo OnlineStatus mancante.\n")

    # EvictionDate → presenza = prodotto archiviato o prossimo all'archiviazione
    if "EvictionDate" in colonne_presenti:
        df["EvictionDate"] = pd.to_datetime(df["EvictionDate"], errors='coerce')
        n_evicted = df["EvictionDate"].notnull().sum()
        print(f"[AUDIT DISPONIBILITÀ] Prodotti con EvictionDate valorizzata: {n_evicted}\n")
    else:
        print("[NOTA] Il campo EvictionDate non è presente.\n")

    # StorageType / Storage class
    possibili_storage = ["Storage", "StorageType"]
    colonna_storage = next((c for c in possibili_storage if c in colonne_presenti), None)

    if colonna_storage:
        print(f"[AUDIT DISPONIBILITÀ] Storage rilevati ({colonna_storage}):")
        print(df[colonna_storage].value_counts(), "\n")
    else:
        print("[NOTA] Nessuna informazione sullo storage.\n")

    # ============================================================
    # 5. DIMENSIONE 3: INTEGRITÀ (CHECKSUM, FOOTPRINT E DIMENSIONE FILE)
    # ============================================================

    # CHECKSUM
    if "Checksum" in colonne_presenti:
        df["Has_Checksum"] = df["Checksum"].notnull()
        integri = df["Has_Checksum"].sum()
        print(f"[AUDIT INTEGRITÀ] Prodotti con Checksum presente: {integri} su {len(df)}")
    else:
        print("[ALERTA AUDIT] Checksum non disponibile.\n")

     # FOOTPRINT
    possibili_foot = ['GeoFootprint', 'Footprint']
    col_foot = next((c for c in possibili_foot if c in colonne_presenti), None)

    if col_foot:
        df['Has_Footprint'] = df[col_foot].notnull()
        print(f"[AUDIT SPAZIALE] Footprint presente per {df['Has_Footprint'].sum()} prodotti.")
    else:
        print("[ALERTA AUDIT] Nessun campo Footprint/GeoFootprint trovato.")

    # CONTENT LENGTH: individuare file vuoti o sospetti
    if "ContentLength" in colonne_presenti:
        df["ContentLength"] = pd.to_numeric(df["ContentLength"], errors='coerce')
        file_zero = (df["ContentLength"] == 0).sum()
        print(f"[AUDIT INTEGRITÀ] File con dimensione 0: {file_zero}")

        df["Size_MB"] = df["ContentLength"] / (1024 * 1024)
    else:
        print("[ALERTA AUDIT] ContentLength mancante.\n")

    # ============================================================
    # 6. ESPORTAZIONE RISULTATI
    # ============================================================

    df.to_csv("risultati_audit_creodias.csv", index=False)
    print("\n--- Fine Procedura ---")
    print("I dati elaborati sono stati salvati in: risultati_audit_creodias.csv")

except Exception as e:
    print(f"ERRORE DURANTE L'ESECUZIONE: {e}")