# 💡 LAB — Carreiras X e Y: Valor Entregue na Prática  
> **Versão:** 8.15.3 — Ambiente 100% local, sem TLS e sem autenticação.  
> **Objetivo:** Demonstrar como **técnica (Carreira X)** e **liderança (Carreira Y)** se conectam por meio do **valor entregue** na observabilidade.

---

## 🧭 1. Contexto e propósito

Este laboratório foi criado para ilustrar **como métricas técnicas podem ser traduzidas em valor de negócio**.

- 👨‍💻 **Carreira X (técnica)**: foca em eficiência, estabilidade, performance.  
- 👔 **Carreira Y (gestão)**: foca em previsibilidade, custo, impacto e decisão.  
- 🧩 **Observabilidade** é o fio que costura os dois mundos — transformando **dados em história** e **história em decisão**.

Aqui, você vai gerar **50.000 documentos reais**, simulando um mês de operação de uma área de tecnologia, e visualizar os resultados em um **dashboard do Kibana** pronto.

---

## 🏗️ 2. Estrutura do LAB

| Componente | Descrição |
|-------------|------------|
| **Elasticsearch 8.15.3** | Armazena e processa os dados simulados. |
| **Kibana 8.15.3** | Interface visual para explorar, consultar e criar dashboards. |
| **seed_valor_entregue.py** | Script Python que gera e envia 50.000 documentos simulados para o índice `carreiras-x-y`. |
| **valor-entregue.ndjson** | Dashboard pronto para importação no Kibana. |
| **docker-compose.yml** | Sobe todo o ambiente local em um único comando. |

---

## ⚙️ 3. Subindo o ambiente

Dentro da pasta do projeto (`lab-carreiras-x-y/`):

```bash
docker compose up -d
