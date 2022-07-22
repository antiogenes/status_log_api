
FROM python:3.8-alpine

ARG VERSAO=1.0.1

ENV \
    VERSAO=$VERSAO

RUN apk update && apk add --virtual .build-dependencies \
  --no-cache \
  build-base==0.5-r3 \
  linux-headers==5.16.7-r1 \
  pcre-dev==8.45-r2 \
  python3-dev==3.10.4-r0

WORKDIR /status_log_api

COPY ./status_log_api /status_log_api

RUN pip install -r /status_log_api/requirements.txt --no-cache-dir

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

EXPOSE 5000