FROM ubuntu:latest

RUN set -xe \
    && apt-get update \
    && apt-get install python3-pip --yes
RUN pip3 install --upgrade pip

RUN mkdir -p online_inference
COPY online_inference/requirements.txt online_inference/requirements.txt

RUN pip install -r online_inference/requirements.txt

COPY ml_project ml_project
COPY online_inference online_inference

CMD ["uvicorn", "online_inference.homework_app:app", "--host", "0.0.0.0", "--port", "80"]
