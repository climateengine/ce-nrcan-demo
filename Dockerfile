FROM python:3.8

RUN pip install earthengine-api==0.1.283

COPY main.py .

CMD ["python", "main.py"]