from uvicorn import run

from api import app

if __name__ == '__main__':
    run('main:app', reload=True,host="0.0.0.0")
