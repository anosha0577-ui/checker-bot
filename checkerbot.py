import requests
import random
import string
import time
import sys
import os
import json
import uuid
import base64
import secrets
from threading import Thread, Lock
from datetime import datetime
import subprocess
from hashlib import md5


try:
    import httpx
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "httpx", "httpx[http2]"])
    import httpx

try:
    from colorama import Fore, Style, init
    init()
except:
    os.system("pip install colorama")
    from colorama import Fore, Style, init


reset = "\033[0m"
fg_red     = "\033[1;31m"
fg_green   = "\033[1;32m"
fg_yellow  = "\033[1;33m"
fg_blue    = "\033[1;34m"
fg_magenta = "\033[1;35m"
fg_cyan    = "\033[1;36m"
fg_white   = "\033[1;37m"
fg_lavender = "\033[1;38;5;183m"
fg_gold     = "\033[1;38;5;220m"
fg_pink     = "\033[1;38;5;213m"
fg_sky      = "\033[1;38;5;117m"
fg_orange   = "\033[1;38;5;208m"
fg_teal     = "\033[1;38;5;37m"
fg_lavender = "\033[38;5;183m"
fg_mint = "\033[38;5;121m"
fg_red = "\033[38;5;196m"
fg_green = "\033[38;5;82m"
fg_gold = "\033[38;5;220m"
fg_white = "\033[38;5;255m"
fg_cyan = "\033[38;5;51m"
fg_magenta = "\033[38;5;201m"
reset = "\033[0m"
bold = "\033[1m"


BOT_TOKEN = "8987246001:AAFPhsq5CQI-Gx6rbVUE3YtN8uX9WTNNl9w"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def generate_android_ua():
    devices = [
        {"brand": "samsung", "model": "SM-G973F", "device": "beyond1", "board": "exynos9820"},
        {"brand": "Google", "model": "Pixel 7", "device": "panther", "board": "panther"},
        {"brand": "Xiaomi", "model": "Redmi Note 10", "device": "sweet", "board": "sm6150"},
        {"brand": "OnePlus", "model": "ONEPLUS A6003", "device": "OnePlus6", "board": "sdm845"},
    ]
    device = random.choice(devices)
    android_version = random.choice(["12", "13", "14"])
    api_level = {"12": "31", "13": "33", "14": "34"}[android_version]
    dpi = random.choice(["320", "450", "480"])
    instagram_ver = f"{random.randint(300, 370)}.0.0.{random.randint(10, 40)}.{random.randint(80, 150)}"
    locale = random.choice(["en_US", "en_IN", "en_GB"])
    return (f"Instagram {instagram_ver} Android ({api_level}/{android_version}; "
            f"{dpi}dpi; 1080x2207; {device['brand']}; {device['model']}; "
            f"{device['device']}; {device['board']}; {locale}; {random.randint(300000000, 400000000)})")

def gen_uuid():
    return str(uuid.uuid4())


def solve_recaptcha_hi2():
    try:
        anchor_url = "https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LfEUPkgAAAAAKTgbMoewQkWBEQhO2VPL4QviKct&co=aHR0cHM6Ly9oaTIuaW46NDQz&hl=en&v=XrIDux0s7SoNe6_IHkjGC92W&size=invisible"
        params = anchor_url.split('?')[1]
        r = requests.get(f'https://www.google.com/recaptcha/enterprise/anchor?{params}', timeout=10)
        recaptcha_token = r.text.split('recaptcha-token" value="')[1].split('"')[0]
        payload = f"v={params.split('v=')[1].split('&')[0]}&reason=q&c={recaptcha_token}&k=6LfEUPkgAAAAAKTgbMoewQkWBEQhO2VPL4QviKct&co=aHR0cHM6Ly9oaTIuaW46NDQz&hl=en&size=invisible"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": f"https://www.google.com/recaptcha/enterprise/anchor?{params}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        resp = requests.post('https://www.google.com/recaptcha/enterprise/reload', data=payload, headers=headers, timeout=10)
        token = resp.text.split('resp","')[1].split('"')[0]
        return token
    except:
        return None


