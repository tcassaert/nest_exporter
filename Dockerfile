FROM centos:centos7

RUN yum install -y centos-release-scl && \
yum install -y rh-python35 rh-python35-python-simplejson rh-python35-python-requests && \
yum clean all

RUN /usr/bin/scl enable rh-python35 'pip install prometheus_client'

COPY nest_exporter.py /opt/
COPY docker-entrypoint.sh /usr/bin

EXPOSE 9601

ENTRYPOINT ["/usr/bin/scl", "enable", "rh-python35"]
CMD ["/usr/bin/docker-entrypoint.sh"]
