"""Task config module."""
from __future__ import annotations

from pydantic import BaseModel


class TableProperties(BaseModel):
    """TableProperties is a list with properties of an specific table."""
    format: str
    mode: str = ''
    path: str
    table_name: str


class TaskConfig(BaseModel):
    """TaskConfig with task properties."""
    sink_table: TableProperties
    source_table: TableProperties
    task_name: str
