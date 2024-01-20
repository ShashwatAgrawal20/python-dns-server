import socket
from core import bind_connection, DNSHeader


def main():
    print("Starting DNS server...")
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bind_connection(udp_socket, "127.0.0.1", 5353)

    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
            # print(f"Received data from {source}")
            response = DNSHeader(
                6969, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)\
                .pack_header_to_bytes()

            udp_socket.sendto(response, source)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break


if __name__ == "__main__":
    main()
