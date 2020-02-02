FROM python:buster

RUN apt-get update && apt-get install -y portaudio19-dev python-pyaudio python3-pyaudio

COPY . /app

WORKDIR /app/backend

RUN pip install -r /app/backend/requirements.txt

ENV FLASK_ENV "production"
ENV FLASK_APP=app.py
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/credentials.json"

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]

EXPOSE 5000