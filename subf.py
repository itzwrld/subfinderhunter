
import argparse

from sources import collect_subdomains
from resolver import resolve_subdomains
from exporter import save_subdomains, save_resolved

VERSION = "1.1.0"


def main():
    parser = argparse.ArgumentParser(
        prog="subf",
        description="SubFinderHunter - Passive Subdomain Discovery"
    )

    parser.add_argument(
        "-u",
        required=True,
        metavar="DOMAIN",
        help="Dominio objetivo"
    )

    parser.add_argument(
        "-r",
        action="store_true",
        help="Resolver IPv4 (activado por defecto)"
    )

    parser.add_argument(
        "-ipv6",
        action="store_true",
        help="Resolver también IPv6"
    )

    parser.add_argument(
        "--no-resolve",
        action="store_true",
        help="Desactivar resolución DNS"
    )

    parser.add_argument(
        "-o", "--output",
        default="results/resolved.txt",
        help="Ruta del archivo de resultados"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"SubFinderHunter {VERSION}"
    )

    args = parser.parse_args()

    if args.no_resolve and (args.r or args.ipv6):
        parser.error("--no-resolve no puede combinarse con -r o -ipv6")

    domain = args.u.lower().strip().rstrip(".")

    print("""
========================================
          SUBFINDERHUNTER
========================================
""")

    print(f"[*] Dominio: {domain}")
    print("[*] Recopilando subdominios...\n")

    # Recopilación
    hosts = collect_subdomains(domain)

    print(f"\n[+] Subdominios encontrados: {len(hosts)}")

    # Guardar todos los subdominios
    save_subdomains(
        hosts,
        "results/subdomains.txt"
    )

    # Resolución DNS activada por defecto
    if not args.no_resolve:

        print("\n[*] Resolviendo DNS...")

        results = resolve_subdomains(
            hosts,
            ipv4=True,
            ipv6=args.ipv6
        )

        save_resolved(results, args.output)

        print("\n========== RESUMEN ==========")
        print(f"Encontrados: {len(hosts)}")
        print(f"Con IP: {len(results)}")
        print(f"Sin IP: {len(hosts) - len(results)}")

    print("\n[+] Proceso finalizado.")


if __name__ == "__main__":
    main()
