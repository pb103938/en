from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "bot status: online (see https://top.gg/bot/791768754518228992 for more)"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()