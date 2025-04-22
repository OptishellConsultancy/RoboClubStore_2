# https://randomnerdtutorials.com/raspberry-pi-mjpeg-streaming-web-server-picamera2/
#  Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-mjpeg-streaming-web-server-picamera2/

# Mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html
# Run this script, then point a web browser at http:<this-ip-address>:7123
# Note: needs simplejpeg to be installed (pip3 install simplejpeg).


# https://github.com/kneave/ne-calib-utils
# https://github.com/raspberrypi/picamera2/issues/1050

import io
import logging
import socketserver
from http import server
from threading import Condition

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

PAGE = """\
<html>
<head>
<title>picamera2 MJPEG streaming demo</title>
</head>
<body>
<h1>Picamera2 MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame_0 = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output_0.condition:
                        output_0.condition.wait()
                        frame_0 = output_0.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame_0))
                    self.end_headers()
                    self.wfile.write(frame_0)
                    self.wfile.write(b'\r\n')

                    with output_1.condition:
                        output_1.condition.wait()
                        frame_1 = output_1.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame_1))
                    self.end_headers()
                    self.wfile.write(frame_1)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True



port = 7123

picam2_0 = Picamera2(0)
picam2_0.configure(picam2_0.create_video_configuration(main={"size": (640, 480)}))
output_0 = StreamingOutput()
picam2_0.start_recording(JpegEncoder(), FileOutput(output_0))
####

# Currently causes ...issues
# picam2_1 = Picamera2(1)
# picam2_1.configure(picam2_1.create_video_configuration(main={"size": (640, 480)}))
# output_1 = StreamingOutput()
# picam2_1.start_recording(JpegEncoder(), FileOutput(output_1))
####
print("Goto address: localhost {}",port )

try:
    address = ('', port)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
finally:
    picam2_0.stop_recording()