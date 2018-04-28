FROM python:3.6
WORKDIR /code
ADD . /code
ENV PULLSBURY_SETTINGS /code/settings.py
RUN pip install pipenv
RUN pipenv install
RUN pipenv install --dev
RUN nosetests -v
