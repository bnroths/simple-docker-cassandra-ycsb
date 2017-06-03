# simple-docker-cassandra-ycsb
```
### build docker image
$ cd /cloned/directory
$ docker build .

### get image id
$ docker images

### run docker image (replace directory with where cassandra.py is)
$ docker run -v /Users/benjamin/Desktop/cassandra:/scripts -d 0f126bf8ef3e

### get name
$ docker ps -a

###  run bash
docker exec -it [name] bash

### run test workload
cd ycsb-0.12.0
./bin/ycsb load basic -P workloads/workloada 

###  run CQL
docker run -v /Users/benjamin/Desktop/cassandra:/scripts -it --link some-cassandra:cassandra --rm cassandra sh -c 'exec cqlsh "$CASSANDRA_PORT_9042_TCP_ADDR"'

###  edit cassandra.yaml

$ cd /etc/cassandra
$ vi +436 /etc/cassandra/cassandra.yaml

###  restart cassandra
docker restart some-cassandra

###  truncate table (CQL)
> TRUNCATE usertable;
