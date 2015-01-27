class result_logger:
	def __init__(self, filename):
		self.filename = filename
		self.output_file = open( self.filename, 'w' )
		self.sublogger = None

	def set_sublogger(self, logger):
		if self.sublogger:
			self.sublogger.logger_close()

		self.sublogger = logger

	def log_uid(self, uid):
		self.output_file.write(str(uid))
		if self.sublogger:
			self.sublogger.log_uid(uid)
			
	def log_make(self, status):
		self.output_file.write(','+status+'\n')
		if self.sublogger:
			self.sublogger.log_make(status)

	def log_exec(self, cmd, status, errmsg=''):
		self.output_file.write(','+cmd+','+status)
		if 'FAILURE' in status:
			self.output_file.write(','+errmsg)
			self.output_file.write('\n')

		if self.sublogger:
			self.sublogger.log_exec(cmd, status, errmsg)

	def log_cmp(self, status):
		self.output_file.write(','+status+'\n')
		if self.sublogger:
			self.sublogger.log_cmp(status)

	def logger_close(self):
		self.output_file.close()
		if self.sublogger:
			self.sublogger.logger_close()
