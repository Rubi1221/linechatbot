from flask import Flask,render_template


from IoTService import app
import os

@app.route("/")
@app.route("/home")

def home():
    return "hello world"


if __name__ == "__main__":
    app.run('localhost',port = 5566)
