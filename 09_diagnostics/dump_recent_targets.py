import os
from pathlib import Path

# We can resolve shortcuts using Python's win32com if pywin32 is installed, 
# or by reading the binary LNK format. Since we are on Windows, we can use 
# PowerShell via subprocess to resolve them, which is extremely robust.

recent_dir = Path(r"C:\Users\maria\AppData\Roaming\Microsoft\Windows\Recent")

def get_lnk_targets():
    print(f"Reading shortcuts from {recent_dir}...")
    if not recent_dir.exists():
        print("Recent directory does not exist.")
        return
        
    import subprocess
    
    lnks = list(recent_dir.glob("*.lnk"))
    print(f"Found {len(lnks)} shortcuts.")
    
    script_parts = []
    for i, lnk in enumerate(lnks[:100]): # Limit to first 100 to avoid buffer overflow
        lnk_path_escaped = str(lnk).replace("'", "''")
        script_parts.append(
            f"try {{ "
            f"  $s = (New-Object -COM WScript.Shell).CreateShortcut('{lnk_path_escaped}'); "
            f"  Write-Output ('{i}|||' + '{lnk.name}'.Replace('|||', '') + '|||' + $s.TargetPath) "
            f"}} catch {{}}"
        )
        
    full_script = "\n".join(script_parts)
    
    # Run powershell
    res = subprocess.run(
        ["powershell", "-NoProfile", "-Command", full_script],
        capture_output=True, text=True, encoding="cp1252", errors="replace", timeout=30
    )
    
    if res.stdout:
        lines = res.stdout.strip().split('\n')
        resolved = []
        for line in lines:
            if '|||' in line:
                parts = line.split('|||')
                if len(parts) >= 3:
                    resolved.append((parts[1], parts[2]))
    else:
        resolved = []
                
    # Sort and print
    print("\nResolved Targets:")
    for name, target in sorted(resolved):
        print(f"{name} -> {target}")

if __name__ == "__main__":
    get_lnk_targets()
