"""Spark Tasks Module."""

import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from source.utils.logging import LoggingHandler
from source.utils.config import TaskConfig

from typing import Dict, TypeVar, Any, Tuple


T = TypeVar('T', bound='SparkTask')


class SparkTask(LoggingHandler):
    """Contract for every Spark Task.

    Attributes:
        app_name (str): Spark session name.
        config (Config): object with read/write configs
        spark_session (SparkSession): Spark Session.

    """

    def __init__(self, app_name: str, config: TaskConfig, *args: Tuple, **kwargs: Dict[str, Any]):
        """Load Config and Init SparkSession.

        Parameters
        ----------
        app_name : str
            Spark session name.
        config : TaskConfig
            Config dataclass.
        """
        super().__init__(*args, **kwargs)

        self.app_name = app_name
        self.config = config

    def start_spark_session(self) -> 'SparkTask':
        """Step to start Spark Session.

        Returns: SparkTask
        """
        self.spark_session = SparkSession \
            .builder \
            .appName(self.app_name) \
            .getOrCreate()

        return self

    def read(self: T) -> T:
        """Step to read SparkTask Data Sources.

        Returns:
            SparkTask
        """
        return self

    def transform(self: T) -> T:
        """Step to transform the data, applying Business Rules.

        Returns:
            SparkTask
        """
        return self

    def write(self: T) -> T:
        """Step to Load the Data to the desired Sinks.

        Returns:
            SparkTask
        """
        return self

    def stop(self: T) -> T:
        """Stop Spark Session.

        Returns:
            SparkTask
        """
        self.spark_session.stop()  # type: ignore
        return self
