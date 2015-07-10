try:
  import Queue as queue
except:
  import queue
import threading


work_q = queue.Queue()

results = {}
results_lock = threading.Lock()

url_handlers = {}
