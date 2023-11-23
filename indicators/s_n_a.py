import numpy as np
import pandas as pd
import talib


class SnATradeIndicator:
    def __init__(
            self,
            dataframe: pd.DataFrame,
            source: str = 'close',
            **kwargs,
    ):
        """
        SnATradeIndicator is a class for generating trading signals based on Smooth Average Range (SAR) and Range Filter.

        Args:
            dataframe (pd.DataFrame): The input DataFrame containing price data.
            source (str): The column name in the DataFrame representing the source price. Default is 'close'.
            smooth_period (int): The period for calculating the Smooth Average Range. Default is 128.
            multiplier (int): The multiplier applied to the Smooth Average Range. Default is 20.

        Attributes:
            dataframe (pd.DataFrame): A copy of the input DataFrame.
            source (pd.Series): The source price data.
            range_filter (pd.Series): The calculated Range Filter.
            conditions (dict): Dictionary containing 'long_conditions' and 'short_conditions' boolean arrays.
            smooth_period (int): The period for calculating the Smooth Average Range.
            multiplier (int): The multiplier applied to the Smooth Average Range.

        Methods:
            smooth_average_range_(source, time_period, mult):
                Calculate the Smooth Average Range.

            get_range_filter_(source, sm_average_range):
                Calculate the Range Filter.

            get_conditions(source, range_filter, up_ward, down_ward):
                Calculate trading conditions based on source data and indicators.

            apply_indicator():
                Apply the Smooth Average Range indicator to the input DataFrame and generate trading signals.

        Example:
            # Create an instance of SnATradeIndicator
            indicator = SnATradeIndicator(dataframe, source='close', smooth_period=128, multiplier=20)

            # Apply the indicator to the DataFrame and get trading signals
            signals_df = indicator.apply_indicator()
        """
        self.dataframe = dataframe.copy()
        self.smooth_period: int = kwargs.get("smooth_period") or 128
        self.multiplier: int = kwargs.get("multiplier") or 20

        self.range_filter = None
        source_type = kwargs.get("source_type", "close")

        if source_type == "open":
            self.source = self.dataframe["Open"]
        elif source_type == "high":
            self.source = self.dataframe["High"]
        elif source_type == "low":
            self.source = self.dataframe["Low"]
        elif source_type == "close":
            self.source = self.dataframe["Close"]
        elif source_type == "hl2":
            self.source = (self.dataframe["High"] + self.dataframe["Low"]) / 2
        elif source_type == "hlc3":
            self.source = (self.dataframe["High"] + self.dataframe["Low"] + self.dataframe["Close"]) / 3
        elif source_type == "ohlc4":
            self.source = (self.dataframe["Open"] + self.dataframe["High"] + self.dataframe["Low"] + self.dataframe["Close"]) / 4
        elif source_type == "hlcc4":
            self.source = (self.dataframe["High"] + self.dataframe["Low"] + self.dataframe["Close"] + self.dataframe["Close"]) / 4
        elif source_type == "another_source":
            self.source = kwargs.get("another_source", self.dataframe["Close"])
        else:
            self.source = self.dataframe["Close"]

        self.source = np.array(self.source)

        # self.source = self.dataframe[source]

    # Create Smooth Average Range by double applying EMA and multiply amplitude
    # smoothrng(src, per, mult)
    # smoothrng(x, t, m) = >
    #   wper = t * 2 - 1
    #   avrng = ta.ema(math.abs(x - x[1]), t)
    #   smoothrng = ta.ema(avrng, wper) * m
    @staticmethod
    def smooth_average_range_(source: pd.Series, time_period: int, mult: int) -> np.array:
        """
        Calculate the Smooth Average Range.

        Args:
            source (pd.Series): The source price data.
            time_period (int): The period for calculating the Smooth Average Range.
            mult (int): The multiplier applied to the Smooth Average Range.

        Returns:
            np.array: Smooth Average Range values.
        """
        w_period = time_period * 2 - 1
        abs_diff = np.abs(source - np.roll(source, -1))#.to_numpy()
        average_range = talib.EMA(abs_diff, time_period)
        return np.array(talib.EMA(average_range, w_period)) * mult

    # Create range filter as base for future calculations 
    # rngfilt(x, r) = >
    #   rngfilt = x
    #   rngfilt := x > nz(rngfilt[1]) ? x - r < nz(rngfilt[1]) ? nz(rngfilt[1]): x - r: x + r > nz(rngfilt[1]) ? nz(
    #     rngfilt[1]): x + r
    @staticmethod
    def get_range_filter_(source: pd.Series, sm_average_range: np.array) -> np.array:
        """
        Calculate the Range Filter.

        Args:
            source (pd.Series): The source price data.
            sm_average_range (np.array): Smooth Average Range values.

        Returns:
            pd.Series: Range Filter values.
        """
        range_filter = source.copy()
        for i in range(1, len(source)):
            if source[i] > range_filter[i - 1]:
                if source[i] - sm_average_range[i] < range_filter[i - 1]:
                    range_filter[i] = range_filter[i - 1]
                else:
                    range_filter[i] = source[i] - sm_average_range[i]
            else:
                if source[i] + sm_average_range[i] > range_filter[i - 1]:
                    range_filter[i] = range_filter[i - 1]
                else:
                    range_filter[i] = source[i] + sm_average_range[i]
        return range_filter

    # Define the long and short conditions
    # longCond = bool(na)
    # shortCond = bool(na)
    # longCond := src > filt and src > src[1] and upward > 0 or src > filt and src < src[1] and upward > 0
    # shortCond := src < filt and src < src[1] and downward > 0 or src < filt and src > src[1] and downward > 0
    @staticmethod
    def get_conditions(source: pd.Series, range_filter: np.array, up_ward: np.array, down_ward: np.array)\
            -> (np.array, np.array):
        """
        Calculate trading conditions based on source data and indicators.

        Args:
            source (pd.Series): The source price data.
            range_filter (pd.Series): The Range Filter.
            up_ward (np.array): Upward movement indicator.
            down_ward (np.array): Downward movement indicator.

        Returns:
            tuple of np.array: Long and short trading conditions.
        """
        # source_l_shifted = source.shift(-1).copy()
        source_l_shifted = np.roll(source, -1)
        long_conditions = (
            (source > range_filter) & (source > source_l_shifted) & (up_ward > 0) |
            (source > range_filter) & (source < source_l_shifted) & (up_ward > 0)
        )
        short_conditions = (
            (source < range_filter) & (source < source_l_shifted) & (down_ward > 0) |
            (source < range_filter) & (source > source_l_shifted) & (down_ward > 0)
        )
        # Add condition initializer
        # CondIni = 0
        # CondIni := longCond ? 1: shortCond ? -1: CondIni[1]
        # longCondition = longCond and CondIni[1] == -1
        # shortCondition = shortCond and CondIni[1] == 1
        cond_init = np.full_like(long_conditions, dtype=int, fill_value=0)
        long_final_condition = np.full_like(long_conditions, 0)
        short_final_condition = np.full_like(short_conditions, 0)
        for i in range(1, len(cond_init)):
            if long_conditions[i]:
                cond_init[i] = 1
            elif short_conditions[i]:
                cond_init[i] = -1
            else:
                cond_init[i] = cond_init[i - 1]
            long_final_condition[i] = long_conditions[i] and (cond_init[i - 1] == -1)
            short_final_condition[i] = short_conditions[i] and (cond_init[i - 1] == 1)
        return long_final_condition, short_final_condition

    def apply_indicator(self) -> pd.DataFrame:
        """
        Apply the Smooth Average Range indicator to the input DataFrame and generate trading signals.

        Returns:
            pd.DataFrame: The DataFrame with added indicator columns and trading signals.
        """
        smooth_average_range = self.smooth_average_range_(self.source, self.smooth_period, self.multiplier)
        self.range_filter = self.get_range_filter_(self.source, smooth_average_range)

        # Filter Direction
        # upward = 0.0
        # upward := filt > filt[1] ? nz(upward[1]) + 1: filt < filt[1] ? 0: nz(upward[1])
        # downward = 0.0
        # downward := filt < filt[1] ? nz(downward[1]) + 1: filt > filt[1] ? 0: nz(downward[1])
        up_ward = np.full_like(self.source, 0.0)
        up_ward_l_shifted = np.roll(up_ward, -1)
        up_ward_l_shifted[-1] = 0.0
        down_ward = np.full_like(self.source, 0.0)
        down_ward_l_shifted = np.roll(down_ward, -1)
        down_ward_l_shifted[-1] = 0.0

        for i in range(1, len(up_ward)):
            if self.range_filter[i] > self.range_filter[i - 1]:
                up_ward[i] = (up_ward[i - 1] or 0) + 1
            elif self.range_filter[i] < self.range_filter[i - 1]:
                up_ward[i] = 0
            else:
                up_ward[i] = up_ward[i - 1] or 0

            if self.range_filter[i] < self.range_filter[i - 1]:
                down_ward[i] = (down_ward[i - 1] or 0) + 1
            elif self.range_filter[i] > self.range_filter[i - 1]:
                down_ward[i] = 0
            else:
                down_ward[i] = down_ward[i - 1] or 0

        # Fill output dataframe with data to process
        self.dataframe['smoothing'] = smooth_average_range
        self.dataframe['range_filter'] = self.range_filter
        self.dataframe['high_band'] = self.range_filter + smooth_average_range
        self.dataframe['low_band'] = self.range_filter - smooth_average_range
        self.dataframe['up_ward'] = up_ward
        self.dataframe['down_ward'] = down_ward
        self.dataframe['source'] = self.source
        # Convert True False signal arrays to expected types
        long_conditions, short_conditions = self.get_conditions(self.source, self.range_filter, up_ward, down_ward)
        self.dataframe['long_conditions'], self.dataframe['short_conditions']\
            = long_conditions, short_conditions
            # = long_conditions.astype(float), short_conditions.astype(float)

        return self.dataframe
