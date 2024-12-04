import pandas as pd
import sqlite3
import os
import numpy as np

#Solicito la ruta donde voy mapear traer la base de datos
def mapear_datos(nombre_bd, formato): 
    carpeta = os.path.dirname(__file__)
    db_path = os.path.join(carpeta, '..', 'data', f'{nombre_bd}{formato}')
    return db_path

#Le solicito me traiga las tablas de la Base de datos y me lo guarde como dicionario
def cargar_datos(ruta_archivo):
    conn = sqlite3.connect(ruta_archivo)
    
    dataframes = {}
    
    tablas = pd.read_sql('SELECT name FROM sqlite_master WHERE type = "table"', conn)
    
    for tabla in tablas['name']:
        dataframes[tabla] = pd.read_sql(f'SELECT * FROM "{tabla}"', conn)
    
    conn.close()   
    
    return dataframes
# Le muestra la ruta de datos
ruta = mapear_datos("Northwind_small",".sqlite")

# Cargar los datos en forma de direccionario
datos = cargar_datos(ruta)
datos

# tablas de la base de datos

orden = datos['Order']
clientes = datos['Customer']
categorias = datos['Category']
ordenes_detalles = datos['OrderDetail']
productos = datos['Product']
empleado = datos['Employee']
region = datos['Region']
proveedor = datos['Supplier']
territorio = datos['Territory']

# Conexion de tablas primer grafico
conteo = ordenes_detalles.groupby("ProductId")["Id"].count()
producto = productos[["ProductName", "Id"]]

conexion = pd.merge(conteo, producto,left_on="ProductId",right_on="Id")
conexion = conexion.rename(columns={"Id_x":"Cantidad"})

conexion_ordenada = conexion.sort_values(by="Cantidad", ascending=False).head(10)

# Conexion de tablas segundo grafico


precio_producto = productos[["UnitPrice"]]
precio_producto = precio_producto.rename(columns={"UnitPrice": "Precio_de_producto"})
precio_orden_compra = ordenes_detalles[["UnitPrice"]]
precio_orden_compra = precio_orden_compra.rename(columns={"UnitPrice": "Precio_Orden"})

precio_combinado = pd.concat([precio_producto, precio_orden_compra], axis=1)

# Conexion de tablas tercero grafico

ordenes= orden[["Id", "ShipRegion"]]
Cantidad = ordenes_detalles[["Quantity","OrderId"]]

merge_1 = pd.merge(ordenes, Cantidad, left_on='Id', right_on='OrderId')

agrupado = merge_1.groupby('ShipRegion')['Quantity'].sum().reset_index(name='conteo_acomulado').sort_values(by='conteo_acomulado', ascending= False)


