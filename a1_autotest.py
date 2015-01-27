import os, sys, glob, random
import assign_builder, paster_exec, png_comparator
from result_logger import *
 
def a1_autotest(path_to_userids):	
	pus = glob.glob( path_to_userids+'/*' )
	output_file = result_logger('autotest_all.csv')

	for pu in pus:
		uid = os.path.basename( pu )
		pua1 = pu+'/a1/'
		pua1bin = pua1+'/bin/'

		print 'entering ' + pu
		output_file.set_sublogger( result_logger(pua1+'autotest.csv') )
		output_file.log_uid(uid)

		sys.stdout.write('\tbuilding...')
		sys.stdout.flush()
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

		for i in range(1,4):
			execute_paster( pua1bin+exe_para, exe_para, i, output_file, 30)
			remove_output()

			execute_paster( pua1bin+exe_nbio, exe_nbio, i, output_file, 30)
			remove_output()

	output_file.logger_close()


def remove_output():
	if os.path.exists('output.png'):
		os.remove('output.png')


def execute_paster(pu_exe, exe_name, img_seq, output_file, timeout):
	num_t = random.randrange(4, 20)
	cmd = exe_name+' -i'+str(img_seq)+' -t'+str(num_t)

	print '\texecuting ' + cmd

	ret = paster_exec.executor_driver(pu_exe, img_seq, num_t, timeout)
	if ret == sys.maxint:
		print '\ttimeout'
		output_file.log_exec(cmd, 'EXECUTION_FAILURE', 'TIMEOUT')
		return
	elif ret != 0:
		print '\tfailed ' + str(ret)
		output_file.log_exec(cmd, 'EXECUTION_FAILURE', 'CODE:'+str(ret))
		return
	else:
		sys.stdout.write('\tsuccess')
		sys.stdout.flush()
		output_file.log_exec(cmd, 'EXECUTION_SUCCESS')	

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

	
	path_to_userids = sys.argv[1]
	a1_autotest(path_to_userids)

	sys.exit(0)