def check_hi2_registration(email):
    
    if "@" in email:
        domain = email.split("@")[1]
        prefix = email.split("@")[0]
    else:
        return None

    solve = solve_recaptcha_hi2()
    if not solve:
        return None

    data = {
        'domain': domain,
        'prefix': prefix,
        'recaptcha': solve,
    }
    headers = {
        'User-Agent': "Mozilla/5.0",
        'Accept': "application/json, text/plain, */*",
        'authorization': "Basic bnVsbA==",
    }
    try:
        response = requests.post("https://hi2.in/api/custom", data=data, headers=headers, timeout=15)
        res = response.json()
        if "already taken" in str(res):
            return True
        else:
            return False
    except:
        return None


def check_instagram_registration(email):
    
    try:
        url = "https://i.instagram.com/api/v1/users/check_email/"
        ua = generate_android_ua()
        response = httpx.Client(http2=True).post(
            url,
            data=f"email={email}",
            headers={
                'User-Agent': ua,
                'content-type': "application/x-www-form-urlencoded; charset=UTF-8"
            },
            timeout=15
        )
        if 'email_is_taken' in response.text:
            return True
        return False
    except:
        return None


def check_bloks_registration(email):
    
    try:
        url = "https://i.instagram.com/api/v1/bloks/async_action/com.bloks.www.caa.ar.search.async/"
        device = str(uuid.uuid4())
        family = str(uuid.uuid4())
        android = "android-" + secrets.token_hex(8)
        payload = {
            'params': '{"client_input_params":{"aac":"{\\"aac_init_timestamp\\":' + str(int(time.time())) + ',\\"aacjid\\":\\"' + str(uuid.uuid4()) + '\\",\\"aaccs\\":\\"' + secrets.token_urlsafe(32) + '\\"}","flash_call_permissions_status":{"READ_PHONE_STATE":"PERMANENTLY_DENIED","READ_CALL_LOG":"DENIED","ANSWER_PHONE_CALLS":"DENIED"},"was_headers_prefill_available":0,"network_bssid":null,"sfdid":"","fetched_email_token_list":{},"search_query":"' + email + '","auth_secure_device_id":"","ig_oauth_token":[],"cloud_trust_token":null,"was_headers_prefill_used":0,"sso_accounts_auth_data":[],"encrypted_msisdn":"","device_network_info":null,"text_input_id":"akyuf0:61","zero_balance_state":null,"android_build_type":"release","accounts_list":[],"is_oauth_without_permission":0,"ig_android_qe_device_id":"' + device + '","gms_incoming_call_retriever_eligibility":"client_not_supported","search_screen_type":"email_or_username","is_whatsapp_installed":1,"lois_settings":{"lois_token":""},"ig_vetted_device_nonce":null,"headers_infra_flow_id":"","fetched_email_list":[]},"server_params":{"event_request_id":"' + str(uuid.uuid4()) + '","is_from_logged_out":0,"layered_homepage_experiment_group":null,"device_id":"' + android + '","login_surface":"login_home","waterfall_id":"' + str(uuid.uuid4()) + '","INTERNAL__latency_qpl_instance_id":6.3987980400102E13,"is_platform_login":0,"context_data":"","login_entry_point":"logged_out","INTERNAL__latency_qpl_marker_id":36707139,"family_device_id":"' + family + '","offline_experiment_group":"caa_iteration_v3_perf_ig_4","access_flow_version":"pre_mt_behavior","is_from_logged_in_switcher":0,"qe_device_id":"' + device + '"}}',
            'bk_client_context': '{"bloks_version":"5e47baf35c5a270b44c8906c8b99063564b30ef69779f3dee0b828bee2e4ef5b","styles_id":"instagram"}',
            'bloks_versioning_id': "5e47baf35c5a270b44c8906c8b99063564b30ef69779f3dee0b828bee2e4ef5b"
        }
        headers = {
            'User-Agent': "Instagram 370.1.0.43.96 Android (34/14; 450dpi; 1080x2207; samsung; SM-A235F; a23; qcom; en_IN; 704872281)",
            'accept-language': "en-IN, en-US",
            'x-bloks-version-id': "5e47baf35c5a270b44c8906c8b99063564b30ef69779f3dee0b828bee2e4ef5b",
            'x-fb-friendly-name': "IgApi: bloks/async_action/com.bloks.www.caa.ar.search.async/",
            'x-ig-android-id': android,
            'x-ig-app-id': "567067343352427",
            'x-ig-app-locale': "en_IN",
            'x-ig-device-id': device,
            'x-ig-family-device-id': family,
            'x-ig-timezone-offset': str(datetime.now().astimezone().utcoffset().total_seconds()),
            'x-mid': base64.urlsafe_b64encode(secrets.token_bytes(18)).decode().rstrip('='),
            'x-pigeon-rawclienttime': str(time.time()),
            'x-pigeon-session-id': f"UFS-{uuid.uuid4()}-0",
        }
        response = requests.post(url, data=payload, headers=headers, timeout=20)
        if email in response.text:
            return True
        return False
    except:
        return None


