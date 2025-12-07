🔥 Port Spectre – A High-Performance Python Port Scanner for Ethical Security Testing
Port Spectre is a fast, modern, multi-threaded port scanner built in Python. Inspired by Nmap’s core concepts, Port Spectre provides speed, clarity, and extensibility while remaining simple to use.

🚀 Features
Feature	Description
⚡ Multi-threaded scanning	Accelerate scans using -m / --multithreading
🎛 Speed profiles	Choose from: slow, normal, fast, aggressive
🔍 Banner grabbing	Fetch service banners with -b / --banner
🛡 OS fingerprinting	TTL-based OS detection via --os
🔎 Service detection	Identify services with -s / --services
🎯 Open-only filtering	Show only open ports using --open-only
🗂 Save results	Export scan output to a file with --save output.txt
🎨 Color-coded output	Optional --no-color to disable colors
📦 Flexible port input	Supports comma lists (80,443) and ranges (1-1000)
🧩 Modular design	Easy to extend and customize
📦 Installation
Clone the repository
bash
git clone https://github.com/0xAbbasSec/Port-Spectre.git
cd Port-Spectre
Make the tool globally accessible
bash
# Rename the script if needed
mv ultimate_scanner.py port-spectre

# Give execute permission
chmod +x port-spectre

# Install system-wide
sudo cp port-spectre /usr/local/bin/
Now you can run it from anywhere:

port-spectre --help
🛠 Usage Examples
Command	Description
port-spectre 192.168.1.10 80	Scan a single port
port-spectre 10.0.0.5 21,22,80,443	Scan a comma-separated list
port-spectre scanme.nmap.org 1-1000	Scan a port range
port-spectre scanme.nmap.org 22,80 -b	Enable banner grabbing
port-spectre 192.168.1.10 1-65535 -m	Multi-threaded full-range scan
port-spectre 192.168.1.10 80 --os	OS detection
port-spectre 10.10.10.10 1-500 --profile aggressive	Aggressive speed profile
port-spectre scanme.nmap.org 80,443 --save results.txt	Save results to file

⚙️ Flags Overview
Flag	Description
-b, --banner	Grab service banners
-m, --multithreading	Enable multithreaded scanning
-s, --services	Show service names
--os	Attempt OS detection (TTL-based)
--profile	Scan speed: slow, normal, fast, aggressive
--open-only	Show only open ports
--save FILE	Save results to a file
--no-color	Disable ANSI color output

⚠️ Legal Disclaimer
Port Spectre is intended only for authorized security testing and education. Do not scan systems or networks without explicit permission. The author is not responsible for misuse.

📖 License
This project is licensed under the MIT License — free to modify, share, and use.
