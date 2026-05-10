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

### Prerequisites
- Windows Operating System
- Python 3.13 or higher
- Telegram Bot Token (create via @BotFather)

### Clone Repository

```bash
git clone https://github.com/s-r-e-e-r-a-j/ShadowRAT.git
```
### Navigate to the ShadowRAT directory 
```
cd ShadowRAT
```
