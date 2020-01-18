FROM centos:7

ENV PATH $PATH:/usr/local/bin/:/usr/bin
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm && yum update -y && yum install python36u -y
COPY files/* /
RUN mkdir /root/.aws/
COPY files/config /root/.aws/
RUN pip3 install --user -r requirements.txt
CMD [ "python3", "copy_emp_to_s3.py" ]
