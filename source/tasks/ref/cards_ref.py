"""Cards Ref Tasks module."""
import pyspark.sql.functions as F

from source.tasks import SparkTask
from source.utils.task_config import TaskConfig
from definitions import ROOT_DIR
from source.utils.files_helper import get_dir_files

from typing import Dict


class CardsRefSparkTask(SparkTask):
    """CardsRefsSparkTask class."""
    def __init__(self, app_name: str, config: TaskConfig) -> None:
        """Class init method."""
        self.cards_df_dict: Dict = {}

        super().__init__(app_name, config)

    def read(self) -> 'CardsRefSparkTask':
        """Read all files from a source."""
        files_name_list = get_dir_files(f'{ROOT_DIR}/{self.config.source_table.path}')

        for file in files_name_list:

            df = self.spark_session.read \
                .option("basePath", f"{ROOT_DIR}/{self.config.source_table.path}") \
                .format(self.config.source_table.path) \
                .parquet(f"{ROOT_DIR}/{self.config.source_table.path}/{file}")

            self.cards_df_dict.update({file: df})

        return self

    def transform(self) -> 'CardsRefSparkTask':
        """Transform all loaded dataframes."""
        for file_name, df in self.cards_df_dict.items():

            df_exp = df.select('cards.*', 'page')

            df_exp = df_exp.withColumn('name_ptBR', F.col('foreignNames.name')[5].alias('name_ptBR')) \
                .withColumn('type_ptBR', F.col('foreignNames.type')[5].alias('type_ptBR')) \
                .withColumn('text_ptBR', F.col('foreignNames.text')[5].alias('text_ptBR')) \
                .withColumn('flavor_ptBR', F.col('foreignNames.flavor')[5].alias('flavor_ptBR')) \
                .withColumn('imageUrl_ptBR', F.col('foreignNames.imageUrl')[5].alias('imageUrl_ptBR')) \
                .withColumn('multiverseid_ptBR', F.col('foreignNames.multiverseid')[5].alias('multiverseid_ptBR')) \
                .select('id', 'name', 'manaCost', 'cmc', 'colors', 'colorIdentity', 'type', 'types', 'subtypes', 'rarity', 'set',
                        'setName', 'text', 'artist', 'number', 'power', 'toughness', 'layout', 'multiverseid', 'imageUrl',
                        'variations', 'printings', 'legalities', 'name_ptBR', 'type_ptBR', 'flavor_ptBR', 'imageUrl_ptBR', 'multiverseid_ptBR',
                        'page')

            self.cards_df_dict.update({file_name: df_exp})

        return self

    def write(self) -> 'CardsRefSparkTask':
        """Write all loaded dataframes."""
        for file_name, df in self.cards_df_dict.items():
            file_name = file_name.replace('.', '_').replace('?', '/')
            df.write \
                .mode(self.config.sink_table.mode) \
                .format(self.config.sink_table.format) \
                .save(f'{ROOT_DIR}/{self.config.sink_table.path}{file_name}')
        return self
