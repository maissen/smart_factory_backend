# ================================
# Metrics Exception Group
# ================================
class MetricsError(Exception):
    """Base class for all metrics-related errors."""
    def __init__(self, message=None):
        if message is None:
            message = "A metrics-related error occurred."
        super().__init__(message)


class EmptyMetricsError(MetricsError):
    """Raised when metrics list is empty."""
    def __init__(self, message=None):
        if message is None:
            message = "Metrics list cannot be empty."
        super().__init__(message)


class MetricsValidationError(MetricsError):
    """Raised when metrics payload is malformed or missing required fields."""
    def __init__(self, message=None):
        if message is None:
            message = "Metrics payload is invalid."
        super().__init__(message)


# ================================
# TSDB Exception Group
# ================================
class TSDBError(Exception):
    """Base class for all time-series database errors."""
    def __init__(self, message=None):
        if message is None:
            message = "A time-series database error occurred."
        super().__init__(message)


class TSDBConnectionError(TSDBError):
    """Raised when InfluxDB cannot be reached."""
    def __init__(self, message=None):
        if message is None:
            message = "Unable to connect to InfluxDB."
        super().__init__(message)


class TSDBWriteError(TSDBError):
    """Raised when writing metrics to InfluxDB fails."""
    def __init__(self, message=None):
        if message is None:
            message = f"Failed to write metrics to InfluxDB."
        super().__init__(message)
