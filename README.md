# 🔍 Network Scanner + Report Generator

A Python-based network reconnaissance tool that scans target IPs for open ports,
identifies running services and versions, and automatically generates a 
professional HTML report — the kind you'd hand to a client after an assessment.

---

## What It Does

- Scans a target IP or range for open ports
- Detects service names and version info on each open port
- Generates a timestamped HTML report with all findings
- Dark-themed, client-ready report output

---

## Real Output

Here's what a scan of localhost looks like:

| Port | Protocol | State | Service | Version |
|------|----------|-------|---------|---------|
| 5000 | TCP | open | rtsp | AirTunes rtspd 775.3.1 |
| 5900 | TCP | open | vnc | Apple remote desktop vnc |
| 7000 | TCP | open | rtsp | AirTunes rtspd 775.3.1 |

Port 5900 running VNC with no auth hardening would be flagged as a 
High severity finding in a real assessment.

---

## Tech Stack

- Python 3
- Nmap (subprocess wrapper)
- Jinja2 (HTML report templating)
- XML parsing (built-in ElementTree)

---

## Setup

**Requirements:**
- Python 3.x
- Nmap installed on your system

**Install dependencies:**
```bash
git clone https://github.com/aakarshandutt011/network-scanner.git
cd network-scanner
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

**Run:**
```bash
sudo python3 scanner.py
```

Enter your target IP and port range when prompted. The report saves 
automatically as `scan_report_TIMESTAMP.html`.

---

## Example Use Cases

- Network reconnaissance during a vulnerability assessment
- Quick security audit of a home or small business network
- Identifying exposed services before an attacker does

---

## Security Notice

Only scan networks and systems you own or have explicit written permission 
to test. Unauthorized scanning is illegal.

---

## Author

**Aakarshan Dutt**  
Security Analyst | Full Stack Developer  
[GitHub](https://github.com/aakarshandutt011) · aakarshandutt@gmail.com