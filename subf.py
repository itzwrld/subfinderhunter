
import argparse

from sources import collect_subdomains
from resolver import resolve_subdomains
from exporter import save_subdomains, save_resolved


VERSION = "1.1.0"

BANNER = r"""
  ███████╗██╗   ██╗██████╗ ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗
  ██╔════╝██║   ██║██╔══██╗██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
  ███████╗██║   ██║██████╔╝███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
  ╚════██║██║   ██║██╔══██╗██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
  ███████║╚██████╔╝██████╔╝██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
  ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝

              SUBDOMAIN DISCOVERY TOOL
"""


def main():

    parser = argparse.ArgumentParser(
        prog="subf",
        description="SubHunter - Subdomain Discovery Tool"
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
        "-o",
        "--output",
        default="results/resolved.txt",
        help="Archivo de salida (predeterminado: results/resolved.txt)"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"SubHunter {VERSION}"
    )

    args = parser.parse_args()

    if args.no_resolve and (args.r or args.ipv6):
        parser.error(
            "--no-resolve no puede combinarse con -r o -ipv6"
        )

    domain = args.u.lower().strip().rstrip(".")

    print(BANNER)
    print(f"       Version: {VERSION}")
    print("       Author: itzwrld\n")

    print(f"[*] Dominio objetivo: {domain}")
    print("[*] Iniciando recopilación pasiva...\n")

    # Recopilar subdominios
    hosts = collect_subdomains(domain)

    print(f"\n[+] Subdominios encontrados: {len(hosts)}")

    # Guardar todos los subdominios
    save_subdomains(
        hosts,
        "results/subdomains.txt"
    )

    # Resolver DNS automáticamente
    if not args.no_resolve:

        print("\n[*] Resolviendo DNS...")

        results = resolve_subdomains(
            hosts,
            ipv4=True,
            ipv6=args.ipv6
        )

        # Guardar solamente los que tienen IP
        save_resolved(
            results,
            args.output
        )

        print("\n========== RESUMEN ==========")
        print(f"Subdominios encontrados: {len(hosts)}")
        print(f"Subdominios con IP: {len(results)}")
        print(f"Sin resolución: {len(hosts) - len(results)}")

    else:
        print("\n[*] Resolución DNS desactivada.")

    print("\n[+] Proceso finalizado.")


if __name__ == "__main__":
    main()
