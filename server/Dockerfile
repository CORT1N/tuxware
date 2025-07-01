FROM python:3.13.5-alpine3.22

WORKDIR /server

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY penguinet.py .

VOLUME /data

CMD ["python", "penguinet.py"]