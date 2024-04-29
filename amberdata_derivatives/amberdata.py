import requests

class AmberdataDerivatives:
    def __init__(self, api_key: str):
        self._base_url = "https://api.amberdata.com"
        self._headers = {
            "accept": "application/json",
            "Accept-Encoding": "gzip",
            "x-api-key": api_key
        }

    def get_instrument_information(self, **kwargs):
        """
        Given an exchange parameter and underlying currency (ex: deribit, BTC) this endpoint retrieves a list of all available active option.
        Users can pass a “timestamp” parameter to view the available active instruments at some point in the past.
        Users can also pass additional parameters to filter to a more narrow subset of tradable instruments.
        
        QUERY PARAMS:
        - exchange (string) [Optional] [Examples] deribit | okex | bybit
        - currency (string) [Optional] [Examples] BTC | SOL_USDC
        - putCall (string) [Optional] [Examples] C | P
        - strike (int32) [Optional] [Examples] 100000 | 3500
        - timestamp (string) [Optional] [Examples] 2024-04-03T08:00:00.000Z
        """

        query_params = {
        **kwargs 
        }
        
        query_string = '&'.join([f"{key}={value}" for key, value in query_params.items()])
        url = f"{self._base_url}/markets/derivatives/analytics/instruments/information?{query_string}"
        return self._make_request(url)

    def get_term_structure_floating(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the term structure (for exchange listed expirations) with forward volatility calculations.
        
        QUERY PARAMS:
        - exchange (string) [Required] [Examples] deribit | okex | bybit
        - currency (string) [Required] [Examples] BTC | SOL_USDC
        - startDate (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timeFormat (string) [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr |
        """

        query_params = {
        'exchange': exchange,
        'currency': currency,
        **kwargs 
        }

        query_string = '&'.join([f"{key}={value}" for key, value in query_params.items()])
        url = f"{self._base_url}/markets/derivatives/analytics/term-structure/forward-volatility?{query_string}"
        return self._make_request(url)

    def get_tickers(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the “Level 1” option chain with associated volatilities, greeks and underlying prices. This is the core underlying options data for many analytics.
        Although this data streams to Amberdata every 100ms this endpoint returns the first observation for each instrument in 1-minute, 1-hour or 1-day intervals.
        Note: Due to the density of data historical date ranges are limited to 60x 1-minute or 24x 1 hour intervals, per call. If no date range is passed, the most recent option chain will be returned.

        QUERY PARAMS:
        - exchange (string) [Required] [Examples] deribit | okex | bybit
        - currency (string) [Required] [Examples] BTC | SOL_USDC
        - instrument (string) [Optional] [Examples] BTC-26APR24-100000-C
        - isAtm (boolean) [Optional] [Examples] TRUE | FALSE
        - putCall (string) [Optional] [Examples] C | P
        - startDate (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - strike (int32) [Optional] [Examples] 100000 | 3500
        - timeInterval (string) [Optional] [Examples] minute | hour | day
        - timeFormat (string) [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr |
        """
        
        query_params = {
        'exchange': exchange,
        'currency': currency,
        **kwargs 
        }
    
        query_string = '&'.join([f"{key}={value}" for key, value in query_params.items()])
        url = f"{self._base_url}/markets/derivatives/analytics/tickers_1m?{query_string}"
        return self._make_request(url)

    def get_delta_surfaces_constant(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the option delta surface with constant maturities.

        Time Range Limit:
        The timeInterval supports minute, hour, day.
        Due to the density of data, historical time ranges (difference between startDate and endDate) are limited to the following call sizes:
        1 year of daily data
        90 days of hourly data
        1 hour of minutely data
        In order to get more than the maximum allowed, you can use the startDate & endDate parameters to move the time frame window to get the next n days/hours/minutes of data.

        QUERY PARAMS:
        - exchange (string) [Required] [Examples] deribit | okex | bybit
        - currency (string) [Required] [Examples] BTC | SOL_USDC
        - startDate (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - daysToExpirationStart (int32) [Optional] [Examples] 0 | 7 | 60
        - daysToExpirationEnd (int32) [Optional] [Examples] 1 | 30 | 180
        - timeInterval (string) [Optional] [Examples] minute | hour | day
        - timeFormat (string) [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr |
        """

        query_params = {
        'exchange': exchange,
        'currency': currency,
        **kwargs 
        }
    
        query_string = '&'.join([f"{key}={value}" for key, value in query_params.items()])
        url = f"{self._base_url}/markets/derivatives/analytics/delta-surfaces/constant?{query_string}"
        return self._make_request(url)

    def get_delta_surfaces_floating(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the option delta surface with floating maturities (exchange listed expirations).

        Time Range Limit:
        The timeInterval supports minute, hour, day.
        Due to the density of data, historical time ranges (difference between startDate and endDate) are limited to the following call sizes:
        1 year of daily data
        90 days of hourly data
        1 hour of minutely data
        In order to get more than the maximum allowed, you can use the startDate & endDate parameters to move the time frame window to get the next n days/hours/minutes of data.

        QUERY PARAMS:
        - exchange (string) [Required] [Examples] deribit | okex | bybit
        - currency (string) [Required] [Examples] BTC | SOL_USDC
        - startDate (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - daysToExpirationStart (int32) [Optional] [Examples] 0 | 7 | 60
        - daysToExpirationEnd (int32) [Optional] [Examples] 1 | 30 | 180
        - timeInterval (string) [Optional] [Examples] minute | hour | day
        - timeFormat (string) [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr |
        """

        query_params = {
        'exchange': exchange,
        'currency': currency,
        **kwargs 
        }
    
        query_string = '&'.join([f"{key}={value}" for key, value in query_params.items()])
        url = f"{self._base_url}/markets/derivatives/analytics/delta-surfaces/floating?{query_string}"
        return self._make_request(url)


    def _make_request(self, url: str):
        """Helper method to make HTTP GET requests and parse the JSON response into a DataFrame."""
        response = requests.get(url, headers=self._headers)
        data = response.json()
        return data