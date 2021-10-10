FROM python:3.8-slim-buster

WORKDIR /opt/app

COPY requirements.txt /opt/app
RUN pip3 install -r requirements.txt

COPY *.py /opt/app/

CMD ["python", "kafka-to-sendgrid.py"]
