FROM mlspec/mlspeclib-action-docker@sha256:e9d9bdee16c2d02c53dd2678f17dad5c919a98a6384bd96b4deafb730a2700c4

RUN apt-get -y update && apt-get -y install python3-all python3-pip

COPY requirements.txt /requirements.txt

ARG FIRSTCACHEBUST=1

RUN python3 -m pip install -U pip
RUN python3 -m pip install --no-cache-dir -r /requirements.txt

COPY .parameters/schemas /src/parameters
COPY integration/.parameters/schemas /src/parameters/test_schemas
COPY step_execution.py /src

ENTRYPOINT ["./entrypoint.sh"]
