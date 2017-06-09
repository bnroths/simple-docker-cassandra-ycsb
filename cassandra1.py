import subprocess, sys
import yaml
from cassandra_yaml import document
import os
import time

with open("cassandra.yaml", 'r') as stream:
	print "file opened"
	yaml_file = yaml.load(stream)

print "HI"
# a 50/50
# b 95 read/ 5 write
# c 100 read
# defaults
concurrent_reads  					= [32] 
concurrent_writes 					= [32] 
read_request_timeout_in_ms 			= [5000]
compaction_throughput_mb_per_sec 	= [16]  # 2 - 8
# # 1162.2
res = {}
concurrent_reads  					= [4, 256, 2048] 
concurrent_writes 					= [4, 256, 2048] 
read_request_timeout_in_ms 			= [1000, 5000, 10000]
compaction_throughput_mb_per_sec 	= [0, 4, 8]  # 2 - 8
# 1105.6 4-256-1000-4

concurrent_reads  					= [4, 128, 256] 
concurrent_writes 					= [128, 256, 1024] 
read_request_timeout_in_ms 			= [500, 1000, 2500]
compaction_throughput_mb_per_sec 	= [2, 4, 6]  # 2 - 8
# 919.6 128-256-2500-6

concurrent_reads  					= [64, 128, 192] 
concurrent_writes 					= [192, 256, 512] 
read_request_timeout_in_ms 			= [1500, 2500, 3500]
compaction_throughput_mb_per_sec 	= [4, 6, 8]  # 2 - 8

# 907.0 192-192-1500-8
concurrent_reads  					= [150, 192, 210] 
concurrent_writes 					= [150, 192, 210] 
read_request_timeout_in_ms 			= [1000, 1500, 2000]
compaction_throughput_mb_per_sec 	= [6, 7, 8]  # 2 - 8

# 1036.8 150-192-1000-7
for read_val in concurrent_reads:
	for timeout_val in read_request_timeout_in_ms:
		for compaction_val in compaction_throughput_mb_per_sec:
			for write_val in concurrent_writes:
				ts1 = time.time()
				print read_val, write_val, timeout_val, compaction_val
				yaml_file['concurrent_reads'] 					= read_val
				yaml_file['concurrent_writes'] 					= write_val
				yaml_file['read_request_timeout_in_ms'] 		= timeout_val
				yaml_file['compaction_throughput_mb_per_sec'] 	= compaction_val
				# print yaml_file
				with open('cassandra.yaml', 'w') as outfile:
					yaml.dump(yaml_file, outfile, default_flow_style=False)

				# "save cassandra file"
				p = subprocess.call("cp -r /scripts/cassandra.yaml /etc/cassandra", shell=True)
				# p.communicate()

				# print "restart cassandra"
				command = ['/usr/sbin/service', 'cassandra', 'restart'];
				subprocess.call(command, shell=False)

				# print "run workloads"
				workloads = ["b"]
				for workload in workloads:
					# print timeout_val
					file_name = "%s-%s-%s-%s" % (read_val, write_val, timeout_val, compaction_val)
					print file_name

					p = subprocess.call("rm -Rf %s/%s" % (workload, file_name), shell=True)
					p = subprocess.call("mkdir %s/%s" % (workload, file_name), shell=True)
					## how many runs to do
					for i in range(5):
						# print i
						with open("%s/%s/%s-stdout.txt" % (workload, file_name, i),"wb") as out, open("%s/%s/%s-stderr.txt" % (workload, file_name, i),"wb") as err:
							p = subprocess.Popen("./ycsb-0.12.0/bin/ycsb run basic -P ycsb-0.12.0/workloads/workload%s" % workload, 
								shell=True, 
								stdout=out,
								stderr=err)
							p.communicate()

				
				for file in os.listdir("%s/%s/" % (workload, file_name)):

					if file.endswith("out.txt"):
						# print "%s/%s/%s" % (workload, file_name, file)

						with open("%s/%s/%s" % (workload, file_name, file), 'r') as f:
							for line in f.readlines():
								if "[READ]" in line:

									l 	= line.split(', ')
									key = l[1]
									val = int(l[2].replace("\n", "").split(".")[0])

									if key not in res:
										res[key] = {}

									if file_name in res[key]:
										res[key][file_name].append(val)
									else:
										res[key][file_name] = [val]
				ts2 = time.time()
				print round(ts2 - ts1, 0)

print res
