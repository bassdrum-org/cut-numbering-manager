# Cut Numbering Manager

A simple PyQt5 application for sending OSC (Open Sound Control) messages with a REC button.

## Features

- Simple GUI with a REC button
- Configurable IP address and port
- Customizable OSC message and value
- Visual feedback when messages are sent

## Requirements

- Python 3.x
- PyQt5
- python-osc

## Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install PyQt5 python-osc
```

## Usage

Run the application:

```bash
python main.py
```

The default settings are:
- IP Address: 127.0.0.1 (localhost)
- Port: 8000
- OSC Message: /record
- Value: 1

You can modify these settings in the application interface before pressing the REC button.

## License

[MIT](LICENSE)
