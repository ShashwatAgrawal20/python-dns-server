"""Module to create DNS answer section for DNS messages. """


from dataclasses import dataclass
from struct import pack
from utils import encode_name


@dataclass
class DNSQuestion:
    """
    The question section is used to carry the "question" in most queries,
    i.e., the parameters that define what is being asked.  The section
    contains QDCOUNT (usually 1) entries, each of the following format:

                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                     QNAME                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QTYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QCLASS                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

    Args:
        *QNAME:* A domain name represented as a sequence of labels, where
        each label consists of a length octet followed by that number of octets

        *QTYPE:* A two octet code which specifies the type of the query.

        *QCLASS:* A two octet code that specifies the class of the query.
    """

    qname: str = "google.com"
    qtype: int = 1
    qclass: int = 1

    def pack_question_to_bytes(self) -> bytes:
        """
        Packs the DNS question into bytes.

                                        1  1  1  1  1  1
          0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        |                                               |
        /                     QNAME                     /
        /                                               /
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        |                     QTYPE                     |
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
        |                     QCLASS                    |
        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

        Note:
            This won't return a fix length of bytes, as the QTYPE and QCLASS
            are 2 bytes long, but the QNAME is of variable length.
        """

        encoded_domain = encode_name(self.qname)
        return encoded_domain + pack(">HH", self.qtype, self.qclass)
