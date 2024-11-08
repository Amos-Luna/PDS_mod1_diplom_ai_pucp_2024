import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim
import folium
from folium import plugins
from folium.plugins import HeatMap
import numpy as np
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')


def temporal_evolution_magnitude(
    df: pd.DataFrame,
    start_year: str, 
    end_year: str
) -> pd.DataFrame:
    
    df = df.copy()
    df = df[(df['YEAR'] > int(start_year)) & (df['YEAR'] < int(end_year))]
    return df.groupby('YEAR')['MAGNITUD'].mean().reset_index()


def temporal_evolution_profundidad(
    df: pd.DataFrame,
    start_year: str, 
    end_year: str
) -> pd.DataFrame:
    
    df = df.copy()
    df = df[(df['YEAR'] > int(start_year)) & (df['YEAR'] < int(end_year))]
    return df.groupby('YEAR')['PROFUNDIDAD'].mean().reset_index()


def make_choropleth(
    df: pd.DataFrame,
    start_year: str, 
    end_year: str
):
    df = df.copy()
    df = df[(df['YEAR'] > int(start_year)) & (df['YEAR'] < int(end_year))]
    df = df.sample(int(df.shape[0]*0.1))
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.LONGITUD, df.LATITUD))
    return gdf


def get_lat_lon_country_peru(
    pais: str = 'Perú'
) -> tuple:
    geolocator = Nominatim(user_agent="my_peru_sismos_app")
    loc = geolocator.geocode(pais)
    if loc:
        return loc.latitude, loc.longitude
    else:
        return None, None


def process_folium_map(
    df: pd.DataFrame,
    start_year: str, 
    end_year: str
):
    try:
        df=df.copy()
        df = df[(df['YEAR'] >= start_year) & (df['YEAR'] <= end_year)]
        df = df.sample(int(df.shape[0]*0.05))
        
        country_lat, country_lon = get_lat_lon_country_peru()
        
        country_map = folium.Map(
            location=[country_lat, country_lon],
            zoom_start=5
        )
        
        heat_map_data = df[["LATITUD", "LONGITUD"]].values.tolist()
        c_map = country_map.add_child(plugins.HeatMap(heat_map_data, min_opacity=0.3, radius=13))
        return c_map
    
    except Exception as e:
        print(f"Error en process_folium_map: {str(e)}")
        return None
    

def process_histogram_magnitude(
    df: pd.DataFrame,
    start_year: str, 
    end_year: str
):
    df=df.copy()
    df = df[(df['YEAR'] >= start_year) & (df['YEAR'] <= end_year)]
    return df