
import requests

HEADERS = {
    "User-Agent": "SubFinderHunter/1.0"
}

TIMEOUT = 15


def in_scope(host, domain):
    host = host.lower().strip().rstrip(".")
    domain = domain.lower().strip().rstrip(".")

    return host == domain or host.endswith("." + domain)


def query_crt(domain):
    found = set()

    try:
        response = requests.get(
            "https://crt.sh/",
            params={"q": f"%.{domain}", "output": "json"},
            headers=HEADERS,
            timeout=TIMEOUT
        )
        response.raise_for_status()

        for cert in response.json():
            for name in cert.get("name_value", "").splitlines():
                name = name.lower().strip().rstrip(".")

                if "*" not in name and in_scope(name, domain):
                    found.add(name)

        print(f"[+] crt.sh: {len(found)} resultados")

    except Exception as error:
        print(f"[!] crt.sh: {error}")

    return found


def query_otx(domain):
    found = set()

    try:
        url = (
            "https://otx.alienvault.com/api/v1/"
            f"indicators/domain/{domain}/passive_dns"
        )

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        response.raise_for_status()

        for record in response.json().get("passive_dns", []):
            host = record.get("hostname", "").lower().strip().rstrip(".")

            if host and in_scope(host, domain):
                found.add(host)

        print(f"[+] AlienVault OTX: {len(found)} resultados")

    except Exception as error:
        print(f"[!] AlienVault OTX: {error}")

    return found


def query_hackertarget(domain):
    found = set()

    try:
        response = requests.get(
            "https://api.hackertarget.com/hostsearch/",
            params={"q": domain},
            headers=HEADERS,
            timeout=TIMEOUT
        )
        response.raise_for_status()

        if "error" in response.text.lower()[:100]:
            print("[!] HackerTarget: respuesta de error o límite de API")
            return found

        for line in response.text.splitlines():
            parts = line.split(",")

            if len(parts) < 2:
                continue

            host = parts[0].lower().strip().rstrip(".")

            if in_scope(host, domain):
                found.add(host)

        print(f"[+] HackerTarget: {len(found)} resultados")

    except Exception as error:
        print(f"[!] HackerTarget: {error}")

    return found


def collect_subdomains(domain, disabled=None):
    disabled = disabled or set()

    sources = {
        "crt": query_crt,
        "otx": query_otx,
        "hackertarget": query_hackertarget
    }

    results = set()

    for name, function in sources.items():
        if name not in disabled:
            results.update(function(domain))

    return sorted(results)