def check_email_availability(email, domain):
    
    
    ig_result = check_instagram_registration(email)
    if ig_result is True:
        return "taken"
    elif ig_result is False:
        
        if domain == "hi2.in":
            hi2_result = check_hi2_registration(email)
            if hi2_result is True:
                return "taken"
            elif hi2_result is False:
                return "not_taken"
            else:
                
                return "not_taken"
        else:
            return "not_taken"
    else:
        
        bloks_result = check_bloks_registration(email)
        if bloks_result is True:
            return "taken"
        elif bloks_result is False:
            if domain == "hi2.in":
                hi2_result = check_hi2_registration(email)
                if hi2_result is True:
                    return "taken"
                elif hi2_result is False:
                    return "not_taken"
            return "not_taken"
        else:
           
            if domain == "hi2.in":
                hi2_result = check_hi2_registration(email)
                if hi2_result is True:
                    return "taken"
                elif hi2_result is False:
                    return "not_taken"
            return "unknown"


def get_updates(offset=None):
    url = f"{API_URL}/getUpdates"
    params = {"timeout": 30, "offset": offset}
    try:
        resp = requests.get(url, params=params, timeout=35)
        return resp.json().get("result", [])
    except:
        return []

def send_message(chat_id, text, parse_mode="HTML", reply_markup=None):
    url = f"{API_URL}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    try:
        requests.post(url, data=data, timeout=10)
    except:
        pass

def edit_message(chat_id, message_id, text, parse_mode="HTML", reply_markup=None):
    
    url = f"{API_URL}/editMessageText"
    data = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": parse_mode}
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    try:
        requests.post(url, data=data, timeout=10)
    except:
        pass

def answer_callback(update_id, callback_query_id, text=None, show_alert=False):
    
    url = f"{API_URL}/answerCallbackQuery"
    data = {"callback_query_id": callback_query_id}
    if text:
        data["text"] = text
        data["show_alert"] = show_alert
    try:
        requests.post(url, data=data, timeout=10)
    except:
        pass

def send_welcome(chat_id):
    
    msg = (
        "╔═══━━━───〔 ✦ 〕───━━━═══╗\n"
        "║   𝐇𝐈2 & 𝐓𝐄𝐋𝐄𝐆𝐌𝐀𝐈𝐋 𝐂𝐇𝐄𝐂𝐊𝐄𝐑   ║\n"
        "╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
        "║       𝐒𝐄𝐋𝐄𝐂𝐓 𝐌𝐎𝐃𝐄 𝐁𝐄𝐋𝐎𝐖       ║\n"
        "╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
        "║  【1】 𝐒𝐢𝐧𝐠𝐥𝐞 𝐂𝐡𝐞𝐜𝐤         ║\n"
        "║  → 𝐂𝐡𝐞𝐜𝐤 𝟏 𝐮𝐬𝐞𝐫𝐧𝐚𝐦𝐞/𝐞𝐦𝐚𝐢𝐥     ║\n"
        "║                              ║\n"
        "║  【2】 𝐁𝐮𝐥𝐤 𝐂𝐡𝐞𝐜𝐤           ║\n"
        "║  → 𝐂𝐡𝐞𝐜𝐤 𝐦𝐮𝐥𝐭𝐢𝐩𝐥𝐞 𝐞𝐦𝐚𝐢𝐥𝐬    ║\n"
        "║  → 𝐅𝐨𝐫𝐦𝐚𝐭: mail1 mail2    ║\n"
        "╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
        "║  𝐅𝐨𝐥𝐥𝐨𝐰 𝐨𝐮𝐫 𝐜𝐡𝐚𝐧𝐧𝐞𝐥 𝐛𝐞𝐥𝐨𝐰    ║\n"
        "╚═══━━━───〔 ✦ 〕───━━━═══╝"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🔹 𝐒𝐢𝐧𝐠𝐥𝐞 𝐌𝐨𝐝𝐞", "callback_data": "mode_single"},
                {"text": "🔸 𝐁𝐮𝐥𝐤 𝐌𝐨𝐝𝐞", "callback_data": "mode_bulk"}
            ],
            [
                {"text": "📢 𝐉𝐨𝐢𝐧 𝐂𝐡𝐚𝐧𝐧𝐞𝐥", "url": "https://t.me/greatemperorrr"}
            ]
        ]
    }
    send_message(chat_id, msg, reply_markup=keyboard)

