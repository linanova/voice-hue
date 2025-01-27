FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-rpi.gpio \
    gcc \
    g++

RUN pip install rpi_ws281x adafruit-circuitpython-neopixel RPi.GPIO

WORKDIR /app

COPY . /app

CMD ["python", "app.py"]