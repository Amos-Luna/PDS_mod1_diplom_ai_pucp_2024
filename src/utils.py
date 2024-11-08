import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import geopandas as gpd
import numpy as np
from constants import FONSTSIZE, FONTWEIGHT
import warnings
warnings.filterwarnings('ignore')


def read_dataset(
    path: str
) -> pd.DataFrame:
    
    df =  pd.read_excel(path)
    df['FECHA_UTC'] = pd.to_datetime(df['FECHA_UTC'], format='%Y%m%d')
    df['YEAR'] = df['FECHA_UTC'].dt.year
    
    return df


def read_shapefile(
    path: str
) -> gpd.GeoDataFrame:
    
    gdf_peru = gpd.read_file(path)
    return  gdf_peru
    
    
def data_loader(
    uploaded_dataset: str, 
    uploaded_geojson: str
) -> tuple[pd.DataFrame, gpd.GeoDataFrame]:

    if (uploaded_dataset is not None) and (uploaded_geojson is not None):        
        df: pd.DataFrame = read_dataset(uploaded_dataset)
        gdf_peru: gpd.GeoDataFrame = read_shapefile(uploaded_geojson)
        return df, gdf_peru
    else:
        return None, None


def plot_temporal_evolution_magnitude(df):
    sns.lineplot(x='YEAR', y='MAGNITUD', data=df, marker='o', color='b')
    plt.xlabel("Año", fontsize=FONSTSIZE, fontweight=FONTWEIGHT)
    plt.ylabel("Magnitud Promedio", fontsize=FONSTSIZE, fontweight=FONTWEIGHT)
    plt.grid(True, linestyle='--', alpha=0.2)
    plt.tight_layout()
    return plt.gcf()

    
def plot_temporal_evolution_profundidad(df):
    sns.lineplot(x='YEAR', y='PROFUNDIDAD', data=df, marker='o', color='g', )
    plt.xlabel("Año", fontsize=FONSTSIZE, fontweight=FONTWEIGHT)
    plt.ylabel("Profundidad Promedio (m)", fontsize=FONSTSIZE, fontweight=FONTWEIGHT)
    plt.grid(True, linestyle='--', alpha=0.2)
    plt.tight_layout()
    return plt.gcf()


def plot_choropleth_peru(df, gdf_peru, gdf_limits_peru):
    fig, ax = plt.subplots(figsize=(6, 6))
    gdf_peru.plot(ax=ax, color='lightblue', edgecolor='black')
    gdf_limits_peru.plot(ax=ax, marker='o', color='red', markersize=df['MAGNITUD'] * 3, label='Eventos sísmicos')
    plt.legend()
    ax.set_xlim(-82, -68)  
    ax.set_ylim(-20, 0)
    ax.set_axis_off()
    plt.tight_layout()
    return plt.gcf()


def plot_folium_map(
    df: pd.DataFrame
):
    sns.lineplot(x='YEAR', y='PROFUNDIDAD', data=df, marker='o', color='g', )
    plt.xlabel("Año", fontsize=FONSTSIZE, fontweight=FONTWEIGHT)
    plt.ylabel("Profundidad Promedio (m)", fontsize=FONSTSIZE, fontweight=FONTWEIGHT)
    plt.tight_layout()
    return plt.gcf()


def plot_histogram_of_magnitud(
    df: pd.DataFrame
):

    counts, bins, _ = plt.hist(
        df['MAGNITUD'], 
        bins=np.arange(
            df['MAGNITUD'].min(), 
            df['MAGNITUD'].max() + 0.2, 
            0.2),
        alpha=0
    )
    
    max_bin_index = np.argmax(counts)
    bin_centers = bins[:-1] + np.diff(bins)/2
    for i, (count, center) in enumerate(zip(counts, bin_centers)):
        if i == max_bin_index:
            color = 'orange'
        else:
            color = 'steelblue'
        
        plt.bar(center, 
                count,
                width=0.1,
                color=color,
                edgecolor='black',
                linewidth=1)

    plt.xlabel('Magnitud', fontsize=FONSTSIZE, fontweight=FONTWEIGHT)
    plt.ylabel('Number of Eventos ocurridos', fontsize=FONSTSIZE, fontweight=FONTWEIGHT)
    plt.xticks(bin_centers, [f'{x:.1f}' for x in bin_centers], rotation=0, fontsize=10)
    plt.xlim(df['MAGNITUD'].min() - 0.2, df['MAGNITUD'].max() + 0.2)
    plt.grid(True, linestyle='--', alpha=0.2)
    plt.tight_layout()
    return plt.gcf()