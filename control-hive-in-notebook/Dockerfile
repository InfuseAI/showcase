FROM jupyter/all-spark-notebook:java-11.0.13

WORKDIR /
USER root
RUN sudo mkdir /hive_bin/ && sudo chmod -R 777 /hive_bin/
USER jovyan

WORKDIR /hive_bin/
RUN wget https://apache.uib.no/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz \
    && tar -xzvf hadoop-3.3.1.tar.gz

RUN wget https://apache.uib.no/hive/hive-3.1.2/apache-hive-3.1.2-bin.tar.gz \
    && tar -xzvf apache-hive-3.1.2-bin.tar.gz

ENV HADOOP_HOME="/hive_bin/hadoop-3.3.1"
ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"

WORKDIR /home/jovyan/