import os

from flask import Flask, request, render_template



# Globals
from kedro.framework.session import KedroSession

PORT = 5001
app = Flask(__name__)


@app.route("/")
def index():
    return 'hello world'


@app.route("/run")
def run():
    with KedroSession.create(project_path=os.getcwd()) as session:
        context = session.load_context()

    return 'hello world'


def main():
    """
    runs the flask server on the provided host and port
    :return:
    """
    app.run(host="0.0.0.0", port=PORT, debug=True)


if __name__ == "__main__":
    main()