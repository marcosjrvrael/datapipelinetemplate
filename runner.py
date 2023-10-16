import argparse
from source.utils import api_task
from source.utils.files_helper import create_dir_if_not_exist

from source import get_config, get_spark_task, run_api_task
from source.utils.logging import LoggingHandler


if __name__ == '__main__':

    logger = LoggingHandler()
    logger.log.info("Starting Runner")

    parser = argparse.ArgumentParser(description='Magic API or Spark pipeline')

    parser.add_argument('--spark_task',
                        dest='spark_task',
                        help='Name of the Spark Task that should be executed')

    parser.add_argument('--config_path',
                        dest='config_path',
                        help='Config Path of the Spark Task')

    parser.add_argument('--api_task',
                        dest='api_task',
                        help='Api task cards or sets')

    parser.add_argument('--api_url_task',
                        dest='api_url_task',
                        help='Collect data from API')

    parser.add_argument('--page_limit',
                        default=1,
                        dest='page_limit',
                        help='Limit of pages to collect usefull for cards endpoint')


    args = parser.parse_args()

    spark_task = args.spark_task

    path = args.config_path

    api_task = args.api_task

    api_url_task = args.api_url_task

    page_limit = int(args.page_limit)

    if api_url_task:
        create_dir_if_not_exist(path="data/tlz/cards")
        create_dir_if_not_exist(path="data/tlz/sets")
        logger.log.info(f"Starting Api {api_task} collect.")
        run_api_task(api_task, api_url_task, page_limit)
        logger.log.info(f"Finished API {api_task} collect.")



    else:
        config = get_config(path=path)
        create_dir_if_not_exist(path="data/raw/cards")
        create_dir_if_not_exist(path="data/raw/sets")
        create_dir_if_not_exist(path="data/ref/cards")
        create_dir_if_not_exist(path="data/ref/sets")

        if config is None:
            raise ValueError(f"Config of {spark_task} doesn't exists")
        spark_task = get_spark_task(spark_task, config)

        spark_task \
            .start_spark_session() \
            .read() \
            .transform() \
            .write()
