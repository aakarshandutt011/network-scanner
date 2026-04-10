import subprocess
import json
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

NMAP_BIN = '/Applications/nmap.app/Contents/Resources/bin/nmap'

def scan_target(target, ports="1-1024"):
    print(f"\n[*] Starting scan on: {target}")
    print(f"[*] Scanning ports: {ports}")
    print("[*] This may take a minute...\n")

    cmd = [NMAP_BIN, "-sV", "--open", "-p", ports, "-oX", "-", target]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"[-] Nmap error: {result.stderr}")
        return None

    results = {
        "target": target,
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hosts": []
    }

    root = ET.fromstring(result.stdout)

    for host in root.findall("host"):
        state = host.find("status").get("state")
        if state != "up":
            continue

        ip = ""
        hostname = ""

        for addr in host.findall("address"):
            if addr.get("addrtype") == "ipv4":
                ip = addr.get("addr")

        hostnames = host.find("hostnames")
        if hostnames is not None:
            hn = hostnames.find("hostname")
            if hn is not None:
                hostname = hn.get("name", "")

        host_data = {
            "ip": ip,
            "hostname": hostname,
            "state": state,
            "protocols": []
        }

        ports_elem = host.find("ports")
        if ports_elem is not None:
            proto_dict = {}

            for port in ports_elem.findall("port"):
                proto = port.get("protocol")
                portid = int(port.get("portid"))
                state_elem = port.find("state")
                port_state = state_elem.get("state") if state_elem is not None else ""

                service_elem = port.find("service")
                service = ""
                product = ""
                version = ""
                if service_elem is not None:
                    service = service_elem.get("name", "")
                    product = service_elem.get("product", "")
                    version = service_elem.get("version", "")

                if proto not in proto_dict:
                    proto_dict[proto] = []

                proto_dict[proto].append({
                    "port": portid,
                    "state": port_state,
                    "service": service,
                    "product": product,
                    "version": version
                })

            for proto_name, proto_ports in proto_dict.items():
                host_data["protocols"].append({
                    "name": proto_name,
                    "ports": proto_ports
                })

        results["hosts"].append(host_data)

    print(f"[+] Scan complete. Found {len(results['hosts'])} host(s).")
    return results


def generate_report(results):
    template_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("report_template.html")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"scan_report_{timestamp}.html"

    html_output = template.render(results=results)

    with open(report_filename, "w") as f:
        f.write(html_output)

    print(f"[+] Report saved as: {report_filename}")
    return report_filename


def main():
    print("=" * 50)
    print("   Network Scanner + Report Generator")
    print("   Built by Aakarshan Dutt")
    print("=" * 50)

    target = input("\nEnter target IP or range (e.g. 192.168.1.1): ").strip()
    custom_ports = input("Enter ports to scan (press Enter for default 1-1024): ").strip()

    if not custom_ports:
        custom_ports = "1-1024"

    if not target:
        print("[-] No target provided. Exiting.")
        return

    results = scan_target(target, custom_ports)

    if not results or not results["hosts"]:
        print("[-] No hosts found. Check your target and try again.")
        return

    report_file = generate_report(results)
    print(f"\n[+] Done! Open {report_file} in your browser to view the report.")

if __name__ == "__main__":
    main()