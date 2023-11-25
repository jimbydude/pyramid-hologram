import subprocess
import threading
import os
import time
import RPi.GPIO as GPIO

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Set up GPIO2 as an input, pulled down to avoid false detection
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def turn_on_display():
    """Turn on the display by setting maximum brightness."""
    try:
        subprocess.run('echo 255 | sudo tee /sys/class/backlight/10-0045/brightness', shell=True, check=True)
        print("Display turned on.")
    except subprocess.CalledProcessError:
        print("Error turning on the display.")

def turn_off_display():
    """Turn off the display by setting brightness to zero."""
    try:
        subprocess.run('echo 0 | sudo tee /sys/class/backlight/10-0045/brightness', shell=True, check=True)
        print("Display turned off.")
    except subprocess.CalledProcessError:
        print("Error turning off the display.")

def check_button():
    """
    Check if the button connected to GPIO2 is pressed.
    Returns True if pressed, False otherwise.
    """
    return GPIO.input(2) == GPIO.LOW

def set_stop_flag():
    with open("/home/roseann/scripts/flag", "w") as f:
        f.write("stop")
    print("Stop signal sent to NeoPixel script.")

# Function to check for a stop signal in a file
def check_for_stop():
    try:
        with open("/home/roseann/scripts/flag", "r") as f:
            return f.read().strip() == "stop"
    except FileNotFoundError:
        return False
    
def clear_stop_flag():
    try:
        with open("/home/roseann/scripts/flag", "w") as f:
            f.write("")  # Writing an empty string to reset the flag
        print("Stop flag reset.")
    except Exception as e:
        print(f"Error resetting stop flag: {e}")

# Modified run_video_script to use file-based approach
def run_video_script(video_file, loop):
    python_executable = '/home/roseann/scripts/hologram/bin/python'
    
    while True:
        # Start the video script
        subprocess.run([python_executable, "/home/roseann/scripts/play_video.py", video_file, loop])

        # Check for the stop signal
        if check_for_stop():
            break

        # Optional: sleep for a short time to prevent high CPU usage
        time.sleep(0.1)

def start_threads(video_file, loop, start_neopixel):
    turn_off_display()  # Blank the screen before starting
    clear_stop_flag()  # Reset the stop flag before starting NeoPixels
    
    threads = []
    video_thread = threading.Thread(target=run_video_script, args=(video_file, loop))
    threads.append(video_thread)
    print("Starting video thread...")
    video_thread.start()

    if start_neopixel:
        print("Starting NeoPixel process...")
        neopixel_process = subprocess.Popen(["sudo", "-E", "env", "PATH=" + os.environ['PATH'], "python3", "/home/roseann/scripts/adele_pixels.py"])
        
        # Thread to wait for the subprocess to complete
        def wait_for_process(proc):
            proc.wait()
            print("NeoPixel process completed.")

        neopixel_wait_thread = threading.Thread(target=wait_for_process, args=(neopixel_process,))
        threads.append(neopixel_wait_thread)
        neopixel_wait_thread.start()

    return threads

def waiting_on_threads(threads):
    print("Waiting to stop threads...")

    time.sleep(1)
    turn_on_display()  # Unblank the screen after starting

    # While at least one thread is alive, keep checking
    while any(thread.is_alive() for thread in threads):
        if check_button():
            print("Button pressed, breaking loop...")
            set_stop_flag()  # Set the stop flag
            turn_off_display()  # Blank the screen before starting
        time.sleep(0.1)  # Short sleep to prevent high CPU usage

    # Ensure all threads are joined
    for thread in threads:
        thread.join()

    time.sleep(2)  # Give the threads some time to stop
    clear_stop_flag()  # Reset the stop flag after all threads have stopped


if __name__ == "__main__":
    turn_off_display()  # Blank the screen before starting
    

    happy_birthday_video = "/home/roseann/Videos/happy_birthday.mp4"
    adele_video = "/home/roseann/Videos/Adele.mp4"
    wine_glass_video = "/home/roseann/Videos/wine_glass.mp4"

    threads = []  # Initialize threads outside the try block
    time.sleep(5)  # Wait for the screen to blank
    try:
        while True:
            # Start playing the default video without NeoPixels
            print("Starting default video...")
            threads = start_threads(happy_birthday_video, "loop", False)
            waiting_on_threads(threads)  # Stop the current threads

            # Start playing the special video with NeoPixels
            print("Starting special video...")
            threads = start_threads(adele_video, "no_loop", True)
            #input("Press Enter to return to the default video...")
            waiting_on_threads(threads)  # Stop the current threads

            # Start playing the wine glass video without NeoPixels
            print("Starting wine glass video...")
            threads = start_threads(wine_glass_video, "loop", False)
            waiting_on_threads(threads)

    finally:
        print("Exiting main...")
        waiting_on_threads(threads)  # Ensure all threads are stopped
        set_stop_flag()  # Ensure NeoPixels are signaled to stop
        GPIO.cleanup()  # Clean up GPIO on exit
        turn_off_display()  # Unblank the screen before exiting


