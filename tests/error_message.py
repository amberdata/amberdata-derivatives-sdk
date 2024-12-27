# ======================================================================================================================

"""
Module containing all the different error messages returned by the API.
"""


# ======================================================================================================================

# pylint: disable=line-too-long,too-few-public-methods
class ErrorMessage:
    """
    Class containing all the different error messages returned by the API.
    """

    INVALID_PARAMETER = "Parameter 'invalid' is not supported."
    INVALID_PARAMETER_EXCHANGE_TRADFI = "Invalid argument exchange: expected one of [tradfi,TRADFI], found '<exchange>'."
    INVALID_PARAMETER_INTERVAL = "Invalid argument interval: expected one of [7d,7D,30d,30D,90d,90D,180d,180D], found '<interval>'."
    INVALID_PARAMETER_IS_ATM = "Invalid argument 'isAtm': expected boolean, found '<is_atm>'."
    INVALID_PARAMETER_MARGIN_TYPE = "Invalid argument marginType: expected one of [coins,stables], found '<margin_type>'."
    INVALID_PARAMETER_PUT_CALL = "Invalid argument putCall: expected one of [P,p,put,Put,PUT,C,c,call,Call,CALL], found '<put_call>'."
    INVALID_PARAMETER_STRIKE = "The argument 'strike' is not in numerical form (<strike>)."
    INVALID_PARAMETER_TIMESTAMP = "Invalid timestamp value: '<timestamp>'."
    INVALID_PARAMETER_TIME_FORMAT = "Invalid argument timeFormat: expected one of [nanoseconds,ns,milliseconds,ms,iso,iso8601,iso8611,human,human_readable,humanReadable,hr], found '<time_format>'."

    UNSUPPORTED_CURRENCY_SVI = "Unsupported currency for SVI: '<currency>'."
    UNSUPPORTED_EXCHANGE = "Parameter 'exchange' is not supported."

# ======================================================================================================================
