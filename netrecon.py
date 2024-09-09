#!/usr/bin/env python3
"""
Asynchronous Network Reconnaissance Tool

This script performs asynchronous TCP port scanning on a given hostname,
supporting both IPv4 and IPv6 addresses.
"""

import argparse
import asyncio
import socket
import sys
from typing import List, Tuple

import aiodns

# Windows-specific event loop policy
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def resolve_hostname(hostname: str) -> List[str]:
    """
    Resolve a hostname to both IPv4 and IPv6 addresses.

    Args:
        hostname (str): The hostname to resolve.

    Returns:
        List[str]: A list of IP addresses (both IPv4 and IPv6).
    """
    resolver = aiodns.DNSResolver()
    ip_addresses = []

    for family in (socket.AF_INET, socket.AF_INET6):
        try:
            result = await resolver.gethostbyname(hostname, family)
            ip_addresses.extend(result.addresses)
        except aiodns.error.DNSError:
            continue  # No addresses found for this family

    return ip_addresses


async def is_port_open(host: str, port: int, timeout: float = 1.0) -> Tuple[str, int, bool]:
    """
    Check if a port is open on a given host.

    Args:
        host (str): The IP address (IPv4 or IPv6) to scan.
        port (int): The port number to check.
        timeout (float, optional): The timeout in seconds. Defaults to 1.0.

    Returns:
        Tuple[str, int, bool]: A tuple containing the IP address, port number,
                               and a boolean indicating if it's open.
    """
    try:
        conn = asyncio.open_connection(host, port)
        await asyncio.wait_for(conn, timeout=timeout)
        return host, port, True
    except (asyncio.TimeoutError, OSError):
        return host, port, False


async def scan_ports(hostname: str, ports: range, timeout: float = 1.0) -> None:
    """
    Scan a range of ports on a given hostname for both IPv4 and IPv6 addresses.

    Args:
        hostname (str): The hostname to scan.
        ports (range): A range of port numbers to check.
        timeout (float, optional): The timeout in seconds for each port check.
                                   Defaults to 1.0.
    """
    try:
        print(f"Resolving hostname: {hostname}")
        ip_addresses = await resolve_hostname(hostname)
        if not ip_addresses:
            print(f"Could not resolve hostname: {hostname}")
            return

        unique_ips = set(ip_addresses)
        print(f"Scanning {len(unique_ips)} unique IP address(es)")

        tasks = []
        for ip_address in unique_ips:
            print(f"Scanning {ip_address}...")
            tasks.extend(
                asyncio.create_task(is_port_open(ip_address, port, timeout))
                for port in ports
            )

        results = await asyncio.gather(*tasks)
        for host, port, is_open in results:
            if is_open:
                print(f"Port {port} is open on {host}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def main(hostname: str, start_port: int, end_port: int, timeout: float) -> None:
    """
    The main function to run the port scanner.

    This function sets up and executes the asynchronous port scanning process.

    Args:
        hostname (str): The hostname to scan.
        start_port (int): The starting port number of the range to scan.
        end_port (int): The ending port number of the range to scan (inclusive).
        timeout (float): The timeout in seconds for each port check.
    """
    try:
        ports = range(start_port, end_port + 1)
        asyncio.run(scan_ports(hostname, ports, timeout))
    except KeyboardInterrupt:
        print("Port scanning interrupted by the user.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Asynchronous Port Scanner (IPv4 and IPv6)")
    parser.add_argument("hostname", help="The hostname to scan")
    parser.add_argument("start_port", type=int, help="The starting port number")
    parser.add_argument("end_port", type=int, help="The ending port number")
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=1.0,
        help="The timeout in seconds for each port check (default: 1.0)",
    )
    args = parser.parse_args()
    main(args.hostname, args.start_port, args.end_port, args.timeout)
    