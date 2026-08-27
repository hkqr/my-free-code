import sys
from .launchers import launch, CLIENTS

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in CLIENTS:
        print("Usage: mfc-client <client> [args...]")
        print("Clients:", ", ".join(CLIENTS))
        raise SystemExit(2)
    raise SystemExit(launch(sys.argv[1], sys.argv[2:]))
