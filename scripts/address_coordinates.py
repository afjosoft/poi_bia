#%%
import os
import json
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

from shapely.wkt import loads
from shapely.geometry import Polygon, Point, shape
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

from arcgis.gis import GIS
#%%
# INGESTA DATOS PRESENCIA USA
shops_df = pd.read_excel('./../data/raw/base_clientes_iberia.xlsx')
shops_df[['customer', 'name', 'address']] = shops_df[shops_df.columns[0]].str.split(': ', expand=True)
shops_df['address'] = shops_df['address'].str.split(',', n=1, expand=True)[0]
shops_df = shops_df.drop(columns=[shops_df.columns[0]])

shops_df.head()
# %%
# Inicializar el geocodificador
geolocator = Nominatim(user_agent="geoapiExercises")

# Usar RateLimiter para evitar superar el límite de consultas
#geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Función para obtener las coordenadas
def get_coordinates(address):
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    else:
        return (None, None)

# Crear la columna 'geometry' con las coordenadas
test_df = shops_df.head(1)
test_df['geometry'] = test_df['address'].apply(get_coordinates)

# Mostrar el DataFrame con la nueva columna
print(test_df)
# %%
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")
addr = '350 5th Ave, New York, NY 10118'
location = geolocator.geocode(addr)
print(location.longitude)
# %%

#%%
# Inicializar el geocodificador
geolocator = Nominatim(user_agent="poi_bia_coordinates10", timeout=10)

# Usar RateLimiter para evitar superar el límite de consultas
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Función para obtener las coordenadas
def get_coordinates(address):
    location = geocode(address)
    if location:
        return (location.latitude, location.longitude)
    else:
        return (None, None)

# Crear una copia de test_df para evitar modificar el original
#test_df = shops_df.head(1000).copy()
test_df = shops_df.iloc[9000:].copy()

# Usar .loc para asignar la nueva columna
test_df.loc[:, 'geometry'] = test_df['address'].apply(get_coordinates)

# Mostrar el DataFrame resultante
#print(test_df['geometry'])
# %%
test_df.to_csv('./../data/processed/base_clientes_iberia_coordinates_09.csv', index=False)
# %%

#%%
# Ruta de la carpeta que contiene los archivos CSV
folder_path = './../data/processed/'

# Lista para almacenar cada DataFrame leído
df_list = []

# Iterar sobre cada archivo en la carpeta
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path)
        df_list.append(df)

# Concatenar todos los DataFrames en uno solo
combined_df = pd.concat(df_list, ignore_index=True)
# %%
# Convertir la columna 'geometry' en geometría utilizando GeoPandas
combined_gdf = gpd.GeoDataFrame(
    combined_df, geometry=gpd.points_from_xy(combined_df['geometry'].apply(lambda x: eval(x)[1]),
                                             combined_df['geometry'].apply(lambda x: eval(x)[0])))

# %%
# Guardar el GeoDataFrame como un archivo GeoJSON
output_geojson_path = './../data/processed/base_clientes_iberia_consolidado.geojson'
combined_gdf.to_file(output_geojson_path, driver='GeoJSON')
# %%
