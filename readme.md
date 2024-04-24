# Risque

Risque is a task queue management server and client API to enable executing
operations with dependencies in parallel from different client processes.

## Installation

To install risque, run: `pip install risque`

## Examples

### Server

To start the server, create an instance of `RisqueServer` class and call run
method.

```python
from risque.server import RisqueServer

rs = RisqueServer()
rs.run()
```

### Client

In client create an instance of `RisqueClient` class.

```python
from risque.client import RisqueClient
from risque.common.task import Task


rs = RisqueClient()

for i in range(10):
    rs.queue_task(
        Task(
            data=i,
            kind="PRINT_A_NUM",
        )
    )
```
