import sys
sys.path.insert(0, '.')

from chaindnscli.chaindns_client import ChainDNSClient
from chaindnscli.bitcoin_client import BitcoinClient


if __name__ == '__main__':
    dns_client = ChainDNSClient('domain.co')
    btc_client = BitcoinClient(dns_client, 'btc')
    dns_client.add_resolver('127.0.0.1', port=8053)
    blockheight = 0
    blockhash = btc_client.get_blockhash(0)
    print('Blockhash for height {} is {}'.format(blockheight, blockhash))
