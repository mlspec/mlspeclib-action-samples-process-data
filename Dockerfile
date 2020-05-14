FROM aronchick/mlspeclib-action-docker:latest

RUN apt-get -y update && apt-get -y install python3-all python3-pip

COPY requirements.txt /requirements.txt

ARG FIRSTCACHEBUST=1

RUN python3 -m pip install -U pip
RUN python3 -m pip install --no-cache-dir -r /requirements.txt

COPY step_execution.py /src

ENTRYPOINT ["./entrypoint.sh"]
