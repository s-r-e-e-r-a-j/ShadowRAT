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

### System Control
- Remote shutdown, restart, sleep, hibernate, lock, logoff
- Input blocking/unblocking
- Task Manager enable/disable
- Windows startup persistence (manual and automatic)
- Alt+F4 simulation
- CMD flood (10 windows)

### Persistence
- Automatic registry-based persistence (/persistence)
- Remove persistence (/nopersistence)

### Keylogger
- Real-time keystroke logging
- Captures all keyboard input including special keys
- Automatic log buffering and saving
- Screenshot capture on each key press (/keylogscreenshot)

### Surveillance
- Live screenshot capture
- Screen recording (customizable duration)
- Webcam photo capture
- Webcam video recording (customizable duration)
- Microphone audio recording

### Advanced Monitoring
- Clipboard monitoring (real-time with logging)
- USB device monitoring (insertion/removal tracking)
- Network connection monitoring (high activity alerts)

### Information Gathering
- Wi-Fi network list and password extraction
- Complete system information (CPU, RAM, disk, battery, uptime)
- Process list with CPU/RAM usage
- Kill process by name or PID
- User account enumeration
- Installed applications list
- Battery status
- IP address and geolocation
- Active network connections

### File Operations
- Directory browsing and navigation
- Upload files to target machine (via Telegram)
- Download files from target machine
- Download files from internet directly
- Execute files remotely
- Create/extract zip archives
- Delete, rename, create, remove files/folders
- Global file search on C drive
- File metadata viewing

### Remote Command Execution
- Single command execution with output
- Batch command execution with long output as file
- Interactive shell session with history
- Directory navigation (cd, cd..)

### Input Simulation
- Keyboard typing simulation
- Single, dual, and triple keypress combinations
- Mouse movement to coordinates
- Mouse left/right click
- Random mouse movement (Mouse Mess)

### Browser Control
- Open URLs in Chrome
- Open URLs in Edge
- Open URLs in Firefox

### Audio/Visual
- Text-to-speech (/textspeech)
- Text-to-speech alias (/say)
- Sound file playback
- Volume control (max, +10, -10, set specific level, mute, unmute)

### Window Management
- Maximize active window
- Minimize active window

### Clipboard
- Read clipboard contents
- Write to clipboard
- Real-time clipboard monitoring

### Security & Passwords
- Chrome saved passwords extraction
- Wi-Fi password extraction

### Messaging
- Custom message box with types (info, warning, error, question)
- Windows native notifications

### Scheduling
- Schedule commands for future execution (seconds-based)
- List scheduled tasks
- Clear all scheduled tasks

### Obfuscation
- Hide script file (Windows hidden attribute)
- Unhide script file

### Wallpaper
- Change desktop wallpaper remotely

### Information
- IP address and geolocation
- System uptime
- Basic and detailed system info

---

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
pip install pyautogui opencv-python pyttsx3 numpy pynput requests pytelegrambotapi pillow pyaudio 
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

### Run the ShadowRAT (Two Ways)

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

---

## Bot Commands

### How to Use

1. Open Telegram and search for your bot username (example: `@ShadowRAT_bot`)
  
2. Send `/start` to the bot

3. Bot asks for password - send `1234567B` (or your custom password)
  
4. Bot replies: `SHADOW RAT Activated` and shows victim info

5. Send any command from the list below

## Authentication
| Command | Description |
|---------|-------------|
| `/start` | Connect to RAT with password |
| `/help` | Show this help menu |

## System Control
| Command | Description |
|---------|-------------|
| `/addstartup` | Add to Windows startup (manual path) |
| `/deletestartup` | Remove from Windows startup |
| `/persistence` | Enable auto-start on boot (automatic) |
| `/nopersistence` | Disable auto-start on boot |
| `/hide` | Hide script file |
| `/unhide` | Unhide script file |
| `/run [path]` | Run a file |
| `/sleep` | Put computer to sleep |
| `/shutdown` | Shutdown computer |
| `/restart` | Restart computer |
| `/lockpc` | Lock computer screen |
| `/logoff` | Log off current user |
| `/hibernate` | Hibernate computer |
| `/altf4` | Send Alt+F4 command |
| `/cmdbomb` | Open 10 CMD windows |
| `/block` | Block keyboard and mouse input |
| `/unblock` | Unblock keyboard and mouse input |
| `/disabletaskmgr` | Disable Task Manager |
| `/enabletaskmgr` | Enable Task Manager |

## System Information
| Command | Description |
|---------|-------------|
| `/info` | Get IP address and geolocation |
| `/pcinfo` | Detailed system information |
| `/shortinfo` | Basic system information (user, PC, OS) |
| `/sysinfo` | Complete system information (CPU, RAM, disk, battery) |
| `/uptime` | Show system uptime |
| `/users` | Show all PC users |
| `/whoami` | Show current username |
| `/apps` | Show installed applications |
| `/batteryinfo` | Show battery status |

## File Management
| Command | Description |
|---------|-------------|
| `/files` | List files in current directory |
| `/cd [path]` | Change current directory |
| `/delete [path]` | Delete file or folder |
| `/rename [old] [new]` | Rename file or folder |
| `/mkdir [name]` | Create new directory |
| `/rmdir [name]` | Remove empty directory |
| `/search [name]` | Search files on C drive |
| `/download [path]` | Download file from victim |
| `/upload` | Upload file to victim (send via Telegram) |
| `/downloadurl [url] [name]` | Download file from internet |
| `/uploadfile [path]` | Upload any file to Telegram |
| `/metadata [path]` | Show file metadata |
| `/zip [folder]` | Create zip archive |
| `/unzip [file]` | Extract zip archive |

