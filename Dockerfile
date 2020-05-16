FROM aronchick/mlspeclib-action-docker@sha256:2488860ae84a90f57469137ea860c1f3d8e5c1bf37d1a153bc36dd6ef69dcda7

RUN apt-get -y update && apt-get -y install python3-all python3-pip

COPY requirements.txt /requirements.txt

ARG FIRSTCACHEBUST=1

RUN python3 -m pip install -U pip
RUN python3 -m pip install --no-cache-dir -r /requirements.txt

COPY .parameters/schemas /src/parameters
COPY integration/.parameters/schemas /src/parameters/test_schemas
COPY step_execution.py /src

ENTRYPOINT ["./entrypoint.sh"]
