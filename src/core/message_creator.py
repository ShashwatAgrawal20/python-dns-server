"""Module to create DNS header section for DNS messages."""


from dataclasses import dataclass
from .header_creator import DNSHeader
from .question_creator import DNSQuestion
from .answer_creator import DNSAnswer


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

    header: DNSHeader
    question: DNSQuestion
    answer: DNSAnswer

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

        packed_header = self.header.pack_header_to_bytes()
        packed_question = self.question.pack_question_to_bytes()
        packed_answer = self.answer.pack_answer_to_bytes()
        return packed_header + packed_question + packed_answer
