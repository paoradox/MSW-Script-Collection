**Yes**, all 3 scripts require Tor to be installed for the `inject()` and `killswitch()` functions to work.

Here's what each function needs:

**`inject()`**
- Requires Tor to be installed so that the `torrc` config file exists to write to
- Requires `obfs4proxy` to be installed for bridge support

**`killswitch()`**
- Requires Tor to be running as a service/process so the SOCKS5 proxy at `127.0.0.1:9050` is active
- Without it, the `requests.get(..., proxies=...)` call will immediately fail

---

**How to install Tor on each platform:**

| Platform | Command |
|---|---|
| Windows | Download installer from [torproject.org](https://www.torproject.org) or `winget install TorProject.TorBrowser` |
| Linux | `sudo apt install tor obfs4proxy` (Debian/Ubuntu) |
| Mac | `brew install tor obfs4proxy` |

---

**The `generate()` and `set_mac()` functions** do NOT require Tor — they only touch the network interface, so those will work independently without Tor installed.