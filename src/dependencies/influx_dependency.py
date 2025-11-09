from influxdb_client import InfluxDBClient
from src.core.settings import settings

def get_influx_client():
    client = InfluxDBClient(
        url=settings.INFLUXDB_URL,
        token=settings.INFLUXDB_TOKEN,
        org=settings.INFLUXDB_ORG
    )
    return client
