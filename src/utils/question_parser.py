"""Module to parse question section and return a DNSHeader."""

from core import DNSQuestion
from struct import unpack


def question_parser(buffer: bytes) -> DNSQuestion | None:
    """
    Parses the DNS header from the given buffer.

    Args:
        buffer (bytes): Buffer containing the DNS header.

    Returns:
        DNSQuestion: DNS question object containing the parsed question fields.
    """
    if not (buffer[12:]):
        raise ValueError("Where's the question?")
    buffer = buffer[12:]
    domain_end = buffer.index(b"\x00")
    domain = buffer[:domain_end + 1]
    qtype, qclass = unpack(
        ">HH", buffer[domain_end + 1: domain_end + 5])
    return DNSQuestion(domain, qtype, qclass)
