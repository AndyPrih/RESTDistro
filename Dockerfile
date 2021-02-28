FROM python:3-slim

ENV PORT 80
ENV MOUNT_POINT /var/log

COPY requirements.txt /usr/local/bin/

RUN pip3 install --upgrade pip \
	&& pip3 install --no-cache-dir -r /usr/local/bin/requirements.txt \
	&& mkdir -p /var/app

WORKDIR /var/app
COPY app/ /var/app/

ENTRYPOINT python3 ./app.py

EXPOSE 80