## Process Management
| Command | Description |
|---------|-------------|
| `/tasklist` | Show running processes |
| `/taskkill [name]` | Kill process by name |
| `/processes` | Detailed process list with CPU/RAM usage |
| `/killpid [pid]` | Kill process by ID |

## Keylogger
| Command | Description |
|---------|-------------|
| `/keylogstart` | Start keylogger |
| `/keylogstop` | Stop keylogger |
| `/keylogdump` | Download keylog file |
| `/keylogscreenshot` | Take screenshot on each key press |

## Surveillance
| Command | Description |
|---------|-------------|
| `/screenshot` | Take screenshot |
| `/screenrecord [sec]` | Record screen (default 10 sec) |
| `/mic [sec]` | Record microphone (default 5 sec) |
| `/webscreen` | Take webcam photo |
| `/webcam [sec]` | Record webcam video (default 5 sec) |

## Monitoring
| Command | Description |
|---------|-------------|
| `/clipboard` | Show current clipboard contents |
| `/changeclipboard [text]` | Change clipboard contents |
| `/clipmonstart` | Start clipboard monitoring |
| `/clipmonstop` | Stop clipboard monitoring |
| `/usbmonitorstart` | Monitor USB device insertion/removal |
| `/usbmonitorstop` | Stop USB monitoring |
| `/networkmonitorstart` | Monitor network connections |
| `/networkmonitorstop` | Stop network monitoring |
| `/netstat` | Show active network connections |

## Network & Wi-Fi
| Command | Description |
|---------|-------------|
| `/wifilist` | Show saved Wi-Fi networks |
| `/wifipass [name]` | Show Wi-Fi password |
| `/passwords` | Extract saved browser passwords (Chrome) |
| `/chrome [url]` | Open URL in Chrome |
| `/edge [url]` | Open URL in Edge |
| `/firefox [url]` | Open URL in Firefox |

## Input Control
| Command | Description |
|---------|-------------|
| `/keytype [text]` | Type text |
| `/keypress [key]` | Press a single key |
| `/keypresstwo [k1] [k2]` | Press two keys together |
| `/keypressthree [k1] [k2] [k3]` | Press three keys together |
| `/mousemove [x] [y]` | Move mouse to coordinates |
| `/mouseclick` | Left click at current position |
| `/mouseright` | Right click at current position |
| `/mousemesstart` | Start random mouse movement |
| `/mousemesstop` | Stop random mouse movement |

## Audio Control
| Command | Description |
|---------|-------------|
| `/fullvolume` | Set volume to maximum |
| `/volumeplus` | Increase volume by 10% |
| `/volumeminus` | Decrease volume by 10% |
| `/volume [0-100]` | Set specific volume level |
| `/mute` | Mute system audio |
| `/unmute` | Unmute system audio |
| `/textspeech [text]` | Convert text to speech |
| `/say [text]` | Text to speech (alias) |
| `/playsound [path]` | Play audio file |

## Window Control
| Command | Description |
|---------|-------------|
| `/maximize` | Maximize active window |
| `/minimize` | Minimize active window |

## Command Execution
| Command | Description |
|---------|-------------|
| `/e [cmd]` | Execute command (short output) |
| `/ex [cmd]` | Execute command (long output as file) |
| `/execute` | Start interactive shell session |

## Messaging
| Command | Description |
|---------|-------------|
| `/msg [type] [title] [text]` | Show message box (types: info, warning, error, question) |
| `/notify [title] [text]` | Show Windows notification |

## Scheduling
| Command | Description |
|---------|-------------|
| `/schedule [seconds] [command]` | Schedule command execution |
| `/listschedules` | List scheduled tasks |
| `/clearschedules` | Clear all scheduled tasks |

## Obfuscation
| Command | Description |
|---------|-------------|
| `/hide` | Hide script file |
| `/unhide` | Unhide script file |

## Other
| Command | Description |
|---------|-------------|
| `/wallpaper` | Change desktop wallpaper (use with /upload first) |

---

## Command Categories Summary

| Category | Number of Commands |
|----------|-------------------|
| Authentication | 2 |
| System Control | 19 |
| System Information | 10 |
| File Management | 14 |
| Process Management | 4 |
| Keylogger | 4 |
| Surveillance | 6 |
| Monitoring | 9 |
| Network & Wi-Fi | 7 |
| Input Control | 9 |
| Audio Control | 9 |
| Window Control | 2 |
| Command Execution | 3 |
| Messaging | 2 |
| Scheduling | 3 |
| Obfuscation | 2 |
| Other | 1 |
| **TOTAL** | **106** |

---

## Quick Reference - Most Used Commands

| Purpose | Command |
|---------|---------|
| Get victim info | `/shortinfo` or `/sysinfo` |
| Browse files | `/files` then `/cd [folder]` |
| Download file | `/download [path]` |
| Upload file | `/upload` then send file |
| Execute command | `/e [command]` |
| Take screenshot | `/screenshot` |
| Start keylogger | `/keylogstart` |
| Get Wi-Fi password | `/wifipass [name]` |
| Lock computer | `/lockpc` |
| Shutdown | `/shutdown` |

---

## License

**Custom Educational and Research License**

Copyright © 2026 Sreeraj S Kurup. All rights reserved.
