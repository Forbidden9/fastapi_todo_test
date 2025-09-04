from enum import Enum


class StateTask(str, Enum):
    pending = "Pending"
    completed = "Completed"
