FROM mlspec/mlspeclib-action-docker@sha256:b10b30184f8babf655a6351aa88961ee74a5fb61b1e4263f68543117b5f5a51c

RUN apt-get -y update && apt-get -y install python3-all python3-pip

ARG FIRSTCACHEBUST=1

COPY requirements.txt /requirements.txt

RUN python3 -m pip install -U pip
RUN python3 -m pip install --no-cache-dir -r /requirements.txt

COPY .parameters/schemas /src/parameters
COPY integration/.parameters/schemas /src/parameters/test_schemas
COPY step_execution.py /src
COPY integration/container_debugging.sh /src

ENTRYPOINT ["/src/entrypoint.sh"]
