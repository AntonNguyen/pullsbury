FROM python:2.7
WORKDIR /code
ADD . /code
ENV PULLSBURY_SETTINGS /code/settings.py
RUN pip install pipenv && pipenv install --two
RUN nosetests -v
