#!/bin/bash
ffplay -flags low_delay -probesize 32 -i udp://[::]:4444
