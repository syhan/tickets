FROM python:3

ARG INFLUX_URL="host.docker.internal"
ARG INFLUX_PORT="8086"
ARG INFLUX_DATABASE="tickets"

LABEL maintainer="syhannnn@gmail.com"

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV INFLUX_URL=${INFLUX_URL}
ENV INFLUX_PORT=${INFLUX_PORT}
ENV INFLUX_DATABASE=${INFLUX_DATABASE}

CMD ["python", "./tickets.py"]