from dnschaincli.dnschain_client import DNSChainClient
from dnschaincli.tools import ipv6_to_data


class BitcoinClient:
    BLOCKHASH_TEMPLATE = '{}.blockhash.{}'

    def __init__(self, dns_client: DNSChainClient, coin):
        self.client = dns_client
        self.coin = coin

    def get_blockhash(self, blockheight):
        response = self.client.get_aaaa(self.BLOCKHASH_TEMPLATE.format(blockheight, self.coin))
        data = ipv6_to_data(response.aaaa)
        blockhash = '0'*8 + data
        return blockhash
