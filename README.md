# Agentes Autônomos - Projeto (Entregável pronto para GitHub)

Conteúdo do repositório:
- `app.py` - Aplicação Streamlit que funciona como interface do agente; carrega CSVs, responde perguntas básicas em linguagem natural (mapeadas para funções internas), gera gráficos e salva memória em JSON.
- `eda_agent.py` - Funções principais de EDA: resumo, histogramas, detecção de outliers, correlações, clustering (KMeans), e conclusão automática (baseline).
- `utils.py` - Utilitários: leitura de CSV, salvamento de memória, helper para gráficos.
- `requirements.txt` - Dependências Python.
- `Agentes_Autonomos_Report.pdf` - Relatório final exigido pela disciplina (exemplo preenchido).
- `example_queries.txt` - Lista de 10 queries suportadas pelo agente.

## Como executar (local)
1. Criar virtualenv e instalar dependências:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. Rodar a app Streamlit:
```bash
streamlit run app.py
```
3. Abra `http://localhost:8501` no navegador.

## Observações importantes
- O agente não usa LLM externos; todas as respostas são produzidas por rotinas de análise programática (conforme pedido).
- Para manter memória, o agente grava as análises realizadas em `memory.json`.
- O app aceita qualquer CSV: basta fazer upload na interface ou fornecer caminho local quando rodando em servidor.