FROM elasticsearch:2.3.5
WORKDIR /usr/share/elasticsearch
VOLUME /usr/share/elasticsearch/logs

ADD elasticsearch-analysis-ik-1.9.5.zip /tmp/

RUN unzip /tmp/elasticsearch-analysis-ik-1.9.5.zip -d /usr/share/elasticsearch/plugins/ik