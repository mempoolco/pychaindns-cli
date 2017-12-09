import random
import dnslib


class DNSResponse:
    def __init__(self, query):
        self.query = query
        self.codes = {
            28: dnslib.QTYPE.AAAA,
            1: dnslib.QTYPE.A,
            5: dnslib.QTYPE.CNAME,
            16: dnslib.QTYPE.TXT,
        }
        self.records = {}

    def _add_record(self, rtype: str, data):
        self.records[rtype] = self.records.get(rtype, [])
        self.records[rtype].append(data)

    def parse_response(self, responses: list):
        for response in responses:
            self._add_record(response.rtype, str(response.rdata))
        return self

    @property
    def txt(self) -> list:
        return self.records.get(dnslib.QTYPE.TXT, [])

    @property
    def cname(self) -> list:
        return self.records.get(dnslib.QTYPE.CNAME, [])

    @property
    def a(self) -> list:
        return self.records.get(dnslib.QTYPE.A, [])

    @property
    def aaaa(self) -> list:
        return self.records.get(dnslib.QTYPE.AAAA, [])


class ChainDNSClient:
    def __init__(self, domain):
        self.resolvers = []
        self.domain = domain

    def add_resolver(self, *a, port=53):
        self.resolvers.extend(['{}:{}'.format(x, port) for x in a])

    def _request(self, question, qtype, resolver=None):
        resolver = resolver or random.choice(self.resolvers)
        assert resolver
        client = dnslib.DNSRecord()
        client.add_question(dnslib.DNSQuestion(question, qtype=qtype))
        host, port = resolver.split(':')
        answers = client.parse(client.send(host, port=int(port)))
        response = DNSResponse(question)
        response.parse_response(answers.rr)
        return response

    def call(self, q, qtype, resolver=None):
        return self._request(q + '.%s' % self.domain, qtype, resolver=resolver)

    def get_aaaa(self, query):
        return self.call(query, dnslib.QTYPE.AAAA)

    def get_a(self, query):
        return self.call(query, dnslib.QTYPE.A)

    def get_txt(self, query):
        return self.call(query, dnslib.QTYPE.TXT)

    def get_cname(self, query):
        return self.call(query, dnslib.QTYPE.CNAME)

    def get_any(self, query):
        return self.call(query, dnslib.QTYPE.ANY)