def send_single_mode_prompt(chat_id, message_id=None):
    
    msg = (
        "╔═══━━━───〔 ✦ 〕───━━━═══╗\n"
        "║     𝐒𝐈𝐍𝐆𝐋𝐄 𝐌𝐎𝐃𝐄 𝐀𝐂𝐓𝐈𝐕𝐀𝐓𝐄𝐃      ║\n"
        "╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
        "║  𝐒𝐞𝐧𝐝 𝐚 𝐮𝐬𝐞𝐫𝐧𝐚𝐦𝐞 (𝐧𝐨 @)      ║\n"
        "║  𝐓𝐨 𝐜𝐡𝐞𝐜𝐤 𝐚𝐯𝐚𝐢𝐥𝐚𝐛𝐢𝐥𝐢𝐭𝐲 𝐨𝐧 :   ║\n"
        "║     • hi2.in                  ║\n"
        "║     • telegmail.com           ║\n"
        "╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
        "║  𝐄𝐱𝐚𝐦𝐩𝐥𝐞𝐬 :                 ║\n"
        "║   john_doe                   ║\n"
        "║   alex123                    ║\n"
        "╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
        "║  𝐎𝐫 𝐬𝐞𝐧𝐝 𝐟𝐮𝐥𝐥 𝐞𝐦𝐚𝐢𝐥 :        ║\n"
        "║   user@hi2.in                ║\n"
        "╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
        "║  𝐔𝐬𝐞 /start 𝐭𝐨 𝐜𝐡𝐚𝐧𝐠𝐞 𝐦𝐨𝐝𝐞     ║\n"
        "╚═══━━━───〔 ✦ 〕───━━━═══╝"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "⬅️ 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐌𝐚𝐢𝐧 𝐌𝐞𝐧𝐮", "callback_data": "back_menu"}
            ]
        ]
    }

    if message_id:
        edit_message(chat_id, message_id, msg, reply_markup=keyboard)
    else:
        send_message(chat_id, msg, reply_markup=keyboard)

def send_bulk_mode_prompt(chat_id, message_id=None):
    
    msg = (
        "╔═══━━━───〔 ✦ 〕───━━━═══╗\n"
        "║     𝐁𝐔𝐋𝐊 𝐌𝐎𝐃𝐄 𝐀𝐂𝐓𝐈𝐕𝐀𝐓𝐄𝐃       ║\n"
        "╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
        "║  𝐒𝐞𝐧𝐝 𝐚𝐥𝐥 𝐞𝐦𝐚𝐢𝐥𝐬 𝐢𝐧 𝐨𝐧𝐞 𝐦𝐬𝐠    ║\n"
        "║  𝐒𝐞𝐩𝐚𝐫𝐚𝐭𝐞𝐝 𝐛𝐲 𝐬𝐩𝐚𝐜𝐞𝐬           ║\n"
        "╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
        "║  𝐅𝐨𝐫𝐦𝐚𝐭 :                    ║\n"
        "║  user1@domain user2@domain     ║\n"
        "║  𝐄𝐱𝐚𝐦𝐩𝐥𝐞 :                   ║\n"
        "║  john@hi2.in jane@telegmail.com ║\n"
        "╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
        "║  𝐔𝐬𝐞 /start 𝐭𝐨 𝐜𝐡𝐚𝐧𝐠𝐞 𝐦𝐨𝐝𝐞     ║\n"
        "╚═══━━━───〔 ✦ 〕───━━━═══╝"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "⬅️ 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐌𝐚𝐢𝐧 𝐌𝐞𝐧𝐮", "callback_data": "back_menu"}
            ]
        ]
    }

    if message_id:
        edit_message(chat_id, message_id, msg, reply_markup=keyboard)
    else:
        send_message(chat_id, msg, reply_markup=keyboard)

