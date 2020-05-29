FROM mlspec/mlspeclib-action-docker@sha256:44aac5b803968a864766b2aa191bfb8f8a7eab5eb26dda585597dee87210f92a

RUN apt-get -y update && apt-get -y install python3-all python3-pip

ARG FIRSTCACHEBUST=1

COPY requirements.txt /requirements.txt

RUN python3 -m pip install -U pip
RUN python3 -m pip install --no-cache-dir -r /requirements.txt

WORKDIR /src
COPY .parameters/schemas /src/parameters
COPY integration/.parameters/schemas /src/parameters/test_schemas
COPY step_execution.py /src
COPY integration/container_debugging.sh /src

ENTRYPOINT ["/src/entrypoint.sh"]
