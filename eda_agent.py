import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def describe_dataframe(df):
    desc = {}
    desc['n_rows'] = df.shape[0]
    desc['n_cols'] = df.shape[1]
    desc['columns'] = []
    for c in df.columns:
        col = {}
        col['name'] = c
        col['dtype'] = str(df[c].dtype)
        if pd.api.types.is_numeric_dtype(df[c]):
            col['min'] = float(df[c].min())
            col['max'] = float(df[c].max())
            col['mean'] = float(df[c].mean())
            col['median'] = float(df[c].median())
            col['std'] = float(df[c].std())
            col['missing'] = int(df[c].isna().sum())
        else:
            col['unique'] = int(df[c].nunique(dropna=True))
            col['top_values'] = df[c].value_counts().head(5).to_dict()
            col['missing'] = int(df[c].isna().sum())
        desc['columns'].append(col)
    return desc

def histogram_plot(df, column, bins=30):
    plt.clf()
    df[column].dropna().hist(bins=bins)
    plt.xlabel(column)
    plt.ylabel("count")
    plt.title(f"Histograma: {column}")
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    return encoded

def correlation_matrix(df, top_n=20):
    num = df.select_dtypes(include=[np.number])
    corr = num.corr().abs().unstack().sort_values(kind="quicksort", ascending=False).drop_duplicates()
    return corr[corr<1].head(top_n).to_dict()

def detect_outliers_iqr(df, column):
    if not pd.api.types.is_numeric_dtype(df[column]):
        return {'error': 'column not numeric'}
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    low = q1 - 1.5*iqr
    high = q3 + 1.5*iqr
    outliers = df[(df[column] < low) | (df[column] > high)][column]
    return {'n_outliers': int(outliers.shape[0]), 'low_threshold': float(low), 'high_threshold': float(high)}

def temporal_trend(df, time_col, value_col):
    # If time_col is numeric (like 'Time' seconds since start) try binning
    series = df[[time_col, value_col]].dropna().copy()
    if pd.api.types.is_numeric_dtype(series[time_col]):
        series['time_bucket'] = (series[time_col] // (3600)).astype(int)  # hourly buckets
    else:
        series[time_col] = pd.to_datetime(series[time_col], errors='coerce')
        series = series.dropna(subset=[time_col])
        series['time_bucket'] = series[time_col].dt.floor('H')
    agg = series.groupby('time_bucket')[value_col].agg(['count','mean','sum']).reset_index()
    return agg.to_dict(orient='list')

def cluster_analysis(df, n_clusters=2):
    num = df.select_dtypes(include=[np.number]).dropna(axis=1, how='all')
    if num.shape[1] < 2:
        return {'error': 'not enough numeric columns'}
    scaler = StandardScaler()
    X = scaler.fit_transform(num.values)
    k = min(n_clusters, max(2, X.shape[0]//10))
    model = KMeans(n_clusters=k, random_state=42, n_init='auto')
    labels = model.fit_predict(X)
    return {'n_clusters': int(k), 'labels_sample': labels[:20].tolist()}