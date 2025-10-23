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
```

Isso irá iniciar dois containers:
- `es-cxy` → Elasticsearch
- `kb-cxy` → Kibana

Acompanhe os logs iniciais (opcional):
```bash
docker compose logs -f elasticsearch
```

Aguarde até ver algo como:
```
Elasticsearch started
```

Então acesse:
👉 **http://localhost:5601**

---

## 🧩 4. Ingestão de dados

O script `seed_valor_entregue.py` gera e envia automaticamente **50.000 documentos** com campos simulados:

| Campo | Descrição |
|--------|------------|
| `timestamp` | Data/hora entre 01/10/2025 e 31/10/2025 |
| `mttr` | Tempo médio de resolução (minutos) |
| `erro_rate` | Taxa de erro (%) |
| `custo_incidente` | Custo médio por incidente (R$) |
| `valor_score` | Índice calculado que representa o “valor entregue” |

### ▶️ Executar a ingestão

```bash
python3 seed_valor_entregue.py
```

Saída esperada (resumo):
```
[init] ES_URL=http://localhost:9200 INDEX=carreiras-x-y DOCS=50000
[ok] enviados 2000/50000
[ok] enviados 4000/50000
...
[done] carga concluída. Abra o Kibana em http://localhost:5601
```

O script cria automaticamente o índice `carreiras-x-y` e insere todos os documentos via `_bulk`.

---

## 🔍 5. Consultando os dados no Kibana (Dev Tools)

Abra o menu lateral do Kibana → **Dev Tools**

### Verificar se o índice existe
```bash
GET _cat/indices?v
```

### Contar documentos
```bash
GET carreiras-x-y/_count
```

### Visualizar alguns registros
```bash
GET carreiras-x-y/_search?size=3
```

### Agregar métricas principais
```bash
POST carreiras-x-y/_search
{
  "size": 0,
  "aggs": {
    "mttr_avg": { "avg": { "field": "mttr" } },
    "erro_avg": { "avg": { "field": "erro_rate" } },
    "custo_avg": { "avg": { "field": "custo_incidente" } },
    "valor_score_avg": { "avg": { "field": "valor_score" } }
  }
}
```

✅ Resultado esperado:
- `mttr_avg` em torno de 40–60  
- `erro_avg` caindo ao longo do mês  
- `valor_score_avg` subindo progressivamente  

---

## 📊 6. Importando o Dashboard no Kibana

1. Acesse **Stack Management → Saved Objects → Import**  
2. Selecione o arquivo:  
   ```
   dashboards/valor-entregue.ndjson
   ```
3. Marque a opção “Automatically overwrite conflicts”  
4. Clique em **Import**

Após a importação:
- Vá em **Dashboard → Carreiras X e Y — Valor Entregue na Prática**

O painel já vem configurado para o intervalo **01/10/2025 → 31/10/2025**.

---

## 🎨 7. Painéis incluídos

| Visualização | Descrição |
|---------------|------------|
| **Valor Score (média)** | Mede o índice geral de valor entregue. |
| **MTTR ao longo do tempo** | Mostra a tendência de eficiência operacional. |
| **Taxa de Erro (%)** | Indica estabilidade e qualidade técnica. |
| **Custo de Incidente (R$)** | Representa o impacto financeiro. |
| **Correlação Valor x Custo** | Mostra a relação direta entre custo e valor entregue (gráfico Vega). |

💬 **Dica:** Use o botão **Refresh** no Kibana e ajuste o intervalo de tempo se necessário.

---

## 🔎 8. Verificando resultados via API

Você também pode testar diretamente via terminal:

```bash
curl -X GET "http://localhost:9200/carreiras-x-y/_count?pretty"
```

Ou verificar um documento específico:
```bash
curl -X GET "http://localhost:9200/carreiras-x-y/_search?size=1&pretty"
```

---

## 🩺 9. Troubleshooting (erros comuns)

| Sintoma | Causa provável | Solução |
|----------|----------------|----------|
| ❌ `Connection refused` ao rodar o script | Containers ainda subindo | Aguarde ~1 min e rode o script novamente |
| ⚠️ Índice sem dados | Script não rodou ou travou | Rode novamente `python3 seed_valor_entregue.py` |
| 🕒 Dashboard vazio | Timepicker fora do período | Ajuste para `Oct 1, 2025 – Oct 31, 2025` |
| 💾 Erro ao importar NDJSON | Versão do Kibana diferente | Use versão 8.x compatível (ideal: 8.15.x) |

---

## 💬 10. Conclusão — O Valor Entregue

Este LAB simboliza a **ponte entre técnica e estratégia**:
- O analista reduz **MTTR**, e o gestor enxerga **previsibilidade**.  
- O SRE automatiza alertas, e o negócio ganha **estabilidade**.  
- O desenvolvedor melhora logs, e o suporte ganha **contexto**.

Tudo está conectado — e **a observabilidade é o fio que costura essa conexão**.

---

## 📚 Créditos

**Autor:** Rafael Silva — *Observabilidade na Prática / DataStackPro*  
🔗 GitHub: [rafasilva1984](https://github.com/rafasilva1984)  
🔗 LinkedIn: [Rafael Silva - Leader Coordenador](https://linkedin.com/in/rafael-silva-leader-coordenador)

---

🟦 **Resumo rápido**
```
docker compose up -d
python3 seed_valor_entregue.py
# Acesse: http://localhost:5601
# Importar dashboards/valor-entregue.ndjson
```
✨ E pronto — você verá, na prática, como **Carreiras X e Y se encontram no valor entregue.**
