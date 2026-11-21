
from pathlib import Path


def save_subdomains(hosts, output):

    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:

        for host in sorted(set(hosts)):
            file.write(f"{host}\n")

    print(f"[+] Subdominios guardados: {path}")


def save_resolved(results, output):

    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:

        for host, ips in sorted(results.items()):

            for ip in ips:
                file.write(f"{host} -> {ip}\n")

    print(f"[+] IP guardadas: {path}")
