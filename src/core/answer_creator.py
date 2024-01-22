"""Module to create DNS answer section for DNS messages."""


from dataclasses import dataclass
from struct import pack
from utils import encode_name


@dataclass
class DNSAnswer:
    """
    Class to represent a DNS answer.

    Attributes:
        name: The domain name
        type: The type of the DNS record
        class: The class of the DNS record
        ttl: The time to live of the DNS record
        length: The length of the DNS record
        data: The data of the DNS record

    Format:
                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                                               /
    /                      NAME                     /
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     CLASS                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TTL                      |
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                   RDLENGTH                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--|
    /                     RDATA                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    """
    name: str = "google.com"
    type_: int = 1
    class_: int = 1
    ttl: int = 69
    length: int = 4
    data: bytes = "\x08\x08\x08\x08"

    def pack_answer_to_bytes(self) -> bytes:
        """Pack the DNS answer to bytes."""
        return (
            encode_name(self.name)
            + pack(">HHIH", self.type_, self.class_, self.ttl, self.length)
            + self.data
        )
