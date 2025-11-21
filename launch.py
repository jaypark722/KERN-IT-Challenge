#!/usr/bin/env python3
"""
Time Keeper Application Launcher
Starts both backend and frontend servers automatically
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def check_requirements():
    """Check if Python and Node.js are installed"""
    print_header("Checking Requirements")
    
    # Check Python
    try:
        python_version = sys.version.split()[0]
        print_success(f"Python {python_version} found")
    except Exception as e:
        print_error(f"Python check failed: {e}")
        return False
    
    # Check Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"Node.js {result.stdout.strip()} found")
        else:
            print_error("Node.js not found. Please install Node.js from https://nodejs.org/")
            return False
    except FileNotFoundError:
        print_error("Node.js not found. Please install Node.js from https://nodejs.org/")
        return False
    
    return True

def check_backend_setup():
    """Check if backend virtual environment exists"""
    backend_dir = Path(__file__).parent / "backend"
    venv_dir = backend_dir / "venv"
    
    if not venv_dir.exists():
        print_warning("Backend virtual environment not found")
        print_info("Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
            print_success("Virtual environment created")
        except subprocess.CalledProcessError as e:
            print_error(f"Failed to create virtual environment: {e}")
            return False
    
    return True

def start_backend():
    """Start the Flask backend server"""
    print_header("Starting Backend Server")
    
    backend_dir = Path(__file__).parent / "backend"
    venv_dir = backend_dir / "venv"
    
    # Determine Python executable in venv
    if sys.platform == "win32":
        python_exe = venv_dir / "Scripts" / "python.exe"
    else:
        python_exe = venv_dir / "bin" / "python"
    
    if not python_exe.exists():
        print_error(f"Python executable not found at {python_exe}")
        return None
    
    # Start backend process
    try:
        print_info("Launching Flask server on http://127.0.0.1:5000")
        process = subprocess.Popen(
            [str(python_exe), "run.py"],
            cwd=str(backend_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
        )
        
        # Wait a moment for server to start
        time.sleep(3)
        
        if process.poll() is None:
            print_success("Backend server started successfully")
            return process
        else:
            print_error("Backend server failed to start")
            return None
            
    except Exception as e:
        print_error(f"Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the React frontend server"""
    print_header("Starting Frontend Server")
    
    frontend_dir = Path(__file__).parent / "frontend"
    
    # Check if node_modules exists
    node_modules = frontend_dir / "node_modules"
    if not node_modules.exists():
        print_warning("Node modules not found. Installing dependencies...")
        print_info("This may take a few minutes...")
        try:
            # On Windows, npm is a shell wrapper named npm.cmd; ensure we call the right executable
            npm_exe = "npm"
            if sys.platform == "win32" or os.name == "nt":
                npm_exe = "npm.cmd"

            subprocess.run(
                [npm_exe, "install"],
                cwd=str(frontend_dir),
                check=True
            )
            print_success("Dependencies installed")
        except subprocess.CalledProcessError as e:
            print_error(f"Failed to install dependencies: {e}\nSee the full output above for details.")
            return None
    
    # Start frontend process
    try:
        print_info("Launching React dev server on http://localhost:3000")
        
        # Set environment variable to prevent browser from auto-opening
        env = os.environ.copy()
        env['BROWSER'] = 'none'
        
        # Use the Windows npm wrapper when on Windows so subprocess can find it
        npm_start = "npm start"
        popen_args = ["npm", "start"]
        if sys.platform == "win32" or os.name == "nt":
            popen_args = ["npm.cmd", "start"]

        process = subprocess.Popen(
            popen_args,
            cwd=str(frontend_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=env,
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
        )
        
        # Wait for server to start
        print_info("Waiting for frontend server to compile...")
        time.sleep(8)
        
        if process.poll() is None:
            print_success("Frontend server started successfully")
            return process
        else:
            print_error("Frontend server failed to start")
            return None
            
    except Exception as e:
        print_error(f"Failed to start frontend: {e}")
        return None

def main():
    """Main launcher function"""
    print_header("🚀 Time Keeper Application Launcher")
    
    # Check requirements
    if not check_requirements():
        print_error("Requirements check failed. Please install missing software.")
        input("\nPress Enter to exit...")
        return 1
    
    # Check backend setup
    if not check_backend_setup():
        print_error("Backend setup failed.")
        input("\nPress Enter to exit...")
        return 1
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print_error("Failed to start backend server.")
        input("\nPress Enter to exit...")
        return 1
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print_error("Failed to start frontend server.")
        if backend_process:
            backend_process.terminate()
        input("\nPress Enter to exit...")
        return 1
    
    # Success!
    print_header("✅ Application Started Successfully!")
    print_info("Backend:  http://127.0.0.1:5000")
    print_info("Frontend: http://localhost:3000")
    print()
    print_success("Opening browser...")
    
    # Open browser
    time.sleep(2)
    try:
        webbrowser.open('http://localhost:3000')
    except:
        print_warning("Could not open browser automatically")
        print_info("Please manually open: http://localhost:3000")
    
    print()
    print(f"{Colors.BOLD}Both servers are running in separate windows.{Colors.ENDC}")
    print(f"{Colors.WARNING}To stop the application, close both terminal windows.{Colors.ENDC}")
    print()
    
    input("Press Enter to exit this launcher (servers will continue running)...")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nLauncher interrupted by user.")
        sys.exit(0)
