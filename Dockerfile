FROM python:3.8.8
ADD . /swapi
WORKDIR /swapi
RUN pip install pip --upgrade &&  pip install -r requirements.txt
CMD pytest
