FROM python:3.8-slim-buster

ENV BUILD "prod"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./src .

ENTRYPOINT ["python3"]
CMD ["-u", "main.py"]
