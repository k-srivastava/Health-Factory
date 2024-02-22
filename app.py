import os

from flask import Flask

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')


@app.route('/')
def homepage() -> str:
    return '<h1>Hello, Health-Factory!</h1>'


if __name__ == '__main__':
    app.run()
