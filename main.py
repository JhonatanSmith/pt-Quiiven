import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Segmentación de Clientes y Asignación de Descuentos",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title(" Segmentación de Clientes y Asignación de Descuentos")
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

data_path = "data/gold/dataset_con_clusters.csv"
df = load_data(data_path)

if 'descuento_%' not in df.columns:
    mediana_1 = df[df['cluster'] == 1]['ratio_avance_compra'].median()
    def asignar_descuento(row):
        if row['cluster'] == 0:
            return 0
        if row['cluster'] == 2:
            return 25
        return 20 if row['ratio_avance_compra'] > mediana_1 else 5
    df['descuento_%'] = df.apply(asignar_descuento, axis=1)

page = st.sidebar.radio("Selecciona página:", ["Análisis Descriptivo", "Segmentación"])

# -- Página 1: Análisis Descriptivo
if page == "Análisis Descriptivo":
    st.header("📋 Análisis Descriptivo")
    st.markdown("Este panel muestra visualizaciones exploratorias generadas a partir del dataset original.")
    
    # Lista de imágenes desde carpeta results/pics
    pics = [
        "avg-sold.png",
        "avg-time-sells.png",
        "cluster-local-distr.png",
        "cluster-m2-avg-price.png",
        "cluster-sell-price.png",
        "estimate-sold.png",
        "k-means.png",
        "local-time-price-sold.png"
    ]
    
    cols = st.columns(2)
    for idx, pic in enumerate(pics):
        col = cols[idx % 2]
        with col:
            caption = pic.replace('.png','').replace('-',' ').replace('_',' ').capitalize()
            st.image(f"results/pics/{pic}", caption=caption, use_container_width=True)
    
    st.stop()  # Salir aquí si está en la página de análisis descriptivo
# -- Página 2: Segmentación
st.header("📈 Segmentación y Descuentos")
st.markdown("Esta sección presenta los resultados del clustering aplicado a los clientes.")

st.subheader("📊 Resumen de Descuentos Asignados")
st.write(
    df['descuento_%']
      .value_counts()
      .rename_axis('Descuento (%)')
      .reset_index(name='Clientes')
)

# -- Botones para mostrar clientes por cluster
st.subheader("👥 Listado de Clientes por Cluster")
clusters = sorted(df['cluster'].unique())
btn_cols = st.columns(len(clusters))
for idx, cl in enumerate(clusters):
    if btn_cols[idx].button(f"Ver Cluster {cl}"):
        st.write(f"**Clientes en Cluster {cl}**")
        st.dataframe(df[df['cluster']==cl][['id_cliente','cluster','descuento_%']])

# -- Estadísticas resumidas
st.subheader("🔍 Estadísticas por Cluster")
tabs = st.tabs([f"Cluster {i}" for i in clusters])
for i, tab in enumerate(tabs):
    with tab:
        subset = df[df['cluster']==i]
        st.write(f"**Cluster {i}: {len(subset)} clientes**")
        st.write(subset[[
            'sale_price',
            'estimated_value',
            'carpet_area',
            'num_rooms',
            'num_bathrooms',
            'spread',
            'price_per_sqft',
            'ratio_avance_compra'
        ]].describe().T[['mean', 'std', 'min', 'max']])


# -- Footer
st.markdown("---")
st.markdown("Fuente: `dataset_con_clusters.csv` procesado y clusterizado con K-Means.")
