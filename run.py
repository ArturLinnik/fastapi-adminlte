# -*- encoding: utf-8 -*-

# run.py

import uvicorn

from apps import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
