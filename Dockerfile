FROM python:2.7
WORKDIR /code
ADD . /code
ENV PULLSBURY_SETTINGS /code/settings.sample.py
RUN pip install -r requirements.txt && pip install .
RUN nosetests -v
