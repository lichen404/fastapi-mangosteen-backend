import os
from uvicorn import run

from api import app

if __name__ == '__main__':
    run('main:app', reload=os.getenv("ENVIRONMENT", "development") == "development", host="0.0.0.0")
