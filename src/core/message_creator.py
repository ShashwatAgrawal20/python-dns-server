from dataclasses import dataclass
from .header_creator import DNSHeader
from .question_creator import DNSQuestion


@dataclass
class DNSMessage:
    """
    Represents a DNS message.

    The DNS message is a single UDP datagram sent from the DNS client to the
    DNS server and from the DNS server to the DNS client.

    The message format is as follows:
        +---------------------+
        |        Header       |
        +---------------------+
        |       Question      | the question for the name server
        +---------------------+
        |        Answer       | RRs answering the question
        +---------------------+
        |      Authority      | RRs pointing toward an authority
        +---------------------+
        |      Additional     | RRs holding additional information
        +---------------------+
    """

    HEADER: DNSHeader
    QUESTION: DNSQuestion

    def pack_message_to_bytes(self) -> bytes:
        """
        Packs the DNS message into bytes.

        Format:
        +---------------------+
        |        Header       |
        +---------------------+
        |       Question      | the question for the name server
        +---------------------+
        |        Answer       | RRs answering the question
        +---------------------+
        |      Authority      | RRs pointing toward an authority
        +---------------------+
        |      Additional     | RRs holding additional information
        +---------------------+

        Returns:
            A sequence of bytes representing the DNS message.
        """

        packed_header = self.HEADER.pack_header_to_bytes()
        packed_question = self.QUESTION.pack_question_to_bytes()
        return packed_header + packed_question
