"""Module to extract domain names into a lable sequence."""


from typing import Tuple


def extract_name(buf: bytes, start_index: int) -> Tuple[bytes, int]:
    """
    Extract a domain name from a buffer.

    Args:
        buf (bytes): Buffer to extract from.
        start_index (int): Index to start extracting from
    """
    packed_remainder = buf[start_index:]
    name = b""
    name_end = 0
    for _ in packed_remainder:
        if start_index + name_end >= len(buf) - 4:
            raise ValueError("Did not find the end of domain label")
        if packed_remainder[name_end] == 0:
            name = packed_remainder[: name_end + 1]
            break
        if (packed_remainder[name_end] >> 6) == 0b11:
            offset = (
                int.from_bytes(packed_remainder[name_end: name_end + 2], "big")
                & 0x3FFF
            )
            pointed_name, _ = extract_name(buf, offset)
            name = pointed_name
            name = packed_remainder[:name_end] + pointed_name
            name_end += 1
            break
        name_end += 1
    return name, name_end
