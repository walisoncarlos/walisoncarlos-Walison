import streamlit as st
from eda_agent import describe_dataframe, histogram_plot, correlation_matrix, detect_outliers_iqr, temporal_trend, cluster_analysis
from utils import load_csv, save_memory, load_memory
import base64, io

st.set_page_config(page_title="Agente EDA Genérico", layout="wide")

st.title("Agente Autônomo de E.D.A. — Genérico (CSV)")

uploaded = st.file_uploader("Faça upload de um CSV ou arraste aqui", type=["csv"])
if uploaded is None:
    st.info("Faça upload de um arquivo CSV para começar. Você também pode usar o exemplo sintético.")
    if st.button("Usar exemplo sintético"):
        import pandas as pd, numpy as np
        rng = np.random.default_rng(42)
        df = pd.DataFrame({
            "Time": (rng.integers(0, 3600*24, size=1000)).tolist(),
            "V1": rng.normal(size=1000),
            "V2": rng.normal(loc=1.0, scale=2.0, size=1000),
            "Amount": rng.exponential(scale=50, size=1000),
            "Class": rng.choice([0,1], size=1000, p=[0.995,0.005])
        })
    else:
        st.stop()
else:
    df = load_csv(uploaded)

st.sidebar.header("Ações rápidas")
if st.sidebar.button("Descrição dos dados"):
    desc = describe_dataframe(df)
    st.json(desc)
if st.sidebar.button("Matriz de correlação (top)"):
    corr = correlation_matrix(df)
    st.json(corr)
if st.sidebar.button("Cluster (KMeans)"):
    res = cluster_analysis(df, n_clusters=3)
    st.json(res)
if st.sidebar.button("Salvar memória (registro)"):
    save_memory({"last_dataset_rows": int(df.shape[0])})
    st.success("Memória atualizada em memory.json")

st.header("Interaja com o agente (perguntas simples)")
q = st.text_input("Digite sua pergunta (ex: 'quais colunas são numéricas?', 'mostre histograma de Amount', 'há outliers em Amount?')")
if st.button("Enviar pergunta"):
    ql = q.lower().strip()
    if "colun" in ql and "numér" in ql:
        nums = df.select_dtypes(include=['number']).columns.tolist()
        st.write("Colunas numéricas:", nums)
    elif "histogram" in ql or "histograma" in ql or "hist" in ql:
        # try to find column name
        for c in df.columns:
            if c.lower() in ql:
                img_b64 = histogram_plot(df, c)
                st.image(base64.b64decode(img_b64))
                break
        else:
            st.warning("Não identifiquei coluna no texto. Tente 'histograma de Amount'")
    elif "outlier" in ql or "atípic" in ql:
        for c in df.columns:
            if c.lower() in ql and c in df.columns:
                st.json(detect_outliers_iqr(df, c))
                break
        else:
            st.info("Peça algo como 'há outliers em Amount?'")
    elif "tend" in ql or "temporal" in ql:
        # try common time cols
        tc = None
        for cand in ["time","timestamp","date","datetime"]:
            if cand in df.columns.str.lower():
                tc = [c for c in df.columns if c.lower()==cand][0]
                break
        if tc is None:
            # fallback to first numeric column named Time
            if "Time" in df.columns:
                tc = "Time"
        if tc:
            st.json(temporal_trend(df, tc, df.select_dtypes(include=['number']).columns[0]))
        else:
            st.warning("Não identifiquei uma coluna de tempo automaticamente.")
    else:
        st.info("Pergunta não mapeada — tente perguntas sobre colunas, histograma, outliers ou temporalidade.")

st.markdown("---")
st.write("Memória corrente:")
st.json(load_memory())