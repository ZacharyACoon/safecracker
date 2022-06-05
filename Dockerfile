FROM python

WORKDIR /app
RUN apt-get update && apt-get install -yq nano
RUN python -m venv /opt/app_venv
ENV PATH="/opt/app_venv/bin/:${PATH}"
RUN /opt/app_venv/bin/python -m pip install --upgrade pip
RUN /opt/app_venv/bin/pip install \
  RPi.GPIO \
  smbus \
  mpu6050-raspberrypi \
  requests \
  curio \
  trio \
  quart-trio

COPY ./ /app/
