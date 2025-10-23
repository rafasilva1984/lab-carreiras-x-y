#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, random, math, time, json
from datetime import datetime, timedelta, timezone
import requests

ES_URL = os.environ.get("ES_URL", "http://localhost:9200")
INDEX = "carreiras-x-y"
DOCS = int(os.environ.get("DOCS", "50000"))
BATCH = int(os.environ.get("BATCH", "2000"))
TZ = timezone.utc

def ensure_index():
    mapping = {
        "settings": {"number_of_shards": 1, "number_of_replicas": 0},
        "mappings": {"properties": {
            "timestamp": {"type":"date"},
            "mttr": {"type":"float"},
            "erro_rate": {"type":"float"},
            "custo_incidente": {"type":"float"},
            "valor_score": {"type":"float"}
        }}
    }
    r = requests.put(f"{ES_URL}/{INDEX}", headers={"Content-Type":"application/json"}, data=json.dumps(mapping))
    if r.status_code not in (200,201):
        print(f"[warn] índice: {r.status_code} {r.text}")

def gen_docs():
    start = datetime(2025,10,1,0,0,0, tzinfo=TZ)
    end   = datetime(2025,10,31,23,59,59, tzinfo=TZ)
    total_seconds = int((end - start).total_seconds())
    for _ in range(DOCS):
        ts = start + timedelta(seconds=random.randint(0, total_seconds))
        progress = (ts - start).total_seconds() / (total_seconds + 1)
        base_mttr = 90 - 60*progress
        mttr = max(5, random.gauss(base_mttr, 8))
        base_err = 0.20 - 0.17*progress
        erro_rate = max(0.005, min(0.5, random.gauss(base_err, 0.02)))
        base_custo = 800 - 200*progress
        custo_incidente = max(50, random.gauss(base_custo + 60*math.sin(12*progress*math.pi), 80))
        mttr_norm = max(0.0, min(1.0, (mttr-5)/(120-5)))
        err_norm = max(0.0, min(1.0, erro_rate/0.25))
        custo_norm = max(0.0, min(1.0, (custo_incidente-50)/(1200-50)))
        raw = 0.25*(1-progress)*0.6 + 0.75*progress
        score = 100 * (0.55*(1-mttr_norm) + 0.25*(1-err_norm) + 0.20*(1-custo_norm))
        score = 0.65*score + 35*raw + random.gauss(0, 2.5)
        yield {
            "timestamp": ts.isoformat(),
            "mttr": round(mttr, 2),
            "erro_rate": round(erro_rate, 4),
            "custo_incidente": round(custo_incidente, 2),
            "valor_score": round(max(5.0, min(99.0, score)), 2),
        }

def bulk_send():
    session = requests.Session()
    buf = []
    sent = 0
    for d in gen_docs():
        buf.append(json.dumps({"index":{"_index":INDEX}}))
        buf.append(json.dumps(d))
        if len(buf) >= 2*BATCH:
            data = "\n".join(buf) + "\n"
            r = session.post(f"{ES_URL}/_bulk", headers={"Content-Type":"application/x-ndjson"}, data=data)
            if r.status_code != 200:
                raise SystemExit(f"Bulk erro {r.status_code}: {r.text}")
            sent += BATCH
            print(f"[ok] enviados {sent}/{DOCS}")
            buf = []
    if buf:
        data = "\n".join(buf) + "\n"
        r = session.post(f"{ES_URL}/_bulk", headers={"Content-Type":"application/x-ndjson"}, data=data)
        if r.status_code != 200:
            raise SystemExit(f"Bulk erro {r.status_code}: {r.text}")
        sent += len(buf)//2
        print(f"[ok] enviados {sent}/{DOCS} (final)")

def wait_es():
    for _ in range(60):
        try:
            r = requests.get(ES_URL)
            if r.ok:
                return True
        except Exception:
            pass
        time.sleep(2)
    return False

if __name__ == "__main__":
    print(f"[init] ES_URL={ES_URL} INDEX={INDEX} DOCS={DOCS}")
    ok = wait_es()
    if not ok:
        print("[erro] Elasticsearch não respondeu a tempo. Tente novamente após 'docker compose up -d'.")
        raise SystemExit(1)
    ensure_index()
    bulk_send()
    print("[done] carga concluída. Abra o Kibana em http://localhost:5601")
