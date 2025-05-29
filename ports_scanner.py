import socket

target_input = input("Enter the IP address or domain: ")

try:
    target = socket.gethostbyname(target_input)
except socket.gaierror:
    print(f"Error: Unable to resolve hostname {target_input}")
    exit()

print(f"\nScanning {target_input} ({target}) for open ports...\n")

for port in range(1, 1025):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    result = s.connect_ex((target, port))
    if result == 0:
        # Port is open, try to get service name
        try:
            service = socket.getservbyport(port)
        except OSError:
            service = "Unknown service"

        # Try banner grabbing for version info
        banner = ""
        try:
            s.sendall(b'HEAD / HTTP/1.0\r\n\r\n')  # HTTP request example for HTTP ports
            banner = s.recv(1024).decode().strip()
        except:
            try:
                s.sendall(b'\r\n')
                banner = s.recv(1024).decode().strip()
            except:
                banner = ""

        if banner:
            banner_summary = banner.split('\n')[0]  # First line of banner
        else:
            banner_summary = "No banner"

        print(f"[+] Port {port} is OPEN - Service: {service} - Banner: {banner_summary}")
    s.close()

