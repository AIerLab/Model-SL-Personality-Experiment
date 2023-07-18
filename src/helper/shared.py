from queue import Queue
from threading import Condition

global IN_QUEUE
global OUT_QUEUE
global CONDITION

IN_QUEUE = Queue()
OUT_QUEUE = Queue()
CONDITION = Condition()
