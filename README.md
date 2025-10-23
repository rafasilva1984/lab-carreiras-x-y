# LAB — Carreiras X e Y: Valor Entregue na Prática

> ⚠️ **Modo LAB (não use em produção):** segurança desativada para facilitar o estudo.

## O que vem
- Elasticsearch + Kibana **8.15.3**
- Índice: **carreiras-x-y**
- **50.000** documentos simulados (out/2025)
- Dashboard: **Carreiras X e Y — Valor Entregue na Prática**

## Pré-requisitos
- Docker + Docker Compose
- Python 3.8+ (`pip install requests`)

## Passo a passo
```bash
docker compose up -d
python3 seed_valor_entregue.py
# Abra o Kibana em http://localhost:5601
# Importar: Stack Management → Saved Objects → Import → dashboards/valor-entregue.ndjson
```
> Dica: altere volume de dados usando `DOCS` e `BATCH`:
> `DOCS=100000 BATCH=5000 python3 seed_valor_entregue.py`

### O que visualizar
- **Valor Score (média)** — métrica unificadora X + Y
- **MTTR ao longo do tempo** — eficiência técnica
- **Taxa de erro** — estabilidade operacional
- **Custo de incidente (R$)** — impacto financeiro
- **Correlação Valor x Custo** — leitura técnica ↔ negócio

### Notas
- Janela de tempo do dashboard já definida para **01/10/2025 → 31/10/2025**
- Se nada aparece, confirme se o índice `carreiras-x-y` tem dados e ajuste o timepicker.

Bom LAB! 💛
