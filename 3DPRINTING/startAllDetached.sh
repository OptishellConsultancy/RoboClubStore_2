mjpg_streamer -i "input_uvc.so -rot 180 -f 15 -r 1920x1080 -d /dev/video0 -rot 180" -o "output_http.so -p 15151 -w ./www" &

cd OctoPrint
venv/bin/octoprint serve &