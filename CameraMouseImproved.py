import cv2
import pyautogui
import time
from pynput import mouse, keyboard

# Global flag to track user activity
user_active = False
#turns off automatic killing of the process when the user moves the mouse to the corner
pyautogui.FAILSAFE = False

# Callback function for mouse activity
def on_mouse_move(x, y):
    global user_active
    user_active = True

# Callback function for keyboard activity
def on_key_press(key):
    global user_active
    user_active = True

# Start listening for user input
mouse_listener = mouse.Listener(on_move=on_mouse_move)
keyboard_listener = keyboard.Listener(on_press=on_key_press)
mouse_listener.start()
keyboard_listener.start()

def detect_motion():
    cap = cv2.VideoCapture(0) # Open webcam
    _, prev_frame = cap.read()
    prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    global user_active

    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_frame, gray)
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        motion_detected = cv2.countNonZero(thresh) > 10000 # Adjust sensitivity

        if motion_detected and not user_active:
            # Move the mouse slightly
            pyautogui.moveRel(1, 0, duration=0.1)
            pyautogui.moveRel(-1, 0, duration=0.1)

            # Click at the current mouse position
            x, y = pyautogui.position()
            pyautogui.click(x=x,y=y)

            print("Motion detected! Mouse moved and clicked.")
        else:
            print("User is active or no motion detected.")

        prev_frame = gray
        user_active = False # Reset user activity flag after each cycle
        time.sleep(1)

if __name__ == "__main__":
    detect_motion()