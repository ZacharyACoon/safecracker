#!/bin/bash
# stream usb camera via udp packets to ip given as an argument.

ffmpeg \
  -f v4l2 -framerate 11 -video_size 640x480 \
  -i /dev/video0 \
  -c:v libx264 -preset ultrafast -tune zerolatency -crf 32 -g 30 -keyint_min 30 -f mpegts \
  udp://${1}:4444?pkt_size=1316
