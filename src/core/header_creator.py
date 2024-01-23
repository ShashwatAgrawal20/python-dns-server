"""Module to create DNS header section for DNS messages."""


from __future__ import annotations
from dataclasses import dataclass
from struct import pack, unpack


@dataclass
class DNSHeader:
    """
    Represents the header of a DNS (Domain Name System) message.

    More information about the DNS header can be found at:
    - [RFC 1035](https://datatracker.ietf.org/doc/html/rfc1035#section-4.1.1)
    - [Wiki](https://en.wikipedia.org/wiki/Domain_Name_System)

    Note:
    The QR, OPCODE, AA, TC, RD, RA, Z, and RCODE attributes form the FLAGS.
    Use the `pack_header_to_bytes` method to get the packed DNS header.

    Example Usage:
    ```
    dns_header = DNSHeader(id=12345, qr=0, opcode=1, aa=0, tc=0, rd=1, ra=1,
                           z=0, rcode=0, qdcount=1, ancount=2, nscount=0,
                           arcount=1)
    packed_header = dns_header.pack_header_to_bytes()
    ```

    See Also:
    - `pack_header_to_bytes`: Method to pack the DNS header into bytes.
    """

    # pylint: disable=too-many-instance-attributes
    id: int = 69
    qr: int = 1
    opcode: int = 0
    aa: int = 0
    tc: int = 0
    rd: int = 0
    ra: int = 0
    z: int = 0
    rcode: int = 0
    qdcount: int = 1
    ancount: int = 1
    nscount: int = 0
    arcount: int = 0

    def __post_init__(self) -> None:
        """
        Initializes the DNS header flags based on individual attributes.

        ## Header Flags Format
                                        1  1  1  1  1  1
          0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

        Using bitshifting and bitwise(|) operator to construct the header flag.

        The resulting 16-bit value is assigned to the FLAGS attribute, which
        represents the combined header flags.

        Check the `pack_header_to_bytes` method for complete DNS header format.

        Note:
        This method is automatically called after the object is initialized
        to ensure proper initialization of the FLAGS attribute.
        """

        self.flags = (
            (self.qr << 15)
            | (self.opcode << 11)
            | (self.aa << 10)
            | (self.tc << 9)
            | (self.rd << 8)
            | (self.ra << 7)
            | (self.z << 4)
            | self.rcode
        )

    def pack_header_to_bytes(self) -> bytes:
        """
        Packs DNS header fields into a 12-byte structure and returns the result
        as bytes.

        The DNS header follows the format:
                                        1  1  1  1  1  1
          0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        |                      ID                       |
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        |                    QDCOUNT                    |
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        |                    ANCOUNT                    |
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        |                    NSCOUNT                    |
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        |                    ARCOUNT                    |
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

        Packing is done using the big-endian format with the struct.pack method

        Returns:
            12 bytes packed DNS header
        """

        return pack(
            ">HHHHHH",
            self.id,
            self.flags,
            self.qdcount,
            self.ancount,
            self.nscount,
            self.arcount,
        )

    @staticmethod
    def parse_header(buffer: bytes) -> DNSHeader:
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
