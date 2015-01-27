import subprocess as sp

#invoke make on root directory
#return code other than 0 indicates compilation errors
def build_assign(assign_root):
	make_process = sp.Popen(['make', '-C', assign_root, 'clean'], stdout=sp.PIPE)
	make_process.communicate()
	make_process = sp.Popen(['make', '-C', assign_root], stdout=sp.PIPE, stderr=sp.PIPE)
	streamdata = make_process.communicate()[0]
	rc = make_process.returncode

	return rc
