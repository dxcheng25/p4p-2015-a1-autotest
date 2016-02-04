import subprocess as sp
import threading as td
import sys, datetime

class paster_executor(td.Thread):
	def __init__(self, ep, arg_i, arg_t):
		self.ep = ep
		self.arg_i = arg_i
		self.arg_t = arg_t
		td.Thread.__init__(self)

	def run(self):
		#self.pp = sp.Popen([self.ep, '-i', str(self.arg_i), '-t', str(self.arg_t)], stdout=sp.PIPE, stderr=sp.PIPE)
		self.pp = sp.Popen([self.ep, '-t', str(self.arg_t)], stdout=sp.PIPE, stderr=sp.PIPE)
		self.pp.communicate()

#create a thread to execute paster
#kill the process if timeout
#return exit code
def executor_driver(ep, arg_i, arg_t, timeout):
	thread = paster_executor(ep, arg_i, arg_t)
    
    # start the executor in a separate thread, record execution time
	st = datetime.datetime.now()
	thread.start()
	thread.join(timeout)
	et = datetime.datetime.now()

	if thread.is_alive():
		#time out
		thread.pp.terminate()
		thread.join()
		return sys.maxint, -1

	return thread.pp.returncode, (et-st).total_seconds()
