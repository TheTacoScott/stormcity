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
    self.sleep = threading.Event()
    self.status_lock = threading.Lock()
    self.work_q = queue.Queue()
    self.status = ""
    self.status_time = -1
  def job_add(self,url):
    pass
  def job_status(self,url):
    pass
  def job_results(self,url):
    pass
  def set_status(self,text):
    with self.status_lock:
      self.status = text
      self.status_time = time.time()

  def get_status(self):
    with self.status_lock:
      return (self.status,self.status_time)

  def run(self):
    self.set_status("Worker Startup")
    while not self.stop.is_set():
      self.sleep.wait(0.1)
      self.sleep.clear()
      #self.sleep.set()
      if self.stop.is_set(): break
    self.set_status("Worker Shutdown")
    
