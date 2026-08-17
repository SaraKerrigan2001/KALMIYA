import os
import subprocess
import sys

def cleanup_kalmiya():
    print("Cleaning up KALMIYA processes...")
    try:
        # Get list of python processes with command line
        output = subprocess.check_output(['wmic', 'process', 'where', "name='python.exe'", 'get', 'commandline,processid'], text=True)
        lines = output.strip().split('\n')[1:]
        
        my_pid = os.getpid()
        
        for line in lines:
            if not line.strip(): continue
            parts = line.rsplit(None, 1)
            if len(parts) < 2: continue
            cmdline = parts[0].strip()
            pid = int(parts[1].strip())
            
            if pid == my_pid: continue
            
            if 'kalmiya' in cmdline.lower():
                print(f"Killing PID {pid}: {cmdline}")
                try:
                    subprocess.run(['taskkill', '/F', '/PID', str(pid)], capture_output=True)
                except Exception as e:
                    print(f"Failed to kill {pid}: {e}")
                    
    except Exception as e:
        print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    cleanup_kalmiya()
