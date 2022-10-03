FROM python:3.8.8
ADD . /
RUN pip install pip --upgrade &&  pip install -r requirements.txt
CMD pytest
