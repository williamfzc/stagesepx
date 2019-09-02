FROM python:3

USER root

RUN apt-get update \
    && apt-get install -y libglib2.0 libsm6 libxrender1 libxext-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root

COPY . .

RUN pip install --no-cache-dir .

WORKDIR /usr/src/app

CMD ["bash"]
