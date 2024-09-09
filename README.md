# Network Reconnaissance Tool

This Python script performs an asynchronous TCP port scan on a given host, supporting both IPv4 and IPv6 addresses. It allows you to scan a range of TCP ports and determine which ports are open on the target host.

This tool is currently a Work In Progress.

## Features

- Asynchronous scanning using the `asyncio` library for improved performance
- Uses `aiodns` for asynchronous DNS resolution, improving performance over blocking `socket.getaddrinfo()`
- Support for scanning both IPv4 and IPv6 addresses
- Handles scenarios where a hostname resolves to multiple IP addresses, scanning ports on each resolved IP address
- Configurable timeout for each connection attempt
- Command-line interface for easy usage
- Windows compatibility with automatic event loop selection

## Limitations

- The script currently only scans TCP ports. UDP scanning is not implemented.
- No specific DNS (port 53) scanning or enumeration is performed. It only checks if TCP port 53 is open like any other port.
- The script does not provide detailed information about the services running on the open ports. It only indicates whether a port is open or closed.
- The script does not include any stealth or evasion techniques. It performs a basic TCP connect scan, which may be detected and logged by intrusion detection systems (IDS) or firewalls.

## Possible Future Enhancements (examples)

- UDP port scanning capabilities
- DNS Scanning and Enumeration
- Service discovery (banner grabbing)
- Stealthier operation
- Network mapping

## Requirements

- Python 3.7 or higher
- `aiodns` library (can be installed via pip: `pip install aiodns`)

## Usage

To use the Asynchronous Port Scanner, run the `netrecon.py` script from the command line with the following arguments:

```bash
python netrecon.py [-h] [-t TIMEOUT] host start_port end_port
```

- `host`: The hostname or IP address to scan.
- `start_port`: The starting port number.
- `end_port`: The ending port number.
- `-t TIMEOUT`, `--timeout TIMEOUT`: (Optional) The timeout in seconds for each connection attempt. Default is 1.0 seconds.

Example:

```bash
python netrecon.py example.com 1 1000 -t 2.0
```

This will scan ports 1 to 1000 on the host "example.com" with a timeout of 2.0 seconds for each connection attempt.

## Output

The script will display the IP addresses being scanned and the open ports found on each IP address. If an error occurs during the scanning process, an error message will be displayed.

Example output:

```
Scanning 192.168.1.1...
Port 80 is open on 192.168.1.1
Port 443 is open on 192.168.1.1
```

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

Use at your own risk. This script is intended for testing and educational purposes only. Use it responsibly and ensure that you have proper authorization before scanning any hosts or networks. The author of this script is not responsible for any misuse or damage caused by this tool.
