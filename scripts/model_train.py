import pandas as pd
import numpy as np
import janitor
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import joblib

df = pd.read_csv('./data/dataset.csv')
df = janitor.clean_names(df)
df['date'] = pd.to_datetime(df['date'])

def reemplazo_mediana(df, columna):
    mediana = df[columna].median()
    df[columna] = df[columna].fillna(mediana)

reemplazo_mediana(df, 'estimated_value')
reemplazo_mediana(df, 'carpet_area')

df.dropna(subset=['locality'], inplace=True)
df = df[df['estimated_value'] > 0]
df['spread'] = ((df['sale_price'] - df['estimated_value']) / df['estimated_value']).round(2)
df['price_per_sqft'] = (df['sale_price'] / df['carpet_area']).round(2)

df['ratio_avance_compra'] = df['estimated_value'] / df['sale_price']

features = [
    'sale_price', 'carpet_area', 'price_per_sqft',
    'spread', 'num_rooms', 'num_bathrooms',
    'ratio_avance_compra'
]
df_cluster = df[features].copy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_cluster)
pca_final = PCA(n_components=3)
X_pca3 = pca_final.fit_transform(X_scaled)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_pca3)

df_cluster['cluster'] = clusters

df_cluster['pca1'] = X_pca3[:, 0]
df_cluster['pca2'] = X_pca3[:, 1]
df_cluster['pca3'] = X_pca3[:, 2]

score_pca3 = silhouette_score(X_pca3, df_cluster['cluster'])


print(f" Silhouette Score en PCA (3 componentes): {score_pca3:.4f}")
joblib.dump(pca_final, './results/models/modelo_pca_3componentes.pkl')
print(' Modelo PCA guardado en: ./results/models/modelo_pca_3componentes.pkl')

# Exportar dataset con columnas originales clave + cluster y PCA
cols_export = ['locality', 'sale_price', 'estimated_value', 'carpet_area',
    'num_rooms', 'num_bathrooms', 'spread', 'price_per_sqft',
    'ratio_avance_compra', 'cluster', 'pca1', 'pca2', 'pca3'
]
df_export = pd.concat([df, df_cluster[['cluster', 'pca1', 'pca2', 'pca3']]], axis=1)
df_export[cols_export].to_csv('./data/gold/dataset_con_clusters.csv', index=False)

print(' Dataset exportado a ./data/gold/dataset_con_clusters.csv')
print(' Job finalizado correctamente')
