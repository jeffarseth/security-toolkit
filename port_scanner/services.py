# Jeffar - Port Services
# Description - Lookup table for naming ports. Please extend or modify for environment-specific services.
# Created - 2026-07-05
# Last updated - 2026-07-05

# Reference: https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers

SERVICE_PORTS = {
    20: "FTP-Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    67: "DHCP-Server",
    68: "DHCP-Client",
    69: "TFTP",

    80: "HTTP",
    110: "POP3",
    119: "NNTP",
    123: "NTP",

    135: "RPC",
    137: "NetBIOS-Name",
    138: "NetBIOS-Datagram",
    139: "NetBIOS-Session",

    143: "IMAP",
    161: "SNMP",
    389: "LDAP",

    443: "HTTPS",
    445: "SMB",

    465: "SMTPS",
    587: "SMTP-Submission",

    636: "LDAPS",
    993: "IMAPS",
    995: "POP3S",

    1433: "MSSQL",
    1521: "Oracle",
    2049: "NFS",

    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",

    8080: "HTTP-Alt",
    8443: "HTTPS-Alt"
}

def get_service(port):
    return SERVICE_PORTS.get(port, "unknown")