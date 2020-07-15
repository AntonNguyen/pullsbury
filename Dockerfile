FROM python:3.8-alpine

RUN apk update && apk add build-base libffi-dev && mkdir -p /code

WORKDIR /code
ADD . /code

ARG ARTIFACTORY_CREDENTIALS_USR
ARG ARTIFACTORY_CREDENTIALS_PSW
RUN ARTIFACTORY_CREDENTIALS_USR=${ARTIFACTORY_CREDENTIALS_USR} ARTIFACTORY_CREDENTIALS_PSW=${ARTIFACTORY_CREDENTIALS_PSW} make install

ENV PULLSBURY_SETTINGS /code/test_settings.py

ENTRYPOINT ["ash", "-c"]
CMD ["pipenv run gunicorn -c ${PULLSBURY_SETTINGS} pullsbury.web:app --log-file=-"]
