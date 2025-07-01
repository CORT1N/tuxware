FROM python:3.13.5-alpine3.22

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY tuxware.py .

CMD ["python", "tuxware.py"]