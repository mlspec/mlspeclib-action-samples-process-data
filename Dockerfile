FROM mlspec/mlspeclib-action-docker@sha256:3fe3c5de527c43e697f04f140794795671fa2876814317e98aa24dc9a9bd8ba7

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