def process_single_check(chat_id, username):
    

    
    username = username.strip().lower()

    if "@" in username:
        parts = username.split("@")
        domain = parts[1].lower()

        if domain not in ["hi2.in", "telegmail.com"]:
            send_message(
                chat_id,
                (
                    "╔═══━━━───〔 ✦ 〕───━━━═══╗\n"
                    "║         𝐈𝐍𝐕𝐀𝐋𝐈𝐃 𝐃𝐎𝐌𝐀𝐈𝐍         ║\n"
                    "╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
                    "║  𝐎𝐧𝐥𝐲 : @hi2.in , @telegmail.com  ║\n"
                    f"║  𝐘𝐨𝐮𝐫 : @{domain}                 \n"
                    "╚═══━━━───〔 ✦ 〕───━━━═══╝"
                )
            )
            return

        chosen_domain = domain
        chosen_user = parts[0]
    else:
        
        chosen_user = username
        domains_to_check = ["hi2.in", "telegmail.com"]

        
        status_msg = f"<b>🔎 Checking availability for <code>{username}</code>...</b>"
        send_message(chat_id, status_msg)

        results = []
        for dom in domains_to_check:
            email = f"{chosen_user}@{dom}"

            
            send_message(chat_id, f"〔 ✦ 〕 𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠 <code>{email}</code> 〔 ✦ 〕")

            availability = check_email_availability(email, dom)

            if availability == "taken":
                results.append(f"〔 ✗ 〕 <code>{email}</code> → 𝐓𝐀𝐊𝐄𝐍")
            elif availability == "not_taken":
                results.append(f"〔 ✓ 〕 <code>{email}</code> → 𝐍𝐎𝐓 𝐓𝐀𝐊𝐄𝐍")
            elif availability == "unknown":
                results.append(f"〔 ! 〕 <code>{email}</code> → 𝐔𝐍𝐊𝐍𝐎𝐖𝐍")
            else:
                results.append(f"〔 × 〕 <code>{email}</code> → 𝐄𝐑𝐑𝐎𝐑")

            time.sleep(1)  

        
        final_msg = (
            "╔═══━━━───〔 ✦ 〕───━━━═══╗\n"
            "║        𝐀𝐕𝐀𝐈𝐋𝐀𝐁𝐈𝐋𝐈𝐓𝐘 𝐑𝐄𝐏𝐎𝐑𝐓        ║\n"
            "╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
            f"║  𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞 : {chosen_user}              \n"
            "╠═══━━━───〔 ✦ 〕───━━━═══╣\n" +
            "\n".join(f"║  {line}" for line in results) + "\n"
            "╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
            "║  𝐉𝐨𝐢𝐧 : @greatemperorrr                 ║\n"
            "╚═══━━━───〔 ✦ 〕───━━━═══╝"
        )
        keyboard = {
            "inline_keyboard": [
                [{"text": "📢 𝐉𝐨𝐢𝐧 𝐂𝐡𝐚𝐧𝐧𝐞𝐥", "url": "https://t.me/greatemperorrr"}]
            ]
        }
        send_message(chat_id, final_msg, reply_markup=keyboard)
        return

    email = f"{chosen_user}@{chosen_domain}"

    send_message(chat_id, f"〔 ✦ 〕 𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠 <code>{email}</code> 〔 ✦ 〕")

    availability = check_email_availability(email, chosen_domain)

    if availability == "taken":
        result_text = "〔 ✗ 〕 𝐓𝐀𝐊𝐄𝐍"
    elif availability == "not_taken":
        result_text = "〔 ✓ 〕 𝐍𝐎𝐓 𝐓𝐀𝐊𝐄𝐍"
    elif availability == "unknown":
        result_text = "〔 ! 〕 𝐔𝐍𝐊𝐍𝐎𝐖𝐍 (Error Checking)"
    else:
        result_text = "〔 × 〕 𝐄𝐑𝐑𝐎𝐑"

    final_msg = (
        f"╔═══━━━───〔 ✦ 〕───━━━═══╗\n"
        f"║        𝐀𝐕𝐀𝐈𝐋𝐀𝐁𝐈𝐋𝐈𝐓𝐘 𝐑𝐄𝐏𝐎𝐑𝐓        ║\n"
        f"╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
        f"║  𝐄𝐦𝐚𝐢𝐥   : {email}\n"
        f"║  𝐃𝐨𝐦𝐚𝐢𝐧  : @{chosen_domain}\n"
        f"║  𝐒𝐭𝐚𝐭𝐮𝐬  : {result_text}\n"
        f"╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
        f"║  𝐉𝐨𝐢𝐧 : @greatemperorrr                 ║\n"
        f"╚═══━━━───〔 ✦ 〕───━━━═══╝"
    )
    keyboard = {
        "inline_keyboard": [
            [{"text": "📢 𝐉𝐨𝐢𝐧 𝐂𝐡𝐚𝐧𝐧𝐞𝐥", "url": "https://t.me/greatemperorrr"}]
        ]
    }
    send_message(chat_id, final_msg, reply_markup=keyboard)

