FROM python

WORKDIR /app
RUN apt-get update && apt-get install -yq nano
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:${PATH}"
RUN /app/venv/bin/python -m pip install --upgrade pip
RUN /app/venv/bin/pip install \
  RPi.GPIO \
  smbus \
  mpu6050-raspberrypi \
  requests \
  curio \
  trio \
  quart-trio

COPY ./ /app/
