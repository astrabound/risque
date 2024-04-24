import socketio
from dataclasses import dataclass
from typing import Dict

from risque.common.constants import (
    DEFAULT_RISQUE_SERVER_HOST, DEFAULT_RISQUE_SERVER_PORT,
)
from risque.common.interfaces import RisqueClientInterface
from risque.common.singleton import SingletonMeta


@dataclass
class TaskRequest:
    kind: str
    data: Dict

    def to_dict(self) -> Dict:
        return {
            "kind": self.kind,
            "data": self.data,
        }


class RisqueClient(RisqueClientInterface, metaclass=SingletonMeta):

    def __init__(
        self,
        host: str = DEFAULT_RISQUE_SERVER_HOST,
        port: int = DEFAULT_RISQUE_SERVER_PORT,
    ) -> None:
        self.host = host
        self.port = port
        self.io = socketio.SimpleClient()

        self.io.connect(f"http://{self.host}:{self.port}")

    def queue_task(self, task_request: TaskRequest = None) -> None:
        self.io.call(
            event="queue_task",
            data=task_request.to_dict()
        )

    def fetch_task(self, task_kind: str = None) -> None:
        return self.io.call(
            event="fetch_task",
            data={
                "kind": task_kind
            }
        )
