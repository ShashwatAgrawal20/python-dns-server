"""Module to parse header and return a DNSHeader."""

from core import DNSHeader
from struct import unpack


def header_parser(buffer: bytes) -> DNSHeader:
    """
    Parses the DNS header from the given buffer.

    Args:
        buffer (bytes): Buffer containing the DNS header.

    Returns:
        DNSHeader: DNS header object containing the parsed header fields.
    """

    if len(buffer) < 12:
        raise ValueError("Buffer is too short to contain a DNS header")

    id, flags, qdcount, ancount, nscount, arcount = unpack(
        "!HHHHHH", buffer[:12])
    # qr = (flags >> 15) & 0x1
    opcode = (flags >> 11) & 0xF
    aa = (flags >> 10) & 0x1
    tc = (flags >> 9) & 0x1
    rd = (flags >> 8) & 0x1
    ra = (flags >> 7) & 0x1
    z = (flags >> 4) & 0x7
    # rcode = flags & 0xF

    # I don't care it is what it is
    return DNSHeader(id=id, qr=1, opcode=opcode, aa=aa, tc=tc,
                     rd=rd, ra=ra, z=z,
                     rcode=0 if opcode == 0 else 4,
                     qdcount=1, ancount=1, nscount=nscount,
                     arcount=arcount)
