# python cli.py --ycsb_path /scripts/ycsb-0.12.0 --yaml_path /etc/cassandra/cassandra.yaml --ycsb_workload b
import subprocess, sys
import yaml
from cassandra_yaml import document
import os
import time
import click

paramters = {
	'concurrent_reads': {
		'min': 1,
		'max': 12,
		'scale': 'log',
		'vals_to_test': [],
		'optimal_value': None
	},
	'concurrent_writes': {
		'min': 1,
		'max': 12,
		'scale': 'log',
		'vals_to_test': [],
		'optimal_value': None
	},
	'read_request_timeout_in_ms': {
		'min': 250,
		'max': 5000,
		'scale': 'linear',
		'vals_to_test': [],
		'optimal_value': None
	},
	'compaction_throughput_mb_per_sec': {
		'min': 16,
		'max': 32,
		'scale': 'linear',
		'vals_to_test': [],
		'optimal_value': None
	},
	'concurrent_counter_writes': {
		'min': 1,
		'max': 12,
		'scale': 'log',
		'vals_to_test': [],
		'optimal_value': None
	},
}

@click.command()
@click.option('--ycsb_path', prompt='Enter the path to ycsb', help='Enter the path to ycsb, enter absolute path')
@click.option('--yaml_path', prompt='Enter the path to your cassandra.yaml file', help='Enter the path to your cassandra.yaml file, enter absolute path')
@click.option('--ycsb_workload', prompt='Enter the ycsb workload', help='a (50r/50w), b (95r/5w), c (100r/0w)')

def hello(ycsb_path, yaml_path, ycsb_workload):
	"""Simple program optimizes your cassandra.yaml configuration."""
	"/scripts//etc/cassandra/bin/ycsb"
	print ycsb_path, yaml_path, ycsb_workload
	with open(yaml_path, 'r') as stream:
		yaml_file = yaml.load(stream)

	for param in paramters:
		print param, paramters[param]['min'], paramters[param]['max'], paramters[param]['scale']
		diff = int(paramters[param]['max'] - paramters[param]['min'])/3
		print 'small', paramters[param]['min'] + diff, 'large', paramters[param]['min'] + 2*diff
		if paramters[param]['scale'] == 'log':
			min_param = 2 ** int(paramters[param]['min'] + diff)
			max_param = 2 ** int(paramters[param]['min'] + 2*diff)
		else:
			min_param = int(paramters[param]['min'] + diff)
			max_param = int(paramters[param]['min'] + 2*diff)
		
		paramters[param]['vals_to_test'] = [min_param, max_param]

	# params = []
	# param_names = []
	# p = subprocess.call("rm -Rf param_test", shell=True)
	# p = subprocess.call("mkdir param_test", shell=True)
	# for a_val in paramters['concurrent_reads']['vals_to_test']:
	# 	for b_val in paramters['concurrent_writes']['vals_to_test']:
	# 		for c_val in paramters['read_request_timeout_in_ms']['vals_to_test']:
	# 			for d_val in paramters['compaction_throughput_mb_per_sec']['vals_to_test']:
	# 				for e_val in paramters['concurrent_counter_writes']['vals_to_test']:
	# 					yaml_file['concurrent_reads'] 					= a_val
	# 					yaml_file['concurrent_writes'] 					= b_val
	# 					yaml_file['read_request_timeout_in_ms'] 		= c_val
	# 					yaml_file['compaction_throughput_mb_per_sec'] 	= d_val
	# 					yaml_file['concurrent_counter_writes'] 			= e_val
						
	# 					## save params
	# 					with open(yaml_path, 'w') as outfile:
	# 						yaml.dump(yaml_file, outfile, default_flow_style=False)
						
	# 					## restart cassandra
	# 					command = ['/usr/sbin/service', 'cassandra', 'restart'];
	# 					subprocess.call(command, shell=False)

	# 					file_name = "%s-%s-%s-%s-%s" % (a_val, b_val, c_val, d_val, e_val)

						
	# 					## how many runs to do
	# 					p = subprocess.call("mkdir param_test/%s" % file_name, shell=True)
	# 					for i in range(2):
	# 						print i, file_name, "param_test/%s/%s-stdout.txt" % (file_name, i)
	# 						with open("param_test/%s/%s-stdout.txt" % (file_name, i), "wb") as out, open("param_test/%s/%s-stderr.txt" % (file_name, i), "wb") as err:
	# 							p = subprocess.Popen("./ycsb-0.12.0/bin/ycsb run basic -P ycsb-0.12.0/workloads/workload%s" % ycsb_workload, 
	# 								shell=True, 
	# 								stdout=out,
	# 								stderr=err)
	# 							p.communicate()

	res = {}
	for folder in os.listdir("param_test/"):
		for file in os.listdir("param_test/%s" % folder):
			if file.endswith("out.txt"):
				with open("param_test/%s/%s" % (folder, file), 'r') as f:
					for line in f.readlines():
						# print line
						if "[READ]" in line:
							l 	= line.split(', ')
							key = l[1]
							val = int(l[2].replace("\n", "").split(".")[0])
							if key not in res:
								res[key] = {}
							if folder in res[key]:
								res[key][folder].append(val)
							else:
								res[key][folder] = [val]

	print res
	min_val = 999999
	for read_val in res['AverageLatency(us)']:
		# print read_val
		avg = sum(res['AverageLatency(us)'][read_val])/len(res['AverageLatency(us)'][read_val])
		# print read_val, avg
		if avg <= min_val:
			param = read_val
			min_val = avg
	print min_val, param	
	# p = subprocess.Popen("%s/bin/ycsb run basic -P %s/workloads/workload%s" % (ycsb_path, ycsb_path, ycsb_workload), 
	# 	shell=True)
	# p.communicate()

if __name__ == '__main__':
    hello()