from functools import partial
from typing import Callable, Dict
import socketio
import uvicorn

from risque.common.constants import (
    DEFAULT_RISQUE_SERVER_HOST, DEFAULT_RISQUE_SERVER_PORT,
)
from risque.common.interfaces import RisqueServerInterface
from risque.common.singleton import SingletonMeta
from risque.server.handlers import server_event_handlers
from risque.task_manager import TaskManager


class RisqueServer(RisqueServerInterface, metaclass=SingletonMeta):
    """
    Main class for risque server. The server instance is run as a centralised
    task execution queue management service. It exposes a websocket interface
    for clients to connect to.

    Example: Run risque server on port 5000 locally.
        ```python
        rs = RisqueServer(
            host="127.0.0.1",
            port=5000
        )
        rs.run()
        ```
    """

    def __init__(
        self,
        host: str = DEFAULT_RISQUE_SERVER_HOST,
        port: int = DEFAULT_RISQUE_SERVER_PORT,
    ) -> None:
        self.host = host
        self.port = port
        self.task_manager = TaskManager()
        self.io = socketio.AsyncServer(async_mode="asgi")
        self.app = socketio.ASGIApp(self.io)

        self.register_handlers(event_handler_map=server_event_handlers)

    def register_handlers(
        self,
        event_handler_map: Dict[str, Callable] = None
    ) -> bool:
        """
        Registers handlers for a set of events for the socket to listen to.

        Args:
        - event_handler_map: Dict[str, Callable]

            A map of event names to handlers for the events.

            Example:
            ```python
            {"connect": lambda: print("socket connected")}
            ```
        """
        if event_handler_map is None:
            return False

        for event, handler in event_handler_map.items():
            self.io.on(
                event=event,
                handler=partial(handler, server=self)
            )

    def run(self) -> None:
        """
        Runs the websocket server app on uvicorn.
        """
        try:
            uvicorn.run(self.app, host=self.host, port=self.port)
        except KeyboardInterrupt:
            pass
