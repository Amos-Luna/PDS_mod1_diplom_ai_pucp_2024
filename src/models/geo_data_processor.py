import pandas as pd
import geopandas as gpd
from pydantic import BaseModel, ConfigDict
import warnings
warnings.filterwarnings('ignore')


class GeoDataProcessor(BaseModel):
    df: pd.DataFrame
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def make_choropleth(
        self, 
        start_year: int, 
        end_year: int
    ) -> gpd.GeoDataFrame:
        df_filtered = self.df[(self.df['YEAR'] > (start_year)) & (self.df['YEAR'] < (end_year))]
        df_sampled = df_filtered.sample(int(df_filtered.shape[0] * 0.1))
        gdf = gpd.GeoDataFrame(df_sampled, geometry=gpd.points_from_xy(df_sampled.LONGITUD, df_sampled.LATITUD))
        return gdf