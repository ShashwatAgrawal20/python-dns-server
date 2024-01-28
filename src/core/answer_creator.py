"""Module to create DNS answer section for DNS messages."""


from dataclasses import dataclass
from struct import pack


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
    name: bytes
    type_: int
    class_: int
    ttl: int
    length: int
    data: bytes

    def pack_answer_to_bytes(self) -> bytes:
        """Pack the DNS answer to bytes."""
        return (
            self.name
            + pack(">HHIH", self.type_, self.class_, self.ttl, self.length)
            + self.data
        )
