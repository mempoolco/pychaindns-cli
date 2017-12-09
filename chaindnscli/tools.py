import base64
import hashlib

import binascii


def ipv6_to_data(ips):
    _d = {}
    for ip in ips:
        this = ip.split(':')
        index = int(this[0].replace('10', ''))
        assert not _d.get(index)
        _d[index] = ''.join(['0'*(4-len(x)) + x for x in this[1:]])
    return ''.join([_d[x] for x in sorted(list(_d.keys()))])


def base64decode(data: str):
    data.strip('"')
    return base64.b64decode(data)


def strip_checksum(data: bytes, tohex=False):
    data, checksum = data[:-2], data[-2:]
    assert hashlib.sha256(data).digest()[:2] == checksum
    if tohex:
        return binascii.hexlify(data).decode()
    return data


class dblsha256:
    def __init__(self, x):
        self.data = x

    def digest(self):
        return hashlib.sha256(hashlib.sha256(self.data).digest()).digest()

    def hexdigest(self):
        return binascii.hexlify(self.digest()).decode()
