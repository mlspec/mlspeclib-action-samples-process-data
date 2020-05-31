FROM mlspec/mlspeclib-action-docker@sha256:85fa6da17625a9c76213d73a4888415ae362d77a5d035cee1fbd1583985d337f

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
COPY utils/utils.py /src/utils

ENTRYPOINT ["/src/entrypoint.sh"]
