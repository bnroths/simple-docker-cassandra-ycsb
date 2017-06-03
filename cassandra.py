import subprocess, sys

# a 50/50
# b 95 read/ 5 write
# c 100 read

workloads = ["c"]
for workload in workloads:
	## how many runs to do
	for i in range(10):
		print i
		with open("%s/512/%s-stdout.txt" % (workload, i),"wb") as out, open("%s/512/%s-stderr.txt" % (workload, i),"wb") as err:
			subprocess.Popen("./ycsb-0.12.0/bin/ycsb run basic -P ycsb-0.12.0/workloads/workload%s" % workload, 
				shell=True, 
				stdout=out,
				stderr=err)