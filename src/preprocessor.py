import pandas as pd
import geopandas as gpd

def read_dataset(
    path: str
) -> pd.DataFrame:
    
    df =  pd.read_excel(path)
    df['FECHA_UTC'] = pd.to_datetime(df['FECHA_UTC'], format='%Y%m%d')
    df['year'] = df['FECHA_UTC'].dt.year
    
    return df


def read_shapefile(
    path: str
) -> gpd.GeoDataFrame:
    
    gdf_peru = gpd.read_file(path)
    return  gdf_peru


def temporal_evolution_magnitude(
    df: pd.DataFrame,
    start_year: str, 
    end_year: str
) -> pd.DataFrame:
    
    df = df.copy()
    df = df[(df['year'] > int(start_year)) & (df['year'] < int(end_year))]
    
    return df.groupby('year')['MAGNITUD'].mean().reset_index()


def temporal_evolution_profundidad(
    df: pd.DataFrame,
    start_year: str, 
    end_year: str
) -> pd.DataFrame:
    
    df = df.copy()
    df = df[(df['year'] > int(start_year)) & (df['year'] < int(end_year))]

    return df.groupby('year')['PROFUNDIDAD'].mean().reset_index()


def make_choropleth(
    df: pd.DataFrame,
    start_year: str, 
    end_year: str
):
    df = df.copy()
    df = df[(df['year'] > int(start_year)) & (df['year'] < int(end_year))]
    df = df.sample(int(df.shape[0]*0.1))
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.LONGITUD, df.LATITUD))
    return gdf