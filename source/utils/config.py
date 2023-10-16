"""General config util methods regarding schema mapper and job config read."""
import json

from source.utils.task_config import TaskConfig


def get_config(path: str) -> TaskConfig:
    """Load config of a specific task.

    Args:
        path (str): Path to config file.

    Returns:
        Optional[TaskConfig]: Task configuration.
    """
    try:
        with open(path) as config_file:
            config_dict = json.load(config_file)

        return TaskConfig(**config_dict)
    except Exception as e:
        raise OSError(f"Unable to load Task Config. \n Error message: {e}")
