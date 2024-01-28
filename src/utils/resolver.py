"""Module implementing the DNS upstream resolver and parsing the content."""

import socket
from typing import Tuple
from core import DNSHeader, DNSQuestion, DNSAnswer
from .header_parser import header_parser
from .question_parser import question_parser
from .answer_parser import answer_parser


def resolver(args, buffer: bytes) -> Tuple[DNSHeader, DNSQuestion, DNSAnswer]:
    """
    Connect and resolves the query by connecting to the upstream server

    Args:
        command line argument created using argparser
        buffer (bytes): Buffer containing the DNS header.

    Returns:
        DNSMessage
    """
    resolver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip, port = args.resolver.split(":")
    # print(f"ip -> {ip}, port -> {port}")
    resolver_socket.sendto(buffer, (ip, int(port)))
    buf, _ = resolver_socket.recvfrom(512)
    parsed_header = header_parser(buf)
    parsed_question, offset = question_parser(buf)
    parsed_answer = answer_parser(buf, offset)
    return parsed_header, parsed_question, parsed_answer
