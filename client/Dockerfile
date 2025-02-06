FROM python:3.9

RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-rpi.gpio \
    flac \
    alsa-utils \
    libatlas-base-dev \
    gfortran \
    build-essential \
    portaudio19-dev \
    libffi-dev \
    gcc \
    g++

WORKDIR /app
COPY . /app

RUN echo "Cython<3" > cython_constraint.txt
RUN PIP_CONSTRAINT=cython_constraint.txt pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm
RUN python -m nltk.downloader wordnet -d /root/nltk_data


CMD ["python", "app.py"]