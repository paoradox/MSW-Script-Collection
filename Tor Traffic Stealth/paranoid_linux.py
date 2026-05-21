import random
import time
import subprocess
import socket
import requests


# ── MAC ADDRESS ──────────────────────────────────────────────────────────────

def generate():
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))  # Linux uses colons + lowercase


def set_mac(interface, mac_address):
    """Change MAC address on Linux via ip link."""
    # Bring interface down first
    subprocess.run(["sudo", "ip", "link", "set", interface, "down"],
                   capture_output=True)

    result = subprocess.run(
        ["sudo", "ip", "link", "set", interface, "address", mac_address],
        capture_output=True, text=True
    )

    # Bring interface back up
    subprocess.run(["sudo", "ip", "link", "set", interface, "up"],
                   capture_output=True)

    if result.returncode == 0:
        print(f"[+] MAC address set to {mac_address} on {interface}")
    else:
        print(f"[-] Failed to set MAC: {result.stderr}")
        print("[!] Try running with sudo.")


# ── BRIDGE COLLECTION ─────────────────────────────────────────────────────────

def get_bridges():
    """Automatically fetch obfs4 bridges from Tor Project API."""
    print()
    print("=" * 60)
    print("[i] BRIDGE COLLECTION")
    print("=" * 60)
    print("[i] Fetching obfs4 bridges from bridges.torproject.org...")

    try:
        response = requests.get(
            "https://bridges.torproject.org/bridges?transport=obfs4",
            timeout=15
        )

        if response.status_code == 200:
            lines = response.text.strip().splitlines()

            bridges = [
                line.strip() for line in lines
                if line.strip().startswith("obfs4")
            ]

            if bridges:
                print(f"[+] Successfully fetched {len(bridges)} bridge(s):")
                for i, b in enumerate(bridges, 1):
                    short = b[:60] + "..." if len(b) > 60 else b
                    print(f"    [{i}] {short}")
                return bridges
            else:
                print("[-] Response received but no valid obfs4 bridges found.")
                print("[i] The API may require a CAPTCHA — falling back to manual input.")
                return get_bridges_manual()

        elif response.status_code == 429:
            print("[-] Rate limited by bridges.torproject.org — too many requests.")
            print("[i] Falling back to manual input.")
            return get_bridges_manual()

        else:
            print(f"[-] Unexpected response: HTTP {response.status_code}")
            print("[i] Falling back to manual input.")
            return get_bridges_manual()

    except requests.exceptions.ConnectionError:
        print("[-] No internet connection or bridges.torproject.org is blocked.")
        print("[i] Try getting bridges by emailing: bridges@torproject.org")
        print("[i] Falling back to manual input.")
        return get_bridges_manual()

    except Exception as e:
        print(f"[-] Unexpected error fetching bridges: {e}")
        print("[i] Falling back to manual input.")
        return get_bridges_manual()


def get_bridges_manual():
    """Fallback: ask the user to input bridges manually."""
    print()
    print("[i] MANUAL BRIDGE INPUT")
    print("[i] Get bridges from https://bridges.torproject.org (select obfs4)")
    print("[i] Or email bridges@torproject.org with the message: get transport obfs4")
    print()
    print("[i] Each bridge looks like this:")
    print("    obfs4 192.95.36.142:443 AB1234CDEF... cert=XXXXX... iat-mode=0")
    print()
    print("[i] Enter bridges below one per line. Type 'done' when finished.")
    print()

    bridges = []
    while True:
        line = input("    Bridge: ").strip()
        if line.lower() == 'done':
            break
        if line.startswith("obfs4") or line.startswith("Bridge obfs4"):
            bridges.append(line.replace("Bridge ", ""))
            print(f"    [+] Added bridge #{len(bridges)}")
        elif line == "":
            continue
        else:
            print("    [!] Invalid format. Bridge must start with 'obfs4'")

    if not bridges:
        print("[-] No bridges entered. Skipping bridge injection.")
        return None

    print(f"[+] {len(bridges)} bridge(s) collected.")
    return bridges


