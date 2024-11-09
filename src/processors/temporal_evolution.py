import pandas as pd
from pydantic import BaseModel, ConfigDict
from processors.data_processor import DataProcessor
import warnings
warnings.filterwarnings('ignore')


class TemporalEvolution(BaseModel):
    processor: DataProcessor
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def magnitude_evolution(
        self, 
        start_year: int,
        end_year: int
    ) -> pd.DataFrame:
        df_filtered = self.processor.filter_by_year_range(start_year, end_year)
        return df_filtered.groupby('YEAR')['MAGNITUD'].mean().reset_index()

    def profundidad_evolution(
        self, 
        start_year: int, 
        end_year: int
    ) -> pd.DataFrame:
        df_filtered = self.processor.filter_by_year_range(start_year, end_year)
        return df_filtered.groupby('YEAR')['PROFUNDIDAD'].mean().reset_index()