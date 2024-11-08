import matplotlib.pyplot as plt
import seaborn as sns

def plot_temporal_evolution(df):
    plt.figure(figsize=(14, 6))
    sns.lineplot(x='año', y='MAGNITUD', data=df, marker='o', color='b')
    plt.title("Evolución Temporal de la Magnitud Promedio por Año", fontsize=16)
    plt.xlabel("Año", fontsize=14)
    plt.ylabel("Magnitud Promedio", fontsize=14)
    plt.tight_layout()
    return plt

    
    
# def plot_magnitude_over_time(df):
#     plt.figure(figsize=(10, 5))
#     plt.plot(df['FECHA_UTC'], df['MAGNITUD'], marker='o', color='b', linestyle='-', markersize=5)
#     plt.title('Magnitud de los sismos a lo largo del tiempo')
#     plt.xlabel('Fecha')
#     plt.ylabel('Magnitud')
#     plt.grid(True)
#     plt.tight_layout()
#     return plt


# def plot_depth_over_time(df):
#     plt.figure(figsize=(10, 5))
#     plt.plot(df['FECHA_UTC'], df['PROFUNDIDAD'], marker='o', color='r', linestyle='-', markersize=5)
#     plt.title('Profundidad de los sismos a lo largo del tiempo')
#     plt.xlabel('Fecha')
#     plt.ylabel('Profundidad (km)')
#     plt.grid(True)
#     plt.tight_layout()
#     return plt