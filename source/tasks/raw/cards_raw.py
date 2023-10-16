"""Cards Raw tasks module."""
import pyspark.sql.functions as F

from source.tasks import SparkTask
from source.utils.task_config import TaskConfig
from definitions import ROOT_DIR
from source.utils.files_helper import get_dir_files, file_name_without_extension

from typing import Dict


class CardsRawSparkTask(SparkTask):
    """CardsRawSparkTask Class."""
    def __init__(self, app_name: str, config: TaskConfig) -> None:
        """Class init method."""
        self.cards_df_dict: Dict = {}

        super().__init__(app_name, config)

    def read(self) -> 'CardsRawSparkTask':
        """Read all files from a source."""
        files_name_list = get_dir_files(f'{ROOT_DIR}/{self.config.source_table.path}')

        for file in files_name_list:
            df = self.spark_session.read.json(f'{ROOT_DIR}/{self.config.source_table.path}{file}')
            self.cards_df_dict.update({file_name_without_extension(file): df})

        return self

    def transform(self) -> 'CardsRawSparkTask':
        """Transform dataframe exploding cards column to generate one line per card."""
        for file_name, df in self.cards_df_dict.items():
            df = df.withColumn('cards', F.explode('cards'))
            self.cards_df_dict.update({file_name: df})

        return self

    def write(self) -> 'CardsRawSparkTask':
        """Write all loaded dataframes."""
        for file_name, df in self.cards_df_dict.items():
            df.write \
                .mode(self.config.sink_table.mode) \
                .format(self.config.sink_table.format) \
                .save(f'{ROOT_DIR}/{self.config.sink_table.path}{file_name}')
        return self
