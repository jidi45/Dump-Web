# Prime Advanced SQLi Scanner

#CREATOR HAMJA

Prime is an advanced **SQL Injection scanner** built for educational and security research purposes.  
It detects:
- Error-based SQLi
- Boolean-based SQLi
- Time-based SQLi
- WAF/Firewall blocking

> ⚠️ This tool is for **educational use only**.  
> Run it only on websites you own or have explicit permission to test.

---

## Features
- Random headers & User-Agent rotation
- Error, Boolean and Time-based SQLi detection
- WAF bypass attempts (URL encoding)
- Colored output (safe/vulnerable/blocked)
- Saves results in both `.txt` and `.json`
- Supports **wordlist.txt** (custom parameters)
- Lightweight & works in Termux / Linux

---

## Installation (Linux / Termux)

Clone repository and install dependencies:

```bash
git clone https://github.com/jidi45/Dump-Web.git
cd Dump-Web
bash installer.sh
