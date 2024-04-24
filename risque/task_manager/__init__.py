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

    def get_task(
        self,
        client_id: str = None,
        kind: str = None
    ) -> TaskInterface:
        pending_task = None

        for task_kind, task_deque in self.tasks.items():
            if kind is not None and task_kind != kind:
                continue

            for i, task in enumerate(task_deque):
                if task.is_running or task.client_id != client_id:
                    continue

                self.tasks[task_kind][i].is_running = True
                pending_task = task
                break

        return pending_task

    def __repr__(self) -> str:
        task_count = sum(map(
            len,
            self.tasks.values()
        ))
        return f"<TaskManager - task count:{task_count}>"
