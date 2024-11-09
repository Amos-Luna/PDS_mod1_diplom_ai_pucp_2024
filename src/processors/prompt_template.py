from typing import ClassVar
from langchain.prompts import PromptTemplate


class InsightsPromptFinder:
    """Find Insigths into a image"""

    system_prompt: ClassVar[PromptTemplate] = PromptTemplate.from_template("""
        The graphs you will see are referenced to earthquakes that occurred in Peru in different years, so use it as a starting point to generate information from the visualizations of your panels.
        
        Analyze the chart shown below and provide a detailed summary of the key insights that can be obtained from it. Consider the following aspects when analyzing the chart:

        1.	What trends or patterns are visible in the data?
        2.	Are there any points or intervals where the data shows atypical behaviors or outliers?
        3.	Which data points appear to be the most relevant or significant based on their frequency, magnitude, or location on the chart?
        4.	Is there any evident relationship between the variables represented?
        5.	What areas of the chart may indicate a problem or opportunity within the context of earthquake data in Peru?
        6.	If the chart shows any segmentation or breakdown of the data, what differences or similarities are observed between the different categories or groups?

        In summary, provide a comprehensive analysis that highlights the most important insights that could be used to make decisions or take actions based on the data presented in the chart. As brief as possible in Spanish.
        
    """
    )