from brain import ask_kalmiya
import os

def test_brain():
    print("Testing KALMIYA Brain...")
    try:
        response = ask_kalmiya("Hola KALMIYA, ¿estás operativa?")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_brain()
