from typing import Any, Dict
from risque.common.interfaces import RisqueServerInterface
from risque.common.task import Task


def on_connect(
    sid: str = None,
    env: Dict = None,
    auth: Any = None,
    server: RisqueServerInterface = None,
):
    """
    On connect, log client details.
    """
    print("New client connected:", sid)


def on_disconnect(
    sid: str = None,
    server: RisqueServerInterface = None,
):
    """
    On disconnect remove all tasks by this client.
    """
    print("Client disconnected! Removing tasks queued by:", sid)
    server.task_manager.remove_task_by_client_id(client_id=sid)


def on_queue_task(
    sid: str = None,
    data: Dict = None,
    server: RisqueServerInterface = None,
):
    task = Task(
        data=data.get("data"),
        kind=data.get("kind"),
        client_id=sid,
    )

    print("Client:", sid, "requested to queue task:", task)
    server.task_manager.add_task(task=task)


def on_fetch_task(
    sid: str = None,
    data: Dict = None,
    server: RisqueServerInterface = None,
):
    task_kind = data.get("kind")
    print("Client:", sid, "requested to fetch task by kind:", task_kind)
    task: Task = server.task_manager.get_task(
        client_id=sid,
        kind=task_kind
    )
    return task.to_dict()


server_event_handlers = {
    "connect": on_connect,
    "disconnect": on_disconnect,
    "queue_task": on_queue_task,
    "fetch_task": on_fetch_task,
}
