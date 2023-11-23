from abc import ABC, abstractmethod
from pandas import DataFrame


class ABCIndicator(ABC):
    @abstractmethod
    def __init__(
        self,
        dataframe: DataFrame,
        source: str = "close",
        **kwargs,
    ):
        """
        Initialize the Indicator instance with the input data and parameters.

        Args:
            dataframe (DataFrame): The input data in the form of a Pandas DataFrame.
            source (str, optional): The source column in the DataFrame to use for calculations (default is "close").
            **kwargs: Additional keyword arguments for customization.
        """
        ...
        
    @abstractmethod    
    def apply_indicator(self) -> DataFrame:
        """
        Apply the trading indicator to the input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with added indicator columns.
        
        Example:
        --------
        ::
            result = indicator.apply_indicator()
        """
        ...