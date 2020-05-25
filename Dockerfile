FROM mlspec/mlspeclib-action-docker@sha256:19a77bd0ca945ccd3f63f550a46f94a4330ab19b418252f58c0e509ed6d42680

RUN apt-get -y update && apt-get -y install python3-all python3-pip

COPY requirements.txt /requirements.txt

ARG FIRSTCACHEBUST=1

RUN python3 -m pip install -U pip
RUN python3 -m pip install --no-cache-dir -r /requirements.txt

COPY .parameters/schemas /src/parameters
COPY integration/.parameters/schemas /src/parameters/test_schemas
COPY step_execution.py /src
COPY integration/container_debugging.sh /src

ENTRYPOINT ["./entrypoint.sh"]
