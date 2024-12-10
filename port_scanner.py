import socket
from common_ports import ports_and_services

def get_open_ports(target, port_range, verbose=False):
    open_ports = []

    # Validate the target
    try:
        ip_address = socket.gethostbyname(target)
    except socket.gaierror:
        if all(char.isdigit() or char == '.' for char in target):  # Check if target looks like an IP
            return "Error: Invalid IP address"
        else:
            return "Error: Invalid hostname"

    # Scan the specified range of ports
    for port in range(port_range[0], port_range[1] + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Timeout for the connection attempt
            if s.connect_ex((ip_address, port)) == 0:  # Port is open
                open_ports.append(port)

    # Handle verbose output
    if verbose:
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
        except socket.herror:
            hostname = None

        host_info = f"{hostname} ({ip_address})" if hostname else ip_address
        result = f"Open ports for {host_info}\nPORT     SERVICE"

        for port in open_ports:
            service_name = ports_and_services.get(port, "unknown")
            result += f"\n{port:<9}{service_name}"

        return result

    return open_ports
