#!/bin/bash

docker build . --tag safecracker
docker run --rm -it \
  --device /dev/gpiomem \
  --device /dev/i2c-1 \
  -p [::]:80:80/tcp \
  safecracker \
  /bin/bash
