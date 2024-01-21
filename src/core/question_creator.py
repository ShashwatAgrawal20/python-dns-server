from dataclasses import dataclass
from struct import pack


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

    QNAME: str = "google.com"
    QTYPE: int = 1
    QCLASS: int = 1

    def parse_QNAME(self):
        """
        Parses the QNAME attribute into a sequence of labels.

        Example:
            google.com -> \x06google\x03com\x00

        Returns:
            A sequence of bytes
        """

        name = self.QNAME
        encoded_domain = ""
        for part in name.split("."):
            encoded_domain += chr(len(part)) + part
        encoded_domain += "\x00"
        return encoded_domain.encode()

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

        encoded_domain = self.parse_QNAME()
        return encoded_domain + pack(">HH", self.QTYPE, self.QCLASS)
