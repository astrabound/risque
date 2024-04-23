from collections import deque

from risque.common.interfaces import TaskInterface, TaskManagerInterface


class TaskManager(TaskManagerInterface):

    def __init__(self) -> None:
        self.tasks = {}

    def add_task(self, task: TaskInterface = None) -> None:
        if task is None:
            return

        if task.kind not in self.tasks:
            self.tasks[task.kind] = deque()

        self.tasks[task.kind].append(task)

    def remove_task_by_client_id(self, client_id: str = None) -> None:

        for task_kind, task_deque in self.tasks.items():
            self.tasks[task_kind] = deque(
                filter(
                    lambda task: task.client_id != client_id,
                    task_deque
                )
            )

    def __repr__(self) -> str:
        task_count = sum(map(
            len,
            self.tasks.values()
        ))
        return f"<TaskManager - task count:{task_count}>"
