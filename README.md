# AI

This repository contains example code for an extremely simple cryptocurrency exchange.

## Running the example

You can run the FastAPI application by installing the dependencies:

```bash
pip install -r exchange/requirements.txt
```

And then start the server:

```bash
python exchange/app.py
```

This will launch a development server listening on port 8000.

Open `http://localhost:8000` in your browser to access a minimal GUI for the
exchange. It lets you view pairs, place orders and inspect the order book.

## Running tests

Unit tests cover the basic order placement and retrieval logic:

```bash
pytest
```

