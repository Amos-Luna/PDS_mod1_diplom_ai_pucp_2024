import pandas as pd
from geopy.geocoders import Nominatim
import folium
from folium import plugins
from pydantic import BaseModel, Field, ConfigDict
import warnings
warnings.filterwarnings('ignore')


class LocationService(BaseModel):
    pais: str = Field(default="Perú")
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def get_lat_lon(self) -> tuple:
        geolocator = Nominatim(user_agent="my_peru_sismos_app")
        loc = geolocator.geocode(self.pais)
        if loc:
            return loc.latitude, loc.longitude
        else:
            return None, None


class MapProcessor(BaseModel):
    df: pd.DataFrame
    location_service: LocationService = LocationService()
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def process_folium_map(
        self, 
        start_year: int, 
        end_year: int
    ):
        try:
            df_filtered = self.df[(self.df['YEAR'] >= start_year) & (self.df['YEAR'] <= end_year)]
            df_sampled = df_filtered.sample(int(df_filtered.shape[0] * 0.05))
            
            country_lat, country_lon = self.location_service.get_lat_lon()
            if country_lat is None or country_lon is None:
                raise ValueError("No se pudo obtener latitud/longitud del país.")
            
            country_map = folium.Map(location=[country_lat, country_lon], zoom_start=5)
            heat_map_data = df_sampled[["LATITUD", "LONGITUD"]].values.tolist()
            folium_map = country_map.add_child(plugins.HeatMap(heat_map_data, min_opacity=0.3, radius=13))
            return folium_map

        except Exception as e:
            print(f"Error en process_folium_map: {str(e)}")
            return None