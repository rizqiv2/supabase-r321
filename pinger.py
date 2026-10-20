import os
import sys
import argparse
import urllib.request
import urllib.error

def main():
    parser = argparse.ArgumentParser(description="Supabase Inactivity Keep-Alive Pinger")
    parser.add_argument("--url", default=os.getenv("SUPABASE_URL", ""), help="Supabase Project URL")
    parser.add_argument("--key", default=os.getenv("SUPABASE_ANON_KEY", ""), help="Supabase Anon/Public Key")
    parser.add_argument("--table", default=os.getenv("SUPABASE_TABLE", "battery_telemetry"), help="Table name to query (default: battery_telemetry)")
    args = parser.parse_args()

    url = args.url.strip().rstrip("/")
    key = args.key.strip()
    table = args.table.strip()

    if not url or not key:
        print("[!] Missing configuration.")
        print("Please provide --url and --key arguments or set SUPABASE_URL and SUPABASE_ANON_KEY environment variables.")
        print("\nExample:")
        print("  python pinger.py --url https://abcdef.supabase.co --key eyJhbGciOi...")
        sys.exit(1)

    endpoint = f"{url}/rest/v1/{table}?select=*&limit=1"
    print(f"[*] Target Endpoint: {endpoint}")

    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "User-Agent": "Supabase-KeepAlive-Pinger/1.0"
    }

    req = urllib.request.Request(endpoint, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            status_code = resp.status
            body = resp.read().decode("utf-8")
            print(f"[✓] Status: {status_code} OK")
            print(f"[✓] Response: {body}")
            print("\n[✓] PostgreSQL query executed successfully! Supabase inactivity counter has been reset.")
    except urllib.error.HTTPError as e:
        print(f"[!] HTTP Error {e.code}: {e.reason}")
        try:
            print(e.read().decode("utf-8"))
        except Exception:
            pass
        sys.exit(1)
    except Exception as e:
        print(f"[!] Connection failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
