import os, sys, glob, random
import assign_builder, paster_exec, png_comparator
 
def a1_autotest(path_to_userids):	
	output_file = open('output.csv', 'w');
	pus = glob.glob( path_to_userids+'/*' )

	for pu in pus:
		uid = os.path.basename( pu )
		print 'entering ' + pu
		output_file.write(uid)

		sys.stdout.write('\tbuilding...')
		sys.stdout.flush()
		ret = assign_builder.build_assign(pu+"/a1/")
		if ret != 0:
			print '\tfailed'
			output_file.write(','.join(['','MAKE_ERROR'])+'\n')
			continue
		else:
			print '\tsuccess'
			output_file.write(','.join(['','MAKE_SUCCESS'])+'\n')


		for i in range(1,4):
			execute_paster( pu, 'paster_parallel', i, output_file, 60)
			remove_output()

			execute_paster( pu, 'paster_nbio', i, output_file, 60)
			remove_output()

	output_file.close()


def remove_output():
	if os.path.exists('output.png'):
		os.remove('output.png')


def execute_paster(pu, exe_name, img_seq, output_file, timeout):
	num_t = random.randrange(4, 20)
	cmd = exe_name+' -i'+str(img_seq)+' -t'+str(num_t)

	print '\texecuting ' + cmd
	output_file.write(',' + cmd )

	ret = paster_exec.autotest_driver(pu+'/a1/bin/'+exe_name, img_seq, num_t, timeout)
	if ret != 0:
		print '\tfailed ' + str(ret)
		output_file.write(','+'EXECUTION_ERROR '+str(ret)+'\n')
		return

	else:
		sys.stdout.write('\tsuccess')
		sys.stdout.flush()
		output_file.write(','+'EXECUTION_SUCCESS')
	
	ret = png_comparator.compare_pngs("output.png", str(img_seq)+".png")
	if ret != True:
		print '\tnot match!'
		output_file.write(','+'NOT MATCH\n')
		return
	else:
		print '\tmatch!'
		output_file.write(','+'MATCH\n')
	return



if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Usage: python a1_autotest.py path_to_userids'
		sys.exit(-1)

	
	path_to_userids = sys.argv[1]
	a1_autotest(path_to_userids)

	sys.exit(0)
