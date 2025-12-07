#!/usr/bin/env python3
import socket
import sys
import argparse
import threading
import time

# ───────────────────────────────────────────────
# GLOBAL SETTINGS
lock = threading.Lock()  # thread-safe printing

# Default speed profiles
SPEED_PROFILES = {
    "slow":     1.5,
    "normal":   0.7,
    "fast":     0.3,
    "aggressive": 0.05
}

# ───────────────────────────────────────────────
# Colors (can be disabled)
def get_colors(enabled=True):
    if not enabled:
        return "", "", "", ""
    return (
        "\033[32m",           # GREEN
        "\033[38;5;160m",     # SOFT RED
        "\033[33m",           # YELLOW
        "\033[36m"            # CYAN
    )

GREEN, SOFT_RED, YELLOW, CYAN = get_colors(True)
RESET = "\033[0m"

# ───────────────────────────────────────────────
# ASCII Banner
BANNER = CYAN + r"""
   ____       ___    __    __           __          
  / __ \_  __/   |  / /_  / /_  ____ __/ /___  _____
 / / / / |/_/ /| | / __ \/ __ \/ __ `/ __/ _ \/ ___/
/ /_/ />  </ ___ |/ /_/ / /_/ / /_/ (_  )  __/ /__  
\____/_/|_/_/  |_/_.___/_.___/\__,_/  _/\___/\___/  
                                   /_/              
""" + RESET


# ───────────────────────────────────────────────
def usage_error(msg):
    print(f"{SOFT_RED}Error: {msg}{RESET}\n")
    sys.exit(1)

# ───────────────────────────────────────────────
def resolve_host(target):
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        usage_error(f"Could not resolve host '{target}'")

# ───────────────────────────────────────────────
def parse_ports(ports):
    ports = ports.strip()

    if "," in ports:
        parts = ports.split(",")
    elif "-" in ports:
        start, end = ports.split("-")
        start, end = start.strip(), end.strip()

        if not start.isdigit() or not end.isdigit():
            usage_error("Port range must contain only numbers")

        start, end = int(start), int(end)
        if start < 1 or end > 65535 or start > end:
            usage_error("Port range must be between 1–65535 and valid")

        return list(range(start, end + 1))
    else:
        parts = [ports]

    final_ports = []
    for p in parts:
        p = p.strip()
        if not p.isdigit():
            usage_error(f"'{p}' is not a valid port number")
        num = int(p)
        if not (1 <= num <= 65535):
            usage_error("Port numbers must be between 1 and 65535")
        final_ports.append(num)

    return final_ports

# ───────────────────────────────────────────────
# Basic service detection
COMMON_SERVICES = {
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    80: "http",
    110: "pop3",
    143: "imap",
    443: "https",
    3306: "mysql",
    3389: "rdp",
    5900: "vnc",
    8080: "http-proxy",
}

def detect_service(port):
    return COMMON_SERVICES.get(port, "unknown")

# ───────────────────────────────────────────────
def grab_banner(sock, port):
    try:
        if port in (80, 443, 8080, 8000, 8888):
            sock.sendall(b"GET / HTTP/1.0\r\n\r\n")
            response = sock.recv(4096).decode(errors="ignore")
            for line in response.split("\r\n"):
                if line.lower().startswith("server:"):
                    return line.split(":", 1)[1].strip()
            return None

        banner = sock.recv(1024).decode(errors="ignore")
        return banner.strip() if banner else None

    except Exception:
        return None

# ───────────────────────────────────────────────
def detect_os(ttl):
    """Very basic TTL OS fingerprinting."""
    if ttl >= 128:
        return "Windows (likely)"
    elif ttl >= 64:
        return "Linux/Unix (likely)"
    elif ttl >= 255:
        return "Cisco/Networking device"
    return "Unknown OS"

# ───────────────────────────────────────────────
def scan_port(target, port, timeout, grab_banner_flag, show_services, show_open_only, save_buffer):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        result = sock.connect_ex((target, port))

        if result == 0:
            service = detect_service(port) if show_services else ""
            banner = grab_banner(sock, port) if grab_banner_flag else None

            message = f"{GREEN}[+] Port {port}: OPEN{RESET}"
            if service:
                message += f" ({service})"

            with lock:
                print(message)
                if banner:
                    print(f"    {YELLOW}Banner: {banner}{RESET}")

                save_buffer.append(message + ("\n" if not banner else f"\nBanner: {banner}\n"))

        else:
            if not show_open_only:
                message = f"{SOFT_RED}[-] Port {port}: CLOSED{RESET}"
                with lock:
                    print(message)
                save_buffer.append(message + "\n")

    finally:
        sock.close()

# ───────────────────────────────────────────────
def scan_host_multithreaded(target, ports, timeout, grab_banner_flag, show_services, show_open_only, save_buffer):
    threads = []
    max_threads = 200  # safe limit

    for port in ports:
        t = threading.Thread(target=scan_port, args=(
            target, port, timeout,
            grab_banner_flag,
            show_services,
            show_open_only,
            save_buffer
        ))
        threads.append(t)
        t.start()

        while threading.active_count() > max_threads:
            time.sleep(0.01)

    for t in threads:
        t.join()

# ───────────────────────────────────────────────
def scan_os(target):
    """Send a ping to measure TTL."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except PermissionError:
        return "Raw socket privilege required (run as root)"

    sock.settimeout(1)
    packet = b"\x08\x00\xf7\xff\x00\x01\x00\x01"  # ICMP Echo Request
    sock.sendto(packet, (target, 1))

    try:
        data, addr = sock.recvfrom(1024)
        ttl = data[8]
        return detect_os(ttl)
    except:
        return "No TTL response received"

# ───────────────────────────────────────────────
if __name__ == "__main__":
    print(BANNER)

    parser = argparse.ArgumentParser(description="Ultimate Python Port Scanner")
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("ports", help="Ports: 80,443 or 20-30 or 22")
    parser.add_argument("-b", "--banner", action="store_true", help="Grab banners")
    parser.add_argument("-m", "--multithreading", action="store_true", help="Enable multi-threading")
    parser.add_argument("-s", "--services", action="store_true", help="Detect service names")
    parser.add_argument("--os", action="store_true", help="Attempt OS detection via TTL")
    parser.add_argument("--profile", choices=["slow", "normal", "fast", "aggressive"], default="normal")
    parser.add_argument("--open-only", action="store_true", help="Show only open ports")
    parser.add_argument("--save", help="Save output to a file")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    args = parser.parse_args()

    # Disable colors if requested
    if args.no_color:
        GREEN, SOFT_RED, YELLOW, CYAN = get_colors(False)

    target_ip = resolve_host(args.target)
    ports = parse_ports(args.ports)
    timeout = SPEED_PROFILES[args.profile]

    print(f"\n[*] Scanning {target_ip} using '{args.profile}' profile...\n")

    save_buffer = []

    # OS Detection
    if args.os:
        print("[*] Detecting OS...")
        os_guess = scan_os(target_ip)
        print(f"    OS Guess: {YELLOW}{os_guess}{RESET}\n")
        save_buffer.append(f"OS Guess: {os_guess}\n\n")

    # Choose scanning mode
    if args.multithreading:
        scan_host_multithreaded(
            target_ip, ports, timeout,
            args.banner, args.services, args.open_only, save_buffer
        )
    else:
        for port in ports:
            scan_port(
                target_ip, port, timeout,
                args.banner, args.services, args.open_only, save_buffer
            )

    print("\nScan complete.\n")

    if args.save:
        with open(args.save, "w") as f:
            f.writelines(save_buffer)
        print(f"[+] Results saved to {args.save}")
