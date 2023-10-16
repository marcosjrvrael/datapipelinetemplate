"""Sets Raw tasks Class."""
import pyspark.sql.functions as F

from source.tasks import SparkTask
from source.utils.task_config import TaskConfig
from definitions import ROOT_DIR
from source.utils.files_helper import get_dir_files, file_name_without_extension

from typing import Dict


class SetsRawSparkTask(SparkTask):
    """SetsRawSparkTask Class."""
    def __init__(self, app_name: str, config: TaskConfig) -> None:
        """Class init method."""
        self.sets_df_dict: Dict = {}

        super().__init__(app_name, config)

    def read(self) -> 'SetsRawSparkTask':
        """Read all files from a source."""
        files_name_list = get_dir_files(f'{ROOT_DIR}/{self.config.source_table.path}')

        for file in files_name_list:
            df = self.spark_session.read.json(f'{ROOT_DIR}/{self.config.source_table.path}{file}')
            self.sets_df_dict.update({file_name_without_extension(file): df})

        return self

    def transform(self) -> 'SetsRawSparkTask':
        """Transform dataframe exploding sets column to generate one line per set."""
        for file_name, df in self.sets_df_dict.items():
            df = df.withColumn('sets', F.explode('sets'))
            self.sets_df_dict.update({file_name: df})

        return self

    def write(self) -> 'SetsRawSparkTask':
        """Write all loaded dataframes."""
        for file_name, df in self.sets_df_dict.items():
            df.write \
                .mode(self.config.sink_table.mode) \
                .format(self.config.sink_table.format) \
                .save(f'{ROOT_DIR}/{self.config.sink_table.path}{file_name}')
        return self
