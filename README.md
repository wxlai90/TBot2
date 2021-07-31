# TBot2

A lightweight and efficient python3 telegram bot framework (WIP). <img src="https://www.techopedia.com/images/uploads/6e13a6b3-28b6-454a-bef3-92d3d5529007.jpeg" width="150px" />

> A declarative telegram bot framework (WIP),
> that cuts down on development and cognitive load.

![](https://img.shields.io/badge/TELEGRAM-v93.0.0-GREEN) ![](https://img.shields.io/badge/PYTHON-3.8.10-GREEN)

## To Start

Get a bot token from Bot Father (@botfather) on Telegram.

Import and instantiate TBot2 with the token.

```python
from TBot2 import TBot2

t = TBot2(TOKEN)
```

Declare handlers for each type of message using @contains, @catch_all etc.

```python
@t.contains('apple')
def my_handler(req):
    return f"I love apple pies"


@t.catch_all()
def catch_all_handler(req):
    return "Sorry, I don't understand you."
```

Call ListenAndServer() to start listening.

```python
t.ListenAndServe()
```

## Full Example

```python
from TBot2 import TBot2

t = TBot2(TOKEN)

@t.contains('apple')
def my_handler(req):
    return f"I love apple pies"


@t.catch_all()
def catch_all_handler(req):
    return "Sorry, I don't understand you."

t.ListenAndServe()
```