# ── TOR BRIDGE INJECTION ─────────────────────────────────────────────────────

def get_torrc_path():
    """Auto-detect or ask user for torrc path on Linux."""
    import os

    candidates = [
        "/etc/tor/torrc",                                               # Default Linux path
        "/usr/local/etc/tor/torrc",                                     # Alternate
        os.path.expanduser("~/.tor/torrc"),                             # User-level
    ]
    for path in candidates:
        if os.path.exists(path):
            print(f"[i] Found torrc at: {path}")
            use_found = input("[?] Use this path? (y/n): ").strip().lower()
            if use_found == 'y':
                return path

    print()
    print("[!] Could not auto-detect torrc path.")
    print("[i] Example paths:")
    print("    /etc/tor/torrc")
    print("    /usr/local/etc/tor/torrc")
    print("    ~/.tor/torrc")
    print()
    print("[i] Tip: Navigate to the Tor folder, then add /torrc at the end.")
    print()

    while True:
        path = input("[?] Enter your torrc path: ").strip().strip('"')
        path = os.path.expanduser(path)

        if os.path.isdir(path):
            path = os.path.join(path, "torrc")
            print(f"[i] Folder detected, appended torrc -> {path}")

        if os.path.exists(path):
            return path
        else:
            print(f"[-] File not found: {path}")
            retry = input("[?] Try again? (y/n): ").strip().lower()
            if retry != 'y':
                return None


def inject(bridge_list):
    torrc_path = get_torrc_path()

    if torrc_path is None:
        print("[-] Skipping bridge injection — no valid torrc path provided.")
        return

    stealth_settings = [
        "UseBridges 1\n",
        "ClientTransportPlugin obfs4 exec /usr/bin/obfs4proxy\n"        # Linux default path
    ]

    for bridge in bridge_list:
        stealth_settings.append(f"Bridge {bridge}\n")

    try:
        with open(torrc_path, "r") as f:
            lines = f.readlines()

        new_lines = [l for l in lines if not any(
            x in l for x in ["Bridge", "UseBridges", "ClientTransportPlugin"]
        )]

        final_config = new_lines + stealth_settings

        with open(torrc_path, "w") as f:
            f.writelines(final_config)

        print("[+] Tor configuration updated with stealth bridges.")
        print("[!] Restart Tor Browser now and wait for it to fully connect.")
        print("[!] Then run this script again to start the killswitch.")

    except PermissionError:
        print("[-] Permission denied. Run with sudo.")
    except Exception as e:
        print(f"[-] Failed to update torrc: {e}")


# ── KILLSWITCH ────────────────────────────────────────────────────────────────

