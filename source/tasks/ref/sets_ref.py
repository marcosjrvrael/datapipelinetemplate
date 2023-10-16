"""Sets Ref Class Module."""
from source.tasks import SparkTask
from source.utils.task_config import TaskConfig
from definitions import ROOT_DIR
from source.utils.files_helper import get_dir_files
from typing import Dict


class SetsRefSparkTask(SparkTask):
    """SetsRefSparkTask class."""
    def __init__(self, app_name: str, config: TaskConfig) -> None:
        """Class init method."""
        self.sets_df_dict: Dict = {}

        super().__init__(app_name, config)

    def read(self) -> 'SetsRefSparkTask':
        """Read all files from a source."""
        files_name_list = get_dir_files(f'{ROOT_DIR}/{self.config.source_table.path}')

        for file in files_name_list:

            df = self.spark_session.read \
                .option("basePath", f"{ROOT_DIR}/{self.config.source_table.path}") \
                .format(self.config.source_table.path) \
                .parquet(f"{ROOT_DIR}/{self.config.source_table.path}/{file}")

            self.sets_df_dict.update({file: df})

        return self

    def transform(self) -> 'SetsRefSparkTask':
        """Apply all transformation in Dataframe."""
        for file_name, df in self.sets_df_dict.items():

            df_exp = df.select('sets.*', 'page')

            self.sets_df_dict.update({file_name: df_exp})

        return self

    def write(self) -> 'SetsRefSparkTask':
        """Write all loaded dataframes."""
        for file_name, df in self.sets_df_dict.items():
            file_name = file_name.replace('.', '_').replace('?', '/')
            df.write \
                .mode(self.config.sink_table.mode) \
                .format(self.config.sink_table.format) \
                .save(f'{ROOT_DIR}/{self.config.sink_table.path}{file_name}')
        return self
