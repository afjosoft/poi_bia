#%%
import json
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

from shapely.wkt import loads
from shapely.geometry import Polygon, Point, shape
from geopy.geocoders import Nominatim

from arcgis.gis import GIS
#%%
# INGESTA DATOS ZIPCODES
CA_geojson = './../data/external/CA_zipcode.geojson'
FL_geojson = './../data/external/FL_zipcode.geojson'
IL_geojson = './../data/external/IL_zipcode.geojson'
NY_geojson = './../data/external/NY_zipcode.geojson'
TX_geojson = './../data/external/TX_zipcode.geojson'

CA_gdf = gpd.read_file(CA_geojson)
FL_gdf = gpd.read_file(FL_geojson)
IL_gdf = gpd.read_file(IL_geojson)
NY_gdf = gpd.read_file(NY_geojson)
TX_gdf = gpd.read_file(TX_geojson)

hot_df = pd.read_excel('./../data/raw/hot_latin_zipcode.xlsx')

zipcodes_gdf = gpd.GeoDataFrame(pd.concat([CA_gdf, FL_gdf, IL_gdf, NY_gdf, TX_gdf], ignore_index=True))
zipcodes_gdf = zipcodes_gdf.to_crs(epsg=4326)
#%%
# INGESTA DATOS PUNTOS DE INTERES
IL_df = pd.read_csv('./../data/raw/illinois.csv')
NY_df = pd.read_csv('./../data/raw/new_york.csv')
TX_df = pd.read_csv('./../data/raw/texas.csv')

IL_df['state'] = 'IL'
NY_df['state'] = 'NY'
TX_df['state'] = 'TX'

states_df = pd.concat([IL_df, NY_df, TX_df], axis=0, ignore_index=True)
states_df['geometry'] = states_df['geometry'].apply(loads)
states_gdf = gpd.GeoDataFrame(states_df, geometry='geometry')
states_gdf.set_crs(epsg=4326, inplace=True)
#%%
# INGESTA DATOS PRESENCIA USA
shops_df = pd.read_excel('./../data/raw/base_clientes_iberia.xlsx')
shops_df[['customer', 'name', 'address']] = shops_df[shops_df.columns[0]].str.split(': ', expand=True)
shops_df['address'] = shops_df['address'].str.split(',', n=1, expand=True)[0]
shops_df = shops_df.drop(columns=[shops_df.columns[0]])
#%%

#%%

# Crear una nueva columna de geometría a partir de las coordenadas
shops_df['geometry'] = shops_df.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)

# Convertir el DataFrame a un GeoDataFrame
gdf = gpd.GeoDataFrame(shops_df, geometry='geometry')

# Establecer el sistema de referencia de coordenadas (CRS)
gdf.set_crs(epsg=4326, inplace=True)

# Mostrar las primeras filas del GeoDataFrame para verificar
print(gdf.head())
#%%

#%%
# Realizar el spatial join
states_gdf = gpd.sjoin(states_gdf, zipcodes_gdf[['geometry', 'ZIP_CODE']], how='left', predicate='within')

# Convertir los polígonos en centroides
states_gdf['geometry'] = states_gdf['geometry'].apply(lambda geom: geom.centroid if geom.type == 'Polygon' else geom)
#%%

#%%
poi_zipcode_gdf = states_gdf[states_gdf['ZIP_CODE'] == '60515'] 
poi_zipcode_gdf.plot()
#%%

#%%

#%%
print(states_gdf['geometry'].geom_type)
#%%

# %%

# %%
