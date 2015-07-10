from flask import Flask,render_template,request,jsonify
import lib
import lib.worker
import signal
import sys
import json
from plugins import *
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

@lib.app.route("/api",methods=['POST'])
def api():
  api_data = request.get_json(force=True)
  return_data = {"status":1}
  if "action" in api_data and "param" in api_data:
    if api_data["action"] == "fetch":
      lib.work_q.put(api_data["param"])
      return_data["status"] = 0 
    elif api_data["action"] == "results":
      with lib.results_lock:
        if api_data["param"] in lib.results:
          return_data["data"] = lib.results[api_data["param"]]
          return_data["status"] = 0
        else:
          return_data["data"] = 0
  
  return jsonify(**return_data)


if __name__ == "__main__":
  lib.app.run(host='0.0.0.0', port=5959,debug=True)
  #lib.app.run()