def disable_interface(interface):
    """Disable the network interface on Linux."""
    result = subprocess.run(
        ["sudo", "ip", "link", "set", interface, "down"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"[!] Interface '{interface}' disabled successfully.")
    else:
        print(f"[-] Failed to disable interface: {result.stderr}")


def handle_leak(interface, current_ip, tor_ip):
    """Ask user what to do when a leak is detected."""
    print()
    print("=" * 60)
    print("[!] IP LEAK DETECTED")
    print("=" * 60)
    print(f"    Tor IP    : {tor_ip}")
    print(f"    Current IP: {current_ip}")
    print()
    print("    What would you like to do?")
    print("    [1] Disable interface immediately (safest)")
    print("    [2] Keep monitoring and alert only")
    print("    [3] Stop killswitch and keep connection alive")
    print()

    while True:
        choice = input("    [?] Enter choice (1/2/3): ").strip()

        if choice == '1':
            print("[!] Disabling interface...")
            disable_interface(interface)
            return "disabled"
        elif choice == '2':
            print("[i] Keeping connection alive. Continuing to monitor...")
            print("[!] WARNING: Your real IP may be exposed!")
            return "monitor"
        elif choice == '3':
            print("[i] Killswitch stopped. Interface remains active.")
            print("[!] WARNING: Your real IP may be exposed!")
            return "stop"
        else:
            print("    [!] Invalid choice. Enter 1, 2, or 3.")


def killswitch(interface):
    """Monitor for IP leaks; ask user before taking action."""
    print()
    print("=" * 60)
    print("[i] KILLSWITCH")
    print("=" * 60)
    print("[!] Make sure Tor Browser is open and fully connected before continuing.")
    proceed = input("[?] Is Tor Browser connected and ready? (y/n): ").strip().lower()
    if proceed != 'y':
        print("[-] Skipping killswitch. Open Tor Browser first, then run again.")
        return

    print("[+] Killswitch active. Monitoring for IP leaks...")
    print("[i] Waiting 10 seconds for Tor to stabilize...")
    time.sleep(10)

    # Step 1: Check if Tor SOCKS proxy is reachable
    try:
        sock = socket.create_connection(("127.0.0.1", 9150), timeout=5)
        sock.close()
        print("[+] Tor SOCKS proxy is reachable at 127.0.0.1:9150")
    except OSError:
        print("[-] Tor SOCKS proxy is NOT reachable at 127.0.0.1:9150")
        print("[!] Make sure Tor Browser is open and connected, then run the script again.")
        print("[!] Skipping killswitch — interface will NOT be disabled.")
        return

    # Step 2: Get Tor IP
    try:
        print("[i] Fetching Tor IP...")
        tor_ip = requests.get(
            'https://check.torproject.org/api/ip',
            proxies={
                'http': 'socks5h://127.0.0.1:9150',
                'https': 'socks5h://127.0.0.1:9150'
            },
            timeout=15
        ).json()["IP"]
        print(f"[+] Secure Tor IP: {tor_ip}")

    except requests.exceptions.ConnectionError as e:
        print(f"[-] Could not reach Tor check site: {e}")
        print("[!] Tor may still be connecting — try again in a few seconds.")
        return
    except Exception as e:
        print(f"[-] Unexpected error fetching Tor IP: {e}")
        return

    # Step 3: Monitor for leaks
    print("[+] Monitoring for IP leaks every 3 seconds... (Ctrl+C to stop)")
    while True:
        try:
            current_ip = requests.get(
                'https://api.ipify.org',
                proxies={
                    'http': 'socks5h://127.0.0.1:9150',
                    'https': 'socks5h://127.0.0.1:9150'
                },
                timeout=10
            ).text.strip()

            if current_ip != tor_ip:
                action = handle_leak(interface, current_ip, tor_ip)
                if action in ("disabled", "stop"):
                    break
            else:
                print(f"[+] No leak. Tor IP: {current_ip}")

        except requests.exceptions.ConnectionError:
            print()
            print("[!] Connection lost during monitoring.")
            action = handle_leak(interface, "UNKNOWN", tor_ip)
            if action in ("disabled", "stop"):
                break
        except KeyboardInterrupt:
            print("\n[i] Killswitch stopped by user. Interface remains active.")
            break
        except Exception as e:
            print(f"[-] Monitoring error: {e}")
            break

        time.sleep(3)


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("         TOR ANONYMITY SCRIPT — LINUX")
    print("=" * 60)

    # Check your interface name with: ip link show
    # Common names: eth0, enp3s0, wlan0, wlp2s0
    INTERFACE = "eth0"

    # Step 1: Generate and set MAC address
    print()
    print("[i] STEP 1 — MAC ADDRESS SPOOFING")
    address = generate()
    print(f"[i] Generated MAC: {address}")
    set_mac(INTERFACE, address)

    # Step 2: Automatically fetch bridges
    print()
    print("[i] STEP 2 — BRIDGE COLLECTION")
    bridges = get_bridges()

    # Step 3: Inject bridges into torrc
    if bridges:
        print()
        print("[i] STEP 3 — TORRC INJECTION")
        inject(bridges)
    else:
        print("[i] STEP 3 — Skipped (no bridges provided)")

    # Step 4: Start killswitch
    print()
    print("[i] STEP 4 — KILLSWITCH")
    killswitch(INTERFACE)