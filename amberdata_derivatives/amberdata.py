# ======================================================================================================================

import requests


# ======================================================================================================================

class AmberdataDerivatives:
    """
    SDK main class to handle Amberdata's API calls.
    """

    def __init__(self, api_key: str):
        """
        Initializes the SDK.

        QUERY PARAMS:
        - api_key (string) [Required] The key granting access to the API.
        """
        self.__base_url = "https://api.amberdata.com"
        self.__headers = {
            "accept":          "application/json",
            "Accept-Encoding": "gzip",
            "x-api-key":       api_key
        }

    def get_decorated_trades(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns option "times and sales" data that's decorated with pre-trade level-1 orderbook data and post-trdae level-1 data. 
        This is the core dataset of the Amberdata direction and GEX "Gamma Exposure" analysis. 
        We use this orderbook impact to analyze the true aggressor of every trade, while assuming that market-makers (aka "dealers") are typically the passive trade participants
        
        QUERY PARAMS:
        - exchange     (string)    [Required] [Examples] deribit | okex | bybit
        - currency     (string)    [Required] [Examples] BTC | SOL_USDC
        - startDate    (date-time) [Required] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate      (date-time) [Required] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - blockTradeId (boolean)   [Optional] [Examples] True | False
        - expiration   (string)    [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:14:00
        - instrument   (string)    [Optional] [Examples] BTC-14JUN24-84000-C
        - putCall      (string)    [Optional] [Examples] C | P
        - strike       (int32)     [Optional] [Examples] 100000 | 3500
        - timeFormat   (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr |
        """

        return self.__make_request(
            'markets/derivatives/analytics/decorated-trades',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_instrument_information(self, **kwargs):
        """
        Given an exchange parameter and underlying currency (ex: deribit, BTC) this endpoint retrieves a list of all
        available active instruments.
        Users can pass a “timestamp” parameter to view the available active instruments at some point in the past.
        Users can also pass additional parameters to filter to a more narrow subset of tradable instruments.

        QUERY PARAMS:
        - exchange  (string)    [Optional] [Examples] deribit | okex | bybit
        - currency  (string)    [Optional] [Examples] BTC | SOL_USDC
        - putCall   (string)    [Optional] [Examples] C | P
        - strike    (int32)     [Optional] [Examples] 100000 | 3500
        - timestamp (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:14:00
        """

        return self.__make_request(
            'markets/derivatives/analytics/instruments/information',
            {
                **kwargs
            }
        )

    def get_level_1_quotes(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the “Level 1” option chain with associated volatilities, greeks and underlying prices.
        This is the core underlying options data for many analytics.
        Although this data streams to Amberdata every 100ms this endpoint returns the first observation for each
        instrument in 1-minute, 1-hour or 1-day intervals.

        Note: Due to the density of data historical date ranges are limited to 60x 1-minute or 24x 1 hour intervals,
        per call. If no date range is passed, the most recent option chain will be returned.

        QUERY PARAMS:
        - exchange     (string)    [Required] [Examples] deribit | okex | bybit
        - currency     (string)    [Required] [Examples] BTC | SOL_USDC
        - instrument   (string)    [Optional] [Examples] BTC-26APR24-100000-C
        - isAtm        (boolean)   [Optional] [Examples] TRUE | FALSE
        - putCall      (string)    [Optional] [Examples] C | P
        - startDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate      (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - strike       (int32)     [Optional] [Examples] 100000 | 3500
        - timeInterval (string)    [Optional] [Examples] minute | hour | day
        - timeFormat   (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr |
        """

        return self.__make_request(
            'markets/derivatives/analytics/level-1-quotes',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_delta_surfaces_constant(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the option delta surface with constant maturities.

        Time Range Limit: The timeInterval supports minute, hour, day.
        Due to the density of data, historical time ranges (difference between startDate and endDate) are limited to the
        following call sizes:
          - 1 year of daily data
          - 90 days of hourly data
          - 1 hour of minutely data

        In order to get more than the maximum allowed, you can use the startDate & endDate parameters to move the time
        frame window to get the next n days/hours/minutes of data.

        QUERY PARAMS:
        - exchange              (string)    [Required] [Examples] deribit | okex | bybit
        - currency              (string)    [Required] [Examples] BTC | SOL_USDC
        - startDate             (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate               (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - daysToExpirationStart (int32)     [Optional] [Examples] 0 | 7 | 60
        - daysToExpirationEnd   (int32)     [Optional] [Examples] 1 | 30 | 180
        - timeInterval          (string)    [Optional] [Examples] minute | hour | day
        - timeFormat            (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr |
        """

        return self.__make_request(
            'markets/derivatives/analytics/delta-surfaces/constant',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_delta_surfaces_floating(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the option delta surface with floating maturities (exchange listed expirations).

        Time Range Limit: The timeInterval supports minute, hour, day.
        Due to the density of data, historical time ranges (difference between startDate and endDate) are limited to the
        following call sizes:
          - 1 year of daily data
          - 90 days of hourly data
          - 1 hour of minutely data

        In order to get more than the maximum allowed, you can use the startDate & endDate parameters to move the time
        frame window to get the next n days/hours/minutes of data.

        QUERY PARAMS:
        - exchange              (string)    [Required] [Examples] deribit | okex | bybit
        - currency              (string)    [Required] [Examples] BTC | SOL_USDC
        - startDate             (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate               (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - daysToExpirationStart (int32)     [Optional] [Examples] 0 | 7 | 60
        - daysToExpirationEnd   (int32)     [Optional] [Examples] 1 | 30 | 180
        - timeInterval          (string)    [Optional] [Examples] minute | hour | day
        - timeFormat            (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr |
        """

        return self.__make_request(
            'markets/derivatives/analytics/delta-surfaces/floating',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_term_structures_floating(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the term structure (for exchange listed expirations) with forward volatility calculations.

        QUERY PARAMS:
        - exchange   (string)    [Required] [Examples] deribit | okex | bybit
        - currency   (string)    [Required] [Examples] BTC | SOL_USDC
        - timestamp  (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:14:00
        - timeFormat (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr |
        """

        return self.__make_request(
            'markets/derivatives/analytics/term-structures/forward-volatility/floating',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_term_structures_constant(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the term structure (for exchange listed expirations) with forward volatility calculations.

        QUERY PARAMS:
        - exchange   (string)    [Required] [Examples] deribit | okex | bybit
        - currency   (string)    [Required] [Examples] BTC | SOL_USDC
        - timestamp  (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:14:00
        - timeFormat (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr |
        """

        return self.__make_request(
            'markets/derivatives/analytics/term-structures/forward-volatility/constant',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_term_structures_richness(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the term structure richness.
        The “Term Structure Richness” is the relative “level” of the Contango or Backwardation shape. 
        A reading of 1.00 would be a perfectly flat term structure - as measured by our method - while readings below/above represent Contango/Backwardation respectively. 
        Using the term structure levels enables us to quantify how extended the term structure pricing currently is, at any point in time.

        QUERY PARAMS:
        - exchange     (string)    [Required] [Examples] deribit | okex | bybit
        - currency     (string)    [Required] [Examples] BTC | SOL_USDC
        - startDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate      (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timeInterval (string)    [Optional] [Examples] minute | hour | day
        - timeFormat   (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr |
        """

        return self.__make_request(
            'markets/derivatives/analytics/term-structures/richness',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_volatility_cones(self, exchange: str, pair: str, **kwargs):
        """
        TThe endpoint returns the percentile distribution of realized volatility for a specific spot trading pair. 
        We can see the RV distribution for multiple measurement windows compared to the end date.

        QUERY PARAMS:
        - exchange     (string)    [Required] [Examples] gdax
        - pair         (string)    [Required] [Examples] btc_usd
        - startDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate      (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timeInterval (string)    [Optional] [Examples] minute | hour | day
        """

        return self.__make_request(
            'markets/derivatives/analytics/volatility-cones',
            {
                'exchange': exchange,
                'pair': pair,
                **kwargs
            }
        )

    def get_volatility_index(self, **kwargs):
        """
        This endpoint returns the value of the BTC (or other altcoin) VIX. 
        The methodology of this index is similar to the VIX but for the underlying crypto. 
        Deribit developed their Bitcoin VIX called the DVOL index.

        QUERY PARAMS:
        - exchange     (string)    [Optional] [Examples] deribit | okex | bybit
        - currency     (string)    [Optional] [Examples] BTC | SOL_USDC
        - startDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate      (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timeInterval (string)    [Optional] [Examples] minute | hour | day
        - timeFormat   (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr |
        """

        return self.__make_request(
            'markets/derivatives/analytics/volatility-index',
            {
                **kwargs
            }
        )

    def get_volatility_index_decorated(self, **kwargs):
        """
        This endpoint returns the value of the BTC (or other altcoin) VIX. 
        Along with the volatility index we are also returned underlying volatility surface datapoints (such as skew) and underlying spot prices.

        QUERY PARAMS:
        - exchange     (string)    [Optional] [Examples] deribit | okex | bybit
        - currency     (string)    [Optional] [Examples] BTC | SOL_USDC
        - startDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate      (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timeInterval (string)    [Optional] [Examples] minute | hour | day
        - timeFormat   (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr |
        """

        return self.__make_request(
            'markets/derivatives/analytics/volatility-index-decorated',
            {
                **kwargs
            }
        )

    # ==================================================================================================================

    def __make_request(self, url_path: str, query_params: dict):
        """Helper method to make HTTP GET requests and parse the JSON response into a DataFrame."""
        query_string = '&'.join([f"{key}={value}" for key, value in query_params.items()])
        url = f"{self.__base_url}/{url_path}?{query_string}"
        response = requests.get(url, headers=self.__headers, timeout=30)
        return response.json()

# ======================================================================================================================
