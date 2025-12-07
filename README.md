⚡ Port Spectre
A High-Performance Python Port Scanner for Ethical Security Testing






Port Spectre is a fast, modern, multi-threaded port scanner built in Python.
Inspired by Nmap’s core concepts, Port Spectre provides speed, clarity, and extensibility while remaining simple to use.

🚀 Features

⚡ Multi-threaded scanning (-m / --multithreading)

🎛 Speed profiles — slow, normal, fast, aggressive

🔍 Banner grabbing (-b / --banner)

🛡 OS fingerprinting via TTL analysis (--os)

🔎 Service detection (-s / --services)

🎯 Open-only filtering (--open-only)

🗂 Save scan results to a file (--save output.txt)

🎨 Color-coded output (with --no-color)

📦 Supports comma lists & ranges (e.g., 80,443 or 1-1000)

🧩 Extremely modular and easy to extend

📦 Installation
Clone the repository
git clone https://github.com/0xAbbasSec/Port-Spectre.git
cd Port-Spectre

Make the tool globally accessible

Rename the script if needed:

mv ultimate_scanner.py port-spectre


Give execute permission:

chmod +x port-spectre


Install system-wide:

sudo cp port-spectre /usr/local/bin/


Now you can run it from anywhere:

port-spectre --help

🛠 Usage Examples
Scan a single port
port-spectre 192.168.1.10 80

Scan a comma-separated list
port-spectre 10.0.0.5 21,22,80,443

Scan a port range
port-spectre scanme.nmap.org 1-1000

Enable banner grabbing
port-spectre scanme.nmap.org 22,80 -b

Multi-threaded full-range scan
port-spectre 192.168.1.10 1-65535 -m

OS detection
port-spectre 192.168.1.10 80 --os

Aggressive profile
port-spectre 10.10.10.10 1-500 --profile aggressive

Save results
port-spectre scanme.nmap.org 80,443 --save results.txt

⚙ Flags Overview
Flag	Description
-b, --banner	Grab service banners
-m, --multithreading	Enable multithreaded scanning
-s, --services	Show service names
--os	Attempt OS detection (TTL-based)
--profile	Scan speed (slow, normal, fast, aggressive)
--open-only	Show only open ports
--save FILE	Save results
--no-color	Disable ANSI color output
⚠ Legal Disclaimer

Port Spectre is intended only for authorized security testing and education.
Do not scan systems or networks without explicit permission.
The author is not responsible for misuse.

📖 License

This project is licensed under the MIT License — free to modify, share, and use.
