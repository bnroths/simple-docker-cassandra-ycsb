import subprocess, sys
import yaml
# from cassandra_yaml import document
import os
import pickle

skip_lines = ["readproportion", "updateproportion", "scanproportion", "insertproportion"]

# save workload files
with open('ycsb-0.12.0/workloads/workloada', 'r') as workloadFile:
    lines = []
    for line in workloadFile:
        for skip_line in skip_lines:
            if skip_line in line:
                break
        lines.append(line)

workloads = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

for workload in workloads:
    output_workload_filename = 'ycsb-0.12.0/workloads/workload{}'.format(workload)
    with open(output_workload_filename, 'w') as output_workload_file:
        for line in lines:
            output_workload_file.write(line)
        output_workload_file.write('\n')

        output_workload_file.write('readproportion={}'.format(workload))
        output_workload_file.write('updateproportion={}'.format(1.0-workload))
        output_workload_file.write('scanproportion=0')
        output_workload_file.write('insertproportion=0')
        output_workload_file.write('\n')


with open("cassandra.yaml", 'r') as stream:
    print "file opened"
    yaml_file = yaml.load(stream)

print "HI"
# a 50/50
# b 95 read/ 5 write
# c 100 read

res = {}
concurrent_reads = [4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
for read_val in concurrent_reads:
    res[read_val] = {}

    yaml_file['concurrent_reads'] = read_val
    # print yaml_file
    with open('cassandra.yaml', 'w') as outfile:
        print("J")
        yaml.dump(yaml_file, outfile, default_flow_style=False)

    
    "save cassandra file"
    p = subprocess.call("cp -r /scripts/cassandra.yaml /etc/cassandra", shell=True)
    # p.communicate()

    print "restart cassandra"
    command = ['/usr/sbin/service', 'cassandra', 'restart'];
    #shell=FALSE for sudo to work.
    subprocess.call(command, shell=False)

    print "run workloads"
    # workloads = ["c"]
    for workload in workloads:
        res[read_val][workload] = {}
        p = subprocess.call("rm -Rf %s/%s" % (workload, read_val), shell=True)
        p = subprocess.call("mkdir %s/%s" % (workload, read_val), shell=True)
        ## how many runs to do
        for i in range(10):
            print i
            with open("%s/%s/%s-stdout.txt" % (workload, read_val, i),"wb") as out, open("%s/%s/%s-stderr.txt" % (workload, read_val, i),"wb") as err:
                p = subprocess.Popen("./ycsb-0.12.0/bin/ycsb run basic -P ycsb-0.12.0/workloads/workload%s" % workload, 
                    shell=True, 
                    stdout=out,
                    stderr=err)
                p.communicate()

    
        for file in os.listdir("%s/%s/" % (workload, read_val)):

            if file.endswith("out.txt"):
                print "%s/%s/%s" % (workload, read_val, file)

                with open("%s/%s/%s" % (workload, read_val, file), 'r') as f:
                    for line in f.readlines():
                        if "[READ]" in line or "[UPDATE]" in line:

                            l   = line.split(', ')
                            key = l[0] + ' - ' + l[1]
                            val = int(l[2].replace("\n", "").split(".")[0])

                            # if key not in res:
                            #     res[key] = {}

                            if key not in res[read_val][workload]:
                                res[read_val][workload][key] = [val]
                            else:
                                res[read_val][workload][key].append(val)

                            # if read_val in res[key]:
                            #     res[key][read_val].append(val)
                            # else:
                            #     res[key][read_val] = [val]

with open('/output.p', 'wb') as fp:
    pickle.dump(res, fp)
    # print res
    