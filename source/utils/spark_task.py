"""SparkTask job definition methods."""
from source.utils.task_config import TaskConfig
from source.tasks import SparkTask

from source.tasks.raw import (
    CardsRawSparkTask,
    SetsRawSparkTask
)

from source.tasks.ref import (
    CardsRefSparkTask,
    SetsRefSparkTask
)


def get_spark_task(pipeline_name: str, config: TaskConfig) -> SparkTask:
    """Method to create instance of an SparkTask according to the parameters received.

    Args:
        pipeline_name (str): Name of the task.
        config (Config): Config dataclass containing parameters to process tasks.

    Returns:
        SparkTask: Instance of an SparkTask to run.
    """
    return {
        'cards_raw': CardsRawSparkTask(pipeline_name, config),
        'sets_raw': SetsRawSparkTask(pipeline_name, config),
        'cards_ref': CardsRefSparkTask(pipeline_name, config),
        'sets_ref': SetsRefSparkTask(pipeline_name, config),
    }[pipeline_name]
