[Unit]
Description=Octoprint
After=network.target

[Service]
ExecStart=/home/pi/octoprint/bin/octoprint serve
WorkingDirectory=/home/pi/octoprint
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi
CPUSchedulingPolicy=rr
CPUSchedulingPriority=80

[Install]
WantedBy=multi-user.target


Then run



sudo systemctl daemon-reload
sudo systemctl enable octoprint
