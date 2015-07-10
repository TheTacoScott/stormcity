from flask import Flask,render_template,request
import lib
import lib.worker
import signal
import sys
import logging
lib.app = Flask(__name__)

worker = lib.worker.Fetcher()
worker.start()

def properexit(signum,frame):
  worker.stop.set()
  worker.join()
  lib.app.logger.info("OS Exit")
  sys.exit()

signal.signal(signal.SIGINT, properexit)

@lib.app.route("/")
@lib.app.route("/<name>")
def main(name="home"):
  return render_template('index.html',name=name)

if __name__ == "__main__":
  lib.app.run(debug=True)