# ======================================================================================================================

"""
Module to handle Amberdata's API calls.
"""

# ======================================================================================================================

import os

import dotenv
import requests

from amberdata_derivatives.version import __version__

dotenv.load_dotenv()


# ======================================================================================================================

# pylint: disable=too-many-lines, too-many-public-methods
class AmberdataDerivatives:
    """
    Main class to handle Amberdata's API calls.
    """

    def __init__(self, api_key: str, time_format: str = None):
        """
        Initializes the SDK.

        QUERY PARAMS:
        - api_key     (string) [Required] The key granting access to the API.
        - time_format (string) [Optional] The default time format for all the endpoints (ms | iso | hr).
        """

        self.__base_url = os.getenv('API_URL', 'https://api.amberdata.com')
        self.__headers = {
            'accept':             'application/json',
            'Accept-Encoding':    'gzip',
            'x-api-key':          api_key,
            'x-amberdata-client': 'python-sdk-' + __version__,
        }
        self.__time_format = time_format
        self.__version = __version__

    # ==================================================================================================================

    def get_version(self):
        """
        Retrieves the version of the SDK.
        """

        return self.__version

    # ==================================================================================================================

    def get_instruments_information(self, **kwargs):
        """
        Given an exchange parameter and underlying currency (ex: deribit, BTC) this endpoint retrieves a list of all
        available active instruments.

        Users can pass a “timestamp” parameter to view the available active instruments at some point in the past.

        Users can also pass additional parameters to filter to a more narrow subset of tradable instruments.

        QUERY PARAMS:
        - exchange   (string)    [Optional] [Examples] deribit | okex | bybit
        - currency   (string)    [Optional] [Examples] BTC | SOL_USDC
        - putCall    (string)    [Optional] [Examples] C | P
        - strike     (int32)     [Optional] [Examples] 100000 | 3500
        - timestamp  (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:14:00
        - timeFormat (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/instruments/information',
            {
                **kwargs
            }
        )

    def get_instruments_most_traded(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the most traded instruments on a selected exchange for a selected underlying currency,
        for a given date range. Users can filter out select trade types: "ALL" trades, "Block" trades and "Non-Block"
        trades.

        QUERY PARAMS:
        - exchange     (string)    [Required] [Examples] deribit | okex | bybit
        - currency     (string)    [Required] [Examples] BTC | SOL_USDC
        - blockTradeId (boolean)   [Optional] [Examples] true
        - startDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate      (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timeFormat   (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/instruments/most-traded',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    # ==================================================================================================================

    def get_futures_perpetuals_apr_basis_constant_maturities(self, asset: str, interval: str, **kwargs):
        """
        This endpoint returns the quoted futures basis, for the various exchanges, interpolated to represent a constant
        DTE (days to expiration).

        The data is returned with 15min granularity, and the default interval is 7D.

        QUERY PARAMS:
        - asset      (string) [Required] [Examples] BTC | ETH
        - interval   (string) [Required] [Examples] 7D | 30D | 90D |180D
        - startDate  (string) [Required] [Optional] 1578531600 | 1578531600000 | 2020-09-01T01:00:00
        - endDate    (string) [Required] [Optional] 1578531600 | 1578531600000 | 2020-09-01T01:00:00
        - timeFormat (string) [Optional] [Optional] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/futures-perpetuals/apr-basis/constant-maturities',
            {
                'asset': asset,
                'interval': interval,
                **kwargs
            }
        )

    # pylint: disable=invalid-name # Disable warning about `marginType` because this is the name as expected in the API
    def get_futures_perpetuals_apr_basis_live_term_structures(self, asset: str, marginType: str, **kwargs):
        """
        This endpoint returns the current quoted futures prices along with the differential to spot and the annualized
        APR of the spot differential.

        QUERY PARAMS:
        - asset      (string) [Required] [Examples] BTC | ETH
        - marginType (string) [Required] [Examples] coins | stables
        - timeFormat (string) [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/futures-perpetuals/apr-basis/live-term-structures',
            {
                'asset': asset,
                'marginType': marginType,
                **kwargs
            }
        )

    def get_futures_perpetuals_open_interest(self, asset: str, **kwargs):
        """
        This endpoint returns the total asset open interest for both futures and perpetuals across all the exchanges.

        The open interest is returned in raw coin amounts and millions of dollars.

        QUERY PARAMS:
        - asset      (string) [Required] [Examples] BTC | ETH
        - startDate  (string) [Optional] [Examples] 1578531600 | 1578531600000 | 2020-09-01T01:00:00
        - endDate    (string) [Optional] [Examples] 1578531600 | 1578531600000 | 2020-09-01T01:00:00
        - timeFormat (string) [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/futures-perpetuals/open-interest-total',
            {
                'asset': asset,
                **kwargs
            }
        )

    # pylint: disable=invalid-name # Disable warning about `marginType` because this is the name as expected in the API
    def get_futures_perpetuals_realized_funding_rates_cumulated(self, asset: str, marginType: str, **kwargs):
        """
        This endpoint returns the total asset open interest for both futures and perpetuals across all the exchanges.

        The open interest is returned in raw coin amounts and millions of dollars.

        QUERY PARAMS:
        - asset      (string) [Required] [Examples] BTC | ETH
        - marginType (string) [Required] [Examples] coins | stables
        - startDate  (string) [Optional] [Examples] 1578531600 | 1578531600000 | 2020-09-01T01:00:00
        - endDate    (string) [Optional] [Examples] 1578531600 | 1578531600000 | 2020-09-01T01:00:00
        - timeFormat (string) [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/futures-perpetuals/realized-funding-rates-cumulated',
            {
                'asset': asset,
                'marginType': marginType,
                **kwargs
            }
        )

    def get_futures_perpetuals_volumes(self, asset: str, **kwargs):
        """
        This endpoint returns the rolling 24h volume for both futures and perpetuals of the underlying asset.

        The endpoint returns the USD volume in millions of dollars and the volume in units of underlying coins.

        QUERY PARAMS:
        - asset      (string) [Required] [Examples] BTC | ETH
        - startDate  (string) [Optional] [Examples] 1578531600 | 1578531600000 | 2020-09-01T01:00:00
        - endDate    (string) [Optional] [Examples] 1578531600 | 1578531600000 | 2020-09-01T01:00:00
        - timeFormat (string) [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/futures-perpetuals/volumes',
            {
                'asset': asset,
                **kwargs
            }
        )

    # ==================================================================================================================

    def get_options_scanner_block_trades(self, exchange: str, currency: str, **kwargs):
        """
        TODO.

        QUERY PARAMS:
        - exchange   (string)    [Required] [Examples] deribit | okex | bybit
        - currency   (string)    [Required] [Examples] BTC | SOL_USDC
        - startDate  (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timeFormat (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/options-scanner/block-trades',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_options_scanner_on_screen_trades(self, exchange: str, currency: str, **kwargs):
        """
        TODO.

        QUERY PARAMS:
        - exchange   (string)    [Required] [Examples] deribit | okex | bybit
        - currency   (string)    [Required] [Examples] BTC | SOL_USDC
        - startDate  (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timeFormat (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/options-scanner/on-screen-trades',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_options_scanner_strikes_bought_sold(self, exchange: str, currency: str, expiration: str, **kwargs):
        """
        TODO.

        QUERY PARAMS:
        - exchange   (string) [Required] [Examples] deribit | okex | bybit
        - currency   (string) [Required] [Examples] BTC | SOL_USDC
        - timeFormat (string) [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/options-scanner/strikes-bought-sold-by-aggressors',
            {
                'exchange': exchange,
                'currency': currency,
                'expiration': expiration,
                **kwargs
            }
        )

    def get_options_scanner_top_trades(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint contains all the relevant information about the most important trades both on screen and blocked.

        Besides the usual information this endpoint have some proprietary nuances that helps market watchers to read
        the flow deeply.

        Among others:
          - "Amberdata Direction" is the metrics we developed for gauging the real initiator of a trade
          - "Delta Hedge" highlight is a block trade contained a futures leg
          - The information of the orderbook prior to the trade ("pre" columns) and post ("post" columns ).

        It returns only active instruments.

        QUERY PARAMS:
        - exchange     (string)    [Required] [Examples] deribit | okex | bybit
        - currency     (string)    [Required] [Examples] BTC | SOL_USDC
        - blockTradeId (boolean)   [Optional] [Examples] true | false
        - startDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate      (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timeFormat   (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/options-scanner/top-trades',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_options_scanner_top_trades_by_unique_trade(self, exchange: str, currency: str, uniqueTrade: str, **kwargs):
        """
        TODO.

        QUERY PARAMS:
        - exchange     (string)    [Required] [Examples] deribit | okex | bybit
        - currency     (string)    [Required] [Examples] BTC | SOL_USDC
        - uniqueTrade  (string)    [Optional] [Examples] ...
        - blockTradeId (boolean)   [Optional] [Examples] true | false
        - timeFormat   (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/options-scanner/top-trades-by-unique-trade',
            {
                'exchange': exchange,
                'currency': currency,
                'uniqueTrade': uniqueTrade,
                **kwargs
            }
        )

    # ==================================================================================================================

    def get_realized_volatility_annual_performance(self, exchange: str, pair: str, **kwargs):
        """
        The endpoint returns the PnL of a pair on an exchange.

        QUERY PARAMS:
        - exchange   (string) [Required] [Examples] gdax
        - pair       (string) [Required] [Examples] btc_usd
        - timeFormat (string) [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """
        return self.__make_request(
            'markets/derivatives/analytics/realized-volatility/annual-performance',
            {
                'exchange': exchange,
                'pair': pair,
                **kwargs
            }
        )

    def get_realized_volatility_cones(self, exchange: str, pair: str, **kwargs):
        """
        The endpoint returns the percentile distribution of realized volatility for a specific spot trading pair.
        We can see the RV distribution for multiple measurement windows compared to the end date.

        QUERY PARAMS:
        - exchange   (string)    [Required] [Examples] gdax
        - pair       (string)    [Required] [Examples] btc_usd
        - startDate  (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timeFormat (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """
        return self.__make_request(
            'markets/derivatives/analytics/realized-volatility/cones',
            {
                'exchange': exchange,
                'pair': pair,
                **kwargs
            }
        )

    def get_realized_volatility_cones_information(self, exchange: str, **kwargs):
        """
        This information endpoint returns the available spot data for realized volatility and price calculations
        provided for each specific exchange.

        (AVAILABLE EXCHANGE: binance, bithumb, bitstamp, gdax, gemini, kraken, okex, poloniex)

        QUERY PARAMS:
        - exchange   (string) [Required] [Examples] binance | bithumb | ...
        - timeFormat (string) [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """
        return self.__make_request(
            'markets/derivatives/analytics/realized-volatility/cones/information',
            {
                'exchange': exchange,
                **kwargs
            }
        )

    def get_realized_volatility_correlation_beta(self, exchange: str, pair: str, pair2: str, **kwargs):
        """
        This endpoint returns the entire series of closing prices for two selected currency pairs from a given exchange.

        In addition to the series of closing prices the endpoint also returns the various realized volatility measures
        (using the high/low Parkinson method), rolling correlation calculation and beta. Beta is a measure of the second
        pair, in terms of the first pair.

        QUERY PARAMS:
        - exchange   (string) [Required] [Examples] gdax
        - pair       (string) [Required] [Examples] btc_usd
        - pair2      (string) [Required] [Examples] btc_usd
        - timeFormat (string) [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """
        return self.__make_request(
            'markets/derivatives/analytics/realized-volatility/correlation-beta',
            {
                'exchange': exchange,
                'pair': pair,
                'pair2': pair2,
                **kwargs
            }
        )

    def get_realized_volatility_implied_vs_realized(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the close-to-close hourly realized volatility for 7-days and 30-days.

        Using the daysToExpiration parameter, users can choose which "at-the-money" implied volatility to compare.

        QUERY PARAMS:
        - exchange   (string)    [Required] [Examples] deribit
        - currency   (string)    [Required] [Examples] BTC | SOL_USDC
        - startDate  (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timeFormat (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """
        return self.__make_request(
            'markets/derivatives/analytics/realized-volatility/implied-vs-realized',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_realized_volatility_monthly_vs_daily_ratio(self, exchange: str, pair: str, **kwargs):
        """
        This endpoint returns the relationship/comparison of Parkinson realized volatility calculation using
        one monthly calculation versus 30 daily calculations.

        The reasons these calculations might differ is due to mean-reversion, intra-month volatility
        and trending markets.

        QUERY PARAMS:
        - exchange   (string) [Required] [Examples] gdax
        - pair       (string) [Required] [Examples] btc_usd
        - timeFormat (string) [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """
        return self.__make_request(
            'markets/derivatives/analytics/realized-volatility/monthly-vs-daily-ratio',
            {
                'exchange': exchange,
                'pair': pair,
                **kwargs
            }
        )

    def get_realized_volatility_performance_comparison(self, exchange: str, pair: str, pair2: str, **kwargs):
        """
        This endpoint compares PnLs between two pairs.

        QUERY PARAMS:
        - exchange   (string)    [Required] [Examples] gdax
        - pair       (string)    [Required] [Examples] btc_usd
        - pair2      (string)    [Required] [Examples] btc_usd
        - startDate  (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timeFormat (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """
        return self.__make_request(
            'markets/derivatives/analytics/realized-volatility/performance-comparison',
            {
                'exchange': exchange,
                'pair': pair,
                'pair2': pair2,
                **kwargs
            }
        )

    def get_realized_volatility_seasonality_day_of_week(self, exchange: str, pair: str, **kwargs):
        """
        This endpoint returns the average realized volatility, for a select date range, grouped by the day-of-the-week.

        Users can view how weekend volatility compares to say, Wednesday realized volatility, etc.

        QUERY PARAMS:
        - exchange   (string)    [Required] [Examples] gdax
        - pair       (string)    [Required] [Examples] btc_usd
        - startDate  (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timeFormat (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """
        return self.__make_request(
            'markets/derivatives/analytics/realized-volatility/seasonality/day-of-week',
            {
                'exchange': exchange,
                'pair': pair,
                **kwargs
            }
        )

    def get_realized_volatility_seasonality_month_of_year(self, exchange: str, pair: str, **kwargs):
        """
        This endpoint returns the average realized volatility, for a select date range,
        grouped by the month-of-the-year.

        Users can view how Q4 volatility compares to say, Q1 volatility, etc.

        QUERY PARAMS:
        - exchange   (string)    [Required] [Examples] gdax
        - pair       (string)    [Required] [Examples] btc_usd
        - startDate  (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timeFormat (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """
        return self.__make_request(
            'markets/derivatives/analytics/realized-volatility/seasonality/month-of-year',
            {
                'exchange': exchange,
                'pair': pair,
                **kwargs
            }
        )

    # ==================================================================================================================

    def get_trades_flow_block_volumes(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the total block traded options volume for a selected exchange and a selected underlying
        currency.

        The volume is broken out by instruments for 3rd party "blockTrades" (venues such as Paradigm, GreeksLive, etc).

        QUERY PARAMS:
        - exchange   (string)    [Required] [Examples] deribit | okex | bybit
        - currency   (string)    [Required] [Examples] BTC | SOL_USDC
        - startDate  (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timeFormat (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/trades-flow/block-volumes',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_trades_flow_decorated_trades(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns option "times and sales" data that's decorated with pre-trade level-1 orderbook data and
        post-trade level-1 data.

        This is the core dataset of the Amberdata direction and GEX "Gamma Exposure" analysis.

        We use this orderbook impact to analyze the true aggressor of every trade, while assuming that market-makers
        (aka "dealers") are typically the passive trade participants.

        QUERY PARAMS:
        - currency     (string)    [Required] [Examples] BTC | SOL_USDC
        - exchange     (string)    [Required] [Examples] deribit | okex | bybit
        - blockTradeId (boolean)   [Optional] [Examples] true
        - startDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate      (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timeFormat   (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        - instrument   (string)    [Optional] [Examples] BTC-26APR24-100000-C
        - putCall      (string)    [Optional] [Examples] C | P
        - strike       (int32)     [Optional] [Examples] 100000 | 3500
        """

        return self.__make_request(
            'markets/derivatives/analytics/trades-flow/decorated-trades',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_trades_flow_gamma_exposures_normalized_usd(self, exchange: str, currency: str, **kwargs):
        """
        This chart depicts the overall impact of "gamma exposure" (GEX) in terms of notional in the underlying for
        a 1% move in spot prices.

        QUERY PARAMS:
        - exchange   (string) [Required] [Examples] deribit | okex | bybit
        - currency   (string) [Required] [Examples] BTC | SOL_USDC
        - timeFormat (string) [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/trades-flow/gamma-exposures/normalized-usd',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_trades_flow_gamma_exposures_snapshots(self, exchange: str, currency: str, **kwargs):
        """
        GEX aims to calculate the gamma exposure of Market Markers (MMs) and the resulting number of underlying
        contracts they must trade to keep their book delta-hedged.

        “Positive/long gamma” => more underlying stability because of “Buy low, sell high” “Negative/short gamma”
        => more underlying volatility because of “Sell low, buy high” Starting point is the direction of trades with our
        proprietary algorithm “AMBERDATA DIRECTION” composed of over 30 heuristics that estimate the “correct direction”
        = side of the initiator/aggressor of the trade at which other side there is "likely" a MMs. With this algorithm
        we are able to flag every trades by tracking the orderbook at millisecond level, to calculate and maintain a
        database of MMs gamma exposure.

        QUERY PARAMS:
        - exchange   (string)    [Required] [Examples] deribit | okex | bybit
        - currency   (string)    [Required] [Examples] BTC | SOL_USDC
        - startDate  (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timeFormat (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/trades-flow/gamma-exposures-snapshots',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_trades_flow_net_positioning(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the historical net positioning.

        QUERY PARAMS:
        - exchange              (string)    [Required] [Examples] deribit | okex | bybit
        - currency              (string)    [Required] [Examples] BTC | SOL_USDC
        - showActiveExpirations (boolean)   [Optional] [Examples] true
        - startDate             (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate               (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timeFormat            (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/trades-flow/net-positioning',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_trades_flow_net_volumes(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the historical net volumes.

        QUERY PARAMS:
        - exchange              (string)    [Required] [Examples] deribit | okex | bybit
        - currency              (string)    [Required] [Examples] BTC | SOL_USDC
        - blockTradeId          (boolean)   [Optional] [Examples] true
        - showActiveExpirations (boolean)   [Optional] [Examples] true
        - startDate             (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate               (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timeFormat            (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/trades-flow/net-volumes',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_trades_flow_options_yields(self, exchange: str, currency: str, **kwargs):
        """
        The “Covered Call” strategy assumes the trader is long exactly one unit of underlying asset after proceeds from
        selling their call.

        Example: Underlying price = $500, Trader position in underlying before selling the call = $475 Short $700 call
        proceeds = $25 Trader positioning in underlying after short call proceeds = $500 (one whole unit)

        RETURN CALCULATIONS
          Absolute Yield: $25/$475 Annualized Yield: $25/$475 (525,600 / minutes left until expiration

        The “Cash Secured Put” yield assumes the trader maintains enough cash on hand AFTER proceeds from selling
        the put.

        Example: Trader’s cash position BEFORE selling put = $275 Short $300 Put Proceeds = $25 Trader cash balance
        AFTER short put proceeds = $300 (100% cash secured)

        RETURN CALCULATIONS
          Absolute Yield: $25/$275 Annualized Yield: $25/$275 (525,600 / minutes left until expiration

        QUERY PARAMS:
        - exchange   (string) [Required] [Examples] deribit | okex | bybit
        - currency   (string) [Required] [Examples] BTC | SOL_USDC
        - timeFormat (string) [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/trades-flow/options-yields',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_trades_flow_put_call_distribution(self, exchange: str, currency: str, **kwargs):
        """
        Using proprietary algorithm (Amberdata direction) that assess real initiator of a trade, we sum by the amounts
        of contracts and premium of the last 24 hours (default) according to put/call/bought/sold metrics.

        QUERY PARAMS:
        - exchange            (string)    [Required] [Examples] deribit | okex | bybit
        - currency            (string)    [Required] [Examples] BTC | SOL_USDC
        - blockTradeId        (boolean)   [Optional] [Examples] true
        - startDate           (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate             (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - strike              (int32)     [Optional] [Examples] 100000 | 3500
        - expirationTimestamp (string)    [Optional] [Examples] 1578531600
        - timeFormat          (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/trades-flow/put-call-distribution',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_trades_flow_volume_aggregates(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the total traded options volume for a selected exchange and a selected underlying
        currency.

        The volume is broken out between onScreen exchange volume and 3rd party "blockTrades" (venues such as Paradigm,
        GreeksLive, etc).

        QUERY PARAMS:
        - exchange     (string)    [Required] [Examples] deribit | okex | bybit
        - currency     (string)    [Required] [Examples] BTC | SOL_USDC
        - startDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate      (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timeFormat   (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        - timeInterval (string)    [Optional] [Examples] minute | hour | day
        """

        return self.__make_request(
            'markets/derivatives/analytics/trades-flow/volume-aggregates',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    # ==================================================================================================================

    def get_volatility_delta_surfaces_constant(self, exchange: str, currency: str, **kwargs):
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
        - timeFormat            (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/volatility/delta-surfaces/constant',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_volatility_delta_surfaces_floating(self, exchange: str, currency: str, **kwargs):
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
        - timeFormat            (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/volatility/delta-surfaces/floating',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_volatility_index(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the value of the BTC (or other altcoin) VIX.
        The methodology of this index is similar to the VIX but for the underlying crypto.
        Deribit developed their Bitcoin VIX called the DVOL index.

        QUERY PARAMS:
        - exchange   (string)    [Required] [Examples] deribit | okex | bybit
        - currency   (string)    [Required] [Examples] BTC | SOL_USDC
        - startDate  (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timestamp  (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:14:00
        - timeFormat (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/volatility/index',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_volatility_index_decorated(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the value of the BTC (or other altcoin) VIX.

        The methodology of this index is similar to the VIX but for the underlying crypto.

        Deribit developed their Bitcoin VIX called the DVOL index.

        Along with the volatility index we are also returned underlying volatility surface datapoints (such as skew)
        and underlying spot prices.

        QUERY PARAMS:
        - currency   (string)    [Required] [Examples] BTC | SOL_USDC
        - exchange   (string)    [Required] [Examples] deribit | okex | bybit
        - startDate  (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timestamp  (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:14:00
        - timeFormat (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/volatility/index-decorated',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_volatility_level_1_quotes(self, exchange: str, currency: str, **kwargs):
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
        - timeFormat   (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/volatility/level-1-quotes',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_volatility_metrics(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint contains all the metrics useful for having an immediate overview of the options market,
        for each active expiry. The current Mark IV is updated every minute.

        These metrics are then compared according to the selected "daysBack" parameter.

        All the differences are found in the columns with the indication "change" (current metrics vs days ago metrics).

        QUERY PARAMS:
        - exchange   (string)    [Required] [Examples] deribit | okex | bybit
        - currency   (string)    [Required] [Examples] BTC | SOL_USDC
        - daysBack   (date-time) [Optional] [Examples] 1 | 7 | 14
        - timeFormat (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/volatility/metrics',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_volatility_of_volatility(self, currency: str, **kwargs):
        """
        This endpoint contains all the metrics useful for having an immediate overview of the options market,
        for each active expiry. The current Mark IV is updated every minute.

        These metrics are then compared according to the selected "daysBack" parameter.

        All the differences are found in the columns with the indication "change" (current metrics vs days ago metrics).

        QUERY PARAMS:
        - exchange   (string)    [Required] [Examples] deribit | okex | bybit
        - currency   (string)    [Required] [Examples] BTC | SOL_USDC
        - daysBack   (date-time) [Optional] [Examples] 1 | 7 | 14
        - timeFormat (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/volatility/volatility-of-volatility',
            {
                'currency': currency,
                **kwargs
            }
        )

    def get_volatility_term_structures_constant(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the term structure (for exchange listed expirations) with forward volatility calculations.

        QUERY PARAMS:
        - exchange   (string)    [Required] [Examples] deribit | okex | bybit
        - currency   (string)    [Required] [Examples] BTC | SOL_USDC
        - timestamp  (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:14:00
        - timeFormat (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/volatility/term-structures/forward-volatility/constant',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_volatility_term_structures_floating(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the term structure (for exchange listed expirations) with forward volatility calculations.

        QUERY PARAMS:
        - exchange   (string)    [Required] [Examples] deribit | okex | bybit
        - currency   (string)    [Required] [Examples] BTC | SOL_USDC
        - timestamp  (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:14:00
        - timeFormat (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/volatility/term-structures/forward-volatility/floating',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_volatility_term_structures_richness(self, exchange: str, currency: str, **kwargs):
        """
        This endpoint returns the term structure richness.

        The “Term Structure Richness” is the relative “level” of the Contango or Backwardation shape. A reading of 1.00
        would be a perfectly flat term structure - as measured by our method - while readings below/above represent
        Contango/Backwardation respectively.

        Using the term structure levels enables us to quantify how extended the term structure pricing currently is,
        at any point in time. The calculation take a ratio of 7-day ATM IV versus, 30-day, 60-day. 90-day and 180-days.

        QUERY PARAMS:
        - exchange   (string)    [Required] [Examples] deribit | okex | bybit
        - currency   (string)    [Required] [Examples] BTC | SOL_USDC
        - startDate  (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - endDate    (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:00:00
        - timestamp  (date-time) [Optional] [Examples] 1578531600 | 1578531600000 | 2024-04-03T08:14:00
        - timeFormat (string)    [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/volatility/term-structures/richness',
            {
                'exchange': exchange,
                'currency': currency,
                **kwargs
            }
        )

    def get_volatility_variance_premium(self, currency: str, **kwargs):
        """
        This endpoint returns the Deribit "DVol" index, shifted to align with historical realized volatility.
        Since option implied volatility is pricing future realized volatility, this endpoint helps users measure the
        accuracy of such expectation. When the VRP (variance risk premium) is positive, implied volatility was higher
        than future realized volatility, meaning options were overpriced. Vice versa when VRP was negative.

        The Deribit DVol index has 30-days to maturity and the measured realized volatility uses a 30-day calculation
        window. Realized volatility is measured using the high/low "Parkinson" volatility method.

        QUERY PARAMS:
        - currency   (string) [Required] [Examples] BTC | SOL_USDC
        - timeFormat (string) [Optional] [Defaults] milliseconds | ms* | iso | iso8601 | hr
        """

        return self.__make_request(
            'markets/derivatives/analytics/volatility/variance-premium',
            {
                'currency': currency,
                **kwargs
            }
        )

    # ==================================================================================================================

    def __make_request(self, url_path: str, query_params: dict):
        """Helper method to make HTTP GET requests and parse the JSON response into a DataFrame."""

        # Add default parameters
        if self.__time_format is not None:
            if 'timeFormat' not in query_params:
                query_params['timeFormat'] = self.__time_format

        # Build query and URL
        query_string = '&'.join([f"{key}={value}" for key, value in query_params.items()])
        url = f"{self.__base_url}/{url_path}?{query_string}"

        # Issue REST call & parse response payload
        response = requests.get(url, headers=self.__headers, timeout=30)
        return response.json()

# ======================================================================================================================
