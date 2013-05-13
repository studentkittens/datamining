import logging
import contextlib
import time

@contextlib.contextmanager
def timing(task):
    start_time = time.time()
    yield
    ready_time = time.time()
    logging.info('%10f: -> %s' % (ready_time - start_time, task))
