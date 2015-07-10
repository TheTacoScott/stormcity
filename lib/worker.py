import threading
import time
import lib
try:
  from urlparse import urlparse as urlparse
except:
  from urllib.parse import urlparse

try:
  import Queue as queue
except:
  import queue

class Fetcher(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.stop = threading.Event()
    self.status_lock = threading.Lock()
    self.status = ""
    self.status_time = -1
    self.purge_time = 60

  #shouldn't run in all threads if we ever were to have more than one, should probably be a seperate thread all-to-gether at some point
  def purge_cache(self):
    with lib.results_lock:
      to_delete = []
      for url in lib.results:
        thetime = lib.results[url]["time"]
        if time.time() - thetime >= self.purge_time:
          to_delete.append(url)
      for key in to_delete:
        del lib.results[key]

  def set_next_purge(self):
    self.next_purge = time.time() + self.purge_time

  def job_update(self,url,data):
    with lib.results_lock:
      lib.results[url] = {"time":time.time(),"data":data}

  def set_status(self,text):
    with self.status_lock:
      self.status = text
      self.status_time = time.time()

  def get_status(self):
    with self.status_lock:
      return (self.status,self.status_time)

  def run(self):
    self.set_next_purge()
    self.set_status("Worker Startup")
    while not self.stop.is_set():

      #purged old results
      if time.time() > self.next_purge:
        self.set_status("Purging Old Cache")
        self.purge_cache()
        self.set_next_purge()

      #get a url from the queue to work on 
      self.set_status("Checking for work...")
      try:
        self.url_to_process = lib.work_q.get(block=True,timeout=0.25)
      except queue.Empty:
        continue
      
      #process job here
      parsed_uri = urlparse(self.url_to_process)
      if parsed_uri.hostname in lib.url_handlers:
        data = lib.url_handlers[parsed_uri.hostname](self.url_to_process)
      else:
        data = lib.url_handlers["GLOBAL"](self.url_to_process)

      #add results to job dict
      self.job_update(self.url_to_process,data)

      self.set_status("Fetching:" + self.url_to_process)
      if self.stop.is_set(): break
    self.set_status("Worker Shutdown")
    
