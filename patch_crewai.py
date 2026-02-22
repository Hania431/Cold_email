"""Patch crewai to work on Windows by fixing Unix signal imports."""

import sys

def patch_system_events():
    """Patch the system_events.py file to handle missing Windows signals."""
    
    file_path = r"C:\Users\Abdul Mueed\AppData\Roaming\Python\Python312\site-packages\crewai\events\types\system_events.py"
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Replace the SignalType class
        old_class = '''class SignalType(IntEnum):
    """Enumeration of supported system signals."""

    SIGTERM = signal.SIGTERM
    SIGINT = signal.SIGINT
    SIGHUP = signal.SIGHUP
    SIGTSTP = signal.SIGTSTP
    SIGCONT = signal.SIGCONT'''
        
        new_class = '''class SignalType(IntEnum):
    """Enumeration of supported system signals."""

    SIGTERM = signal.SIGTERM
    SIGINT = signal.SIGINT
    SIGHUP = signal.SIGHUP if hasattr(signal, 'SIGHUP') else 1
    SIGTSTP = signal.SIGTSTP if hasattr(signal, 'SIGTSTP') else 20
    SIGCONT = signal.SIGCONT if hasattr(signal, 'SIGCONT') else 18'''
        
        if old_class in content:
            content = content.replace(old_class, new_class)
            with open(file_path, 'w') as f:
                f.write(content)
            print("✅ Successfully patched crewai for Windows compatibility!")
            return True
        else:
            print("⚠️ Could not find the exact pattern to patch. File may already be patched or different version.")
            return False
            
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        print("Make sure crewai is installed.")
        return False
    except Exception as e:
        print(f"❌ Error patching file: {e}")
        return False

if __name__ == "__main__":
    success = patch_system_events()
    sys.exit(0 if success else 1)
