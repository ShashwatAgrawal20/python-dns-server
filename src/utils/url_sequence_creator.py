"""Module to parse domain names into a lable sequence."""


def encode_name(domain: str) -> bytes:
    """
    Parses the QNAME attribute into a sequence of labels.

    Example:
        google.com -> \x06google\x03com\x00

    Returns:
        A sequence of bytes
    """

    name = ""
    for part in domain.split("."):
        name += chr(len(part)) + part
    name += "\x00"
    return name.encode()
