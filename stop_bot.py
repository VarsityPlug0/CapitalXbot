#!/usr/bin/env python3
"""
Script to stop any running bot instances
"""

import os
import signal
import psutil
import sys

def kill_python_processes():
    """Kill all Python processes except this script"""
    current_pid = os.getpid()
    killed_count = 0
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Check if it's a Python process
            if proc.info['name'] == 'python.exe' or proc.info['name'] == 'python':
                # Skip this script's process
                if proc.info['pid'] != current_pid:
                    # Check if it's running our bot files
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if 'beginner_main.py' in cmdline or 'main.py' in cmdline:
                        print(f"Terminating Python process {proc.info['pid']}: {cmdline}")
                        proc.kill()
                        killed_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return killed_count

if __name__ == '__main__':
    print("Stopping any running bot instances...")
    count = kill_python_processes()
    print(f"Stopped {count} bot process(es)")