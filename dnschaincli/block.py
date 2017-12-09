import binascii
import struct


class Block:
    def __init__(self):
        self.transactions = None
        self.blockhash = None
        self.blocktime = None
        self.prevblockhash = None
        self.merkle_root = None
        self.version = None
        self.nbits = None
        self.nonce = None
        self.transactions = None
        self._height = None
        self._checkpoints = dict()
        self._checkpoint = False

    def _ensure_checkpoint(self, value):
        if value in self._checkpoints:
            assert self.blockhash and self.blockhash == self._checkpoints[value]
            self._checkpoint = True

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._ensure_checkpoint(value)
        self._height = value

    @property
    def checkpoint(self):
        return self._checkpoint

    @classmethod
    def get(cls, blockhash, blockheader, height=None):
        self = cls()
        rawh = binascii.unhexlify(blockheader)
        self.version = binascii.hexlify(rawh[0:4][::-1]).decode()
        self.prevblockhash = binascii.hexlify(rawh[4:36][::-1]).decode()
        self.blocktime = struct.unpack('<L', rawh[68:72])[0]
        self.nbits = binascii.hexlify(rawh[72:76][::-1]).decode()
        self.nonce = struct.unpack('<L', rawh[76:80])[0]
        self.blockhash = blockhash
        self.height = height
        return self


class BitcoinBlock(Block):
    def __init__(self):
        super().__init__()
        self._checkpoints = {
            0: '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f',
            50000: '000000001aeae195809d120b5d66a39c83eb48792e068f8ea1fea19d84a4278a',
            100000: '000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506',
            150000: '0000000000000a3290f20e75860d505ce0e948a1d1d846bec7e39015d242884b',
            200000: '000000000000034a7dedef4a161fa058a2d67a173a90155f3a2fe6fc132e0ebf',
            250000: '000000000000003887df1f29024b06fc2200b55f8af8f35453d7be294df2d214',
            300000: '000000000000000082ccf8f1557c5d40b21edabb18d2d691cfbf87118bac7254',
            350000: '0000000000000000053cf64f0400bb38e0c4b3872c38795ddde27acb40a112bb',
            400000: '000000000000000004ec466ce4732fe6f1ed1cddc2ed4b328fff5224276e3f6f',
            450000: '0000000000000000014083723ed311a461c648068af8cef8a19dcd620c07a20b'
        }
