FROM centos
RUN yum install -y gcc make
COPY src /opt/mobcal/src
COPY examples /opt/mobcal/examples
WORKDIR /opt/mobcal/src
RUN make
WORKDIR /opt/mobcal/examples
ENTRYPOINT [ "/opt/mobcal/src/mobcal_shm" ]