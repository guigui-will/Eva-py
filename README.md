# eva-py

Python bindings for the [EVA DCL](https://github.com/Carla-Corp/eva-ts) configuration language.

## Requirements

- Python 3.10+
- The compiled EVA native library (`libeva-<platform>-<arch>.so`)

## Installation

```bash
git clone https://github.com/your-org/eva-py
cd eva-py
```

Place the compiled `libeva` shared library inside the `eva/` folder at the root of the project.

## Usage

```python
from eva_dcl import Eva

config = Eva("path/to/config.eva")

name = config.get("project", "name")
version = config.get("project", "version")

messages = config.get("dev", "messages")
for msg in messages:
    print(msg)

meta = config.get("project", "meta")
author = meta.get("author")
```

## API

### `Eva(filepath)`

Loads and parses an `.eva` file. Raises `RuntimeError` if the file can't be opened.

### `eva.get(namespace, field)`

Returns the value of `field` inside `namespace`. Raises `KeyError` if it doesn't exist.

Return types:

| EVA type | Python type |
|----------|-------------|
| string   | `str`       |
| number   | `float`     |
| bool     | `bool`      |
| nil      | `EvaNil`    |
| list     | `EvaList`   |
| map      | `EvaMap`    |

### `EvaList`

| Member | Description |
|--------|-------------|
| `.length` | Number of elements |
| `.get(i)` | Get element at index `i` |
| `.list()` | Return all elements as a Python list |

### `EvaMap`

| Member | Description |
|--------|-------------|
| `.length` | Number of keys |
| `.get(key)` | Get value by key |
| `.keys()` | Return an `EvaList` of all keys |

### `EvaNil`

Represents a null value. Evaluates to `False`, `0`, and `"nil"` in their respective contexts.

## License

MIT
