
import dns.resolver


def resolve_host(host, ipv4=True, ipv6=False):

    resolver = dns.resolver.Resolver()
    resolver.timeout = 3
    resolver.lifetime = 5

    addresses = []

    record_types = []

    if ipv4:
        record_types.append("A")

    if ipv6:
        record_types.append("AAAA")

    for record_type in record_types:

        try:
            answers = resolver.resolve(host, record_type)

            for answer in answers:
                addresses.append(str(answer))

        except (
            dns.resolver.NXDOMAIN,
            dns.resolver.NoAnswer,
            dns.resolver.Timeout,
            dns.exception.DNSException
        ):
            continue

    return sorted(set(addresses))


def resolve_subdomains(hosts, ipv4=True, ipv6=False):

    results = {}

    for host in hosts:

        ips = resolve_host(
            host,
            ipv4=ipv4,
            ipv6=ipv6
        )

        if ips:
            results[host] = ips

            print(
                f"[+] {host} -> {', '.join(ips)}"
            )

        else:
            print(f"[-] {host} -> Sin IP")

    return results
