FROM python:3.8

RUN pip install earthengine-api

COPY main.py .

CMD ['python', 'main.py']