import os, sys, glob, random
import assign_builder, paster_exec, png_comparator
from result_logger import *
 
def a1_autotest(path_to_userids):	
	#grab all users' repo roots
	pus = glob.glob( path_to_userids+'/*' )
	output_file = result_logger('autotest_all.csv')

	for pu in pus:
		#grep userid
		uid = os.path.basename( pu )
		#.../userid/a1/
		pua1 = pu+'/'
		#.../userid/a1/bin
		pua1bin = pua1+'bin/'

		print 'entering ' + pua1
		output_file.set_sublogger( result_logger(pua1+'autotest.csv') )
		output_file.log_uid(uid)

		sys.stdout.write('\tbuilding...')
		sys.stdout.flush()
		#execute make under .../userid/a1/
		ret = assign_builder.build_assign(pua1)

		if ret != 0:
			print '\tfailed'
			output_file.log_make('MAKE_FAILURE')	
			continue
		else:
			print '\tsuccess'
			output_file.log_make('MAKE_SUCCESS')


		exe_para = 'paster_parallel'
		exe_nbio = 'paster_nbio'

		#ignore -i argument due to an error in the provided source code
		#for i in range(1,4):
		#.../userid/a1/bin/paster_parallel -i[1:3]
		execute_paster( pua1bin+exe_para, exe_para, 1, output_file, 30)
		remove_output()

		#.../userid/a1/bin/paster_nbio -i[1:3]
		execute_paster( pua1bin+exe_nbio, exe_nbio, 1, output_file, 30)
		remove_output()

	output_file.logger_close()


def remove_output():
	if os.path.exists('output.png'):
		os.remove('output.png')


def execute_paster(pu_exe, exe_name, img_seq, output_file, timeout):
	#number of t is randomly generated within [4,20]
	num_t = random.randrange(4, 16)

	#cmd = exe_name+' -i'+str(img_seq)+' -t'+str(num_t)
	cmd = exe_name+' -t'+str(num_t)

	print '\texecuting ' + cmd

	if not os.path.exists( pu_exe ):
		print '\texecutable not found'
		output_file.log_exec(cmd, 'EXECUTION_FAILURE', 'EXECUTABLE_NOT_FOUND')
		return

	ret = paster_exec.executor_driver(pu_exe, img_seq, num_t, timeout)
	if ret == sys.maxint:
		#execution timeout
		print '\ttimeout'
		output_file.log_exec(cmd, 'EXECUTION_FAILURE', 'TIMEOUT')
		return
	elif ret != 0:
		#execution failure
		print '\tfailed ' + str(ret)
		output_file.log_exec(cmd, 'EXECUTION_FAILURE', 'CODE:'+str(ret))
		return
	else:
		#execution success
		sys.stdout.write('\tsuccess')
		sys.stdout.flush()
		output_file.log_exec(cmd, 'EXECUTION_SUCCESS')	
	
	if not os.path.exists("output.png"):
		print '\tno output'
		output_file.log_cmp('NO OUTPUT')
		return

	ret = png_comparator.compare_pngs("output.png", str(img_seq)+".png")

	if ret != True:
		print '\tnot match!'
		output_file.log_cmp('NOT MATCH')
		return
	else:
		print '\tmatch!'
		output_file.log_cmp('MATCH')

	return



if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Usage: python a1_autotest.py path_to_userids'
		sys.exit(-1)

	
	#enclosing directory containing all userids
	path_to_userids = sys.argv[1]
	a1_autotest(path_to_userids)

	sys.exit(0)
