import sys
from pathlib import Path
import plotly.express as px
import streamlit as st

root = Path(__file__).parent.parent
sys.path.append(str(root))
from utils.dependencias import * 

# Mostrar las tarjetas con información clave
col1, col2 = st.columns(2)

# Tarjeta 1: Producto más vendido
col1.metric("Producto Más Vendido", conexion_ordenada.iloc[0]["ProductName"], f"{conexion_ordenada.iloc[0]['Cantidad']} Unidades")

# Tarjeta 2: Precio promedio de producto
precio_promedio = precio_producto["Precio_de_producto"].mean()
col2.metric("Precio Promedio de Producto", f"$ {precio_promedio:.2f}")



# Filtro  1
producto_seleccionado = st.sidebar.selectbox(
    "Selecciona un producto para los gráficos:",
    ["Todos los productos"] + conexion_ordenada["ProductName"].tolist()
)

# Filtro dos
rango_precio_producto = st.sidebar.slider(
    'Selecciona el rango de precio de producto:',
    min_value=float(precio_combinado['Precio_de_producto'].min()),
    max_value=float(precio_combinado['Precio_de_producto'].max()),
    value=(float(precio_combinado['Precio_de_producto'].min()), 
           float(precio_combinado['Precio_de_producto'].max()))
)

# Filtro 3
rango_precio_orden = st.sidebar.slider(
    'Selecciona el rango de precio de orden:',
    min_value=float(precio_combinado['Precio_Orden'].min()),
    max_value=float(precio_combinado['Precio_Orden'].max()),
    value=(float(precio_combinado['Precio_Orden'].min()), 
           float(precio_combinado['Precio_Orden'].max()))
)

# Filtrar los datos según el producto seleccionado y los rangos de precios
if producto_seleccionado != "Todos los productos":
    conexion_ordenada = conexion_ordenada[conexion_ordenada["ProductName"] == producto_seleccionado]

# Crear las máscaras para los rangos de precio
mask_precio_producto = (precio_combinado['Precio_de_producto'] >= rango_precio_producto[0]) & \
                        (precio_combinado['Precio_de_producto'] <= rango_precio_producto[1])

mask_precio_orden = (precio_combinado['Precio_Orden'] >= rango_precio_orden[0]) & \
                    (precio_combinado['Precio_Orden'] <= rango_precio_orden[1])

# Filtrar los datos con las máscaras
precio_combinado_filtrado = precio_combinado[mask_precio_producto & mask_precio_orden]

# Primer gráfico: Productos más vendidos
grafico1 = px.bar(
    conexion_ordenada,
    x="ProductName",
    y="Cantidad",
    title="Top 10 Productos Más Vendidos",
    labels={"ProductName": "Producto", "Cantidad": "Cantidad Vendida"},
    color="Cantidad",
    color_continuous_scale="Blues"
)

st.plotly_chart(grafico1)

# Segundo gráfico: Relación entre precios de productos y órdenes de compra (con los filtros aplicados)
fig2 = px.scatter(
    precio_combinado_filtrado, 
    x='Precio_de_producto', 
    y='Precio_Orden', 
    title='Relación entre precios de productos y órdenes de compra',
    labels={'Precio_de_producto': 'Precio de Producto', 'Precio_Orden': 'Precio de Orden'}
)

# Ajustar los títulos 
fig2.update_layout(
    xaxis_title='Precio de Producto',
    yaxis_title='Precio de Orden'
)

st.plotly_chart(fig2)

# Tercer gráfico
with st.container():
    filtrar_region = st.selectbox('Selecciona la Región de Envío para Filtrar', ['Todos'] + list(agrupado['ShipRegion'].unique()))

    if filtrar_region != 'Todos':
        mask_region = agrupado['ShipRegion'] == filtrar_region
        agrupado = agrupado[mask_region]

    grafico3 = px.bar(agrupado, 
                 x='ShipRegion', 
                 y='conteo_acomulado', 
                 title=f'Cantidad Acumulada por Región de Envío (Filtrado: {filtrar_region})',
                 labels={'ShipRegion': 'Región de Envío', 'conteo_acomulado': 'Cantidad Acumulada'})

    st.plotly_chart(grafico3)
