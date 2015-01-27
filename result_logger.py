class result_logger:
	def __init__(self, filename):
		self.filename = filename
		self.output_file = open( self.filename, 'w' )

	def log_uid(self, uid):
		self.output_file.write(str(uid))
	
	def log_make(self, status):
		self.output_file.write(','+status+'\n')

	def log_exec(self, cmd, status):
		self.output_file.write(','+cmd+','+status)
		if 'ERROR' in status:
			self.output_file.write('\n')

	def log_cmp(self, status):
		self.output_file.write(','+status+'\n')

	def logger_close(self):
		self.output_file.close();
