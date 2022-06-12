#!/bin/bash
# stream usb camera via udp packets to ip given as an argument.
set -x

ffmpeg \
  -f lavfi -i anullsrc \
  -f v4l2 -framerate 11 -video_size 640x480 \
  -i /dev/video0 \
  -c:v libx264 -preset ultrafast -crf 32 -r 30 -g 30 -keyint_min 30 \
  -c:a aac \
  -f flv -vf "format=yuv420p" \
  rtmp://a.rtmp.youtube.com/live2/${1}
