# systemd

```
[Unit]
Description=AAR1-Webserver

[Service]
Type=simple
Restart=always
RestartSec=3
StandardOutput=journal
ExecStart=python3 /home/pi/repos/firmware/src/webapp/app.py

[Install]
WantedBy=default.target
```