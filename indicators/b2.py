import numpy as np
import pandas as pd
import talib


class B2TradeIndicator:
    """
    B2TradeIndicator class calculates trading indicators based on input data.

    Args:
        dataframe (pd.DataFrame): The input data in the form of a Pandas DataFrame.
        source (str, optional): The source column in the DataFrame to use for calculations (default is "close").
        **kwargs: Additional keyword arguments for customization.

    Attributes:
        dataframe (pd.DataFrame): A copy of the input DataFrame.
        periods (int): The number of periods for ATR and other calculations.
        multiplier (float): A multiplier used in the indicator calculations.
        changeATR (bool): Whether to change the ATR calculation method.
        showsignals (bool): Whether to show buy/sell signals.
        close (pd.Series): The close price data from the DataFrame.
        low (pd.Series): The low price data from the DataFrame.
        high (pd.Series): The high price data from the DataFrame.
        open (pd.Series): The open price data from the DataFrame.

    Methods:
        apply_indicator(): Calculate and apply the trading indicator to the DataFrame.

    Example:
    --------
    ::
        indicator = B2TradeIndicator(dataframe, source="close", periods=14, multiplier=2.0, changeATR=True)
        result = indicator.apply_indicator()
    """

    def __init__(
        self,
        dataframe: pd.DataFrame,
        source: str = "close",
        **kwargs,
    ):
        """
        Initialize the B2TradeIndicator instance with the input data and parameters.

        Args:
            dataframe (pd.DataFrame): The input data in the form of a Pandas DataFrame.
            source (str, optional): The source column in the DataFrame to use for calculations (default is "close").
            **kwargs: Additional keyword arguments for customization.
        """
        self.dataframe = dataframe.copy()
        self.periods = kwargs.get("periods") or 200
        
        self.multiplier = kwargs.get("multiplier") or 0.5
        self.changeATR = kwargs.get("changeATR") or False
        self.showsignals = kwargs.get("showsignals") or True

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
        
        self.low = self.dataframe["Low"]
        self.close = self.dataframe["Close"]
        self.high = self.dataframe["High"]
        self.open = self.dataframe["Open"]

    @property
    def atr(
        self,
    ):
        """
        Calculate the Average True Range (ATR) based on the chosen calculation method.

        Returns:
            pd.Series: The ATR values.
        
        Example:
        --------
        ::
            atr_values = indicator.atr
        """
        if self.changeATR:
            return talib.ATR(
                self.high,
                self.low,
                self.close,
                self.periods,
            )
        return talib.SMA(
            talib.TRANGE(
                self.high,
                self.low,
                self.close,
            ),
            self.periods,
        )

    def apply_indicator(self) -> pd.DataFrame:
        """
        Apply the trading indicator to the input DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with added indicator columns.
        
        Example:
        --------
        ::
            result = indicator.apply_indicator()
        """
        
        # def nz(a, b):
        #     if a == np.nan:
        #         return b
        #     return a
        nz = lambda a, b: b if a == np.nan else a

        # src = input(hl2, title="Source")
        src = self.source

        # atr = changeATR ? atr(Periods) : atr2
        atr = np.array(self.atr)

        # up=src-(Multiplier*atr)
        up = src - (self.multiplier * atr)
        # dn=src+(Multiplier*atr)
        dn = src + (self.multiplier * atr)
        # trend = 1
        trend = np.full_like(dn, 1)
        upPlot = np.full_like(dn, np.nan)
        dnPlot = np.full_like(dn, np.nan)
        changeCond = np.full_like(dn, np.nan)
        buySignal = np.full_like(dn, False,dtype=bool)
        sellSignal = np.full_like(dn, False,dtype=bool)
        for index in range(1, len(self.source)):
            # up1 = nz(up[1],up)
            # up := close[1] > up1 ? max(up,up1) : up
            up1 = nz(up[index - 1], up[index])
            if self.source[index - 1] > up1:
                up[index] = max(up[index], up1)
            # dn1 = nz(dn[1], dn)
            # dn := close[1] < dn1 ? min(dn, dn1) : dn
            dn1 = nz(dn[index - 1], dn[index])
            if self.source[index - 1] < dn1:
                dn[index] = min(dn[index], dn1)
            # trend := nz(trend[1], trend)
            trend[index] = nz(trend[index - 1], trend[index])
            if trend[index] == -1 and self.source[index] > dn1:
                trend[index] = 1
            elif trend[index] == 1 and self.source[index] < up1:
                trend[index] = -1

            # upPlot
            if trend[index] == 1:
                upPlot[index] = up[index]

            # dnPlot
            if trend[index] != 1:
                dnPlot[index] = dn[index]
            # else:
            #     trend[index] = np.nan

            # buySignal
            buySignal[index] = trend[index] == 1 and trend[index - 1] == -1
            # sellSignal
            sellSignal[index] = trend[index] == -1 and trend[index - 1] == 1
            # changeCond = trend != trend[1]
            changeCond[index] = trend[index] != trend[index - 1]

        mPlot = (self.open + self.high + self.low + self.close) / 4
        # print(self.dataframe["Close"], self.close)
        # self.dataframe['Up'] = np.where(trend != 1, np.nan, up)#.ffill()
        # print(buySignal[-50:], sellSignal[-50:])
        self.dataframe["Up"] = upPlot
        # self.dataframe['Dn'] = np.where(trend == 1, np.nan, dn)
        self.dataframe["Dn"] = dnPlot
        self.dataframe["M"] = mPlot
        self.dataframe["long_conditions"] = buySignal
        self.dataframe["short_conditions"] = sellSignal
        self.dataframe["ChangeCond"] = changeCond
        self.dataframe["Trend"] = trend
        self.dataframe["source"] = self.source
        # print(f"{self.dataframe['Dn']=}")
        # print(f"{self.dataframe['Up'].tail(50)=}")
        return self.dataframe