FROM library/cassandra

RUN apt-get -y update
RUN	apt-get -y install curl
RUN	apt-get -y install vim 

RUN curl -O --location https://github.com/brianfrankcooper/YCSB/releases/download/0.12.0/ycsb-0.12.0.tar.gz
RUN tar xfvz ycsb-0.12.0.tar.gz