def process_bulk_check(chat_id, text):
    
    
    raw_emails = text.strip().split()
    emails = [e.strip().lower() for e in raw_emails if e.strip()]

    
    valid_emails = []
    invalid_entries = []
    for entry in emails:
        if "@" in entry:
            parts = entry.split("@")
            domain = parts[1].lower()
            if domain in ["hi2.in", "telegmail.com"]:
                valid_emails.append(entry)
            else:
                invalid_entries.append(f"{entry} (invalid domain)")
        else:
            invalid_entries.append(f"{entry} (missing @)")

    if not valid_emails:
        send_message(
            chat_id,
            "╔═══━━━───〔 ✦ 〕───━━━═══╗\n"
            "║    𝐍𝐎 𝐕𝐀𝐋𝐈𝐃 𝐄𝐌𝐀𝐈𝐋𝐒 𝐅𝐎𝐔𝐍𝐃      ║\n"
            "╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
            "║  𝐔𝐬𝐞 𝐟𝐨𝐫𝐦𝐚𝐭:                   ║\n"
            "║  user1@hi2.in user2@telegmail.com ║\n"
            "╚═══━━━───〔 ✦ 〕───━━━═══╝"
        )
        return

    
    start_msg = (
        f"╔═══━━━───〔 ✦ 〕───━━━═══╗\n"
        f"║     𝐁𝐔𝐋𝐊 𝐂𝐇𝐄𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃        ║\n"
        f"╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
        f"║  𝐓𝐨𝐭𝐚𝐥 : {len(valid_emails)} 𝐞𝐦𝐚𝐢𝐥(𝐬)        ║\n"
        f"╚═══━━━───〔 ✦ 〕───━━━═══╝"
    )
    send_message(chat_id, start_msg)

    results = []
    processed = 0

    for email in valid_emails:
        domain = email.split("@")[1].lower()
        parts = email.split("@")
        chosen_user = parts[0]
        chosen_domain = parts[1].lower()

        
        send_message(chat_id, f"〔 {processed+1}/{len(valid_emails)} 〕 𝐂𝐡𝐞𝐜𝐤𝐢𝐧𝐠 <code>{email}</code>")

        availability = check_email_availability(email, chosen_domain)

        if availability == "taken":
            results.append(f"〔 ✗ 〕 <code>{email}</code> → 𝐓𝐀𝐊𝐄𝐍")
        elif availability == "not_taken":
            results.append(f"〔 ✓ 〕 <code>{email}</code> → 𝐍𝐎𝐓 𝐓𝐀𝐊𝐄𝐍")
        elif availability == "unknown":
            results.append(f"〔 ! 〕 <code>{email}</code> → 𝐔𝐍𝐊𝐍𝐎𝐖𝐍")
        else:
            results.append(f"〔 × 〕 <code>{email}</code> → 𝐄𝐑𝐑𝐎𝐑")

        processed += 1
        time.sleep(1)  

    
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"║  {i}. {r}")

    final_msg = (
        "╔═══━━━───〔 ✦ 〕───━━━═══╗\n"
        "║     𝐁𝐔𝐋𝐊 𝐀𝐕𝐀𝐈𝐋𝐀𝐁𝐈𝐋𝐈𝐓𝐘 𝐑𝐄𝐏𝐎𝐑𝐓     ║\n"
        "╠═══━━━───〔 ✦ 〕───━━━═══╣\n" +
        "\n".join(lines) + "\n"
        "╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
        f"║  𝐓𝐨𝐭𝐚𝐥 : {len(valid_emails)} 𝐜𝐡𝐞𝐜𝐤𝐞𝐝                ║\n"
        "║  𝐉𝐨𝐢𝐧 : @greatemperorrr                 ║\n"
        "╚═══━━━───〔 ✦ 〕───━━━═══╝"
    )
    keyboard = {
        "inline_keyboard": [
            [{"text": "📢 𝐉𝐨𝐢𝐧 𝐂𝐡𝐚𝐧𝐧𝐞𝐥", "url": "https://t.me/greatemperorrr"}]
        ]
    }
    send_message(chat_id, final_msg, reply_markup=keyboard)

    
    if invalid_entries:
        inv_msg = (
            "╔═══━━━───〔 ✦ 〕───━━━═══╗\n"
            "║     𝐈𝐍𝐕𝐀𝐋𝐈𝐃 𝐄𝐍𝐓𝐑𝐈𝐄𝐒 𝐒𝐊𝐈𝐏𝐏𝐄𝐃    ║\n"
            "╠═══━━━───〔 ✦ 〕───━━━═══╣\n" +
            "\n".join(f"║  • {e}" for e in invalid_entries) + "\n"
            "╚═══━━━───〔 ✦ 〕───━━━═══╝"
        )
        send_message(chat_id, inv_msg)


