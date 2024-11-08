import pandas as pd

def preprocess_data(
    df: pd.DataFrame,
    start_date: str, 
    end_date: str, 
    min_magnitude: float, 
    max_depth: float) -> pd.DataFrame:

    df['FECHA_UTC'] = pd.to_datetime(df['FECHA_UTC'], format='%Y%m%d')
    df['año'] = df['FECHA_UTC'].dt.year
    promedios_por_año = df.groupby('año')['MAGNITUD'].mean().reset_index()
    
    return promedios_por_año