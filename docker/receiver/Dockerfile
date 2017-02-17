FROM armhf/alpine:3.4
MAINTAINER Kyle Bai <kyle.b@inwinstack.com>

ADD ./start.sh /opt/start.sh
ADD ./discover.py /opt/discover.py
ADD ./receiver.py /opt/receiver.py

RUN apk --no-cache add python nmap tzdata && \
    python -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip install --upgrade pip setuptools && \
    pip install requests && \
    pip install paho-mqtt && \
    rm -r /root/.cache && \
    chmod +x /opt/start.sh && \
    cp /usr/share/zoneinfo/Asia/Taipei /etc/localtime && \
    apk del tzdata && \
    rm -rf /var/cache/apk/*

CMD ["/opt/start.sh"]
