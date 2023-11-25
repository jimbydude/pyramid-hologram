import time
import board
import neopixel
import random
import threading
import subprocess

# Configuration for Orchestra LEDs
ORCH_LED_PIN = board.D21
ORCH_NUM_PIXELS = 8
ORCH_BRIGHTNESS = 50 #percent

# Configuration for Fire LEDs
FIRE_LED_PIN = board.D12
FIRE_NUM_PIXELS = 5
FIRE_BRIGHTNESS = 50 # percent

# Initialize NeoPixel
fire_pixels = neopixel.NeoPixel(FIRE_LED_PIN, FIRE_NUM_PIXELS, brightness=FIRE_BRIGHTNESS, auto_write=False)
orch_pixels = neopixel.NeoPixel(ORCH_LED_PIN, ORCH_NUM_PIXELS, brightness=ORCH_BRIGHTNESS, auto_write=False)

# Animation parameters
fire_min_brightness = 5  # percent
fire_max_brightness = 15  # percent
orch_min_brightness = 50  # percent
orch_max_brightness = 100  # percent
duration_buffer = 0.5  # seconds
NO_FIRE = False  # Set to True to skip the fire animation
NO_ORCHESTRA = False  # Set to True to skip the orchestra animation
ADELE_STARTS = 25  # seconds
animation_settings = [
# Each item is a tuple: (function_name, trigger_time_secs,                          max_bright,              fade_in_time, duration, end_bright,             fade_out_time)
    # Fire timings
    ("animate_fire",                    ADELE_STARTS+58,                            fire_max_brightness,     5,            152,      fire_min_brightness,   3),
    ("animate_fire",                    ADELE_STARTS+210,                           fire_max_brightness,     1,            32,       0,                     5), # end fire and fade to 0
    # Orchestra timings
    ("animate_orchestra",               ADELE_STARTS+100,                           orch_max_brightness,     2,            40,      orch_min_brightness,   5),
    ("animate_orchestra",               ADELE_STARTS+154,                           orch_max_brightness,     2,            20,      orch_min_brightness,   5),
    ("animate_orchestra",               ADELE_STARTS+174,                           orch_max_brightness,     2,            75,      0,                     5), # end orchestra and fade to 0
    # ("animate_orchestra",               10,               orch_max_brightness,     2,            10,   orch_min_brightness,   5),
    # ("animate_orchestra",               30,               orch_max_brightness,     2,            10,   orch_min_brightness,   5),
    # ("animate_orchestra",               50,               orch_max_brightness,     2,            10,   0,                     5), # end orchestra and fade to 0
]

def check_for_stop():
    try:
        with open("/home/roseann/scripts/flag", "r") as f:
            return f.read().strip() == "stop"
    except FileNotFoundError:
        return False
    
