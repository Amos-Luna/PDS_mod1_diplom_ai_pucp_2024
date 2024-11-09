import pandas as pd
from pydantic import BaseModel, ConfigDict
import warnings
warnings.filterwarnings('ignore')


class DataProcessor(BaseModel):
    df: pd.DataFrame
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    def filter_by_year_range(
        self, 
        start_year: int, 
        end_year: int
    ) -> pd.DataFrame:
        df_filtered = self.df[(self.df['YEAR'] > (start_year)) & (self.df['YEAR'] < (end_year))]
        return df_filtered