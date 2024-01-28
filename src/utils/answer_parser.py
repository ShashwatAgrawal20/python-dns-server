"""Module to parse answer section and return a DNSAnswer."""

from struct import unpack
from core import DNSAnswer
from common_module import extract_name


def answer_parser(buffer: bytes, start_index) -> DNSAnswer:
    """
    Parses the DNS answer from the given buffer.

    Args:
        buffer (bytes): Buffer containing the DNS answer.
        start_index (int): The starting index for answer.

    Returns:
        DNSAnswer: DNS question object containing the parsed answer fields.
    """
    name, name_end = extract_name(buffer, start_index)
    name_end = start_index + name_end + 1
    data_start = name_end + 10
    atype, aclass, ttl, length = unpack(
        ">HHIH", buffer[name_end:data_start])
    data = buffer[data_start: data_start + length]
    unpacked_answer = DNSAnswer(
        name=name, type_=atype, class_=aclass, ttl=ttl, length=length, data=data
    )
    return unpacked_answer
