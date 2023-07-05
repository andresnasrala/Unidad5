from flask import Flask

app = Flask(__name__)
app.config.from_pyfile("config.py")


import src.models
import src.routes

if __name__ == "__main__":
    app.run(debug=True)
