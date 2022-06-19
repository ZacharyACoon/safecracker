#!/bin/bash

docker build . --tag safecracker
docker run --rm -it \
  --device /dev/gpiomem \
  --device /dev/i2c-1 \
  -p [::]:80:80/tcp \
  -v "$(pwd)/:/app/" \
  safecracker \
  /bin/bash
