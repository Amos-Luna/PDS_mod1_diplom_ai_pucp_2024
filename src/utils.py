import matplotlib.pyplot as plt
import seaborn as sns

def plot_temporal_evolution_magnitude(df):
 
    sns.lineplot(x='year', y='MAGNITUD', data=df, marker='o', color='b')
    plt.xlabel("Año", fontsize=14)
    plt.ylabel("Magnitud Promedio", fontsize=14)
    plt.tight_layout()
    return plt

    
def plot_temporal_evolution_profundidad(df):
    sns.lineplot(x='year', y='PROFUNDIDAD', data=df, marker='o', color='g', )
    plt.xlabel("Año", fontsize=14)
    plt.ylabel("Profundidad Promedio (m)", fontsize=14)
    plt.tight_layout()
    return plt


def plot_choropleth_peru(df, gdf_peru, gdf_limits_peru):

    fig, ax = plt.subplots(figsize=(10, 10))
    gdf_peru.plot(ax=ax, color='lightblue', edgecolor='black')
    gdf_limits_peru.plot(ax=ax, marker='o', color='red', markersize=df['MAGNITUD'] * 3, label='Eventos sísmicos')
    plt.legend()
    ax.set_xlim(-82, -68)  
    ax.set_ylim(-20, 0)
    ax.set_axis_off()
    plt.tight_layout()
    return plt