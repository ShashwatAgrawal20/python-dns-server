from dataclasses import dataclass
from struct import pack


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
    dns_header = DNSHeader(ID=12345, QR=0, OPCODE=1, AA=0, TC=0, RD=1, RA=1,
                           Z=0, RCODE=0, QDCOUNT=1, ANCOUNT=2, NSCOUNT=0,
                           ARCOUNT=1)
    packed_header = dns_header.pack_header_to_bytes()
    ```

    See Also:
    - `pack_header_to_bytes`: Method to pack the DNS header into bytes.
    """

    ID: int = 69
    QR: int = 1
    OPCODE: int = 0
    AA: int = 0
    TC: int = 0
    RD: int = 0
    RA: int = 0
    Z: int = 0
    RCODE: int = 0
    QDCOUNT: int = 0
    ANCOUNT: int = 0
    NSCOUNT: int = 0
    ARCOUNT: int = 0

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

        self.FLAGS = (
            (self.QR << 15)
            | (self.OPCODE << 11)
            | (self.AA << 10)
            | (self.TC << 9)
            | (self.RD << 8)
            | (self.RA << 7)
            | (self.Z << 4)
            | self.RCODE
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
            self.ID,
            self.FLAGS,
            self.QDCOUNT,
            self.ANCOUNT,
            self.NSCOUNT,
            self.ARCOUNT,
        )
