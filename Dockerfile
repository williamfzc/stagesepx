FROM python:3.7-slim

USER root

RUN apt-get update \
    # opencv
    && apt-get install -y libglib2.0 libsm6 libxrender1 libxext-dev \
    # ffmpeg
    && apt-get install -y ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root

COPY . .

RUN pip install --no-cache-dir .

WORKDIR /usr/src/app

CMD ["bash"]
