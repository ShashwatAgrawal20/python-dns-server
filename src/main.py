"""A shitty DNS server."""
import socket
from core import bind_connection
from core import DNSHeader, DNSQuestion, DNSMessage, DNSAnswer


def main():
    """
    Function to start the DNS server

    Returns:
        None
    """
    print("Starting DNS server...")
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bind_connection(udp_socket, "127.0.0.1", 5353)

    while True:
        try:
            # Dns Packet are only limited to 512 bytes
            buf, source = udp_socket.recvfrom(512)
            # print(f"Received data from {source}")
            header = DNSHeader(id=69, qdcount=1, ancount=1)
            question = DNSQuestion(qname="google.com")
            answer = DNSAnswer(name="google.com", data=b"\x08\x08\x08\x08")
            response = DNSMessage(
                header, question, answer).pack_message_to_bytes()

            udp_socket.sendto(response, source)
        except Exception as e:
            print(f"Error receiving data: {e}")
            raise e


if __name__ == "__main__":
    main()