def run_bot():
    print(
        "╔═══━━━───〔 ✦ 〕───━━━═══╗\n"
        "║        𝐁𝐎𝐓 𝐒𝐓𝐀𝐑𝐓𝐄𝐃        ║\n"
        "╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
        "║   ✓ 𝐋𝐢𝐬𝐭𝐞𝐧𝐢𝐧𝐠 𝐟𝐨𝐫 𝐦𝐞𝐬𝐬𝐚𝐠𝐞𝐬   ║\n"
        "╚═══━━━───〔 ✦ 〕───━━━═══╝"
    )

    last_update_id = 0
    
    user_modes = {}  

    
    bot_messages = {}

    while True:
        try:
            updates = get_updates(offset=last_update_id + 1)

            for update in updates:
                update_id = update.get("update_id")
                if update_id and update_id >= last_update_id:
                    last_update_id = update_id

                
                if "callback_query" in update:
                    cq = update["callback_query"]
                    chat_id = cq["message"]["chat"]["id"]
                    message_id = cq["message"]["message_id"]
                    callback_data = cq.get("data", "")
                    callback_id = cq["id"]

                    
                    answer_callback(update_id, callback_id)

                    if callback_data == "mode_single":
                        user_modes[chat_id] = "single"
                        send_single_mode_prompt(chat_id, message_id)

                    elif callback_data == "mode_bulk":
                        user_modes[chat_id] = "bulk"
                        send_bulk_mode_prompt(chat_id, message_id)

                    elif callback_data == "back_menu":
                        user_modes[chat_id] = None
                        
                        msg = (
                            "╔═══━━━───〔 ✦ 〕───━━━═══╗\n"
                            "║   𝐇𝐈2 & 𝐓𝐄𝐋𝐄𝐆𝐌𝐀𝐈𝐋 𝐂𝐇𝐄𝐂𝐊𝐄𝐑   ║\n"
                            "╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
                            "║       𝐒𝐄𝐋𝐄𝐂𝐓 𝐌𝐎𝐃𝐄 𝐁𝐄𝐋𝐎𝐖       ║\n"
                            "╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
                            "║  【1】 𝐒𝐢𝐧𝐠𝐥𝐞 𝐂𝐡𝐞𝐜𝐤         ║\n"
                            "║  → 𝐂𝐡𝐞𝐜𝐤 𝟏 𝐮𝐬𝐞𝐫𝐧𝐚𝐦𝐞/𝐞𝐦𝐚𝐢𝐥     ║\n"
                            "║                              ║\n"
                            "║  【2】 𝐁𝐮𝐥𝐤 𝐂𝐡𝐞𝐜𝐤           ║\n"
                            "║  → 𝐂𝐡𝐞𝐜𝐤 𝐦𝐮𝐥𝐭𝐢𝐩𝐥𝐞 𝐞𝐦𝐚𝐢𝐥𝐬    ║\n"
                            "║  → 𝐅𝐨𝐫𝐦𝐚𝐭: mail1 mail2    ║\n"
                            "╠═══━━━───〔 ✦ 〕───━━━═══╣\n"
                            "║  𝐅𝐨𝐥𝐥𝐨𝐰 𝐨𝐮𝐫 𝐜𝐡𝐚𝐧𝐧𝐞𝐥 𝐛𝐞𝐥𝐨𝐰    ║\n"
                            "╚═══━━━───〔 ✦ 〕───━━━═══╝"
                        )
                        keyboard = {
                            "inline_keyboard": [
                                [
                                    {"text": "🔹 𝐒𝐢𝐧𝐠𝐥𝐞 𝐌𝐨𝐝𝐞", "callback_data": "mode_single"},
                                    {"text": "🔸 𝐁𝐮𝐥𝐤 𝐌𝐨𝐝𝐞", "callback_data": "mode_bulk"}
                                ],
                                [
                                    {"text": "📢 𝐉𝐨𝐢𝐧 𝐂𝐡𝐚𝐧𝐧𝐞𝐥", "url": "https://t.me/greatemperorrr"}
                                ]
                            ]
                        }
                        edit_message(chat_id, message_id, msg, reply_markup=keyboard)

                
                elif "message" in update:
                    msg = update["message"]
                    chat_id = msg["chat"]["id"]
                    text = msg.get("text", "")

                   
                    if text == "/start":
                        user_modes[chat_id] = None
                        send_welcome(chat_id)

                    
                    elif text == "/help":
                        send_welcome(chat_id)

                    
                    elif text and not text.startswith("/"):
                        current_mode = user_modes.get(chat_id)

                        if current_mode is None:
                            
                            send_welcome(chat_id)
                        elif current_mode == "single":
                            process_single_check(chat_id, text)
                        elif current_mode == "bulk":
                            process_bulk_check(chat_id, text)

            time.sleep(1)

        except KeyboardInterrupt:
            print(f"\n{fg_red}{bold}[!] Bot shutting down...{reset}")
            
            for cid in list(user_modes.keys()):
                send_message(cid, "🔴 Bot is shutting down. Goodbye!")
            break
        except Exception as e:
            print(f"{fg_red}{bold}[!] Error: {e}{reset}")
            time.sleep(5)


if __name__ == "__main__":
    
    os.system('cls' if os.name == 'nt' else 'clear')

    
    banner = f"""
{fg_lavender}╔═✦═✦═〔 𝐁𝐎𝐓 𝐒𝐓𝐀𝐓𝐔𝐒 〕═✦═✦═╗{reset}
{fg_lavender}║{reset}
{fg_lavender}║{reset}  {fg_cyan}⌁ 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 ➜{reset} {fg_magenta}@greatemperorrr{reset}
{fg_lavender}║{reset}  {fg_cyan}⌁ 𝐃𝐄𝐕 ➜{reset} {fg_magenta}@CHAMMMAK_CHALLO{reset}
{fg_lavender}║{reset}
{fg_lavender}║{reset}  {fg_gold}⌁ 𝐁𝐎𝐓 𝐈𝐒{reset} {fg_green}𝐑𝐔𝐍𝐍𝐈𝐍𝐆{reset}
{fg_lavender}║{reset}
{fg_lavender}╚═✦═✦═✦═✦═✦═✦═✦═✦═✦═╝{reset}
"""
    print(banner)

    run_bot()
