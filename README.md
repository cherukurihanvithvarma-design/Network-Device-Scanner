# Network Device Scanner

A Python-based desktop application for discovering and monitoring devices connected to a local Wi-Fi/LAN network. The application scans active hosts, stores device information in a SQLite database, highlights newly detected devices, and provides a simple graphical interface using PyQt5.

## Features

- Scan devices connected to a local network
- Discover IP address, MAC address, and vendor information
- Store discovered devices in SQLite
- Highlight newly connected devices
- Automatic periodic network scanning
- Event logging
- User-friendly PyQt5 GUI

## Technologies Used

- Python
- PyQt5
- SQLite
- python-nmap

## Project Structure

```
Network-Device-Scanner/
│── main.py
│── scanner.py
│── database.py
│── event.py
│── requirements.txt
│── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Design Decision

To improve scan performance, operating system detection was intentionally omitted. The scanner prioritizes rapid host discovery using IP addresses, MAC addresses, and vendor information, making periodic monitoring faster and more responsive.

## Limitations

- Designed for local Wi-Fi/LAN environments.
- Discovery depends on network configuration and device visibility.
- Enterprise networks with firewalls, VLANs, or access controls may restrict host discovery.

## Future Enhancements

- Optional OS detection (optional feature, disabled to prevent unnecessary time taken to scan the device info)
- Port scanning
- Device trust management
- Export reports (CSV/PDF)
- Real-time notifications
- Search and filtering
- Auto-periodic scanning (optional feature, disabled to prevent unnecessary database accumulation)

## Copyright

© 2026 Hanvith Varma. All rights reserved.

This repository is provided for portfolio and evaluation purposes only. Copying, modifying, or redistributing the source code without prior written permission is not permitted.
