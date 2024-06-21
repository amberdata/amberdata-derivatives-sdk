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
    INVALID_PARAMETER_MARGIN_TYPE = "Invalid argument marginType: expected one of [coins,stables], found '<margin_type>'."
    INVALID_PARAMETER_PUT_CALL = "Invalid argument putCall: expected one of [ALL,P,p,put,Put,PUT,C,c,call,Call,CALL], found '<put_call>'."
    INVALID_PARAMETER_TIMESTAMP = "Invalid timestamp value: '<timestamp>'."
    INVALID_PARAMETER_TIME_FORMAT = "Invalid argument timeFormat: expected one of [nanoseconds,ns,milliseconds,ms,iso,iso8601,iso8611,human,human_readable,humanReadable,hr], found '<time_format>'."

# ======================================================================================================================
