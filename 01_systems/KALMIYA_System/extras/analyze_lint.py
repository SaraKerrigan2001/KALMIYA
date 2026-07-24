"""Utility to analyze a pylint JSON report and display summary."""
import json

def analyze_pylint():
    """Read pylint_report.json and print error/warning summary."""
    try:
        # Intentar leer con utf-16le como falló antes
        try:
            with open('pylint_report.json', 'r', encoding='utf-16') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Failed to read with utf-16: {e}")
            with open('pylint_report.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        errors = [m for m in data if m['type'] in ['error', 'fatal']]
        warnings = [m for m in data if m['type'] == 'warning']
        
        print(f"Total Errors: {len(errors)}")
        print(f"Total Warnings: {len(warnings)}")
        
        print("\n--- TOP ERRORS ---")
        for e in errors[:10]:
            print(f"{e['path']}:{e['line']} - {e['symbol']} - {e['message']}")
            
        print("\n--- TOP WARNINGS ---")
        for w in warnings[:10]:
            print(f"{w['path']}:{w['line']} - {w['symbol']} - {w['message']}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_pylint()
