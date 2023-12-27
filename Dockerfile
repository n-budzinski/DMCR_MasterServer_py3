FROM ubuntu:jammy
FROM python:3.11

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

ADD DMCREmu .

CMD ["python", "./main.py"]

EXPOSE 34001/tcp
EXPOSE 34000/udp