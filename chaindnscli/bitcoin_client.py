from chaindnscli.chaindns_client import ChainDNSClient
from chaindnscli.tools import ipv6_to_data, base64decode, strip_checksum


class BitcoinClient:
    BLOCKHASH_TEMPLATE = '{}.blockhash.{}'
    BLOCKHEADER_TEMPLATE = '{}.blockheader.{}'

    def __init__(self, dns_client: ChainDNSClient, coin):
        self.client = dns_client
        self.coin = coin

    def get_blockhash(self, blockheight):
        response = self.client.get_aaaa(self.BLOCKHASH_TEMPLATE.format(blockheight, self.coin))
        data = ipv6_to_data(response.aaaa)
        blockhash = '0'*8 + data
        return blockhash

    def get_blockheaders(self, blockhash):
        if len(blockhash) == 64:
            assert blockhash[:8] == '00000000'
            blockhash = blockhash[8:]
        assert len(blockhash) == 56
        response = self.client.get_txt(self.BLOCKHEADER_TEMPLATE.format(blockhash, self.coin))
        data = base64decode(response.txt[0])
        data = strip_checksum(data, tohex=1)
        return data
