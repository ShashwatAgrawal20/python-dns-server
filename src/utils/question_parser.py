"""Module to parse question section and return a DNSQuestion."""

from struct import unpack
from typing import Tuple
from core import DNSQuestion
from common_module import extract_name


def question_parser(buffer: bytes) -> Tuple[DNSQuestion, int]:
    """
    Parses the DNS question from the given buffer.

    Args:
        buffer (bytes): Buffer containing the DNS header.

    Returns:
        DNSQuestion: DNS question object containing the parsed question fields.
    """
    if not buffer[12:]:
        raise ValueError("Where's the question?")
    offset = 12
    name, name_end = extract_name(buffer, offset)
    # print(name)
    qtype, qclass = unpack(
        ">HH", buffer[offset + name_end +
                      1: offset + name_end + 5]
    )
    offset += name_end + 5
    question = DNSQuestion(qname=name, qtype=qtype, qclass=qclass)
    return (question, offset)