# function to animate the fire LEDs to look like a flame
def animate_fire(max_brightness, fade_in_time, duration, end_bright, fade_out_time):
    if NO_FIRE:
        print("Skipping fire animation...")
        return

    print(f"Animating fire: max_bright={max_brightness}, fade_in_time={fade_in_time}, duration={duration}, end_bright={end_bright}, fade_out_time={fade_out_time}")

    # Create a list of colors to animate
    colors = [(255, 0, 0), (255, 85, 0), (255, 140, 0)]  # Red, Orange, Yellowish
    
    # Calculate the time when the main animation should end
    end_time = time.time() + duration - (fade_out_time + fade_in_time + duration_buffer)
    print(f"FIRE: Adjusted end_time={int(end_time - time.time())}...")

    # Fade in
    print("FIRE: Fading in...")
    fade_in_steps = max_brightness
    for step in range(fade_in_steps):
        brightness = (step / fade_in_steps) * max_brightness
        fire_pixels.brightness = brightness / 100.0
        for i in range(len(fire_pixels)):
            color = random.choice(colors)
            fire_pixels[i] = color
        fire_pixels.show()
        time.sleep(fade_in_time / fade_in_steps)
    print("FIRE: Done fading in.")

    print("FIRE: Main animation loop...")
    while time.time() < end_time:
        if check_for_stop():
            print("FIRE: Stop signal detected.")
            break  # Exit the loop if stop signal is detected
    
        for i in range(len(fire_pixels)):
            color = random.choice(colors)
            fire_pixels[i] = color
        fire_pixels.show()
        time.sleep(random.uniform(0.05, 0.1))
    print("FIRE: Done with main animation loop.")

    print("FIRE: Fading out...")
    fade_out_steps = max_brightness
    fade_out_step_duration = fade_in_time / fade_in_steps
    # print(f"fade_out_steps={fade_out_steps}")

    if fade_out_steps > 0:
        for step in range(fade_out_steps + 1):
            # Calculate the current brightness level
            current_brightness = max_brightness - int((step / fade_out_steps) * max_brightness)
            #print(f"Step {step}, Brightness: {current_brightness}")  # Added for debugging

            # Apply the current brightness to the selected LEDs
            for i in range(len(fire_pixels)):
                color = random.choice(colors)
                fire_pixels[i] = color
                fire_pixels[i] = (current_brightness, current_brightness, current_brightness)

            # Update the LED strip
            fire_pixels.show()
            time.sleep(fade_out_step_duration)

        print("FIRE: Done fading out.")
    else:
        print("FIRE: No need to fade out.")

    # # Turn off all LEDs at the end
    # print("FIRE:Turning off LEDs...")
    # fire_pixels.fill((0, 0, 0))
    # fire_pixels.show()

# function to animate the fire LEDs to look like a flame
def animate_orchestra(max_brightness, fade_in_time, duration, end_bright, fade_out_time):
    if NO_ORCHESTRA:
        print("Skipping orchestra animation...")
        return
    
    print(f"Animating Orchestra: max_bright={max_brightness}, fade_in_time={fade_in_time}, duration={duration}, end_bright={end_bright}, fade_out_time={fade_out_time}")

    # Calculate the time when the main animation should end
    end_time = time.time() + duration - (fade_out_time + fade_in_time + duration_buffer)
    print(f"ORCHESTRA: Adjusted end_time={int(end_time - time.time())}...")

    # Create a list of colors to animate
    colors = [(255, 0, 0), (255, 85, 0), (255, 140, 0)]  # Red, Orange, Yellowish
    
    # Start with some random LEDs lit
    num_leds_to_light = random.randint(1, len(orch_pixels))  # Random number of LEDs to fade in
    leds_to_light = random.sample(range(len(orch_pixels)), num_leds_to_light)  # Select random LEDs
    print(f"ORCHESTRA: Fading in {num_leds_to_light} LEDs: {leds_to_light}")

    # Fade in
    print("ORCHESTRA: Fading in...")

    # Calculate the number of steps for fading in
    fade_in_steps = max_brightness
    fade_in_step_duration = fade_in_time / fade_in_steps

    for step in range(fade_in_steps + 1):
        # Calculate the current brightness level
        current_brightness = int((step / fade_in_steps) * max_brightness)
        #print(f"Step {step}, Brightness: {current_brightness}")  # Added for debugging

        # Apply the current brightness to the selected LEDs
        for i in leds_to_light:
            orch_pixels[i] = (current_brightness, current_brightness, current_brightness)

        # Update the LED strip
        orch_pixels.show()
        time.sleep(fade_in_step_duration)

    print("ORCHESTRA: Done fading in.")

    # Main animation loop
    print("ORCHESTRA:Main animation loop...")
    while time.time() < end_time:

        if check_for_stop():
            print("ORCHESTRA:Stop signal detected.")
            break  # Exit the loop if stop signal is detected

        num_leds_to_light = random.randint(1, len(orch_pixels))  # Random number of LEDs to fade in
        leds_to_light = random.sample(range(len(orch_pixels)), num_leds_to_light)  # Select random LEDs

        for i in leds_to_light:
            # Fade in to white
            for brightness in range(max_brightness):
                orch_pixels[i] = (brightness, brightness, brightness)  # Set to white with increasing brightness
                orch_pixels.show()
                time.sleep(random.uniform(0.01, 0.02))  # Random fade-in speed

        # Reset LEDs to original colors for next loop iteration
        for i in range(len(orch_pixels)):
            orch_pixels[i] = (0, 0, 0)
    print("ORCHESTRA:Done with main animation loop.")

    # Fade out
    print("ORCHESTRA:Fading out...")
    fade_out_steps = max_brightness
    fade_out_step_duration = fade_in_time / fade_in_steps
    # print(f"fade_out_steps={fade_out_steps}")

    if fade_out_steps > 0:
        for step in range(fade_out_steps + 1):
            # Calculate the current brightness level
            current_brightness = max_brightness - int((step / fade_out_steps) * max_brightness)
            #print(f"Step {step}, Brightness: {current_brightness}")  # Added for debugging

            # Apply the current brightness to the selected LEDs
            for i in leds_to_light:
                orch_pixels[i] = (current_brightness, current_brightness, current_brightness)

            # Update the LED strip
            orch_pixels.show()
            time.sleep(fade_out_step_duration)

        print("ORCHESTRA: Done fading out.")
    else:
        print("ORCHESTRA: No need to fade out.")


    # # Turn off all LEDs at the end
    # print("ORCHESTRA:Turning off LEDs...")
    # orch_pixels.fill((0, 0, 0))
    # orch_pixels.show()

