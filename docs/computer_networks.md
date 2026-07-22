# Computer Networks

Computer networking is the practice of connecting computers and devices to share resources and communicate. Networks form the backbone of the internet and modern computing infrastructure.

## OSI Model

The OSI (Open Systems Interconnection) model is a conceptual framework with seven layers that describes how data moves through a network:

1. **Physical Layer**: Deals with raw bit transmission over physical media (cables, wireless signals). Defines voltage levels, data rates, and physical connectors.
2. **Data Link Layer**: Handles framing, error detection (CRC), and MAC addressing. Ethernet and Wi-Fi operate here. Switches work at this layer.
3. **Network Layer**: Manages logical addressing (IP addresses) and routing. Routers operate at this layer. IP (Internet Protocol) is the primary protocol.
4. **Transport Layer**: Provides end-to-end communication. TCP (reliable, connection-oriented) and UDP (unreliable, connectionless) operate here.
5. **Session Layer**: Manages sessions between applications. Handles establishment, maintenance, and termination of connections.
6. **Presentation Layer**: Data translation, encryption, and compression. Converts data between application and network formats.
7. **Application Layer**: Closest to the end user. Protocols include HTTP, FTP, SMTP, DNS, and SSH.

In practice, the TCP/IP model is more commonly used and has four layers: Network Interface, Internet, Transport, and Application.

## TCP vs UDP

**TCP (Transmission Control Protocol)** provides reliable, ordered, error-checked delivery of data. It uses a three-way handshake (SYN, SYN-ACK, ACK) to establish connections. Features include flow control (sliding window), congestion control, and retransmission of lost packets. TCP is used for HTTP, email, file transfer, and any application requiring guaranteed delivery.

**UDP (User Datagram Protocol)** is connectionless and provides no guarantees on delivery, order, or error checking (beyond a basic checksum). It is faster and has lower overhead than TCP. UDP is used for DNS queries, video streaming, online gaming, and VoIP where speed matters more than reliability. Applications using UDP often implement their own reliability mechanisms at the application layer.

## IP Addressing

IPv4 addresses are 32-bit numbers typically written in dotted decimal notation (e.g., 192.168.1.1). The address space is divided into network and host portions using subnet masks. CIDR (Classless Inter-Domain Routing) notation like /24 specifies the number of network bits. Private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) are used for internal networks and are not routable on the public internet. NAT (Network Address Translation) allows multiple devices to share a single public IP.

IPv6 uses 128-bit addresses written in hexadecimal (e.g., 2001:0db8::1), providing a vastly larger address space to address IPv4 exhaustion.

## HTTP and HTTPS

HTTP (Hypertext Transfer Protocol) is the foundation of data communication on the web. It uses a request-response model with methods like GET (retrieve data), POST (submit data), PUT (update data), and DELETE (remove data). HTTP is stateless — each request is independent. Cookies and sessions are used to maintain state.

HTTPS adds TLS/SSL encryption on top of HTTP, providing confidentiality, integrity, and authentication. The TLS handshake establishes an encrypted connection using asymmetric cryptography for key exchange and symmetric cryptography for data transfer. Certificates issued by Certificate Authorities (CAs) verify server identity.

## DNS

The Domain Name System (DNS) translates human-readable domain names (like google.com) into IP addresses. DNS uses a hierarchical structure with root servers, TLD (Top-Level Domain) servers, and authoritative name servers. DNS queries can be recursive (resolver handles the full lookup) or iterative (client queries each server in the hierarchy). DNS caching at multiple levels reduces query latency. Common DNS record types include A (IPv4 address), AAAA (IPv6 address), CNAME (canonical name alias), and MX (mail server).
