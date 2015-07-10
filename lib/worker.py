import threading
import time
import lib
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
    
    self.results = {}
    self.results_lock = threading.Lock()

  def set_next_purge(self):
    self.next_purge = time.time() + 120

  def job_update(self,url,data):
    with self.results_lock:
      pass

  def job_status(self,url):
    with self.results_lock:
      pass

  def job_results(self,url):
    with self.results_lock:
      pass

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
        for key in self.results:
          pass
        self.set_next_purge()

      #get a url from the queue to work on 
      try:
        self.url_to_process = lib.work_q.get(block=True,timeout=0.25)
      except queue.Empty:
        continue

      #process job here
      #add results to job dict

      self.set_status("Fetching:" + self.url_to_process)
      if self.stop.is_set(): break
    self.set_status("Worker Shutdown")
    
