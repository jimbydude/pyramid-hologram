import board
import neopixel

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

# Define a cleanup function
def cleanup():
    fire_pixels.fill((0, 0, 0))
    orch_pixels.fill((0, 0, 0))
    fire_pixels.show()
    orch_pixels.show()
    print("LEDs turned off.")

def main():
    # Your main code here
    cleanup()

if __name__ == "__main__":
    main()
