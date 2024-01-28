"""A shitty DNS server."""
import socket
import argparse
from core import bind_connection
from core import DNSMessage
from utils import resolver


def main():
    """
    Function to start the DNS server

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="pass resolver ip:port")
    parser.add_argument("--resolver", required=False, default=None)
    args = parser.parse_args()
    print("Starting DNS server...")
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bind_connection(udp_socket, "127.0.0.1", 5353)

    while True:
        try:
            # Dns Packet are only limited to 512 bytes
            buf, source = udp_socket.recvfrom(512)
            # print(f"Received data from {source}")
            if args.resolver:
                header, question, answer = resolver(args, buf)
                response = DNSMessage(
                    header, question, answer).pack_message_to_bytes()
                udp_socket.sendto(response, source)
        except Exception as e:
            print(f"Error receiving data: {e}")
            raise e


if __name__ == "__main__":
    main()