# Function mappings
function_map = {
    "animate_fire": animate_fire,
    "animate_orchestra": animate_orchestra
    # Add more mappings as needed
}

# Define a cleanup function
def cleanup():
    fire_pixels.fill((0, 0, 0))
    orch_pixels.fill((0, 0, 0))
    fire_pixels.show()
    orch_pixels.show()
    print("LEDs turned off.")

# Register the cleanup function with atexit
# atexit.register(cleanup)

# Main animation function
def run_animations():
#    print("Globals:", globals())

    start_time = time.time()  # Record the start time
    print(f"Start time = ", {start_time})

    threads = []  # Initialize the list to store threads

    # Sorting the list by the start_time, which is the second element in each tuple
    sorted_animation_settings = sorted(animation_settings, key=lambda x: x[1])

    stop_requested = False  # Declare the flag before the for loop
    for func_name, trigger_time, *params in sorted_animation_settings:

            # Wait until the trigger time is reached
            print(f"Starting next animation at mark {trigger_time-(start_time < trigger_time)} seconds... to run {func_name}")
            while time.time() - start_time < trigger_time:
                print(f"Waiting... {int(time.time() - start_time)} < {trigger_time}")
                if check_for_stop():
                        stop_requested = True  # Set the flag
                        break  # Exit the loop early if stop condition is met
                time.sleep(0.5)

            if stop_requested:
                break  # Exit the outer loop if stop was requested

            # Retrieve the animation function from the dictionary
            animation_func = function_map.get(func_name)
            print(f"Running animation {func_name}...")
            
            if animation_func:
                # Create and start a new thread for the animation
                print(f"Creating thread for {func_name}...")
                thread = threading.Thread(target=animation_func, args=params)
                thread.start()
                threads.append(thread)
            else:
                print(f"Function {func_name} not found.")

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

def set_stop_flag():
    with open("/home/roseann/scripts/flag", "w") as f:
        f.write("stop")
    print("Stop signal sent to NeoPixel script.")

def turn_off_display():
    """Turn off the display by setting brightness to zero."""
    try:
        subprocess.run('echo 0 | sudo tee /sys/class/backlight/10-0045/brightness', shell=True, check=True)
        print("Display turned off.")
    except subprocess.CalledProcessError:
        print("Error turning off the display.")

if __name__ == "__main__":
    try:
        print("Starting pixel animations...")
        cleanup()
        run_animations()

    finally:
        turn_off_display()
        print("Exiting main...")
        cleanup()  # Ensure cleanup is called
        set_stop_flag()
