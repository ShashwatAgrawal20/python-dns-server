from dataclasses import dataclass
from struct import pack


@dataclass
class DNSHeader:
    """
    Parameters:
    - ID : ID to be set in the DNS header.
    - OR : A flag to indicate if the message is a query or a response.
    - OPCODE : A four bit field that specifies kind of query in this message.
    - AA : Authoritative Answer.
    - TC : Truncation flag.
    - RD : Recursion Desired.
    - RA : Recursion Available.
    - Z : Reserved for future use. Must be zero in all queries and responses.
    - RCODE : Response code.
    - QDCOUNT : An unsigned 16 bit integer specifying the number of entries in the question section.
    - ANCOUNT : An unsigned 16 bit integer specifying the number of resource records in the answer section.
    - NSCOUNT : An unsigned 16 bit integer specifying the number of name server resource records in the authority records section.
    - ARCOUNT : An unsigned 16 bit integer specifying the number of resource records in the additional records section.
    """
    ID: int
    QR: int
    OPCODE: int
    AA: int
    TC: int
    RD: int
    RA: int
    Z: int
    RCODE: int
    QDCOUNT: int
    ANCOUNT: int
    NSCOUNT: int
    ARCOUNT: int

    def __post_init__(self) -> None:
        """
        ## Header Flags Format
                                        1  1  1  1  1  1
          0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

        Making 16-bit Header flags which will be used in the pack method
        Using bitwise operators to properly set the flags

        Check the pack method for looking at the whole header format
        """
        print("__post_init__ called")
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
        ## Header Format
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

        Packing the header into bytes using the pack method from struct module

        Using the big-endian format to pack the header
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
