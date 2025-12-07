# ⚡ Port Spectre

A high-performance Python port scanner for ethical security testing.

Port Spectre is a fast, modern, multi-threaded port scanner built in Python. Inspired by Nmap’s core ideas, Port Spectre provides speed, clarity, and extensibility — all while remaining easy to use.

---

## 🚀 Features

- ⚡ **Multi-threaded scanning** (`-m / --multithreading`)  
- 🎛 **Speed profiles** — `slow`, `normal`, `fast`, `aggressive`  
- 🔍 **Banner grabbing** (`-b / --banner`)  
- 🛡 **OS fingerprinting via TTL analysis** (`--os`)  
- 🔎 **Service detection** (`-s / --services`)  
- 🎯 **Open-only filtering** (`--open-only`)  
- 🗂 **Save scan results to a file** (`--save output.txt`)  
- 🎨 **Color-coded output** (use `--no-color` to disable)  
- 📦 Support for comma-separated lists **and** port ranges (e.g. `80,443` or `1-1000`)  
- 🧩 Modular, easy to extend and maintain

---

## 📦 Installation

### 1. Clone the repository

git clone https://github.com/0xAbbasSec/Port-Spectre.git
cd Port-Spectre

### 2. Make the tool globally accessible

Give execute permissions:
```sh
chmod +x port-spectre
```

Install system-wide (on Linux/macOS):
```sh
sudo cp port-spectre /usr/local/bin/
```

You can now run the tool from anywhere:
```sh
port-spectre --help
```

---

### 🛠 Usage Examples
Scan a single port
```sh
port-spectre 192.168.1.10 80
```

Scan a comma-separated list of ports
```sh
port-spectre 10.0.0.5 21,22,80,443
```
Scan a port range
```sh
port-spectre scanme.nmap.org 1-1000
```
Enable banner grabbing
```sh
port-spectre scanme.nmap.org 22,80 -b
```

Multi-threaded scan (full-range)
```sh
port-spectre 192.168.1.10 1-65535 -m
```
Attempt OS detection
```sh
port-spectre 192.168.1.10 80 --os
```

Use aggressive scanning speed
```sh
port-spectre 10.10.10.10 1-500 --profile aggressive
```
Save the scan results to a file
```sh
port-spectre scanme.nmap.org 80,443 --save results.txt
```

---

### ⚙ Command-Line Flags/ Flag	Description

-b, --banner	  Grab service banners
-m, --multithreading	  Enable multi-threaded scanning
-s, --services	  Show service names next to open ports
--os	  Attempt simple OS detection (via TTL)
--profile <mode>	  Choose scan speed: slow, normal, fast, aggressive
--open-only	  Show only open ports (hide closed ports)
--save <file>	  Save scan results to a text file
--no-color	  Disable colorized output (for plain terminals or logs)

---

### ⚠️ Legal Disclaimer

Port Spectre is intended only for authorized security testing and educational purposes.
Do not use this tool to scan networks or systems without explicit permission.
The author assumes no responsibility for misuse.

---

###📄 License

This project is licensed under the MIT License — feel free to use, modify, and redistribute.
