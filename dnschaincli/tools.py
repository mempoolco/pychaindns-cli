def ipv6_to_data(ips):
    _d = {}
    for ip in ips:
        this = ip.split(':')
        index = int(this[0].replace('10', ''))
        assert not _d.get(index)
        _d[index] = ''.join(['0'*(4-len(x)) + x for x in this[1:]])
    return ''.join([_d[x] for x in sorted(list(_d.keys()))])