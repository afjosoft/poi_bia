#%%
import pandas as pd
import geopandas as gpd
import folium

from folium.plugins import MarkerCluster

#%%
#-- Load files
zipcodes_gdf = gpd.read_file('./../data/internal/zipcodes.geojson')
poi_gdf = gpd.read_file('./../data/internal/points_of_interes.geojson')
iberia_shops_gdf = gpd.read_file('./../data/internal/iberia_shops.geojson')

poi_gdf = poi_gdf.to_crs(epsg=4326)
multipolygon_mask = poi_gdf.geometry.geom_type == 'MultiPolygon'
poi_gdf.loc[multipolygon_mask, 'geometry'] = poi_gdf.loc[multipolygon_mask, 'geometry'].centroid

#%%
IL_poi_gdf = poi_gdf[poi_gdf['state'] == 'IL']
IL_poi_gdf = IL_poi_gdf.sort_values(by='ZIP_CODE', ascending=True)
#%%
# Crear un mapa centrado en las coordenadas medias de tus puntos
test_poi_gdf = IL_poi_gdf

map_center = [test_poi_gdf.geometry.y.mean(), test_poi_gdf.geometry.x.mean()]
mymap = folium.Map(location=map_center, zoom_start=5)

# Crear un diccionario para almacenar los markers por ZIP_CODE
zip_code_layers = {}

# Agregar los puntos de interés al mapa
for idx, row in test_poi_gdf.iterrows():
    zip_code = row['ZIP_CODE']
    hot_latin_zipcode = row['hot_latin_zipcode']

    # Crear o usar una capa por cada ZIP_CODE
    if zip_code not in zip_code_layers:
        zip_code_layers[zip_code] = folium.FeatureGroup(name=f"ZIP Code: {zip_code}", show=False)
        mymap.add_child(zip_code_layers[zip_code])
    
    # Definir el ícono basado en el valor de 'hot_latin_zipcode'
    if hot_latin_zipcode == 'Si':
        icon = folium.Icon(icon='star', prefix='fa', color='red')
    else:
        icon = folium.Icon(icon='info-sign', color='blue')

    # Añadir un marcador para cada punto
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=f"ZIP Code: {zip_code}",
        icon=icon
    ).add_to(zip_code_layers[zip_code])

# Agregar control de capas al mapa
folium.LayerControl().add_to(mymap)

# Guardar el mapa en un archivo HTML
mymap.save('map_with_zipcode_selection.html')
# %%
