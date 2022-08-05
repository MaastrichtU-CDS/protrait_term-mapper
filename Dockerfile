FROM python:3.10.6-bullseye

COPY requirements.txt requirements.txt
ADD fairifier fairifier
COPY app.py app.py

ADD build build

RUN pip install -r requirements.txt

EXPOSE 5000
CMD [ "python", "app.py" ]